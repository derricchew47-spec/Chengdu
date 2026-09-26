# -*- coding: utf-8 -*-
"""Frozen Landing page.

Do not change this module's visuals, timing, media, interactions, or behavior
unless the approved Landing design is intentionally being revised.
"""

CSS = r'''/* ───── LANDING ───── */
#landing{position:fixed;z-index:200;inset:0;margin:auto;width:min(100vw,460px);height:100dvh;overflow:hidden;background:#d8ebe3;transition:opacity .7s ease,visibility .7s ease}
#landing.hidden{opacity:0;visibility:hidden;pointer-events:none}
.land-scene{position:absolute;inset:0;overflow:hidden;background:#d8ebe3}
.land-scene img{width:100%;height:100%;object-fit:cover;object-position:50% 50%;animation:landCamera 8.8s cubic-bezier(.2,.72,.2,1) forwards}
.land-scene video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%;display:block;background:#d8ebe3}
.land-scene:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(250,253,247,.48) 0%,rgba(250,253,247,.02) 34%,rgba(19,71,52,.02) 61%,rgba(13,51,38,.52) 100%)}
@keyframes landCamera{0%{transform:scale(1.045) translate3d(0,1%,0)}100%{transform:scale(1) translate3d(0,-.4%,0)}}
.land-bamboo{position:absolute;z-index:2;left:-45px;top:-18px;width:215px;height:330px;opacity:.75;transform-origin:top;animation:sway 4.8s ease-in-out infinite alternate;pointer-events:none}
@keyframes sway{to{transform:rotate(2.4deg) translateX(3px)}}
.land-bamboo svg{width:100%;height:100%}
.land-brand{position:absolute;z-index:3;left:25px;right:25px;top:max(30px,env(safe-area-inset-top));text-align:center;color:#13231c;text-shadow:0 1px 12px rgba(255,255,255,.7);animation:titleReveal 1.2s ease both}
.land-brand h1{font:600 44px/.88 var(--serif);margin:0;letter-spacing:-1.3px}
.land-brand p{margin:11px 0 0;font:500 9px var(--sans);letter-spacing:4px}
.land-brand:after{content:"";display:block;width:28px;height:1px;background:#526358;margin:16px auto}
@keyframes titleReveal{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:none}}
.land-note{position:absolute;z-index:3;left:28px;right:28px;top:24%;text-align:right;color:#213f34;opacity:0;animation:noteIn .9s 2.4s ease forwards}
.land-note .cn{font:400 21px/1.55 var(--hand);letter-spacing:1px}.land-note .en{font:italic 13px var(--serif);color:#676c63}
@keyframes noteIn{to{opacity:1;transform:translateY(-6px)}}
.land-bubble{position:absolute;z-index:5;right:18px;left:68px;top:38%;padding:15px 18px 14px;border-radius:25px 25px 7px 25px;background:rgba(255,254,248,.93);color:#1e3a2f;box-shadow:0 13px 36px rgba(23,74,54,.16);opacity:0;transform:translateY(12px) scale(.97);animation:bubbleIn .7s 6.15s cubic-bezier(.2,.8,.2,1) forwards}
.land-bubble .cn{font:600 15px/1.5 var(--cn-serif)}.land-bubble .en{font:italic 12px/1.35 var(--serif);color:#74776e;margin-top:4px}
@keyframes bubbleIn{to{opacity:1;transform:none}}
.land-final{position:absolute;z-index:6;left:14px;right:14px;bottom:max(16px,env(safe-area-inset-bottom));border:1px solid rgba(255,255,255,.7);border-radius:28px;background:rgba(251,255,249,.94);box-shadow:0 20px 50px rgba(13,65,45,.24);padding:15px;opacity:0;transform:translateY(25px);animation:finalIn .8s 8.25s ease forwards}
@keyframes finalIn{to{opacity:1;transform:none}}
.land-final-top{display:flex;gap:12px;align-items:center}.land-avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.1)}
.land-final h3{font:600 20px/1 var(--serif);margin:0 0 4px}.land-final p{font-size:10px;color:var(--muted);margin:0}
.enter-btn{width:100%;margin-top:13px;border:0;border-radius:17px;padding:13px 15px;background:var(--forest);color:#fff;display:flex;align-items:center;justify-content:center;gap:9px;font-size:12px;cursor:pointer}
.land-skip{position:absolute;z-index:9;top:max(18px,env(safe-area-inset-top));right:16px;border:0;background:rgba(255,255,255,.5);backdrop-filter:blur(10px);padding:8px 11px;border-radius:99px;font-size:9px;color:#2d3e35;cursor:pointer}

@media (min-width:461px){.app-shell{margin:18px 0;border-radius:32px;min-height:calc(100dvh - 36px)}#landing{height:calc(100dvh - 36px);top:18px;border-radius:32px}.bottom-nav{bottom:18px;border-radius:0 0 32px 32px}}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.001ms!important;animation-delay:0ms!important;transition-duration:.001ms!important;transition-delay:0ms!important}}
</style>'''

