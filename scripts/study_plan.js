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
      content += `<article class="task ${row.done?'done':''}"><p class="module">${escape(task.module)} · ${task.hour}/${task.moduleHours}h</p><div class="task-head"><input type="checkbox" id="done-${row.id}" data-done="${row.id}" ${row.done?'checked':''}><label for="done-${row.id}">${escape(task.title)} · 1h</label></div><p>${escape(task.outcome)}</p><p>建议：阅读 / 梳理 20 分钟 + 编码 30 分钟 + 复盘 10 分钟。</p><a href="PythonAI-学习资料库.html#${task.anchor}" target="_blank" rel="noopener">${task.outline?'课程大纲 ↗ · 待补充资料':'打开学习文档 ↗'}</a>${row.done?'':`<div class="reschedule"><label for="date-${row.id}">调整至</label><input type="date" id="date-${row.id}" min="${settings.start}" max="2099-12-31" value="${row.date}"><button data-move="${row.id}">改期</button><button data-free="${row.id}">顺延至空闲日</button></div>`}</article>`;
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
