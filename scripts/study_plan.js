(() => {
  'use strict';
  const START = '2026-10-20';
  const KEY = 'pythonai-study-plan-v1';
  const catalog = JSON.parse(document.getElementById('task-data').textContent);
  const $ = id => document.getElementById(id);
  const iso = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const parse = value => new Date(`${value}T12:00:00`);
  const advance = (day, count = 1) => { const d = parse(day); d.setDate(d.getDate()+count); return iso(d); };
  const capacity = day => [0,6].includes(parse(day).getDay()) ? 4 : 2;
  const today = () => new Intl.DateTimeFormat('sv-SE', { timeZone:'Asia/Shanghai', year:'numeric', month:'2-digit', day:'2-digit' }).format(new Date());
  const validDate = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && value >= START && value <= '2099-12-31' && iso(parse(value)) === value;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const defaults = () => {
    let day = START, used = 0;
    return catalog.map(task => {
      if (used >= capacity(day)) { day = advance(day); used = 0; }
      used++;
      return { id:task.id, date:day, done:false };
    });
  };
  const validate = data => {
    if (!data || data.version !== 1 || !Array.isArray(data.tasks) || data.tasks.length !== catalog.length) throw new Error('备份版本或任务数量不匹配');
    const map = new Map(data.tasks.map(t => [t.id,t]));
    if (map.size !== catalog.length) throw new Error('备份任务重复');
    return catalog.map(t => {
      const row = map.get(t.id);
      if (!row || !validDate(row.date) || typeof row.done !== 'boolean') throw new Error('备份日期或任务状态无效');
      return {id:t.id,date:row.date,done:row.done};
    });
  };
  let state = defaults();
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) state = validate(JSON.parse(raw));
  } catch (error) { $('notice').textContent = '本地记录无法读取，当前显示初始计划。可导入备份恢复；若浏览器限制存储，请定期导出备份。'; }
  const baseline = defaults().at(-1).date;
  let selected = location.hash.slice(1);
  if (!validDate(selected)) selected = today();
  if (!validDate(selected)) selected = START;
  let month = parse(selected); month.setDate(1);
  const tasksOn = day => state.filter(t => t.date === day);
  const detail = id => catalog.find(t => t.id === id);
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify({version:1,tasks:state})); $('notice').textContent = '已保存到当前浏览器。'; }
    catch { $('notice').textContent = '浏览器无法保存记录；当前操作已生效，请导出备份以免丢失。'; }
  }
  function selectDay(day, focus = false) {
    selected = day; month = parse(day); month.setDate(1);
    location.hash = day; render();
    if (focus) { $('daily').focus({preventScroll:true}); $('daily').scrollIntoView({behavior:'smooth',block:'start'}); }
  }
  function render() {
    const completed = state.filter(t => t.done).length;
    const end = state.reduce((last,t) => t.date > last ? t.date : last, START);
    $('stats').innerHTML = [
      ['已完成 / 总预算', `${completed}<small>/ ${state.length} 小时</small>`],
      ['完成进度', `${Math.round(completed/state.length*100)}<small>%</small>`],
      ['计划结束', `${end.slice(5).replace('-','.')}<small>${end.slice(0,4)}</small>`],
      ['初始预计结束', `${baseline.slice(5).replace('-','.')}<small>${baseline.slice(0,4)}</small>`]
    ].map(([label,value])=>`<div class="stat"><span>${label}</span><strong>${value}</strong></div>`).join('');
    $('month-title').textContent = `${month.getFullYear()} 年 ${month.getMonth()+1} 月`;
    $('prev').disabled = month.getFullYear() === 2026 && month.getMonth() === 9;
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
      content += `<article class="task ${row.done?'done':''}"><p class="module">${escape(task.module)} · ${task.hour}/${task.moduleHours}h</p><div class="task-head"><input type="checkbox" id="done-${row.id}" data-done="${row.id}" ${row.done?'checked':''}><label for="done-${row.id}">${escape(task.title)} · 1h</label></div><p>${escape(task.outcome)}</p><p>建议：阅读 / 梳理 20 分钟 + 编码 30 分钟 + 复盘 10 分钟。</p><a href="PythonAI-学习资料库.html#${task.anchor}" target="_blank" rel="noopener">${task.outline?'课程大纲 ↗ · 待补充资料':'打开学习文档 ↗'}</a>${row.done?'':`<div class="reschedule"><label for="date-${row.id}">调整至</label><input type="date" id="date-${row.id}" min="${START}" max="2099-12-31" value="${row.date}"><button data-move="${row.id}">改期</button><button data-free="${row.id}">顺延至空闲日</button></div>`}</article>`;
    }
    $('tasks').innerHTML = content;
  }
  function move(id, date) {
    if (!validDate(date)) { $('notice').textContent = '请选择 2026-10-20 至 2099-12-31 的有效日期。'; return; }
    const task = state.find(t=>t.id===id);
    if (!task || task.done) return;
    task.date = date; persist(); selectDay(date);
    $('notice').textContent += ` 任务已调整至 ${date}。`;
  }
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
  $('today').onclick = () => selectDay(validDate(today())?today():START,true);
  window.addEventListener('hashchange', () => { const day = location.hash.slice(1); if(validDate(day)) { selected=day; month=parse(day); month.setDate(1); render(); } });
  $('export').onclick = () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify({version:1,tasks:state},null,2)],{type:'application/json'}));
    const a = document.createElement('a'); a.href=url; a.download=`PythonAI-学习进度-${today()}.json`; a.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  $('import').onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 1024*1024) throw new Error('备份文件过大');
      const restored = validate(JSON.parse(await file.text()));
      state = restored; persist(); render();
    } catch(error) { $('notice').textContent = `导入失败：${error.message}。原有进度已保留。`; }
    event.target.value = '';
  };
  render();
})();