MARKUP = r'''  <div id="landing" aria-label="Our Chengdu Story opening">
    <div class="land-scene"><video id="landingVideo" muted playsinline preload="auto" aria-label="Panda walking through a Chengdu garden"></video><img id="landingPhoto" alt="A giant panda walking beside a Chengdu garden lake" style="display:none"></div>
    <div class="land-bamboo" aria-hidden="true"><svg viewBox="0 0 210 330" fill="none"><path d="M21-5c16 91 30 192 47 345M83-10c5 102 13 203 20 344" stroke="#60775f" stroke-width="4" opacity=".62"/><g fill="#748a70" opacity=".75"><path d="M33 48C7 22 3 11 1 2c25 3 43 14 51 33-5 8-11 12-19 13Z"/><path d="M46 85C16 70 7 59 3 50c26-3 46 4 58 20-2 8-7 13-15 15Z"/><path d="M62 141c-31-9-42-18-48-26 25-8 47-5 62 8 0 8-6 14-14 18Z"/><path d="M94 52c22-25 35-30 45-31-7 25-20 41-39 46-7-6-9-10-6-15Z"/><path d="M101 112c28-18 42-20 51-18-13 22-30 34-50 34-5-7-6-12-1-16Z"/><path d="M108 183c29-17 43-18 52-16-14 22-32 32-52 31-5-7-5-12 0-15Z"/></g></svg></div>
    <button class="land-skip" id="landingSkip" onclick="enterApp()">跳过</button>
    <div class="land-brand"><h1 id="landingBrand">我们的<br>成都故事</h1><p id="landingTagline">一家人的旅程</p></div>
    <div class="land-note"><div class="cn" id="landingNote">慢一点，<br>和家人在一起。</div></div>
    <div class="land-bubble" id="landingBubble"></div>
    <div class="land-final">
      <div class="land-final-top"><img class="land-avatar" id="landingAvatar" alt="Panda"><div><h3 id="landingPhase">成都之前</h3><p id="landingDates">2026年10月15–20日 · 家庭旅行</p></div></div>
      <button class="enter-btn" id="landingEnter" onclick="enterApp()">开启我们的成都之旅 <span>→</span></button>
    </div>
  </div>'''

JAVASCRIPT = r'''/* ───── Landing ───── */
function landingMessage(){
  const p=phase(),d=currentDay();
  const zh={1:'今天先去山城。<br>重庆见 ♡',2:'慢慢走，<br>山城的故事藏在高低之间。',3:'再看一眼重庆，<br>然后回成都啦。',4:'今天会看到可爱的家伙，<br>也会看到蓝色的夜。',5:'从古蜀醒来，<br>再慢慢走回成都的日常。',6:'把这趟旅程，<br>一起带回家。'};
  const en={1:'First stop: the mountain city.<br>See you in Chongqing. ♡',2:'Take it slow.<br>Chongqing unfolds between every climb and turn.',3:'One last look at Chongqing,<br>then back to Chengdu.',4:'Pandas by day,<br>blue lights by night.',5:'Start with ancient Shu,<br>then ease back into Chengdu life.',6:'Take the journey<br>home with you.'};
  if(p==='before')return{msg:lang==='zh'?'我在成都等着你哦 ♡':"I'll be waiting for you in Chengdu.",phase:L('before')};
  if(p==='after')return{msg:lang==='zh'?'我在成都很想你。下次再回来，好不好？':'Come back when Chengdu calls again.',phase:L('after')};
  return{msg:(lang==='zh'?zh:en)[d],phase:lang==='zh'?`第${d}天 · ${days[d-1].date}`:`Day ${d} · ${days[d-1].date}`};
}
function renderLandingText(){
  const ids={landingSkip:'skip',landingBrand:'brand',landingTagline:'family_journey',landingNote:'landing_note',landingDates:'landing_dates'};
  Object.entries(ids).forEach(([id,key])=>{const el=$('#'+id);if(el)el.innerHTML=L(key)});
  const enter=$('#landingEnter');if(enter)enter.innerHTML=`${L('enter')} <span>→</span>`;
  const m=landingMessage(),bubble=$('#landingBubble'),phaseEl=$('#landingPhase');
  if(bubble)bubble.innerHTML=`<div class="${lang==='zh'?'cn':'en'}">${m.msg}</div>`;
  if(phaseEl)phaseEl.textContent=m.phase;
}
function prepareLanding(){
  const v=$('#landingVideo'),f=$('#landingPhoto');
  if(DATA.landing_video){
    v.src=DATA.landing_video;
    v.style.display='block';
    f.style.display='none';
    v.currentTime=0;
    const tryPlay=()=>v.play().catch(()=>{});
    v.addEventListener('canplay',tryPlay,{once:true});
    tryPlay();
  }else{
    v.style.display='none';
    f.style.display='block';
    f.src=DATA.landing_image||DATA.images.panda_portrait;
  }
  $('#landingAvatar').src=DATA.images.panda_portrait.replace(/w=\d+/,'w=200');
  $('#landingAvatar').alt=lang==='zh'?'熊猫头像':'Panda portrait';
  renderLandingText();
  const last=Number(store.get('chengduLandingAt')||0);
  if(Date.now()-last<3*60*60*1000)$('#landing').classList.add('hidden');
}
function enterApp(){
  const v=$('#landingVideo');if(v&&!v.paused)v.pause();
  store.set('chengduLandingAt',String(Date.now()));$('#landing').classList.add('hidden');sizeSwipe();settleAtTop()
}

function fitFrame(){
  try{
    if(!window.frameElement)return;
    const h=Math.max(640,window.parent.innerHeight||window.innerHeight||640);
    window.frameElement.style.height=`${h}px`;
  }catch(e){}
}

'''
