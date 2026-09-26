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
function foodQueryText(){
  const a=`(around:${Math.round(foodRadius*1000)},${userLocation.lat},${userLocation.lon})`;
  let s='';
  if(foodCategory==='coffee')s=`nwr["amenity"="cafe"]${a};`;
  else if(foodCategory==='dessert')s=`nwr["amenity"~"ice_cream|cafe"]["cuisine"~"dessert|ice_cream|cake|bakery",i]${a};`;
  else if(foodCategory==='hotpot')s=`nwr["amenity"="restaurant"]["cuisine"~"hot_pot|hotpot",i]${a};`;
  else if(foodCategory==='noodles')s=`nwr["amenity"~"restaurant|fast_food"]["cuisine"~"noodle|ramen|noodles",i]${a};`;
  else if(foodCategory==='sichuan')s=`nwr["amenity"="restaurant"]["cuisine"~"sichuan|chinese",i]${a};`;
  else if(foodCategory==='snacks')s=`nwr["amenity"~"fast_food|food_court"]${a};`;
  else s=`nwr["amenity"~"restaurant|fast_food|cafe|food_court|ice_cream"]${a};`;
  return`[out:json][timeout:20];(${s});out center tags;`
}
async function loadFoodPois(force=false){
  if(!userLocation)return;
  requestServerFood(force)
}
function selectFoodCategory(k){foodCategory=k;userLocation?loadFoodPois():renderFood()}
function setFoodRadius(r){foodRadius=r;userLocation?loadFoodPois():renderFood()}
function setFoodSearch(v){foodQuery=v.trim().toLowerCase();clearTimeout(foodSearchTimer);foodSearchTimer=setTimeout(renderFood,180)}

