# -*- coding: utf-8 -*-
"""Food page data and browser behavior."""

from shared import IMG


FOODS = [
    [IMG["mapo"], "陈麻婆豆腐（总店）", "川菜", 1.2, 16, "Open", 4.6, ["DP", "AM", "RED"]],
    [IMG["hotpot"], "蜀大侠火锅", "火锅", 0.45, 6, "Open", 4.5, ["DP", "AM", "RED"]],
    [IMG["snack"], "建设路小吃街", "小吃", 1.8, 23, "Open", 4.4, ["DP", "AM", "RED"]],
    [IMG["noodles"], "明婷饭店", "川菜", 1.1, 14, "Open", 4.4, ["DP", "AM"]],
    [IMG["coffee"], "% Arabica · 太古里", "咖啡", 0.75, 9, "Open", 4.6, ["AM", "GG"]],
    [IMG["dessert"], "成都小甜水", "甜品", 0.9, 12, "Open", 4.3, ["DP", "RED"]],
]

JAVASCRIPT = r'''/* ───── Food ───── */
function foodQueryText(){const a=`(around:${Math.round(foodRadius*1000)},${userLocation.lat},${userLocation.lon})`;let s='';if(foodCategory==='coffee')s=`nwr["amenity"="cafe"]${a};`;else if(foodCategory==='dessert')s=`nwr["amenity"~"ice_cream|cafe"]["cuisine"~"dessert|ice_cream|cake",i]${a};`;else if(foodCategory==='hotpot')s=`nwr["amenity"="restaurant"]["cuisine"~"hot_pot|hotpot",i]${a};`;else if(foodCategory==='noodles')s=`nwr["amenity"~"restaurant|fast_food"]["cuisine"~"noodle|ramen",i]${a};`;else if(foodCategory==='sichuan')s=`nwr["amenity"="restaurant"]["cuisine"~"sichuan|chinese",i]${a};`;else if(foodCategory==='snacks')s=`nwr["amenity"~"fast_food|food_court"]${a};`;else s=`nwr["amenity"~"restaurant|fast_food|cafe|food_court|ice_cream"]${a};`;return`[out:json][timeout:20];(${s});out center tags;`}
async function loadFoodPois(force=false){if(!userLocation)return;foodLoading=true;foodError='';renderFood();const key=`chengduPoi:food:${locCache()}:${foodRadius}:${foodCategory}`;if(force)store.set(key,'');try{const r=await fetchOverpass(foodQueryText(),key);foodPois=normalizePois(r.data,'food').filter(p=>p.distance<=foodRadius*1000);foodError=r.cached?'cached':''}catch(e){foodPois=[];foodError='failed'}foodLoading=false;renderFood()}
function selectFoodCategory(k){foodCategory=k;userLocation?loadFoodPois():renderFood()}
function setFoodRadius(r){foodRadius=r;userLocation?loadFoodPois():renderFood()}
function setFoodSearch(v){foodQuery=v.trim().toLowerCase();clearTimeout(foodSearchTimer);foodSearchTimer=setTimeout(renderFood,180)}
function nearbyToolsHTML(){
  const icons={attractions:'landmark',convenience:'shopping',toilets:'toilet',pharmacy:'pharmacy',coffee:'coffee',shopping:'shopping',hotels:'hotel'};
  return`<section class="nearby-tools"><div class="nearby-tools-head"><h2>${L('nearby_services')}</h2><small>${L('opens_amap')}</small></div><div class="nearby-tools-grid">${AMAP_NEARBY_TYPES.map(k=>`<button class="nearby-tool" onclick="openAmapNearby('${k}')">${icon(icons[k])}<span>${L(k==='shopping'?'shopping_places':k)}</span></button>`).join('')}</div></section>`
}
function foodCard(p){const photo=p.photo?`<img class="food-photo" src="${esc(p.photo)}" alt="${esc(p.name)}" loading="lazy" onerror="this.outerHTML='<div class=&quot;food-placeholder&quot;>🍜</div>'">`:`<div class="food-placeholder">🍜</div>`;return`<article class="food-card live paper-card" onclick="openFoodSheet('${esc(p.id)}')">${photo}<div><h3>${esc(p.name)}</h3><div class="score">${p.score}</div><div class="food-line">${foodLabel(p.foodCat)} · ${distanceText(p.distance)} · ${L('walk',{n:p.walk})}</div><div class="food-bottom"><span class="smart">${L('smart_score')} ${p.score}</span>${p.status?`<span class="open-label">${p.status}</span>`:''}<span class="confidence">${p.confidence}</span></div></div></article>`}
function locationState(source){
  if(geoStatus==='pending')return`<div class="state-card paper-card"><div class="spinner"></div><h3>${L('locating')}</h3></div>`;
  const states={denied:['location_denied','location_denied_body'],insecure:['location_insecure','location_insecure_body'],unavailable:['location_unavailable','location_unavailable_body']};
  const copy=states[geoStatus]||['location_title','location_body'];
  return`<div class="state-card paper-card"><div class="state-icon">${icon('locate','lg')}</div><h3>${L(copy[0])}</h3><p>${L(copy[1])}</p><button class="primary-btn" onclick="requestLocation('${source}')">${L(geoStatus==='idle'?'locate':'retry')}</button></div>`
}
function renderFood(){
  const shown=foodPois.filter(p=>!foodQuery||p.name.toLowerCase().includes(foodQuery));
  $('#food').className='page app-page'+(currentPage==='food'?' active':'');
  $('#food').innerHTML=`<div class="app-head"><div><h1>${L('food_title')}</h1><p>${L('food_sub')}</p></div><div class="head-actions"><button class="icon-btn" onclick="requestLocation('food')" aria-label="${L('locate')}">${icon('locate')}</button></div></div>
  ${nearbyToolsHTML()}
  <div class="tool-row"><div class="search-box">${icon('search','sm')}<input value="${esc(foodQuery)}" oninput="setFoodSearch(this.value)" placeholder="${L('search_food')}"></div></div>
  <div class="filter-scroll">${FOOD_FILTERS.map(k=>`<button class="filter-chip ${k===foodCategory?'active':''}" onclick="selectFoodCategory('${k}')">${L(k)}</button>`).join('')}</div>
  <div class="radius-select"><span class="radius-label">${L('range')}</span>${[.5,1,2,5].map(r=>`<button class="${r===foodRadius?'active':''}" onclick="setFoodRadius(${r})">${r<1?'500m':r+'km'}</button>`).join('')}</div>
  ${!userLocation?locationState('food'):foodLoading?`<div class="state-card paper-card"><div class="spinner"></div><h3>${L('nearby_loading')}</h3></div>`:`${foodError?`<div class="local-note">${L(foodError==='cached'?'cached':'service_down')} ${foodError==='failed'?`<button class="mini-btn" onclick="loadFoodPois(true)">${L('retry')}</button> <a class="mini-btn" target="_blank" rel="noopener" href="${amapNearbyUrl('food')}">${L('amap_nearby')}</a>`:''}</div>`:''}<div class="food-list">${shown.map(foodCard).join('')||`<div class="state-card paper-card"><h3>${L('nothing_food')}</h3><p>${L('wider')}</p></div>`}</div>`}`;
  if(currentPage==='food'&&userLocation&&!foodLoading&&!foodPois.length&&!foodError)setTimeout(()=>loadFoodPois(),80);
}
function openFoodSheet(id){const p=foodPois.find(x=>x.id===id);if(!p)return;selectedFood=p;const img=p.photo?`<img class="detail-photo" src="${esc(p.photo)}" alt="${esc(p.name)}" onerror="this.outerHTML='<div class=&quot;detail-placeholder&quot;>🍜</div>'">`:`<div class="detail-placeholder">🍜</div>`;const q=encodeURIComponent(p.name);showModal(`<div class="sheet-title"><div><h2>${esc(p.name)}</h2><p>${foodLabel(p.foodCat)} · ${distanceText(p.distance)}</p></div><button class="sheet-close" onclick="closeModal()">×</button></div>${img}<div class="detail-grid"><div class="detail-stat"><small>${L('smart_score')}</small><b>${p.score}</b></div><div class="detail-stat"><small>${L('walking')}</small><b>${L('walk',{n:p.walk})}</b></div><div class="detail-stat"><small>${L('status')}</small><b>${p.status||L('unknown')}</b></div><div class="detail-stat"><small>${L('price')}</small><b>${esc(p.tags['price:range']||L('unknown'))}</b></div></div><div class="sheet-actions"><a class="main" target="_blank" rel="noopener" href="${amapNavigationUrl(p)}">${L('navigate')}</a><a target="_blank" rel="noopener" href="https://m.dianping.com/search?keyword=${q}">${L('search_dp')}</a><a target="_blank" rel="noopener" href="https://www.xiaohongshu.com/search_result?keyword=${q}">${L('search_red')}</a></div>`)}
function showModal(html){closeModal();document.body.insertAdjacentHTML('beforeend',`<div class="modal-backdrop" id="modalBackdrop" onclick="if(event.target===this)closeModal()"><div class="sheet-modal"><div class="sheet-grab"></div>${html}</div></div>`)}
function closeModal(){const m=$('#modalBackdrop');if(m)m.remove()}

'''
