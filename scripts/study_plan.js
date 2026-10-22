(() => {
  'use strict';
  const KEY = 'pythonai-study-plan-v1';
  const DEFAULT_SETTINGS = { start: '2026-10-20', weekday: 2, weekend: 4 };
  const catalog = JSON.parse(document.getElementById('task-data').textContent);
  const $ = id => document.getElementById(id);
  const iso = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const parse = value => new Date(`${value}T12:00:00`);
  const advance = (day, count = 1) => { const d = parse(day); d.setDate(d.getDate()+count); return iso(d); };
  const isISODate = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && iso(parse(value)) === value;
  const isHours = value => Number.isInteger(value) && value >= 0 && value <= 10;
  const today = () => new Intl.DateTimeFormat('sv-SE', { timeZone:'Asia/Shanghai', year:'numeric', month:'2-digit', day:'2-digit' }).format(new Date());
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const sanitizeSettings = value => {
    if (!value || !isISODate(value.start) || !isHours(value.weekday) || !isHours(value.weekend)) return null;
    if (value.weekday === 0 && value.weekend === 0) return null;
    return { start: value.start, weekday: value.weekday, weekend: value.weekend };
  };
  let settings = { ...DEFAULT_SETTINGS };
  const capacity = day => [0,6].includes(parse(day).getDay()) ? settings.weekend : settings.weekday;
  const validDate = value => isISODate(value) && value >= settings.start && value <= '2099-12-31';
  const defaults = () => {
    let day = settings.start, used = 0;
    return catalog.map(task => {
      while (capacity(day) === 0) day = advance(day);
      if (used >= capacity(day)) {
        day = advance(day); used = 0;
        while (capacity(day) === 0) day = advance(day);
      }
      used++;
      return { id:task.id, date:day, done:false };
    });
  };
  const validateTasks = data => {
    if (!data || !Array.isArray(data) || data.length !== catalog.length) throw new Error('备份版本或任务数量不匹配');
    const map = new Map(data.map(t => [t.id,t]));
    if (map.size !== catalog.length) throw new Error('备份任务重复');
    return catalog.map(t => {
      const row = map.get(t.id);
      if (!row || !validDate(row.date) || typeof row.done !== 'boolean') throw new Error('备份日期或任务状态无效');
      return {id:t.id,date:row.date,done:row.done};
    });
  };
  let state = defaults();
  let restored = false;
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (raw) {
      if (raw.version === 2) {
        const stored = sanitizeSettings(raw.settings);
        if (stored) settings = stored;
      }
      state = validateTasks(raw.tasks);
      restored = true;
    }
  } catch (error) { $('notice').textContent = '本地记录无法读取，当前显示初始计划。可导入备份恢复；若浏览器限制存储，请定期导出备份。'; }
  if (!restored) state = defaults();
  let baseline = defaults().at(-1).date;
  let selected = location.hash.slice(1);
  if (!validDate(selected)) selected = today();
  if (!validDate(selected)) selected = settings.start;
  let month = parse(selected); month.setDate(1);
  const tasksOn = day => state.filter(t => t.date === day);
  const detail = id => catalog.find(t => t.id === id);
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify({version:2,settings,tasks:state})); $('notice').textContent = '已保存到当前浏览器。'; }
    catch { $('notice').textContent = '浏览器无法保存记录；当前操作已生效，请导出备份以免丢失。'; }
  }
  function updateSettingsUI() {
    $('set-start').value = settings.start;
    $('set-weekday').value = String(settings.weekday);
    $('set-weekend').value = String(settings.weekend);
    const weekly = settings.weekday * 5 + settings.weekend * 2;
    $('plan-chips').innerHTML = [
      `起点 ${settings.start.replace(/-/g,'.')}`,
      `工作日 ${settings.weekday}h / 天`,
      `周末 ${settings.weekend}h / 天`,
      `每周约 ${weekly}h`
    ].map(label => `<span>${label}</span>`).join('');
    syncAllSelects();
  }
  function selectDay(day, focus = false) {
    selected = day; month = parse(day); month.setDate(1);
    location.hash = day; render();
    if (focus) { $('daily').focus({preventScroll:true}); $('daily').scrollIntoView({behavior:'smooth',block:'start'}); }
  }
  function render() {
    const completed = state.filter(t => t.done).length;
    const end = state.reduce((last,t) => t.date > last ? t.date : last, settings.start);
    $('stats').innerHTML = [
      ['已完成 / 总预算', `${completed}<small>/ ${state.length} 小时</small>`],
      ['完成进度', `${Math.round(completed/state.length*100)}<small>%</small>`],
      ['计划结束', `${end.slice(5).replace('-','.')}<small>${end.slice(0,4)}</small>`],
      ['初始预计结束', `${baseline.slice(5).replace('-','.')}<small>${baseline.slice(0,4)}</small>`]
    ].map(([label,value])=>`<div class="stat"><span>${label}</span><strong>${value}</strong></div>`).join('');
    $('month-title').textContent = `${month.getFullYear()} 年 ${month.getMonth()+1} 月`;
    const startMonth = parse(settings.start);
    $('prev').disabled = month.getFullYear()*12 + month.getMonth() <= startMonth.getFullYear()*12 + startMonth.getMonth();
    $('next').disabled = month.getFullYear() === 2099 && month.getMonth() === 11;
    const offset = (month.getDay()+6)%7;
    const days = new Date(month.getFullYear(),month.getMonth()+1,0).getDate();
    let calendar = '<span class="day empty" aria-hidden="true"></span>'.repeat(offset);
    for (let n=1;n<=days;n++) {
      const day = iso(new Date(month.getFullYear(),month.getMonth(),n,12));
      const rows = tasksOn(day), done = rows.filter(t=>t.done).length;
      const classes = ['day',day===selected?'selected':'',day===today()?'today':'',rows.length&&done===rows.length?'completed':'',rows.length>capacity(day)?'overloaded':''].filter(Boolean).join(' ');
      const topic = rows.length ? detail(rows[0].id).module.split(' ')[0] : '';
      calendar += `<button class="${classes}" data-day="${day}" aria-pressed="${day===selected}" ${day===today()?'aria-current="date"':''} aria-label="${day}，${rows.length} 小时，已完成 ${done} 小时"><span class="number">${n}</span><span class="hours">${rows.length ? (done===rows.length?'✓ ': '● ')+rows.length+'h' : '—'}</span><span class="topic">${escape(topic)}</span></button>`;
    }
    $('calendar').innerHTML = calendar;
    $('day-title').textContent = `${selected} · ${['周日','周一','周二','周三','周四','周五','周六'][parse(selected).getDay()]}`;
    const rows = tasksOn(selected), done = rows.filter(t=>t.done).length;
    $('day-meta').textContent = `已排 ${rows.length} 小时 / 建议 ${capacity(selected)} 小时 · 已完成 ${done} 小时`;
    let content = rows.length > capacity(selected) ? '<p class="warning">当天超出学习预算，可将任务改到其他日期。</p>' : '';
    if (!rows.length) content += '<p>这一天还没有任务。可以休息、复盘，或把未完成任务调整到这里。</p>';
    for (const row of rows) {
      const task = detail(row.id);
      content += `<article class="task ${row.done?'done':''}"><p class="module">${escape(task.module)} · ${task.hour}/${task.moduleHours}h</p><div class="task-head"><input type="checkbox" id="done-${row.id}" data-done="${row.id}" ${row.done?'checked':''}><label for="done-${row.id}">${escape(task.title)} · 1h</label></div><p>${escape(task.outcome)}</p><p>建议：阅读 / 梳理 20 分钟 + 编码 30 分钟 + 复盘 10 分钟。</p><a href="PythonAI-学习资料库.html#${task.anchor}" target="_blank" rel="noopener">${task.outline?'课程大纲 ↗ · 待补充资料':'打开学习文档 ↗'}</a>${row.done?'':`<div class="reschedule"><label for="date-${row.id}">调整至</label><div class="date-field"><input type="date" id="date-${row.id}" min="${settings.start}" max="2099-12-31" value="${row.date}"><button type="button" class="date-trigger" data-calendar-for="date-${row.id}" aria-label="打开日历选择新日期" aria-haspopup="dialog" aria-controls="sp-calendar" aria-expanded="false"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><rect x="2.2" y="3.2" width="11.6" height="10.6" rx="2"></rect><path d="M2.2 6.4h11.6M5.4 1.8v2.8M10.6 1.8v2.8"></path></svg></button></div><button data-move="${row.id}">改期</button><button data-free="${row.id}">顺延至空闲日</button></div>`}</article>`;
    }
    $('tasks').innerHTML = content;
  }
  function move(id, date) {
    if (!validDate(date)) { $('notice').textContent = `请选择 ${settings.start} 至 2099-12-31 的有效日期。`; return; }
    const task = state.find(t=>t.id===id);
    if (!task || task.done) return;
    task.date = date; persist(); selectDay(date);
    $('notice').textContent += ` 任务已调整至 ${date}。`;
  }
  const within = (target, selector) => target instanceof Element ? target.closest(selector) : null;
  const boundsOf = input => ({ min: input.min || '0000-01-01', max: input.max || '9999-12-31' });
  const monthKey = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}`;
  const shiftMonthDay = (day, delta) => {
    const source = parse(day);
    const target = new Date(source.getFullYear(), source.getMonth() + delta, 1, 12);
    const last = new Date(target.getFullYear(), target.getMonth() + 1, 0).getDate();
    target.setDate(Math.min(source.getDate(), last));
    return iso(target);
  };

  const selectMenu = document.createElement('div');
  selectMenu.className = 'sp-select-menu';
  selectMenu.id = 'sp-select-menu';
  selectMenu.setAttribute('role', 'listbox');
  selectMenu.setAttribute('aria-label', '选择每日学习时长');
  selectMenu.hidden = true;
  document.body.appendChild(selectMenu);

  const calendar = document.createElement('div');
  calendar.className = 'sp-calendar';
  calendar.id = 'sp-calendar';
  calendar.setAttribute('role', 'dialog');
  calendar.setAttribute('aria-label', '选择日期');
  calendar.hidden = true;
  calendar.innerHTML = `<div class="sp-cal-head"><button type="button" class="sp-cal-nav" data-cal-nav="-1" aria-label="上个月"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.8 3.4 5.2 8l4.6 4.6"></path></svg></button><strong class="sp-cal-title"></strong><button type="button" class="sp-cal-nav" data-cal-nav="1" aria-label="下个月"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.2 3.4 10.8 8l-4.6 4.6"></path></svg></button></div><div class="sp-cal-week" aria-hidden="true"><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span><span>日</span></div><div class="sp-cal-grid" role="grid"></div><div class="sp-cal-foot"><button type="button" class="sp-cal-today">今天</button><button type="button" class="sp-cal-close">关闭</button></div>`;
  document.body.appendChild(calendar);

  let activeSelect = null;
  let activeCalendar = null;
  let placementFrame = 0;

  function syncSelectTrigger(select) {
    const trigger = document.querySelector(`.select-trigger[data-select-for="${select.id}"]`);
    if (!trigger) return;
    const option = select.options[select.selectedIndex];
    trigger.querySelector('.select-value').textContent = option ? option.textContent : '';
  }
  function syncAllSelects() {
    for (const id of ['set-weekday','set-weekend']) syncSelectTrigger($(id));
  }
  function renderSelectMenu() {
    if (!activeSelect) return;
    const { select, index } = activeSelect;
    selectMenu.innerHTML = [...select.options].map((option, i) => `<div class="sp-select-option${i === index ? ' active' : ''}" id="sp-select-option-${i}" role="option" data-index="${i}" aria-selected="${i === select.selectedIndex}">${escape(option.textContent)}<span class="sp-check" aria-hidden="true">✓</span></div>`).join('');
  }
  function setActiveOption(index, scroll = true) {
    if (!activeSelect) return;
    const options = [...selectMenu.querySelectorAll('.sp-select-option')];
    if (!options.length) return;
    activeSelect.index = Math.min(Math.max(index, 0), options.length - 1);
    options.forEach((option, i) => option.classList.toggle('active', i === activeSelect.index));
    const active = options[activeSelect.index];
    activeSelect.trigger.setAttribute('aria-activedescendant', active.id);
    if (scroll) active.scrollIntoView({ block: 'nearest' });
  }
  function openSelect(trigger) {
    const select = $(trigger.dataset.selectFor);
    if (!select) return;
    closeCalendar();
    closeSelect();
    const selectedIndex = Math.max(0, select.selectedIndex);
    activeSelect = { trigger, select, index: selectedIndex };
    trigger.setAttribute('aria-expanded', 'true');
    const width = Math.min(Math.max(132, Math.round(trigger.getBoundingClientRect().width)), window.innerWidth - 16);
    selectMenu.style.width = `${width}px`;
    renderSelectMenu();
    placePopover(selectMenu, trigger);
    setActiveOption(selectedIndex);
  }
  function chooseSelectOption(index) {
    if (!activeSelect) return;
    const { select, trigger } = activeSelect;
    if (select.selectedIndex !== index) {
      select.selectedIndex = index;
      select.dispatchEvent(new Event('change', { bubbles: true }));
    }
    syncSelectTrigger(select);
    closeSelect();
    trigger.focus({ preventScroll: true });
  }
  function closeSelect(returnFocus = false) {
    if (!activeSelect) return;
    const { trigger } = activeSelect;
    activeSelect = null;
    trigger.setAttribute('aria-expanded', 'false');
    trigger.removeAttribute('aria-activedescendant');
    selectMenu.hidden = true;
    selectMenu.innerHTML = '';
    if (returnFocus) trigger.focus({ preventScroll: true });
  }

  function renderCalendar(focus = false) {
    if (!activeCalendar) return;
    const { input, year, month } = activeCalendar;
    const { min, max } = boundsOf(input);
    const selected = isISODate(input.value) ? input.value : '';
    const currentToday = today();
    const first = new Date(year, month, 1, 12);
    const offset = (first.getDay() + 6) % 7;
    const gridStart = new Date(year, month, 1 - offset, 12);
    calendar.querySelector('.sp-cal-title').textContent = `${year} 年 ${month + 1} 月`;
    calendar.querySelector('[data-cal-nav="-1"]').disabled = monthKey(new Date(year, month - 1, 1, 12)) < min.slice(0, 7);
    calendar.querySelector('[data-cal-nav="1"]').disabled = monthKey(new Date(year, month + 1, 1, 12)) > max.slice(0, 7);
    let html = '';
    for (let i = 0; i < 42; i++) {
      const date = new Date(gridStart);
      date.setDate(gridStart.getDate() + i);
      const day = iso(date);
      const disabled = day < min || day > max;
      const classes = ['sp-cal-day', date.getMonth() !== month ? 'out' : '', day === selected ? 'selected' : '', day === currentToday ? 'today' : ''].filter(Boolean).join(' ');
      html += `<button type="button" class="${classes}" data-cal-day="${day}" tabindex="-1" ${disabled ? 'disabled' : ''} ${day === selected ? 'aria-selected="true"' : ''} ${day === currentToday ? 'aria-current="date"' : ''} aria-label="${day}${disabled ? '，不可选' : ''}">${date.getDate()}</button>`;
    }
    calendar.querySelector('.sp-cal-grid').innerHTML = html;
    calendar.querySelector('.sp-cal-today').disabled = currentToday < min || currentToday > max;
    if (focus) {
      const state = activeCalendar;
      requestAnimationFrame(() => {
        if (activeCalendar !== state) return;
        const target = calendar.querySelector(`[data-cal-day="${state.focus}"]:not(:disabled)`) || calendar.querySelector('.sp-cal-day:not(:disabled)');
        target?.focus({ preventScroll: true });
      });
    }
  }
  function openCalendar(input, anchor) {
    closeSelect();
    closeCalendar();
    const { min, max } = boundsOf(input);
    let base = isISODate(input.value) ? input.value : today();
    if (base < min) base = min;
    if (base > max) base = max;
    const date = parse(base);
    activeCalendar = { input, anchor, position: input.closest('.date-field') || anchor, year: date.getFullYear(), month: date.getMonth(), focus: base };
    anchor.setAttribute('aria-expanded', 'true');
    renderCalendar(true);
    placePopover(calendar, activeCalendar.position);
    calendar.scrollTop = 0;
  }
  function chooseCalendarDay(day) {
    if (!activeCalendar) return;
    const input = activeCalendar.input;
    input.value = day;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    closeCalendar();
    input.focus({ preventScroll: true });
  }
  function focusCalendarDay(day) {
    if (!activeCalendar) return;
    const { min, max } = boundsOf(activeCalendar.input);
    let next = day;
    if (next < min) next = min;
    if (next > max) next = max;
    const date = parse(next);
    activeCalendar.year = date.getFullYear();
    activeCalendar.month = date.getMonth();
    activeCalendar.focus = next;
    renderCalendar(true);
  }
  function closeCalendar(returnFocus = false) {
    if (!activeCalendar) return;
    const { anchor } = activeCalendar;
    activeCalendar = null;
    calendar.hidden = true;
    anchor.setAttribute('aria-expanded', 'false');
    if (returnFocus) anchor.focus({ preventScroll: true });
  }
  function placePopover(popover, anchor) {
    popover.hidden = false;
    const gap = 6, margin = 8;
    const rect = anchor.getBoundingClientRect();
    const box = popover.getBoundingClientRect();
    let left = Math.min(Math.max(margin, rect.left), Math.max(margin, window.innerWidth - box.width - margin));
    let top = rect.bottom + gap;
    if (top + box.height > window.innerHeight - margin) {
      const above = rect.top - gap - box.height;
      top = above >= margin ? above : Math.max(margin, window.innerHeight - box.height - margin);
    }
    popover.style.left = `${Math.round(left)}px`;
    popover.style.top = `${Math.round(top)}px`;
  }
  function repositionPopovers() {
    placementFrame = 0;
    if (activeSelect) {
      const width = Math.min(Math.max(132, Math.round(activeSelect.trigger.getBoundingClientRect().width)), window.innerWidth - 16);
      selectMenu.style.width = `${width}px`;
      placePopover(selectMenu, activeSelect.trigger);
    }
    if (activeCalendar) placePopover(calendar, activeCalendar.position);
  }
  const queuePlacement = () => {
    if ((activeSelect || activeCalendar) && !placementFrame) placementFrame = requestAnimationFrame(repositionPopovers);
  };
  window.addEventListener('scroll', queuePlacement, true);
  window.addEventListener('resize', queuePlacement);

  selectMenu.addEventListener('pointerover', event => {
    const option = within(event.target, '.sp-select-option');
    if (option && activeSelect) setActiveOption(Number(option.dataset.index), false);
  });
  calendar.addEventListener('click', event => {
    if (!activeCalendar) return;
    const nav = within(event.target, '[data-cal-nav]');
    if (nav) {
      focusCalendarDay(shiftMonthDay(activeCalendar.focus, Number(nav.dataset.calNav)));
      return;
    }
    if (within(event.target, '.sp-cal-today')) {
      const current = today();
      const { min, max } = boundsOf(activeCalendar.input);
      if (current >= min && current <= max) chooseCalendarDay(current);
      return;
    }
    if (within(event.target, '.sp-cal-close')) { closeCalendar(true); return; }
    const day = within(event.target, '[data-cal-day]');
    if (day && !day.disabled) chooseCalendarDay(day.dataset.calDay);
  });
  calendar.addEventListener('keydown', event => {
    if (!activeCalendar) return;
    const button = within(event.target, '[data-cal-day]');
    if (!button) return;
    const current = button.dataset.calDay;
    let next = null;
    switch (event.key) {
      case 'ArrowLeft': next = advance(current, -1); break;
      case 'ArrowRight': next = advance(current, 1); break;
      case 'ArrowUp': next = advance(current, -7); break;
      case 'ArrowDown': next = advance(current, 7); break;
      case 'Home': next = advance(current, -((parse(current).getDay() + 6) % 7)); break;
      case 'End': next = advance(current, 6 - ((parse(current).getDay() + 6) % 7)); break;
      case 'PageUp': next = shiftMonthDay(current, -1); break;
      case 'PageDown': next = shiftMonthDay(current, 1); break;
      default: return;
    }
    event.preventDefault();
    focusCalendarDay(next);
  });

  document.addEventListener('click', event => {
    const selectTrigger = within(event.target, '.select-trigger');
    if (selectTrigger) {
      if (activeSelect && activeSelect.trigger === selectTrigger) closeSelect(true);
      else openSelect(selectTrigger);
      return;
    }
    const dateTrigger = within(event.target, '[data-calendar-for]');
    if (dateTrigger) {
      const input = $(dateTrigger.dataset.calendarFor);
      if (!input) return;
      if (activeCalendar && activeCalendar.input === input) closeCalendar(true);
      else openCalendar(input, dateTrigger);
      return;
    }
    const option = within(event.target, '.sp-select-option');
    if (option && activeSelect) chooseSelectOption(Number(option.dataset.index));
  });
  document.addEventListener('pointerdown', event => {
    if (activeSelect && !within(event.target, '.sp-select-menu') && !within(event.target, '.select-trigger')) closeSelect();
    if (activeCalendar && !within(event.target, '.sp-calendar') && !within(event.target, '[data-calendar-for]')) closeCalendar();
  }, true);
  document.addEventListener('focusin', event => {
    if (activeSelect && !within(event.target, '.sp-select-menu') && event.target !== activeSelect.trigger) closeSelect();
    if (activeCalendar && !within(event.target, '.sp-calendar') && event.target !== activeCalendar.input && event.target !== activeCalendar.anchor) closeCalendar();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      if (activeSelect) { event.preventDefault(); closeSelect(true); return; }
      if (activeCalendar) { event.preventDefault(); closeCalendar(true); return; }
    }
    if ((event.altKey && event.key === 'ArrowDown') || event.key === 'F4') {
      const input = within(event.target, 'input[type="date"]');
      if (input) {
        event.preventDefault();
        const trigger = document.querySelector(`[data-calendar-for="${input.id}"]`);
        if (trigger) openCalendar(input, trigger);
        return;
      }
    }
    const trigger = within(event.target, '.select-trigger');
    if (!trigger) return;
    const select = $(trigger.dataset.selectFor);
    if (!select) return;
    if (!activeSelect || activeSelect.trigger !== trigger) {
      if (['ArrowDown','ArrowUp','Enter',' '].includes(event.key)) {
        event.preventDefault();
        openSelect(trigger);
        if (event.key === 'ArrowUp') setActiveOption(select.options.length - 1);
      }
      return;
    }
    switch (event.key) {
      case 'ArrowDown': event.preventDefault(); setActiveOption(activeSelect.index + 1); break;
      case 'ArrowUp': event.preventDefault(); setActiveOption(activeSelect.index - 1); break;
      case 'Home': event.preventDefault(); setActiveOption(0); break;
      case 'End': event.preventDefault(); setActiveOption(select.options.length - 1); break;
      case 'Enter':
      case ' ': event.preventDefault(); chooseSelectOption(activeSelect.index); break;
      case 'Tab': closeSelect(); break;
    }
  });
  for (const id of ['set-weekday','set-weekend']) {
    const select = $(id);
    for (let hours = 0; hours <= 10; hours++) {
      const option = document.createElement('option');
      option.value = String(hours);
      option.textContent = hours === 0 ? '休息' : `${hours} 小时`;
      select.appendChild(option);
    }
  }
  updateSettingsUI();
  $('settings-form').addEventListener('submit', event => {
    event.preventDefault();
    const next = sanitizeSettings({
      start: $('set-start').value,
      weekday: Number($('set-weekday').value),
      weekend: Number($('set-weekend').value)
    });
    if (!next) { $('notice').textContent = '请选择有效的起点，且工作日和周末至少保留 1 小时学习时间。'; return; }
    const done = new Map(state.map(t => [t.id, t.done]));
    settings = next;
    state = defaults().map(t => ({ ...t, done: done.get(t.id) || false }));
    baseline = defaults().at(-1).date;
    persist(); updateSettingsUI();
    selected = validDate(today()) ? today() : settings.start;
    month = parse(selected); month.setDate(1);
    location.hash = selected;
    render();
    $('notice').textContent = '已按新的起点与每日时长重新排期，完成勾选已保留。';
  });
  $('calendar').addEventListener('click', event => {
    const button = event.target.closest('[data-day]');
    if (button) selectDay(button.dataset.day,true);
  });
  $('tasks').addEventListener('change', event => {
    const id = event.target.dataset.done;
    if (!id) return;
    state.find(t=>t.id===id).done = event.target.checked;
    persist(); render();
    $(`done-${id}`).focus({preventScroll:true});
  });
  $('tasks').addEventListener('click', event => {
    const id = event.target.dataset.move;
    if (id) move(id,$(`date-${id}`).value);
    const freeId = event.target.dataset.free;
    if (freeId) {
      let date = advance(state.find(t=>t.id===freeId).date);
      if (date < today()) date = today();
      while (validDate(date) && tasksOn(date).length >= capacity(date)) date = advance(date);
      move(freeId,date);
    }
  });
  $('prev').onclick = () => { month.setMonth(month.getMonth()-1); render(); };
  $('next').onclick = () => { month.setMonth(month.getMonth()+1); render(); };
  $('today').onclick = () => selectDay(validDate(today())?today():settings.start,true);
  window.addEventListener('hashchange', () => { const day = location.hash.slice(1); if(validDate(day)) { selected=day; month=parse(day); month.setDate(1); render(); } });
  $('export').onclick = () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify({version:2,settings,tasks:state},null,2)],{type:'application/json'}));
    const a = document.createElement('a'); a.href=url; a.download=`PythonAI-学习进度-${today()}.json`; a.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  $('import').onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 1024*1024) throw new Error('备份文件过大');
      const data = JSON.parse(await file.text());
      if (!data || (data.version !== 1 && data.version !== 2)) throw new Error('备份版本不支持');
      let nextSettings = settings;
      if (data.version === 2) {
        const stored = sanitizeSettings(data.settings);
        if (!stored) throw new Error('备份中的学习节奏设置无效');
        nextSettings = stored;
      }
      const previous = settings;
      settings = nextSettings;
      let restoredTasks;
      try { restoredTasks = validateTasks(data.tasks); } catch (error) { settings = previous; throw error; }
      state = restoredTasks;
      baseline = defaults().at(-1).date;
      persist(); updateSettingsUI();
      selected = validDate(selected) ? selected : settings.start;
      month = parse(selected); month.setDate(1);
      render();
      $('notice').textContent = '备份已导入，学习节奏与任务进度已恢复。';
    } catch(error) { $('notice').textContent = `导入失败：${error.message}。原有进度已保留。`; }
    event.target.value = '';
  };
  render();
})();