const CUISINE_ALIASES={
  hot_pot:'tag_hotpot',hotpot:'tag_hotpot',
  sichuan:'tag_sichuan',chinese:'tag_chinese',
  noodles:'tag_noodles',noodle:'tag_noodles',ramen:'tag_noodles',
  seafood:'tag_seafood',fish:'tag_seafood',
  barbecue:'tag_bbq',bbq:'tag_bbq',grill:'tag_bbq',
  curry:'tag_curry',
  malaysian:'tag_malaysian',singaporean:'tag_southeast_asian',
  thai:'tag_thai',vietnamese:'tag_vietnamese',
  japanese:'tag_japanese',korean:'tag_korean',
  western:'tag_western',burger:'tag_burger',pizza:'tag_pizza',
  fast_food:'tag_fastfood',
  dessert:'tag_dessert',cake:'tag_dessert',ice_cream:'tag_icecream',
  coffee:'tag_coffee',tea:'tag_tea',bubble_tea:'tag_tea',
  bakery:'tag_bakery',pastry:'tag_bakery',
  dim_sum:'tag_dimsum',dumpling:'tag_dumpling',
  vegetarian:'tag_vegetarian',vegan:'tag_vegetarian',
  rice:'tag_rice',fried_rice:'tag_rice',
  snack:'tag_snacks',snacks:'tag_snacks'
};
function cuisineTokens(p){
  const t=p.tags||{},raw=[t.cuisine,t['cuisine:1'],t['cuisine:2']].filter(Boolean).join(';').toLowerCase();
  let keys=raw.split(/[;,|]/).map(x=>x.trim().replace(/\s+/g,'_')).filter(Boolean)
    .map(x=>CUISINE_ALIASES[x]).filter(Boolean);
  if(t.amenity==='cafe')keys.push('tag_coffee');
  if(t.amenity==='ice_cream')keys.push('tag_icecream');
  if(t.amenity==='fast_food')keys.push('tag_fastfood');
  if(!keys.length){
    const fallback={sichuan:'tag_sichuan',hotpot:'tag_hotpot',snacks:'tag_snacks',noodles:'tag_noodles',coffee:'tag_coffee',dessert:'tag_dessert'}[p.foodCat];
    if(fallback)keys.push(fallback)
  }
  return [...new Set(keys)].slice(0,4)
}
function cuisineChips(p,limit=4){
  const keys=cuisineTokens(p).slice(0,limit);
  if(!keys.length)return`<span class="cuisine-chip muted">${L('category_unknown')}</span>`;
  return keys.map(k=>`<span class="cuisine-chip">${L(k)}</span>`).join('')
}
function compactStatus(p){
  return p.status?`<span class="food-status">${esc(p.status)}</span>`:`<span class="food-status quiet">${L('no_hours')}</span>`
}
function foodCarouselCard(p){
  return`<article class="food-focus-card" onclick="openFoodSheet('${esc(p.id)}')">
    <div class="food-card-handle"></div>
    <h3>${esc(p.name)}</h3>
    <div class="food-focus-meta">${foodLabel(p.foodCat)} · ${distanceText(p.distance)} · ${L('walk',{n:p.walk})}</div>
    <div class="food-focus-rule"></div>
    <div class="food-focus-stats"><span class="smart-pill">${L('smart_score')} ${p.score}</span>${compactStatus(p)}</div>
    <div class="cuisine-row">${cuisineChips(p,3)}</div>
  </article>`
}
function foodCompactCard(p){
  return`<article class="food-compact-card" onclick="openFoodSheet('${esc(p.id)}')">
    <div class="food-compact-main">
      <h3>${esc(p.name)}</h3>
      <div class="food-compact-meta">${foodLabel(p.foodCat)} · ${distanceText(p.distance)} · ${L('walk',{n:p.walk})}</div>
    </div>
    <div class="food-compact-bottom">
      <span class="smart-inline">${L('smart_score')} ${p.score}</span>${compactStatus(p)}
      <div class="compact-cuisines">${cuisineChips(p,2)}</div>
    </div>
  </article>`
}
function nearbyToolsHTML(){
  const icons={attractions:'landmark',convenience:'shopping',toilets:'toilet',pharmacy:'pharmacy',coffee:'coffee',shopping:'shopping',hotels:'hotel'};
  return`<details class="nearby-tools nearby-tools-collapsed">
    <summary><span>${L('nearby_services')}</span><small>${L('opens_amap')}</small></summary>
    <div class="nearby-tools-grid">${AMAP_NEARBY_TYPES.map(k=>`<button class="nearby-tool" onclick="openAmapNearby('${k}')">${icon(icons[k])}<span>${L(k==='shopping'?'shopping_places':k)}</span></button>`).join('')}</div>
  </details>`
}
function locationState(source){
  if(geoStatus==='pending')return`<div class="state-card paper-card"><div class="spinner"></div><h3>${L('locating')}</h3></div>`;
  const states={denied:['location_denied','location_denied_body'],insecure:['location_insecure','location_insecure_body'],unavailable:['location_unavailable','location_unavailable_body']};
  const copy=states[geoStatus]||['location_title','location_body'];
  return`<div class="state-card paper-card"><div class="state-icon">${icon('locate','lg')}</div><h3>${L(copy[0])}</h3><p>${L(copy[1])}</p><button class="primary-btn" onclick="requestLocation('${source}')">${L(geoStatus==='idle'?'locate':'retry')}</button></div>`
}
function renderFood(){
  const shown=foodPois.filter(p=>!foodQuery||p.name.toLowerCase().includes(foodQuery));
  const focus=shown.slice(0,6),more=shown.slice(6,18);
  $('#food').className='page app-page'+(currentPage==='food'?' active':'');
  $('#food').innerHTML=`<div class="app-head food-head">
    <div><h1>${L('food_title')}</h1><p>${L('food_sub')}</p></div>
    <div class="head-actions"><button class="location-pill" onclick="requestLocation('food')" aria-label="${L('locate')}">${icon('pin','sm')}<span>${foodRadius<1?'500 m':foodRadius+' km'}</span></button></div>
  </div>
  <div class="filter-scroll food-filter-tabs">${FOOD_FILTERS.map(k=>`<button class="filter-chip ${k===foodCategory?'active':''}" onclick="selectFoodCategory('${k}')">${L(k)}</button>`).join('')}</div>
  <div class="food-tools-row">
    <div class="search-box">${icon('search','sm')}<input value="${esc(foodQuery)}" oninput="setFoodSearch(this.value)" placeholder="${L('search_food')}"></div>
    <div class="radius-mini">${[.5,1,2,5].map(r=>`<button class="${r===foodRadius?'active':''}" onclick="setFoodRadius(${r})">${r<1?'500m':r+'km'}</button>`).join('')}</div>
  </div>
  ${!userLocation?locationState('food'):foodLoading?`<div class="state-card paper-card"><div class="spinner"></div><h3>${L('nearby_loading')}</h3></div>`:(!foodPois.length&&!foodError&&!DATA.server_food)?`<div class="state-card paper-card food-search-ready"><h3>${L('server_search_now')}</h3><p>${L('server_search_hint')}</p><button class="primary-btn" onclick="requestServerFood(false)">${L('server_search_now')}</button></div>`:
  `${foodError?`<div class="local-note">${L(foodError==='cached'?'cached':'service_down')} ${foodError==='failed'?`<button class="mini-btn" onclick="loadFoodPois(true)">${L('retry')}</button> <a class="mini-btn" target="_blank" rel="noopener" href="${amapNearbyUrl('food')}">${L('amap_nearby')}</a>`:''}</div>`:''}
   ${focus.length?`<section class="food-focus-section"><div class="food-carousel" id="foodCarousel">${focus.map(foodCarouselCard).join('')}</div><div class="food-carousel-dots">${focus.map((_,i)=>`<span class="${i===0?'active':''}"></span>`).join('')}</div></section>`:''}
   ${more.length?`<section class="food-more-section"><div class="food-section-head"><h2>${L('more_recommendations')}</h2><span>${L('sorted_by_score')}</span></div><div class="food-more-list">${more.map(foodCompactCard).join('')}</div></section>`:''}
   ${(!shown.length&&foodError!=='failed')?`<div class="state-card paper-card"><h3>${L('nothing_food')}</h3><p>${L('wider')}</p></div>`:''}
   ${nearbyToolsHTML()}`}`;
  bindFoodCarousel();
}
function bindFoodCarousel(){
  const sc=$('#foodCarousel');if(!sc)return;
  const dots=[...document.querySelectorAll('.food-carousel-dots span')];
  let raf=0;
  const update=()=>{raf=0;const cards=[...sc.querySelectorAll('.food-focus-card')];if(!cards.length)return;const center=sc.scrollLeft+sc.clientWidth/2;let best=0,bd=Infinity;cards.forEach((c,i)=>{const d=Math.abs(c.offsetLeft+c.offsetWidth/2-center);if(d<bd){bd=d;best=i}});dots.forEach((d,i)=>d.classList.toggle('active',i===best))};
  sc.addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(update)},{passive:true});
  requestAnimationFrame(update)
}
function openFoodSheet(id){
  const p=foodPois.find(x=>x.id===id);if(!p)return;selectedFood=p;
  const tags=cuisineTokens(p);
  showModal(`<div class="sheet-title food-sheet-title"><div><h2>${esc(p.name)}</h2><p>${foodLabel(p.foodCat)} · ${distanceText(p.distance)} · ${L('walk',{n:p.walk})}</p></div><button class="sheet-close" onclick="closeModal()">×</button></div>
    <div class="food-sheet-score-row"><span class="smart-pill large">${L('smart_score')} ${p.score}</span>${compactStatus(p)}</div>
    <section class="food-sheet-section"><h3>${L('food_categories')}</h3><div class="cuisine-row detail">${tags.length?tags.map(k=>`<span class="cuisine-chip">${L(k)}</span>`).join(''):`<span class="cuisine-chip muted">${L('category_unknown')}</span>`}</div></section>
    <div class="food-info-panel">
      <div><span>${L('hours')}</span><b>${p.tags.opening_hours?L('hours_listed'):L('no_hours')}</b></div>
      <div><span>${L('distance')}</span><b>${distanceText(p.distance)} · ${L('walk',{n:p.walk})}</b></div>
      <div><span>${L('data_source')}</span><b>OpenStreetMap</b></div>
      <div><span>${L('data_status')}</span><b>${esc(p.confidence)}</b></div>
    </div>
    <div class="food-source-note">${L('osm_notice')}</div>
    <div class="sheet-actions food-only-nav"><a class="main" target="_blank" rel="noopener" href="${amapNavigationUrl(p)}">${L('open_amap')}</a></div>`)
}
function showModal(html){closeModal();document.body.insertAdjacentHTML('beforeend',`<div class="modal-backdrop" id="modalBackdrop" onclick="if(event.target===this)closeModal()"><div class="sheet-modal food-sheet"><div class="sheet-grab"></div>${html}</div></div>`)}
function closeModal(){const m=$('#modalBackdrop');if(m)m.remove()}
'''
