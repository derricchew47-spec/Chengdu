# -*- coding: utf-8 -*-
"""Expenses and family split-ledger behavior."""

JAVASCRIPT = r'''/* ───── Shared expenses + Splitwise engine ───── */
function loadLocalLedger(){try{const x=JSON.parse(store.get('chengduLedgerV3')||'null');if(x&&Array.isArray(x.members))return x}catch(e){}return{members:[],expenses:[],splits:[],settlements:[]}}
function saveLocalLedger(){store.set('chengduLedgerV3',JSON.stringify(ledger))}
function meId(){return store.get('chengduCurrentMember')||''}
function activeMembers(){return ledger.members.filter(m=>m.is_active!==false)}
function member(id){return ledger.members.find(m=>m.id===id)}
function memberName(id){return member(id)?.display_name||L('unknown')}
async function sbRequest(table,method='GET',query='',body=null,prefer='return=representation'){const base=CFG.supabase_url.replace(/\/$/,'')+`/rest/v1/${table}${query?`?${query}`:''}`,headers={apikey:CFG.supabase_key,'Content-Type':'application/json',Prefer:prefer};if(String(CFG.supabase_key).split('.').length===3)headers.Authorization=`Bearer ${CFG.supabase_key}`;const r=await fetch(base,{method,headers,body:body==null?undefined:JSON.stringify(body)});if(!r.ok)throw Error(await r.text());const out=await r.text();return out?JSON.parse(out):[]}
const OUTBOX_KEY='chengduLedgerOutboxV1';let outboxFlushing=false;
function loadOutbox(){try{const q=JSON.parse(store.get(OUTBOX_KEY)||'[]');return Array.isArray(q)?q:[]}catch(e){return[]}}
function saveOutbox(q){store.set(OUTBOX_KEY,JSON.stringify(q))}
function queueMutation(op){const q=loadOutbox();q.push({op_id:uid(),created_at:new Date().toISOString(),...op});saveOutbox(q)}
async function flushOutbox(){
  if(!CLOUD||outboxFlushing)return !loadOutbox().length;
  outboxFlushing=true;
  try{
    let q=loadOutbox();
    while(q.length){const op=q[0],query=op.method==='POST'?[op.query,'on_conflict=id'].filter(Boolean).join('&'):op.query,prefer=op.method==='POST'?'resolution=merge-duplicates,return=minimal':'return=minimal';try{await sbRequest(op.table,op.method,query||'',op.body??null,prefer);q.shift();saveOutbox(q)}catch(e){cloudStatus='failed';return false}}
    cloudStatus='cloud';return true;
  }finally{outboxFlushing=false}
}
function mergeRows(remote,local){const m=new Map((remote||[]).map(x=>[x.id,x]));(local||[]).forEach(x=>m.set(x.id,x));return[...m.values()]}
function mergeRemoteWithLocal(remote,pending){const merged={members:mergeRows(remote.members,ledger.members),expenses:mergeRows(remote.expenses,ledger.expenses),splits:mergeRows(remote.splits,ledger.splits),settlements:mergeRows(remote.settlements,ledger.settlements)};pending.filter(x=>x.method==='DELETE').forEach(op=>{const p=new URLSearchParams(op.query||''),id=(p.get('id')||'').replace(/^eq\./,''),expenseId=(p.get('expense_id')||'').replace(/^eq\./,'');const key=op.table==='expense_splits'?'splits':op.table;if(id&&merged[key])merged[key]=merged[key].filter(x=>x.id!==id);if(expenseId&&merged.splits)merged.splits=merged.splits.filter(x=>x.expense_id!==expenseId)});return merged}
async function syncLedger(){if(!CLOUD){cloudStatus='local';return}cloudStatus='syncing';renderExpenses();await flushOutbox();try{const q=`trip_id=eq.${encodeURIComponent(TRIP_ID)}&order=created_at.asc`,[members,expenses,splits,settlements]=await Promise.all([sbRequest('members','GET',q),sbRequest('expenses','GET',q),sbRequest('expense_splits','GET',`trip_id=eq.${encodeURIComponent(TRIP_ID)}&order=created_at.asc`),sbRequest('settlements','GET',q)]),remote={members,expenses,splits,settlements},pending=loadOutbox();ledger=pending.length?mergeRemoteWithLocal(remote,pending):remote;saveLocalLedger();cloudStatus=pending.length?'failed':'cloud'}catch(e){cloudStatus='failed'}renderExpenses()}
async function cloudBatch(ops){if(!CLOUD)return true;ops.forEach(queueMutation);const ok=await flushOutbox();if(!ok)toast(L('queued_offline'));if(currentPage==='expenses')renderExpenses();return ok}
async function cloudInsert(table,row){return cloudBatch([{table,method:'POST',query:'',body:row}])}
async function cloudPatch(table,id,row){return cloudBatch([{table,method:'PATCH',query:`id=eq.${encodeURIComponent(id)}&trip_id=eq.${encodeURIComponent(TRIP_ID)}`,body:row}])}
async function cloudDelete(table,query){return cloudBatch([{table,method:'DELETE',query,body:null}])}
function ledgerStats(){const stats={};ledger.members.forEach(m=>stats[m.id]={paid:0,share:0,net:0});ledger.expenses.forEach(e=>{if(stats[e.paid_by_member_id])stats[e.paid_by_member_id].paid+=Number(e.amount)});ledger.splits.forEach(s=>{if(stats[s.member_id])stats[s.member_id].share+=Number(s.share_amount)});Object.values(stats).forEach(x=>x.net=x.paid-x.share);ledger.settlements.forEach(s=>{if(stats[s.from_member_id])stats[s.from_member_id].net+=Number(s.amount);if(stats[s.to_member_id])stats[s.to_member_id].net-=Number(s.amount)});const creditors=Object.entries(stats).filter(([,x])=>x.net>.005).map(([id,x])=>({id,amt:x.net})).sort((a,b)=>b.amt-a.amt),debtors=Object.entries(stats).filter(([,x])=>x.net<-.005).map(([id,x])=>({id,amt:-x.net})).sort((a,b)=>b.amt-a.amt),transfers=[];let i=0,j=0;while(i<debtors.length&&j<creditors.length){const a=Math.min(debtors[i].amt,creditors[j].amt);if(a>.005)transfers.push({from:debtors[i].id,to:creditors[j].id,amount:Math.round(a*100)/100});debtors[i].amt-=a;creditors[j].amt-=a;if(debtors[i].amt<.005)i++;if(creditors[j].amt<.005)j++}return{stats,transfers}}
function fxText(n){return fxRate?`RM ${(Number(n)*fxRate).toFixed(2)}`:''}
async function loadFx(){const c=cacheRead('chengduFxCnyMyr',12*60*60*1000)||cacheAny('chengduFxCnyMyr');if(c?.rate)fxRate=c.rate;try{const r=await fetch('https://open.er-api.com/v6/latest/CNY'),j=await r.json();if(j?.rates?.MYR){fxRate=Number(j.rates.MYR);cacheWrite('chengduFxCnyMyr',{rate:fxRate})}}catch(e){}if(currentPage==='expenses')renderExpenses()}

const EXPENSE_AVATARS=DATA.avatar_options||[];

function avatarIndexForMember(m){
  if(m&&Number.isInteger(m.avatar_index)&&m.avatar_index>=0&&m.avatar_index<EXPENSE_AVATARS.length)return m.avatar_index;
  const s=String(m?.id||m?.display_name||'member');
  let h=0;for(let i=0;i<s.length;i++)h=((h<<5)-h+s.charCodeAt(i))|0;
  return Math.abs(h)%Math.max(1,EXPENSE_AVATARS.length)
}
function memberAvatar(id){
  const m=member(id),opt=EXPENSE_AVATARS[avatarIndexForMember(m)];
  return opt?.src||''
}
function avatarHTML(id,cls='balance-avatar'){
  const src=memberAvatar(id),name=memberName(id);
  return src?`<img class="${cls}" src="${src}" alt="${esc(name)}">`:`<span class="${cls} avatar">${esc((name[0]||'?').toUpperCase())}</span>`
}
function expenseThumb(category){
  const map={'餐饮':3,'交通':9,'门票':0,'购物':7,'住宿':2,'其他':5};
  const idx=map[category]??5;
  return EXPENSE_AVATARS[idx]?.src||''
}
function setExpenseFocus(k){expenseFocus=k;renderExpenses()}
function toggleMemberBalances(){memberBalancesExpanded=!memberBalancesExpanded;renderExpenses()}
function expenseDate(e){
  const d=new Date(e.created_at);if(Number.isNaN(d.getTime()))return'';
  return lang==='zh'?`${d.getMonth()+1}月${d.getDate()}日`:d.toLocaleDateString('en',{month:'short',day:'numeric'})
}
function expenseTime(e){
  const d=new Date(e.created_at);if(Number.isNaN(d.getTime()))return'';
  return d.toLocaleTimeString(lang==='zh'?'zh-CN':'en',{hour:'2-digit',minute:'2-digit',hour12:false})
}
function focusedExpenses(me){
  const all=[...ledger.expenses].sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)));
  if(!me)return all;
  if(expenseFocus==='paid')return all.filter(e=>e.paid_by_member_id===me);
  if(expenseFocus==='owed'){
    return all.filter(e=>{
      if(e.paid_by_member_id!==me)return false;
      const mine=ledger.splits.find(s=>s.expense_id===e.id&&s.member_id===me);
      return ledger.splits.some(s=>s.expense_id===e.id&&s.member_id!==me&&Number(s.share_amount)>0) || !!mine
    })
  }
  if(expenseFocus==='owe'){
    return all.filter(e=>e.paid_by_member_id!==me&&ledger.splits.some(s=>s.expense_id===e.id&&s.member_id===me&&Number(s.share_amount)>0))
  }
  return all
}
function cloudMiniStatus(){
  const key=CLOUD&&cloudStatus==='cloud'?'cloud_mode':cloudStatus==='syncing'?'syncing':cloudStatus==='failed'?'sync_failed':'local_mode';
  return `<div class="expense-cloud-note">${L(key)}</div>`
}
function expenseShell(inner){
  const members=activeMembers();
  const panda=DATA.expense_hero||DATA.images.panda_bamboo||DATA.images.panda_portrait||'';
  return`<div class="expenses-hero-head" style="--expense-panda:url('${panda}')">
      <div class="expenses-hero-title"><h1>${L('expenses_title')}</h1><p>${L('trip_expense_sub',{n:members.length||8})}</p></div>
      <button class="expense-refresh" onclick="syncLedger()" aria-label="${L('refresh')}">${icon('refresh','sm')}</button>
    </div>${inner}<button class="expense-fab" onclick="openExpenseSheet()" aria-label="${L('add_expense')}">＋</button>`
}
function renderExpenses(){
  $('#expenses').className='page app-page'+(currentPage==='expenses'?' active':'');
  let inner='';
  if(expenseTab==='overview')inner=renderExpenseOverview();
  else if(expenseTab==='bills')inner=renderBills();
  else if(expenseTab==='split')inner=renderSplit();
  else inner=renderMembers();
  $('#expenses').innerHTML=expenseShell(inner);
}
function renderExpenseOverview(){
  const me=meId(),{stats,transfers}=ledgerStats(),mine=stats[me]||{paid:0,share:0,net:0};
  const owed=transfers.filter(x=>x.to===me).reduce((s,x)=>s+x.amount,0);
  const owe=transfers.filter(x=>x.from===me).reduce((s,x)=>s+x.amount,0);
  const ms=activeMembers().slice(0,8);
  const nonZero=ms.filter(m=>Math.abs((stats[m.id]?.net||0))>.005).length;
  const recent=focusedExpenses(me).slice(0,3);

  return`${cloudMiniStatus()}
    <section class="expense-overview-card">
      <div class="expense-overview-label">${L('actual_spend')}</div>
      <div class="expense-overview-amount">${money(mine.share)}</div>
      ${fxRate?`<div class="expense-overview-fx">≈ ${fxText(mine.share)}</div>`:''}
      <div class="expense-overview-rule"></div>
      <div class="expense-overview-pair">
        <div class="expense-metric"><div class="expense-metric-icon">${icon('wallet','sm')}</div><div><small>${L('i_paid')}</small><b>${money(mine.paid)}</b></div></div>
        <div class="expense-overview-divider"></div>
        <div class="expense-metric"><div class="expense-metric-icon">${icon('refresh','sm')}</div><div><small>${L('owed_to_me')}</small><b>${money(owed)}</b></div></div>
      </div>
    </section>

    <div class="expense-focus-tabs">
      ${[
        ['paid','my_payments','My payments'],
        ['owed','owed_to_me_tab','Owed to me'],
        ['owe','i_owe_others','I owe others']
      ].map(x=>`<button class="expense-focus-tab ${expenseFocus===x[0]?'active':''}" onclick="setExpenseFocus('${x[0]}')"><span class="tab-main">${L(x[1])}</span></button>`).join('')}
    </div>

    ${renderMemberBalanceCard(ms,stats,nonZero)}
    ${renderRecentExpenses(recent)}
    ${renderSettlementSuggestions(transfers)}
    ${!me?`<div class="local-note">${L('no_me')}</div>`:''}`
}
function renderMemberBalanceCard(ms,stats,nonZero){
  const overlap=ms.map(m=>avatarHTML(m.id)).join('');
  const grid=ms.map(m=>{
    const net=stats[m.id]?.net||0;
    const cls=Math.abs(net)<.005?'balance-zero':net>0?'balance-positive':'balance-negative';
    const value=Math.abs(net)<.005?L('settled_short'):`${net>0?'+':'−'}${money(Math.abs(net)).replace('¥ ','¥')}`;
    return`<div class="member-balance-person">${avatarHTML(m.id,'')}<b>${esc(m.display_name)}</b><span class="${cls}">${value}</span></div>`
  }).join('');
  return`<section class="expense-section-card member-balance-card ${memberBalancesExpanded?'expanded':''}" onclick="toggleMemberBalances()">
      <div class="expense-section-head"><h3>${L('member_balance')}</h3><button class="expense-section-link" onclick="event.stopPropagation();toggleMemberBalances()">${L(memberBalancesExpanded?'collapse':'view_all')} ${memberBalancesExpanded?'⌃':'›'}</button></div>
      <div class="member-balance-summary">
        <div class="member-overlap">${overlap}</div>
        <div class="member-balance-summary-copy"><b>${L('members_count',{n:ms.length})}</b><small>${L('balances_count',{n:nonZero})}</small></div>
      </div>
      <div class="member-balance-grid-wrap"><div class="member-balance-grid-clip"><div class="member-balance-grid">${grid}</div></div></div>
    </section>`
}
function renderRecentExpenses(recent){
  const rows=recent.map(e=>{
    const sp=ledger.splits.filter(s=>s.expense_id===e.id);
    const src=expenseThumb(e.category);
    return`<div class="expense-recent-row" onclick="openExpenseDetail('${e.id}',this)">
      ${src?`<img class="expense-thumb" src="${src}" alt="">`:`<div class="expense-thumb"></div>`}
      <div class="expense-recent-main"><b>${esc(e.description||catLabel(e.category))}</b><small>${L('paid_by_short',{name:memberName(e.paid_by_member_id),n:sp.length})}</small></div>
      <div class="expense-recent-money"><b>${money(e.amount)}</b><small>${expenseDate(e)}</small></div>
      <div class="expense-row-chevron">›</div>
    </div>`
  }).join('');
  return`<section class="expense-section-card">
      <div class="expense-section-head"><h3>${L('recent_expenses')}</h3><button class="expense-section-link" onclick="expenseTab='bills';renderExpenses()">${L('view_all')} ›</button></div>
      <div class="expense-recent-list">${rows||`<div class="state-card"><h3>${L('no_expenses')}</h3><p>${L('start_today')}</p></div>`}</div>
    </section>`
}
function renderSettlementSuggestions(transfers){
  const rows=transfers.slice(0,3).map(x=>`<div class="settlement-row">
      <div class="settlement-route">${avatarHTML(x.from,'')}<b>${esc(memberName(x.from))}</b><span class="settlement-arrow">→</span>${avatarHTML(x.to,'')}<b>${esc(memberName(x.to))}</b></div>
      <div class="settlement-amount">${money(x.amount)}</div>
      <button class="settlement-remind" onclick="settleDebt('${x.from}','${x.to}',${x.amount})">${L('remind')}</button>
    </div>`).join('');
  return`<section class="expense-section-card settlement-card">
      <div class="expense-section-head"><h3>✦ ${L('settlement_suggestions')}</h3><button class="expense-section-link" onclick="expenseTab='split';renderExpenses()">${L('view_details')} ›</button></div>
      ${rows||`<div class="state-card"><h3>${L('settled')}</h3><p>${L('no_balances')}</p></div>`}
    </section>`
}
function renderBills(){
  const rows=[...ledger.expenses].sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at))).map(e=>{
    const sp=ledger.splits.filter(s=>s.expense_id===e.id),src=expenseThumb(e.category);
    return`<div class="expense-recent-row" onclick="openExpenseDetail('${e.id}',this)">
      ${src?`<img class="expense-thumb" src="${src}" alt="">`:''}
      <div class="expense-recent-main"><b>${esc(e.description||catLabel(e.category))}</b><small>${L('paid_by_short',{name:memberName(e.paid_by_member_id),n:sp.length})}</small></div>
      <div class="expense-recent-money"><b>${money(e.amount)}</b><small>${expenseDate(e)}</small></div><div class="expense-row-chevron">›</div></div>`
  }).join('');
  return`${cloudMiniStatus()}<section class="expense-section-card"><div class="expense-section-head"><h3>${L('bills')}</h3><button class="expense-section-link" onclick="expenseTab='overview';renderExpenses()">‹ ${L('overview')}</button></div><div class="expense-recent-list">${rows||`<div class="state-card"><h3>${L('no_expenses')}</h3></div>`}</div></section>`
}
function renderSplit(){
  const {stats,transfers}=ledgerStats(),ms=activeMembers().slice(0,8);
  return`${cloudMiniStatus()}<section class="expense-section-card"><div class="expense-section-head"><h3>${L('member_balance')}</h3><button class="expense-section-link" onclick="expenseTab='overview';renderExpenses()">‹ ${L('overview')}</button></div>
    <div class="member-balance-grid" style="border-top:0;padding-top:3px">${ms.map(m=>{const net=stats[m.id]?.net||0,cls=Math.abs(net)<.005?'balance-zero':net>0?'balance-positive':'balance-negative',v=Math.abs(net)<.005?L('settled_short'):`${net>0?'+':'−'}${money(Math.abs(net)).replace('¥ ','¥')}`;return`<div class="member-balance-person">${avatarHTML(m.id,'')}<b>${esc(m.display_name)}</b><span class="${cls}">${v}</span></div>`}).join('')}</div></section>${renderSettlementSuggestions(transfers)}`
}
function renderMembers(){
  const rows=ledger.members.map(m=>`<div class="member-row paper-card ${m.is_active===false?'inactive':''}">
      ${avatarHTML(m.id,'balance-avatar')}
      <div class="member-main"><b>${esc(m.display_name)} ${m.id===meId()?`<span class="me-badge">${L('this_is_me')}</span>`:''}</b><small>${m.is_active===false?L('inactive_label'):''}</small></div>
      <div class="row-actions">${m.is_active!==false&&m.id!==meId()?`<button onclick="chooseMe('${m.id}')" aria-label="${L('this_is_me')}">${icon('check','sm')}</button>`:''}<button onclick="openMemberSheet('${m.id}')" aria-label="${L('rename')}">${icon('edit','sm')}</button><button onclick="toggleMember('${m.id}')" aria-label="${L(m.is_active===false?'activate':'deactivate')}">${m.is_active===false?'↺':icon('users','sm')}</button></div></div>`).join('');
  return`${cloudMiniStatus()}<section class="expense-section-card"><div class="expense-section-head"><h3>${L('members')}</h3><button class="expense-section-link" onclick="expenseTab='overview';renderExpenses()">‹ ${L('overview')}</button></div><button class="primary-btn full" onclick="openMemberSheet()">＋ ${L('add_member')}</button><div class="member-list" style="margin-top:9px">${rows||`<div class="state-card"><h3>${L('member_needed')}</h3></div>`}</div></section>`
}
function chooseMe(id){store.set('chengduCurrentMember',id);renderExpenses()}

function avatarPickerHTML(selected){
  return`<div class="field"><label>${L('choose_avatar')}</label><div class="expense-avatar-picker">${EXPENSE_AVATARS.map((a,i)=>`<button type="button" class="expense-avatar-choice ${i===selected?'selected':''}" data-avatar-index="${i}" onclick="selectAvatarChoice(${i})"><img src="${a.src}" alt="${L(a.key)}"><span>${L(a.key)}</span></button>`).join('')}</div><input type="hidden" id="memberAvatarInput" value="${selected}"></div>`
}
function selectAvatarChoice(i){
  const input=$('#memberAvatarInput');if(input)input.value=String(i);
  $$('.expense-avatar-choice').forEach(b=>b.classList.toggle('selected',Number(b.dataset.avatarIndex)===i))
}
function openMemberSheet(id=''){
  const m=member(id),selected=avatarIndexForMember(m);
  showExpenseModal(`<div class="sheet-title"><h2>${m?L('rename'):L('add_member')}</h2><button class="sheet-close" onclick="closeExpenseModal()">×</button></div><div class="form-grid"><div class="field"><label>${L('member_name')}</label><input id="memberNameInput" value="${esc(m?.display_name||'')}" maxlength="40" autocomplete="off"></div>${avatarPickerHTML(selected)}${!m?`<label class="check-pill"><input id="memberMeInput" type="checkbox" ${!meId()?'checked':''}> ${L('this_is_me')}</label>`:''}<button class="primary-btn full" onclick="saveMemberSheet('${id}')">${L('save')}</button></div>`);
  setTimeout(()=>$('#memberNameInput')?.focus(),80)
}
async function saveMemberSheet(id){
  const input=$('#memberNameInput'),name=input.value.trim(),avatarIndex=Math.max(0,Math.min(EXPENSE_AVATARS.length-1,Number($('#memberAvatarInput')?.value)||0));
  if(!name){input.focus();return}
  if(ledger.members.some(m=>m.display_name.toLowerCase()===name.toLowerCase()&&m.id!==id)){toast(L('member_exists'));return}
  if(id){
    const m=member(id);m.display_name=name;m.avatar_index=avatarIndex;saveLocalLedger();closeExpenseModal();renderExpenses();
    try{await cloudPatch('members',id,{display_name:name})}catch(e){toast(L('sync_failed'))}
  }else{
    const m={id:uid(),trip_id:TRIP_ID,display_name:name,is_active:true,avatar_index:avatarIndex,created_at:new Date().toISOString()};
    ledger.members.push(m);if($('#memberMeInput')?.checked||!meId())store.set('chengduCurrentMember',m.id);saveLocalLedger();closeExpenseModal();renderExpenses();
    try{await cloudInsert('members',{id:m.id,trip_id:m.trip_id,display_name:m.display_name,is_active:m.is_active,created_at:m.created_at})}catch(e){toast(L('sync_failed'))}
  }
}
async function toggleMember(id){const m=member(id);if(!m)return;if(m.id===meId()&&m.is_active!==false){toast(L('cannot_deactivate_me'));return}if(m.is_active!==false&&!confirm(L('confirm_deactivate')))return;m.is_active=m.is_active===false;saveLocalLedger();renderExpenses();try{await cloudPatch('members',id,{is_active:m.is_active})}catch(e){toast(L('sync_failed'))}}

function openExpenseSheet(){
  const ms=activeMembers();if(!ms.length){toast(L('member_needed'));expenseTab='members';renderExpenses();return}
  const cats=['餐饮','交通','门票','购物','住宿','其他'];
  showExpenseModal(`<div class="sheet-title"><h2>${L('add_expense')}</h2><button class="sheet-close" onclick="closeExpenseModal()">×</button></div><div class="form-grid"><div class="field"><label>${L('amount')} · CNY</label><input id="billAmount" inputmode="decimal" placeholder="¥ 0.00" oninput="updateSplitFields()"></div><div class="field"><label>${L('category')}</label><select id="billCategory">${cats.map(c=>`<option value="${c}">${catLabel(c)}</option>`).join('')}</select></div><div class="field"><label>${L('description')}</label><input id="billNote" placeholder="${L('optional')}"></div><div class="field"><label>${L('paid_by')}</label><select id="billPayer">${ms.map(m=>`<option value="${m.id}" ${m.id===meId()?'selected':''}>${esc(m.display_name)}</option>`).join('')}</select></div><div class="field"><label>${L('participants')}</label><div class="check-grid">${ms.map(m=>`<label class="check-pill"><input class="participant-check" type="checkbox" value="${m.id}" checked onchange="updateSplitFields()"> ${esc(m.display_name)}</label>`).join('')}</div></div><div class="field"><label>${L('split_method')}</label><select id="billMethod" onchange="updateSplitFields()"><option value="equal">${L('equal')}</option><option value="exact">${L('exact')}</option><option value="percentage">${L('percentage')}</option><option value="shares">${L('shares')}</option></select></div><div id="splitFields" class="split-lines"></div><div id="billValidation" class="validation"></div><button class="primary-btn full" onclick="saveExpense()">${L('save')}</button></div>`);
  updateSplitFields()
}

let expenseModalOrigin=null,expenseModalClosing=false;
function showExpenseModal(html,originEl=null){
  closeExpenseModal(true);
  expenseModalOrigin=originEl||null;expenseModalClosing=false;
  const back=document.createElement('div');back.className=originEl?'expense-detail-backdrop':'expense-sheet-backdrop';back.id='expenseModalBackdrop';
  back.innerHTML=`<div class="${originEl?'expense-detail-panel':'expense-sheet-panel'}" id="expenseModalPanel">${html}</div>`;
  back.addEventListener('click',e=>{if(e.target===back)closeExpenseModal()});document.body.appendChild(back);
  const panel=$('#expenseModalPanel'),mainEl=document.querySelector('main');if(mainEl)mainEl.style.overflowY='hidden';
  if(!originEl){panel.style.opacity='1';return}
  const target=panel.getBoundingClientRect(),src=originEl.getBoundingClientRect();
  const sx=Math.max(.15,Math.min(1.5,src.width/target.width)),sy=Math.max(.15,Math.min(1.5,src.height/target.height));
  const dx=(src.left+src.width/2)-(target.left+target.width/2),dy=(src.top+src.height/2)-(target.top+target.height/2);
  panel.style.transform=`translate3d(${dx}px,${dy}px,0) scale(${sx},${sy})`;panel.style.borderRadius=getComputedStyle(originEl).borderRadius||'16px';
  requestAnimationFrame(()=>requestAnimationFrame(()=>{back.style.opacity='1';panel.style.opacity='1';panel.style.transform='translate3d(0,0,0) scale(1)';panel.style.borderRadius='25px'}))
}
function closeExpenseModal(immediate=false){
  const back=$('#expenseModalBackdrop');if(!back)return;
  const panel=$('#expenseModalPanel'),mainEl=document.querySelector('main');
  if(immediate||!expenseModalOrigin||!panel){
    back.remove();if(mainEl)mainEl.style.overflowY='auto';expenseModalOrigin=null;expenseModalClosing=false;return
  }
  if(expenseModalClosing)return;expenseModalClosing=true;
  const src=expenseModalOrigin&&expenseModalOrigin.isConnected?expenseModalOrigin.getBoundingClientRect():null,target=panel.getBoundingClientRect();
  back.style.opacity='0';
  if(src){
    const sx=Math.max(.15,Math.min(1.5,src.width/target.width)),sy=Math.max(.15,Math.min(1.5,src.height/target.height));
    const dx=(src.left+src.width/2)-(target.left+target.width/2),dy=(src.top+src.height/2)-(target.top+target.height/2);
    panel.style.transform=`translate3d(${dx}px,${dy}px,0) scale(${sx},${sy})`;panel.style.opacity='.15';panel.style.borderRadius=getComputedStyle(expenseModalOrigin).borderRadius||'16px'
  }
  setTimeout(()=>{back.remove();if(mainEl)mainEl.style.overflowY='auto';expenseModalOrigin=null;expenseModalClosing=false},300)
}
function openExpenseDetail(id,originEl){
  const e=ledger.expenses.find(x=>String(x.id)===String(id));if(!e)return;
  const splits=ledger.splits.filter(s=>s.expense_id===e.id),names=splits.map(s=>memberName(s.member_id)).join(' · ');
  showExpenseModal(`<div class="expense-detail-title"><div><h2>${esc(e.description||catLabel(e.category))}</h2><small>${expenseDate(e)} · ${expenseTime(e)}</small></div><button class="sheet-close" onclick="closeExpenseModal()">×</button></div>
    <div class="expense-detail-amount">${money(e.amount)}</div>
    <div class="expense-detail-list">
      <div class="expense-detail-item"><span>${L('category')}</span><b>${catLabel(e.category)}</b></div>
      <div class="expense-detail-item"><span>${L('paid_by')}</span><b>${esc(memberName(e.paid_by_member_id))}</b></div>
      <div class="expense-detail-item"><span>${L('participants')}</span><b>${splits.length} · ${esc(names)}</b></div>
      <div class="expense-detail-item"><span>${L('split_method')}</span><b>${L('equal')}</b></div>
    </div>
    <button class="expense-detail-primary" onclick="closeExpenseModal()">${L('done')}</button>
    <button class="expense-detail-delete" onclick="deleteExpense('${e.id}');closeExpenseModal(true)">${L('delete')}</button>`,originEl)
}

function participantIds(){return $$('.participant-check:checked').map(x=>x.value)}
function updateSplitFields(){const box=$('#splitFields');if(!box)return;const ids=participantIds(),amt=Math.round((parseFloat($('#billAmount')?.value)||0)*100)/100,method=$('#billMethod')?.value||'equal',pctBase=Math.floor(10000/Math.max(1,ids.length))/100;box.innerHTML=ids.map((id,i)=>{let val='';if(method==='equal')val=ids.length?(amt/ids.length).toFixed(2):'0.00';else if(method==='percentage')val=(i===ids.length-1?100-pctBase*(ids.length-1):pctBase).toFixed(2);else if(method==='shares')val='1';return`<div class="split-line"><span>${esc(memberName(id))}</span><input class="split-value" data-member="${id}" value="${val}" ${method==='equal'?'disabled':''} inputmode="decimal" oninput="validateSplitPreview()"></div>`}).join('');validateSplitPreview()}
function collectSplits(){const rawAmount=Number($('#billAmount').value),amount=Math.round(rawAmount*100),ids=participantIds(),method=$('#billMethod').value;if(!Number.isFinite(rawAmount)||!(amount>0)||!ids.length)return{ok:false};if(method==='equal'){const base=Math.floor(amount/ids.length),rem=amount-base*ids.length;return{ok:true,rows:ids.map((id,i)=>({member_id:id,cents:base+(i<rem?1:0)}))}}const vals=$$('.split-value').map(x=>({id:x.dataset.member,v:Number(x.value)}));if(vals.some(x=>!Number.isFinite(x.v)||x.v<0))return{ok:false};if(method==='exact'){const cents=vals.map(x=>Math.round(x.v*100)),sum=cents.reduce((a,b)=>a+b,0);return{ok:Math.abs(sum-amount)<=1,rows:vals.map((x,i)=>({member_id:x.id,cents:cents[i]}))}}if(method==='percentage'){const sum=vals.reduce((s,x)=>s+x.v,0);if(Math.abs(sum-100)>.01)return{ok:false};let used=0;const rows=vals.map((x,i)=>{const c=i===vals.length-1?amount-used:Math.round(amount*x.v/100);used+=c;return{member_id:x.id,cents:c}});return{ok:true,rows}}const total=vals.reduce((s,x)=>s+x.v,0);if(total<=0)return{ok:false};let used=0;const rows=vals.map((x,i)=>{const c=i===vals.length-1?amount-used:Math.round(amount*x.v/total);used+=c;return{member_id:x.id,cents:c}});return{ok:true,rows}}
function validateSplitPreview(){const v=$('#billValidation');if(!v)return;const r=collectSplits();v.textContent=r.ok?'':L(participantIds().length?'invalid_total':'select_participant')}
async function saveExpense(){const result=collectSplits();if(!result.ok){validateSplitPreview();return}const amount=Math.round(parseFloat($('#billAmount').value)*100)/100,expense={id:uid(),trip_id:TRIP_ID,amount,currency:'CNY',category:$('#billCategory').value,description:$('#billNote').value.trim(),paid_by_member_id:$('#billPayer').value,created_at:new Date().toISOString(),created_by_member_id:meId()||null},splits=result.rows.map(r=>({id:uid(),trip_id:TRIP_ID,expense_id:expense.id,member_id:r.member_id,share_amount:r.cents/100,created_at:expense.created_at}));ledger.expenses.push(expense);ledger.splits.push(...splits);saveLocalLedger();closeExpenseModal();renderExpenses();toast(L('saved'));if(CLOUD)await cloudBatch([{table:'expenses',method:'POST',query:'',body:expense},{table:'expense_splits',method:'POST',query:'',body:splits}])}
async function deleteExpense(id){if(!confirm(L('confirm_delete_expense')))return;ledger.expenses=ledger.expenses.filter(e=>e.id!==id);ledger.splits=ledger.splits.filter(s=>s.expense_id!==id);saveLocalLedger();renderExpenses();if(CLOUD)await cloudBatch([{table:'expense_splits',method:'DELETE',query:`expense_id=eq.${encodeURIComponent(id)}&trip_id=eq.${encodeURIComponent(TRIP_ID)}`,body:null},{table:'expenses',method:'DELETE',query:`id=eq.${encodeURIComponent(id)}&trip_id=eq.${encodeURIComponent(TRIP_ID)}`,body:null}])}
function openSettlementSheet(prefFrom='',prefTo='',prefAmount=''){const ms=activeMembers();if(ms.length<2){toast(L('member_needed'));return}showModal(`<div class="sheet-title"><h2>${L('record_payment')}</h2><button class="sheet-close" onclick="closeExpenseModal()">×</button></div><div class="form-grid"><div class="field"><label>${L('from')}</label><select id="settleFrom">${ms.map(m=>`<option value="${m.id}" ${m.id===prefFrom?'selected':''}>${esc(m.display_name)}</option>`).join('')}</select></div><div class="field"><label>${L('to')}</label><select id="settleTo">${ms.map(m=>`<option value="${m.id}" ${m.id===prefTo?'selected':''}>${esc(m.display_name)}</option>`).join('')}</select></div><div class="field"><label>${L('payment_amount')}</label><input id="settleAmount" inputmode="decimal" value="${prefAmount||''}" placeholder="¥ 0.00"></div><button class="primary-btn full" onclick="saveSettlement()">${L('save')}</button></div>`)}
function settleDebt(from,to,amount){openSettlementSheet(from,to,amount.toFixed(2))}
async function saveSettlement(){const from=$('#settleFrom').value,to=$('#settleTo').value,raw=Number($('#settleAmount').value),amount=Math.round(raw*100)/100;if(from===to||!Number.isFinite(raw)||!(amount>0)){toast(L('invalid_total'));return}const s={id:uid(),trip_id:TRIP_ID,from_member_id:from,to_member_id:to,amount,created_at:new Date().toISOString()};ledger.settlements.push(s);saveLocalLedger();closeExpenseModal();renderExpenses();toast(L('saved'));try{await cloudInsert('settlements',s)}catch(e){toast(L('sync_failed'))}}

'''
