# -*- coding: utf-8 -*-
"""Frozen Home page and approved swipe-card stack.

Do not change this module's UI, artwork mapping, interactions, or behavior unless
the approved Home design is intentionally being revised.
"""

DAYS = [
    {
        "day": 1, "iso": "2026-10-15", "date": "15 Oct", "dow": "Thu", "city": "Chengdu → Chongqing",
        "vt": "初见山城", "note": "今天先去山城。",
        "nodes": [
            ["天府机场", "airport", "plane"], ["高铁前往重庆", "chongqing_train", "plane"],
            ["抵达重庆", "chongqing_city", "landmark"], ["自由活动", "chongqing_night", "leaf"],
        ],
    },
    {
        "day": 2, "iso": "2026-10-16", "date": "16 Oct", "dow": "Fri", "city": "Chongqing",
        "vt": "山城漫游", "note": "山城的故事藏在高低之间。",
        "nodes": [
            ["山城步道", "shancheng_trail", "landmark"], ["十八梯", "shibati", "landmark"],
            ["下浩里", "xiahaoli", "landmark"], ["解放碑", "jiefangbei", "landmark"],
            ["朝天门广场", "chaotianmen", "landmark"], ["洪崖洞", "hongya", "landmark"],
        ],
    },
    {
        "day": 3, "iso": "2026-10-17", "date": "17 Oct", "dow": "Sat", "city": "Chongqing → Chengdu",
        "vt": "渝蓉之间", "note": "再看一眼重庆，然后回成都。",
        "nodes": [
            ["磁器口", "ciqikou", "landmark"], ["李子坝", "liziba", "landmark"],
            ["八一路好吃街", "bayi", "food"], ["返回成都", "chongqing_train", "plane"],
        ],
    },
    {
        "day": 4, "iso": "2026-10-18", "date": "18 Oct", "dow": "Sun", "city": "Chengdu / Dujiangyan",
        "vt": "熊猫都江", "note": "白天看熊猫，夜里看蓝色的水。",
        "nodes": [
            ["熊猫基地", "panda_base", "leaf"], ["花花", "panda_huahua", "leaf"],
            ["都江堰", "dujiangyan_waterworks", "landmark"], ["灌县古城", "guanxian", "landmark"],
            ["钟书阁", "zhongshuge", "landmark"], ["南桥", "nanqiao", "landmark"],
            ["蓝眼泪夜景", "blue_tears", "landmark"],
        ],
    },
    {
        "day": 5, "iso": "2026-10-19", "date": "19 Oct", "dow": "Mon", "city": "Chengdu",
        "vt": "成都慢游", "note": "古蜀文明，成都慢生活，再回到城市中心。",
        "nodes": [
            ["三星堆", "sanxingdui_mask", "landmark"],
            ["人民公园", "people_park", "leaf"],
            ["IFS", "ifs_panda", "landmark"],
            ["春熙路", "taikoo_day", "landmark"],
        ],
    },
    {
        "day": 6, "iso": "2026-10-20", "date": "20 Oct", "dow": "Tue", "city": "Chengdu",
        "vt": "带回成都", "note": "旅程会结束，故事还在。",
        "nodes": [
            ["酒店出发", "taikoo_day", "hotel"], ["天府机场", "airport_hall", "plane"],
            ["返程", "airport", "plane"],
        ],
    },
]

CSS = r'''/* ───── HOME ───── */
.home-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:2px 12px 10px}
.greeting{font:700 clamp(30px,8.4vw,36px)/1 var(--cn-serif);letter-spacing:.01em;color:#173126}
.greeting-en{font:500 11px/1.15 var(--serif);color:var(--slate-ink);letter-spacing:.35px;margin-top:4px}
.home-poem{font:500 clamp(12px,3.45vw,14px)/1.28 var(--cn-serif);color:#4f6658;margin-top:4px;max-width:230px;letter-spacing:.03em}
.wx{text-align:right;flex:none}
.wx-row{display:flex;align-items:center;justify-content:flex-end;gap:7px}
.wx-row svg{width:30px;height:30px}
.wx-temp{font:600 clamp(22px,6.4vw,27px)/1 var(--serif);color:#1c2a23}
.wx small{display:block;margin-top:5px;font:400 11px var(--sans);color:var(--slate-ink);letter-spacing:.2px}
.hero{position:relative;height:clamp(166px,42vw,190px);border-radius:22px;overflow:hidden;background:#3d4a3a;isolation:isolate;box-shadow:0 10px 26px rgba(40,60,45,.14)}
.hero img{width:100%;height:100%;object-fit:cover;object-position:72% 38%}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,28,18,.56) 0%,rgba(9,28,18,.12) 58%,transparent 100%),linear-gradient(180deg,transparent 52%,rgba(9,24,16,.34) 100%)}
.hero-copy{position:absolute;z-index:2;left:20px;top:22%;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.35)}
.hero-copy .cn1,.hero-copy .cn2{font:400 clamp(27px,8.2vw,36px)/1.14 var(--hand);letter-spacing:2px}
.hero-copy .cn2{padding-left:26px}
.hero-copy .en{font:500 clamp(17px,5vw,21px)/1.05 var(--script);margin-top:9px;font-style:italic}
.sheet{position:relative;z-index:3;margin-top:6px;background:transparent;padding:0 0 10px}
.journey-seam{height:0}

/* ───── SWIPE CARD STACK — approved reference-card style ───── */
.sheet{padding:7px 0 14px}
.swipe-shell{position:relative;width:min(100%,430px);margin:0 auto;padding:0 12px 8px}
.swipe-stage{
  position:relative;height:clamp(438px,114vw,520px);
  perspective:1500px;touch-action:pan-y;user-select:none;-webkit-user-select:none
}
.swipe-card{
  position:absolute;inset:0 11px;border-radius:21px;transform-origin:50% 88%;
  will-change:transform,opacity;
  transition:transform .34s cubic-bezier(.22,.9,.24,1),opacity .28s ease;
  filter:drop-shadow(0 18px 26px rgba(42,52,45,.16))
}
.swipe-card[data-depth="0"]{z-index:30;transform:translateY(0) scale(1)}
.swipe-card[data-depth="1"]{z-index:20;transform:translateY(12px) scale(.94)}
.swipe-card[data-depth="2"]{z-index:10;transform:translateY(24px) scale(.90)}
.swipe-card[data-role="prev"],.swipe-card[data-role="next"]{opacity:0;pointer-events:none}
.swipe-stage[data-reveal="prev"] .swipe-card[data-role="prev"],.swipe-stage[data-reveal="next"] .swipe-card[data-role="next"]{opacity:1}
.swipe-card.dragging{transition:none}
.swipe-card.throwing{transition:transform .34s cubic-bezier(.18,.72,.2,1),opacity .28s ease}
.swipe-card-inner{position:absolute;inset:0;transform-style:preserve-3d;-webkit-transform-style:preserve-3d;transition:transform .58s cubic-bezier(.2,.75,.2,1);-webkit-transition:-webkit-transform .58s cubic-bezier(.2,.75,.2,1)}
.swipe-card.flipped .swipe-card-inner{transform:rotateY(180deg);-webkit-transform:rotateY(180deg)}
.swipe-face{
  position:absolute;inset:0;overflow:hidden;border-radius:21px;
  backface-visibility:hidden!important;-webkit-backface-visibility:hidden!important;
  transform-style:preserve-3d;-webkit-transform-style:preserve-3d;
  border:1px solid rgba(91,83,64,.20);
  background:
    radial-gradient(circle at 18% 7%,rgba(156,135,93,.08),transparent 23%),
    linear-gradient(180deg,#fffdf5 0%,#faf5e8 100%);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.9),
    inset 0 0 32px rgba(161,138,92,.035)
}
.swipe-face:after{
  content:"";position:absolute;inset:0;pointer-events:none;z-index:20;opacity:.26;
  background:
    radial-gradient(circle at 10% 20%,rgba(119,104,76,.035) 0 1px,transparent 1.5px),
    radial-gradient(circle at 82% 68%,rgba(119,104,76,.028) 0 1px,transparent 1.5px);
  background-size:13px 13px,17px 17px
}
.swipe-front{transform:rotateY(0deg) translateZ(.1px);-webkit-transform:rotateY(0deg) translateZ(.1px)}
.swipe-back{transform:rotateY(180deg) translateZ(.1px);-webkit-transform:rotateY(180deg) translateZ(.1px)}
.swipe-face>*{backface-visibility:hidden;-webkit-backface-visibility:hidden}
@supports (-webkit-touch-callout:none){
  .swipe-card.flipped .swipe-front{visibility:hidden;transition:visibility 0s linear .29s}
  .swipe-card:not(.flipped) .swipe-back{visibility:hidden;transition:visibility 0s linear .29s}
}
.card-front-head{
  position:absolute;left:19px;right:19px;top:15px;z-index:8;
  display:flex;align-items:flex-start;justify-content:space-between;gap:12px
}
.day-kicker{font:800 11px/1 var(--serif);letter-spacing:.13em;color:#172f26;text-transform:uppercase}
.card-front-title{
  margin-top:5px;font:700 clamp(28px,7vw,34px)/1.02 var(--cn-serif);
  color:#142c23;letter-spacing:.025em;text-shadow:0 1px 0 rgba(255,255,255,.6)
}
.lang-en .card-front-title{font-family:var(--serif);font-size:clamp(24px,6vw,30px);letter-spacing:0}
.card-date{font:600 10.5px/1.2 var(--serif);color:#7d786b;text-align:right;padding-top:1px}

/* Front: the approved hand-painted postcard artwork is embedded per day. */
.card-cover-art{
  position:absolute;left:10px;right:10px;top:68px;bottom:76px;overflow:hidden;
  border-radius:14px 14px 17px 17px;background:#f5efdf;
  box-shadow:inset 0 0 0 1px rgba(77,85,63,.15)
}
.cover-main{
  position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;
  filter:none;transform:scale(1.006)
}
.cover-main.day1{object-position:center 50%}
.cover-main.day2{object-position:center 54%}
.cover-main.day3{object-position:57% 51%}
.cover-main.day4{object-position:51% 51%}
.cover-main.day5{object-position:47% 50%}
.cover-main.day6{object-position:center 54%}
.card-cover-art:before{
  content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
  background:
    linear-gradient(180deg,rgba(255,250,237,.12),transparent 20%,transparent 76%,rgba(250,244,226,.12)),
    radial-gradient(ellipse at center,transparent 67%,rgba(247,239,216,.12) 100%)
}
.card-cover-art:after{
  content:"";position:absolute;inset:-1px;z-index:3;pointer-events:none;
  box-shadow:inset 0 0 11px 4px rgba(250,246,233,.16);border-radius:inherit
}
.cover-panda{
  position:absolute;left:18%;bottom:-9px;z-index:5;width:94px;height:132px;
  filter:drop-shadow(0 7px 7px rgba(29,42,35,.18))
}
.cover-panda img{width:100%;height:100%;object-fit:contain}
.card-front-bottom{position:absolute;left:18px;right:18px;bottom:12px;z-index:8;text-align:center}
.card-route-summary{
  font:600 10.8px/1.35 var(--cn-serif);color:#3a493f;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.lang-en .card-route-summary{font-family:var(--sans);font-size:9.8px}
.flip-hint{
  margin-top:7px;display:inline-flex;align-items:center;gap:6px;
  font:600 10.5px/1 var(--cn-serif);color:#1f4a38
}
.lang-en .flip-hint{font-family:var(--sans)}
.flip-hint svg{width:15px;height:15px}

/* Back: one illustrated route postcard per day, with live labels and traveler. */
.swipe-back-head{
  position:absolute;top:14px;left:17px;right:17px;z-index:12;
  display:flex;justify-content:space-between;align-items:flex-start
}
.back-title b{display:block;font:700 18.5px/1.05 var(--cn-serif);color:#162f25}
.lang-en .back-title b{font-family:var(--serif)}
.back-title small{display:block;margin-top:4px;font:600 9.5px var(--sans);color:#827d70}
.flip-back{
  border:1px solid rgba(64,87,72,.11);background:rgba(250,246,234,.90);
  border-radius:999px;width:31px;height:31px;display:grid;place-items:center;
  color:#315d48;padding:0;z-index:14
}
.card-route-map{
  position:absolute;left:10px;right:10px;top:54px;bottom:10px;overflow:hidden;
  border-radius:15px;
  background:#f8f1df;box-shadow:inset 0 0 0 1px rgba(77,85,63,.13)
}
.route-back-art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}
.route-label{position:absolute;z-index:6;width:31%;pointer-events:none}
.route-label.left{transform:translate(-103%,-50%);text-align:right}
.route-label.right{transform:translate(8%,-50%);text-align:left}
.route-label b{
  display:inline-block;max-width:112px;padding:3px 6px 4px;border-radius:7px;
  font:700 10.2px/1.14 var(--cn-serif);color:#1f352b;
  background:rgba(255,250,235,.91);box-shadow:0 2px 7px rgba(57,62,46,.07)
}
.lang-en .route-label b{font-family:var(--sans);font-size:8.8px}
.card-route-map.count-6 .route-label b,.card-route-map.count-7 .route-label b{font-size:9px;padding:2px 4px 3px}
.lang-en .card-route-map.count-6 .route-label b,.lang-en .card-route-map.count-7 .route-label b{font-size:7.8px}
.route-panda{
  position:absolute;z-index:9;width:58px;height:88px;transform:translate(-50%,-84%);
  filter:drop-shadow(0 6px 6px rgba(30,50,40,.20));transition:left .9s ease,top .9s ease
}
.route-panda img,.route-panda svg{width:100%;height:100%;object-fit:contain}
.stack-dots{display:flex;justify-content:center;gap:7px;margin-top:9px;height:9px}
.stack-dots button{width:7px;height:7px;border-radius:50%;padding:0;border:0;background:#c5c1b4;transition:all .25s}
.stack-dots button.active{width:18px;border-radius:5px;background:#184f3b}
.stack-help{text-align:center;margin-top:7px;font:500 10px/1.2 var(--cn-serif);color:#7b796f}
.lang-en .stack-help{font-family:var(--sans)}
.stack-arrow{
  position:absolute;top:48%;z-index:60;transform:translateY(-50%);
  width:34px;height:34px;border-radius:50%;border:1px solid rgba(54,88,66,.13);
  background:rgba(255,253,247,.82);backdrop-filter:blur(4px);
  display:grid;place-items:center;color:#285440;padding:0;opacity:.86
}
.stack-arrow.prev{left:1px}.stack-arrow.next{right:1px}.stack-arrow svg{width:17px;height:17px}
@media(max-width:390px){
  .swipe-stage{height:438px}.swipe-card{inset:0 8px}
  .card-front-title{font-size:28px}.route-label b{font-size:9px}
}

'''

JAVASCRIPT = r'''/* ───── panda-head day markers (Mahjong circle-dot layouts) ───── */
const LAY={1:[[30,30]],2:[[30,16],[30,44]],3:[[15,15],[30,30],[45,45]],4:[[18,18],[42,18],[18,42],[42,42]],5:[[16,16],[44,16],[30,30],[16,44],[44,44]],6:[[18,11],[42,11],[18,30],[42,30],[18,49],[42,49]]};
const RAD={1:20,2:14,3:11,4:11.5,5:10,6:9.2};
function pandaHead(cx,cy,R){
  const k=v=>(v*R).toFixed(2), e='#242c28';
  return `<g transform="translate(${cx} ${cy})"><circle cx="${k(-.62)}" cy="${k(-.6)}" r="${k(.31)}" fill="${e}"/><circle cx="${k(.62)}" cy="${k(-.6)}" r="${k(.31)}" fill="${e}"/><ellipse cx="0" cy="${k(.08)}" rx="${k(.8)}" ry="${k(.72)}" fill="#fffef8" stroke="#2a322d" stroke-width="${k(.05)}"/><ellipse cx="${k(-.32)}" cy="${k(.02)}" rx="${k(.17)}" ry="${k(.25)}" transform="rotate(22 ${k(-.32)} ${k(.02)})" fill="${e}"/><ellipse cx="${k(.32)}" cy="${k(.02)}" rx="${k(.17)}" ry="${k(.25)}" transform="rotate(-22 ${k(.32)} ${k(.02)})" fill="${e}"/><circle cx="${k(-.3)}" cy="${k(-.03)}" r="${k(.05)}" fill="#fff"/><circle cx="${k(.3)}" cy="${k(-.03)}" r="${k(.05)}" fill="#fff"/><ellipse cx="0" cy="${k(.3)}" rx="${k(.1)}" ry="${k(.075)}" fill="${e}"/><path d="M${k(-.09)} ${k(.42)}Q0 ${k(.52)} ${k(.09)} ${k(.42)}" fill="none" stroke="${e}" stroke-width="${k(.045)}" stroke-linecap="round"/></g>`;
}
const marker=n=>`<svg viewBox="0 0 60 60" role="img" aria-label="${n}">${LAY[n].map(p=>pandaHead(p[0],p[1],RAD[n])).join('')}</svg>`;

/* ───── hand-painted chapter cover art (new Chongqing + Chengdu itinerary) ─────
   These are deliberately illustrated rather than photographic.
   The visual language stays consistent with the cream-paper / sage / ink-wash Home. */
const pine=(x,y,s,c)=>`<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 -17L-5.5 -6.5H-2.6L-7.5 1.5H-3.4L-8.6 10H8.6L3.4 1.5H7.5L2.6 -6.5H5.5Z" fill="${c}"/><rect x="-1" y="10" width="2" height="4" fill="#75624d"/></g>`;
const tree=(x,y,s,c)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-.9" y="-3" width="1.8" height="8" fill="#7a664f"/><circle cx="0" cy="-10" r="6.6" fill="${c}"/><circle cx="-5" cy="-5" r="5" fill="${c}"/><circle cx="5" cy="-5" r="5" fill="${c}"/></g>`;
const leaf=(x,y,a,l,c)=>`<path transform="translate(${x} ${y}) rotate(${a})" d="M0 0Q${l*.5} ${-l*.2} ${l} 0Q${l*.5} ${l*.2} 0 0Z" fill="${c}" opacity=".9"/>`;
function bamboo(x,top,bot,w){
  let s=`<path d="M${x} ${bot}L${x+.5} ${top}" stroke="#789c7b" stroke-width="${w}" stroke-linecap="round"/>`;
  for(let y=bot-20;y>top+6;y-=21)s+=`<path d="M${x-w*.7} ${y}h${w*1.4}" stroke="#4f7656" stroke-width=".75"/>`;
  for(let k=0;k<5;k++){const y=top+6+k*11,r=k%2;s+=leaf(x,y,r?-25-k*5:-155+k*5,13-k*.8,r?'#88ad84':'#6f9873')+leaf(x,y+4,r?15+k*5:165-k*5,11-k*.6,'#9ab58e')}
  return s;
}
const lantern=(x,y,r,l)=>`<g><path d="M${x} ${y}V${y+l}" stroke="#5a3b2a" stroke-width=".7"/><circle cx="${x}" cy="${y+l+r}" r="${(r*2.4).toFixed(1)}" fill="#f1a84e" opacity=".22"/><ellipse cx="${x}" cy="${y+l+r}" rx="${r}" ry="${(r*1.12).toFixed(1)}" fill="#c95446"/><path d="M${x-r*.55} ${y+l+r*.7}Q${x} ${y+l+r*1.5} ${x+r*.55} ${y+l+r*.7}" stroke="#f2b09f" stroke-width=".5" fill="none"/><path d="M${x} ${y+l+r*2.1}v${r*1.5}" stroke="#d99f44" stroke-width=".9"/></g>`;

const PB=`<ellipse cx="17" cy="59" rx="6" ry="4.5" fill="#242c28"/><ellipse cx="31" cy="57" rx="6" ry="4.5" fill="#242c28"/><ellipse cx="24" cy="42" rx="16" ry="17" fill="#fffef8" stroke="#2a322d" stroke-width=".8"/><path d="M8.5 37c2-9 10-13 15.5-13s13.5 4 15.5 13c-3-3-8-4.5-15.5-4.5S11.5 34 8.5 37z" fill="#242c28"/><ellipse cx="9" cy="43" rx="5.2" ry="11" transform="rotate(8 9 43)" fill="#242c28"/><ellipse cx="39" cy="43" rx="5.2" ry="11" transform="rotate(-8 39 43)" fill="#242c28"/><rect x="13.5" y="33" width="21" height="22" rx="5.5" fill="#7f9c5c" stroke="#5a7340" stroke-width=".8"/><rect x="13.5" y="33" width="21" height="9" rx="4.5" fill="#93ae6f"/><rect x="18" y="44" width="12" height="7" rx="2.5" fill="#6f8a4f" stroke="#5a7340" stroke-width=".6"/><path d="M16 34v20M32 34v20" stroke="#5a7340" stroke-width=".9" opacity=".6"/><rect x="11.5" y="29.5" width="25" height="5.5" rx="2.7" fill="#d9b56a" stroke="#a78440" stroke-width=".6"/><circle cx="10.5" cy="9" r="5.3" fill="#242c28"/><circle cx="37.5" cy="9" r="5.3" fill="#242c28"/><ellipse cx="24" cy="17" rx="15" ry="13" fill="#fffef8" stroke="#2a322d" stroke-width=".8"/>`;
const PANDA=`<svg viewBox="0 0 48 64" aria-hidden="true">${PB}</svg>`;

function art(d){
  const lg=(id,stops)=>`<linearGradient id="${id}${d}" x1="0" y1="0" x2="0" y2="1">${stops.map(s=>`<stop offset="${s[0]}" stop-color="${s[1]}"${s[2]!=null?` stop-opacity="${s[2]}"`:''}/>`).join('')}</linearGradient>`;
  const defs=`<defs>
    <filter id="wc${d}" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".025 .055" numOctaves="3" seed="${d+19}" result="paper"/>
      <feDisplacementMap in="SourceGraphic" in2="paper" scale="3.8" xChannelSelector="R" yChannelSelector="G" result="edge"/>
      <feGaussianBlur in="edge" stdDeviation=".13" result="soft"/>
      <feBlend in="edge" in2="soft" mode="multiply"/>
    </filter>
    <filter id="wash${d}" x="-15%" y="-15%" width="130%" height="130%">
      <feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="2" seed="${d+31}" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7"/>
      <feGaussianBlur stdDeviation="1.25"/>
    </filter>
    ${lg('sky',[[0,'#edf2e9'],[1,'#f8f2e5']])}
    ${lg('river',[[0,'#9ccdcc'],[1,'#5ea7b0']])}
    ${lg('night',[[0,'#65788c'],[1,'#273e4b']])}
    ${lg('gold',[[0,'#f0d79b'],[1,'#c99855']])}
    ${lg('sage',[[0,'#adc3a5'],[1,'#6f9276']])}
    <radialGradient id="glow${d}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f5ad57" stop-opacity=".5"/><stop offset="1" stop-color="#f5ad57" stop-opacity="0"/></radialGradient>
  </defs>`;

  const A={
    /* Day 1 — first glimpse of Chongqing: mountains, stacked city, train into the valley */
    1:`<rect width="100" height="250" fill="url(#sky${d})"/>
       <g filter="url(#wash${d})" opacity=".55">
         <path d="M0 133L14 111 28 122 43 88 60 116 73 98 100 126V190H0Z" fill="#afc3b3"/>
         <path d="M0 156L18 137 33 145 53 121 70 145 84 132 100 148V196H0Z" fill="#8fa995"/>
       </g>
       <g filter="url(#wc${d})">
         <path d="M0 182C20 168 35 176 52 164S83 164 100 175V250H0Z" fill="#718f7c" opacity=".9"/>
         <g opacity=".94">
           ${[[7,165,16,31],[18,154,17,43],[33,170,16,28],[47,145,19,53],[65,158,16,40],[79,137,17,59]].map((b,i)=>`<rect x="${b[0]}" y="${b[1]}" width="${b[2]}" height="${b[3]}" rx="1.2" fill="${i%2?'#c99c72':'#d9b78f'}"/><path d="M${b[0]+3} ${b[1]+6}h${b[2]-6}M${b[0]+3} ${b[1]+13}h${b[2]-6}" stroke="#f3dfb8" stroke-width="1.4" opacity=".7"/>`).join('')}
         </g>
         <path d="M0 205C27 194 49 198 100 187" stroke="#7b786a" stroke-width="3.2" fill="none"/>
         <path d="M0 210C28 199 54 201 100 192" stroke="#b9b2a1" stroke-width=".8" fill="none"/>
         <g transform="translate(35 193) rotate(-7)">
           <rect x="0" y="0" width="34" height="9" rx="3" fill="#f4f2e8" stroke="#768b90" stroke-width=".8"/>
           <path d="M4 2h5v4H4zM12 2h5v4h-5zM20 2h5v4h-5z" fill="#8eb1bd" opacity=".8"/>
           <path d="M31 1l6 3.5-6 3.5Z" fill="#d3604f"/>
         </g>
         ${lantern(15,180,2.6,6)}${lantern(86,165,2.5,9)}
         <path d="M0 219C20 209 44 220 66 210S90 211 100 217V250H0Z" fill="#c9c1ad"/>
         <path d="M5 225h90M18 219l-8 31M48 215v35M78 211l10 39" stroke="#aba28f" stroke-width=".6" opacity=".7"/>
       </g>`,

    /* Day 2 — Chongqing mountain-city walk: stairs, layered houses, Hongya glow and river */
    2:`<rect width="100" height="250" fill="url(#sky${d})"/>
       <g filter="url(#wash${d})" opacity=".5">
         <path d="M0 122L20 94 34 111 53 76 71 106 86 87 100 109V194H0Z" fill="#a3b9aa"/>
       </g>
       <g filter="url(#wc${d})">
         <path d="M0 170C17 153 31 161 45 149S71 144 100 158V250H0Z" fill="#829e88"/>
         <path d="M8 187L28 167H56L72 151H93V218H8Z" fill="#b87857"/>
         <path d="M12 187V213H92V160H73L58 176H30Z" fill="#c98a62"/>
         ${[17,27,39,52,66,78].map((x,i)=>`<rect x="${x}" y="${i%2?181:174}" width="7" height="8" fill="#f2c56e" opacity=".92"/>`).join('')}
         <path d="M10 182H94M28 168H58M71 153H94" stroke="#4c4f4d" stroke-width="2.2"/>
         <path d="M10 214H93" stroke="#58483a" stroke-width="2.5"/>
         ${lantern(19,165,2.2,6)}${lantern(43,155,2.5,9)}${lantern(78,142,2.3,8)}
         <path d="M0 217C24 211 54 221 100 213V250H0Z" fill="url(#river${d})"/>
         <path d="M12 230q14-4 29 0M51 238q16-4 32 0" stroke="#edf7f1" stroke-width="1.3" fill="none" opacity=".75"/>
         <path d="M4 218L16 198H22L11 250H4ZM30 214L40 195H45L37 250H29Z" fill="#9e9685" opacity=".65"/>
         <path d="M7 244L26 220H36L17 244ZM18 248L39 223H50L29 248Z" fill="#d3c4aa" opacity=".9"/>
       </g>`,

    /* Day 3 — Chongqing to Chengdu: Liziba monorail through a building, old-street roofline */
    3:`<rect width="100" height="250" fill="url(#sky${d})"/>
       <g filter="url(#wash${d})" opacity=".5">
         <path d="M0 135L18 104 35 121 52 93 72 122 88 101 100 118V188H0Z" fill="#b7c7b6"/>
       </g>
       <g filter="url(#wc${d})">
         <rect x="20" y="151" width="61" height="74" rx="2" fill="#c8b49b"/>
         <path d="M20 151H81V164H20Z" fill="#8e7866"/>
         ${[28,40,52,64].map(x=>`<rect x="${x}" y="169" width="7" height="7" fill="#91aab0"/><rect x="${x}" y="183" width="7" height="7" fill="#91aab0"/><rect x="${x}" y="197" width="7" height="7" fill="#91aab0"/>`).join('')}
         <rect x="18" y="176" width="65" height="14" rx="4" fill="#646a68" opacity=".9"/>
         <g transform="translate(8 176)">
           <rect x="0" y="1" width="84" height="11" rx="5" fill="#f0efe8" stroke="#60747a" stroke-width=".8"/>
           <path d="M7 3h10v6H7zM21 3h10v6H21zM35 3h10v6H35zM49 3h10v6H49zM63 3h10v6H63z" fill="#8db1bd"/>
           <path d="M78 2l8 4.5-8 4.5Z" fill="#ca5649"/>
         </g>
         <path d="M8 214Q22 199 36 214Q50 198 64 214Q78 199 92 214V228H8Z" fill="#6c6156"/>
         <path d="M11 214Q22 205 33 214M39 214Q50 205 61 214M67 214Q78 205 89 214" stroke="#d8c7a6" stroke-width="1.4" fill="none"/>
         ${lantern(17,213,2.2,4)}${lantern(83,213,2.2,4)}
         <path d="M0 228H100V250H0Z" fill="#c8c0ae"/>
         <path d="M6 235h88M24 228l-7 22M52 228v22M80 228l7 22" stroke="#aca28e" stroke-width=".7"/>
       </g>`,

    /* Day 4 — Panda + Dujiangyan: bamboo, panda, bridge and luminous blue river */
    4:`<rect width="100" height="250" fill="url(#sky${d})"/>
       <g filter="url(#wash${d})" opacity=".55">
         <path d="M0 124L17 99 31 112 50 82 67 112 84 94 100 116V185H0Z" fill="#b4c7b4"/>
       </g>
       <g filter="url(#wc${d})">
         ${bamboo(8,78,250,2.5)}${bamboo(19,98,250,1.9)}${bamboo(91,82,250,2.5)}
         <path d="M0 174C20 156 39 169 59 156S87 158 100 169V250H0Z" fill="#85a78b"/>
         <path d="M0 204C24 194 51 205 100 196V250H0Z" fill="url(#river${d})"/>
         <path d="M10 219q13-4 27 0M52 229q17-4 34 0M21 239q14-3 29 0" stroke="#effcfa" stroke-width="1.3" fill="none" opacity=".8"/>
         <rect x="18" y="185" width="67" height="4" fill="#8a5d43"/>
         <rect x="22" y="174" width="59" height="11" fill="#d0b17e"/>
         <path d="M22 174V185M34 174V185M49 174V185M64 174V185M81 174V185" stroke="#744c35" stroke-width="1.4"/>
         <path d="M16 176Q50 165 87 176L84 179H19Z" fill="#555f61"/>
         <g transform="translate(28 184) scale(.62)">${PB}</g>
         <ellipse cx="54" cy="236" rx="35" ry="8" fill="#6bc6c9" opacity=".25"/>
       </g>`,

    /* Day 5 — Sanxingdui: bronze-mask landmark with a warm Chengdu paper palette */
    5:`<rect width="100" height="250" fill="#f4eee0"/>
       <g filter="url(#wash${d})" opacity=".42">
         <path d="M0 135L18 110 34 123 52 94 69 119 84 104 100 126V193H0Z" fill="#b7c6ae"/>
         <circle cx="82" cy="71" r="24" fill="#d7bd79" opacity=".22"/>
       </g>
       <g filter="url(#wc${d})">
         <path d="M0 198C18 187 39 195 60 184S88 187 100 194V250H0Z" fill="#9fac78"/>
         ${tree(12,187,1.25,'#8fa36f')}${tree(91,187,1.15,'#9da973')}
         <g transform="translate(50 148)">
           <path d="M-25 -36Q0-50 25-36L19 8Q0 30-19 8Z" fill="#6f8e7d" stroke="#48695c" stroke-width="1.6"/>
           <path d="M-17 -26Q-11-34-4-25L-9-7Q-15-8-19-15Z" fill="#d7c58e"/>
           <path d="M17 -26Q11-34 4-25L9-7Q15-8 19-15Z" fill="#d7c58e"/>
           <path d="M-7 4Q0 11 7 4Q6 17 0 20Q-6 17-7 4Z" fill="#c5b177"/>
           <path d="M-4-12Q0-17 4-12L3-2H-3Z" fill="#b79d63"/>
           <path d="M-28-31L-41-44M28-31L41-44" stroke="#48695c" stroke-width="5" stroke-linecap="round"/>
           <path d="M-37-45l-8-4M37-45l8-4" stroke="#8ea07b" stroke-width="3" stroke-linecap="round"/>
           <ellipse cx="0" cy="-39" rx="8" ry="4" fill="#d8c68e"/>
         </g>
         <path d="M10 208H90V228H10Z" fill="#d5c2a0"/>
         <path d="M15 208Q50 193 85 208" fill="#c47d4c"/>
         <path d="M23 228v13M50 228v13M77 228v13" stroke="#8c7255" stroke-width="2"/>
         ${lantern(19,190,2.1,5)}${lantern(82,188,2.1,7)}
       </g>`,

    /* Day 6 — homeward: open sky, airport silhouette and backpack panda */
    6:`<rect width="100" height="250" fill="url(#sky${d})"/>
       <g filter="url(#wash${d})" opacity=".45">
         <ellipse cx="24" cy="118" rx="21" ry="7" fill="#ffffff"/><ellipse cx="75" cy="137" rx="24" ry="7" fill="#ffffff"/>
       </g>
       <g filter="url(#wc${d})">
         <path d="M54 116Q31 130 8 139" stroke="#fff" stroke-width="2.2" opacity=".85" stroke-linecap="round" fill="none"/>
         <g transform="translate(68 105) rotate(-15)">
           <path d="M-15 0Q-15-3.4-8-3.4H10Q17-3.4 19 0Q17 3.4 10 3.4H-8Q-15 3.4-15 0Z" fill="#fbfbf6" stroke="#8ea6b6" stroke-width=".7"/>
           <path d="M-2 0L-9-11 -4-11 5 0Z" fill="#e8eef0" stroke="#8ea6b6" stroke-width=".6"/>
           <path d="M-13-1L-16-7-12-7-8-1Z" fill="#d35e4d"/>
         </g>
         <path d="M4 176Q22 154 44 166Q64 178 80 162Q90 156 98 164V190H4Z" fill="#e8ece7" stroke="#9fb0aa" stroke-width=".8"/>
         <rect x="8" y="176" width="88" height="13" fill="#b8ced0"/><path d="M14 176v13M25 176v13M36 176v13M47 176v13M58 176v13M69 176v13M80 176v13M91 176v13" stroke="#fff" stroke-width=".6" opacity=".8"/>
         <path d="M0 190H100V250H0Z" fill="#d5d1c2"/><path d="M29 250L43 192H57L76 250Z" fill="#c4bdab"/>
         <path d="M34 236H70M38 222H66M42 208H62M51 192V250" stroke="#a9a18e" stroke-width=".7" fill="none"/>
         ${bamboo(8,125,250,2.3)}${bamboo(92,123,250,2.4)}
         <g transform="translate(34 201) scale(.64)">${PB}</g>
       </g>`
  };
  return `<svg viewBox="0 0 100 250" preserveAspectRatio="xMidYMax slice" aria-hidden="true">${defs}${A[d]}</svg>`;
}

/* ───── approved scenic route for Home accordion only ─────
   Time remains internal for panda progress; the UI only shows place + image. */
const HOME_ROUTE={
  1:[["天府机场","airport"],["高铁前往重庆","chongqing_train"],["抵达重庆","chongqing_city"],["自由活动","chongqing_night"]],
  2:[["山城步道","shancheng_trail"],["十八梯","shibati"],["下浩里","xiahaoli"],["解放碑","jiefangbei"],["朝天门广场","chaotianmen"],["洪崖洞","hongya"]],
  3:[["磁器口","ciqikou"],["李子坝","liziba"],["八一路好吃街","bayi"],["返回成都","chongqing_train"]],
  4:[["熊猫基地","panda_base"],["花花","panda_huahua"],["都江堰","dujiangyan_waterworks"],["灌县古城","guanxian"],["钟书阁","zhongshuge"],["南桥","nanqiao"],["蓝眼泪夜景","blue_tears"]],
  5:[["三星堆","sanxingdui_mask"],["人民公园","people_park"],["IFS","ifs_panda"],["春熙路","taikoo_day"]],
  6:[["酒店出发","taikoo_day"],["天府机场","airport_hall"],["返程","airport"]]
};
// Visual progress anchors only — update when confirmed transport/activity times are available.
const INTERNAL_ROUTE_TIMES={
  1:["09:00","11:30","14:00","16:00"],2:["09:00","10:30","12:30","15:00","17:30","20:00"],
  3:["09:00","12:00","14:30","17:30"],4:["08:00","10:00","13:00","15:30","17:00","18:30","20:00"],
  5:["09:00","12:30","15:00","16:30"],6:["08:00","10:00","12:00"]
};
const routeStops=d=>(HOME_ROUTE[d.day]||[]).map((x,i)=>[INTERNAL_ROUTE_TIMES[d.day]?.[i]||"12:00",x[0],x[1]]);


/* ───── route geometry ───── */
const lerp=(a,b,t)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});
const seg=(a,b)=>{const ym=(a.y+b.y)/2;return[a,{x:a.x,y:ym},{x:b.x,y:ym},b]};
function bez(s,t){const u=1-t,f=(c)=>u*u*u*s[0][c]+3*u*u*t*s[1][c]+3*u*t*t*s[2][c]+t*t*t*s[3][c];return{x:f('x'),y:f('y')}}
function leftPart(s,t){const a=lerp(s[0],s[1],t),b=lerp(s[1],s[2],t),c=lerp(s[2],s[3],t),d=lerp(a,b,t),e=lerp(b,c,t);return[s[0],a,d,lerp(d,e,t)]}
const P=p=>`${p.x.toFixed(2)} ${p.y.toFixed(2)}`, cub=s=>`C${P(s[1])} ${P(s[2])} ${P(s[3])}`;
function progress(d){
  const stops=routeStops(d),n=stops.length,now=chinaNow();
  if(now.iso<d.iso)return{idx:0,st:'future'};
  if(now.iso>d.iso)return{idx:n-1,st:'past'};
  const m=now.h*60+now.m,T=stops.map(x=>hm(x[0]));
  if(m<=T[0])return{idx:0,st:'today'};
  for(let i=0;i<n-1;i++)if(m<T[i+1])return{idx:i+(m-T[i])/(T[i+1]-T[i]),st:'today'};
  return{idx:n-1,st:'today'};
}
const thumbUrl=u=>u.replace(/width=\d+/,'width=760').replace(/w=\d+/,'w=760');
function routeGeom(d){
  const stops=routeStops(d),n=stops.length,pr=progress(d);
  // Chronological journey starts at the BOTTOM and climbs upward.
  const top=16,bottom=82;
  const pts=stops.map((_,i)=>({
    x:i%2===0 ? 39-(i%3)*1.2 : 64+(i%3)*1.2,
    y:bottom-i*((bottom-top)/(n-1))
  }));
  const segs=pts.slice(0,-1).map((p,i)=>seg(p,pts[i+1]));
  const base='M'+P(pts[0])+segs.map(cub).join('');
  let done='';
  if(pr.st==='past')done=base;
  else if(pr.st==='today'&&pr.idx>0){
    const k=Math.min(Math.floor(pr.idx),n-2),u=pr.idx>=n-1?1:pr.idx-k;
    done='M'+P(pts[0])+segs.slice(0,k).map(cub).join('')+cub(leftPart(segs[k],u));
  }
  const k=Math.min(Math.floor(pr.idx),n-2),u=pr.idx>=n-1?1:pr.idx-k;
  return{n,pr,pts,base,done,target:bez(segs[k],u),stops};
}
function routeHTML(d,quiet){
  const g=routeGeom(d),{pr,pts,n,stops}=g;
  const nodes=stops.map((nd,i)=>{
    const st=pr.st==='past'?'done':pr.st==='future'?'':(pr.idx>=n-1?'done':i<Math.floor(pr.idx)?'done':i===Math.floor(pr.idx)?'cur':'');
    return `<div class="node ${st}" style="top:${pts[i].y}%;--d:${(i*.07).toFixed(2)}s">
      <i class="dot" style="left:${pts[i].x}%"></i>
      <div class="card ${i%2?'l':'r'}">
        <div class="thumb">
          <img src="${thumbUrl(DATA.images[nd[2]])}" alt="${esc(proper(nd[1]))}" loading="lazy" onerror="this.style.display='none'">
          <div class="t"><b>${esc(proper(nd[1]))}</b></div>
        </div>
      </div>
    </div>`;
  }).join('');
  const raw=quiet?g.target:pts[0];
  // The traveler visually trails the route slightly so it feels like it is walking upward.
  const start={x:raw.x,y:Math.min(91,raw.y+6.5)};
  const traveler=DATA.traveler_panda
    ? `<img src="${DATA.traveler_panda}" alt="${lang==='zh'?'背着绿色背包向前走的熊猫':'Panda walking ahead with a green backpack'}">`
    : PANDA;
  return `<svg class="line" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <path class="wash" d="${g.base}"/>
      <path class="base" d="${g.base}"/>
      ${g.done?`<path class="done" d="${g.done}"/>`:''}
    </svg>
    ${nodes}
    <div class="panda ${pr.st==='today'?'walk':''}" style="left:${start.x}%;top:${start.y}%">${traveler}</div>`;
}

/* ───── Home ───── */
function wxIcon(c){
  if(c===null)return `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="8" fill="#f2a33a"/><g stroke="#f2a33a" stroke-width="2" stroke-linecap="round"><path d="M20 4v5M20 31v5M4 20h5M31 20h5M8.7 8.7l3.5 3.5M27.8 27.8l3.5 3.5M31.3 8.7l-3.5 3.5M12.2 27.8l-3.5 3.5"/></g></svg>`;
  if(c<=1)return wxIcon(null);
  const cloud='<path d="M11 30h17a6 6 0 0 0 .8-11.9A8.5 8.5 0 0 0 12.3 16.6 6.7 6.7 0 0 0 11 30Z" fill="#dfe8ee" stroke="#8ea3b5" stroke-width="1.6"/>';
  if(c>=51)return `<svg viewBox="0 0 40 40">${cloud}<path d="M14 33l-1.5 4M20 33l-1.5 4M26 33l-1.5 4" stroke="#5b9bc4" stroke-width="2" stroke-linecap="round"/></svg>`;
  return `<svg viewBox="0 0 40 40"><circle cx="14" cy="13" r="6" fill="#f2a33a"/>${cloud}</svg>`;
}
// Home is now an infinite swipe-card stack.
// Right swipe = next day. Left swipe = previous day. Tap = flip to the route map.
const SWIPE_THRESHOLD=.35;
let dragState=null,swipeAnimating=false;

function daySummary(d){return (HOME_ROUTE[d.day]||[]).map(x=>proper(x[0])).join(' · ')}
const ROUTE_ART_POINTS={
  1:[[47,24],[57,36],[46,58],[54,79]],
  2:[[49,18],[60,31],[43,44],[60,56],[42,69],[60,82]],
  3:[[42,25],[59,45],[44,59],[61,76]],
  4:[[48,18],[61,23],[47,35],[58,47],[42,59],[56,70],[44,82]],
  5:[[40,27],[58,43],[42,63],[55,80]],
  6:[[58,25],[40,51],[67,76]]
};
function cardFrontHTML(d){
  const main=DATA.card_art?.[d.day]?.front||'';
  const panda=d.day===6&&DATA.traveler_panda?`<div class="cover-panda"><img src="${DATA.traveler_panda}" alt=""></div>`:'';
  return `<div class="swipe-face swipe-front">
    <div class="card-front-head">
      <div><div class="day-kicker">${lang==='zh'?`第 ${d.day} 天`:`DAY ${d.day}`}</div><div class="card-front-title">${esc(proper(d.vt))}</div></div>
      <div class="card-date">${esc(d.date)}</div>
    </div>
    <div class="card-cover-art">
      <img class="cover-main day${d.day}" src="${main}" alt="${esc(proper(d.vt))}" loading="eager">
      ${panda}
    </div>
    <div class="card-front-bottom">
      <div class="card-route-summary">${esc(daySummary(d))}</div>
      <div class="flip-hint"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 11V5a2 2 0 1 1 4 0v5.5-1.3a2 2 0 1 1 4 0v4.8l2.3 2.2a3.7 3.7 0 0 1 .7 4.5L19.3 22H10l-5-6.2A2 2 0 0 1 8 13l1 1" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg><span>${lang==='zh'?'轻触查看路线':'Tap to view route'}</span></div>
    </div>
  </div>`
}
function cardRouteBackHTML(d){
  const stops=routeStops(d),n=stops.length;
  const pts=(ROUTE_ART_POINTS[d.day]||[]).map(p=>({x:p[0],y:p[1]}));
  const pr=progress(d),k=Math.min(Math.floor(pr.idx),Math.max(0,n-2)),u=pr.idx>=n-1?1:pr.idx-k;
  let px=pts[0]?.x||50,py=pts[0]?.y||82;
  if(n>1){const a=pts[k],b=pts[Math.min(k+1,n-1)];px=a.x+(b.x-a.x)*u;py=a.y+(b.y-a.y)*u}
  if(pr.st==='future'){px=pts[0]?.x||50;py=(pts[0]?.y||82)+5}
  if(pr.st==='past'){px=pts[n-1]?.x||50;py=(pts[n-1]?.y||18)+5}
  const nodes=stops.map((s,i)=>{
    return `<div class="route-label ${i%2===0?'left':'right'}" style="left:${pts[i].x}%;top:${pts[i].y}%">
      <b>${esc(proper(s[1]))}</b>
    </div>`
  }).join('');
  const art=DATA.card_art?.[d.day]?.back||'';
  const traveler=DATA.route_traveler_panda
    ?`<img src="${DATA.route_traveler_panda}" alt="${lang==='zh'?'正面背包熊猫':'Front-facing backpack panda'}">`
    :PANDA;
  return `<div class="swipe-face swipe-back">
    <div class="swipe-back-head">
      <div class="back-title"><b>${esc(proper(d.vt))}</b><small>${lang==='zh'?`第 ${d.day} 天路线`:`Day ${d.day} Route`}</small></div>
      <button class="flip-back" onclick="event.stopPropagation();flipTopCard(false)" aria-label="${lang==='zh'?'翻回正面':'Flip back'}">${icon('refresh','sm')}</button>
    </div>
    <div class="card-route-map count-${n}">
      <img class="route-back-art" src="${art}" alt="" loading="eager">
      ${nodes}
      <div class="route-panda" style="left:${px}%;top:${Math.min(93,py+4)}%">${traveler}</div>
    </div>
  </div>`
}
function stackCardHTML(idx,depth,role='current'){
  const safe=(idx+days.length)%days.length,d=days[safe];
  return `<article class="swipe-card" data-role="${role}" data-depth="${depth}" data-index="${safe}" aria-label="${L('day',{n:d.day})} ${esc(proper(d.vt))}"><div class="swipe-card-inner">${cardFrontHTML(d)}${cardRouteBackHTML(d)}</div></article>`
}
function initialSwipeIndex(){
  const saved=Number(store.get('chengduSwipeDay')),now=chinaNow();
  if(now.iso>=days[0].iso&&now.iso<=days[days.length-1].iso)return currentDay()-1;
  if(now.iso<days[0].iso)return 0;
  if(Number.isInteger(saved)&&saved>=0&&saved<days.length)return saved;
  return days.length-1
}
function renderSwipeStack(index=swipeDayIdx){
  swipeDayIdx=(index+days.length)%days.length;store.set('chengduSwipeDay',String(swipeDayIdx));swipeFlipped=false;
  const stage=$('#swipeStage');if(!stage)return;
  const curr=swipeDayIdx;
  const prev=(curr-1+days.length)%days.length,prev2=(curr-2+days.length)%days.length;
  const next=(curr+1)%days.length,next2=(curr+2)%days.length;
  stage.dataset.reveal='next';
  stage.innerHTML=stackCardHTML(prev2,2,'prev')+stackCardHTML(prev,1,'prev')+stackCardHTML(next2,2,'next')+stackCardHTML(next,1,'next')+stackCardHTML(curr,0,'current');
  bindSwipeTop();renderStackDots()
}
function renderStackDots(){const box=$('#stackDots');if(box)box.innerHTML=days.map((d,i)=>`<button class="${i===swipeDayIdx?'active':''}" onclick="jumpDay(${i})" aria-label="${L('day',{n:d.day})}"></button>`).join('')}
function jumpDay(i){if(!swipeAnimating){swipeDayIdx=(i+days.length)%days.length;renderSwipeStack(swipeDayIdx)}}
function flipTopCard(force=null){const top=$('#swipeStage .swipe-card[data-depth="0"]');if(!top)return;swipeFlipped=force===null?!swipeFlipped:!!force;top.classList.toggle('flipped',swipeFlipped)}
function setStackReveal(direction){const stage=$('#swipeStage');if(stage)stage.dataset.reveal=direction>0?'next':'prev'}
function animateLower(p,direction){
  p=Math.max(0,Math.min(1,p));setStackReveal(direction);
  const role=direction>0?'next':'prev';
  const b=$(`#swipeStage .swipe-card[data-role="${role}"][data-depth="1"]`),c=$(`#swipeStage .swipe-card[data-role="${role}"][data-depth="2"]`);
  if(b)b.style.transform=`translateY(${12*(1-p)}px) scale(${(.94+.06*p).toFixed(4)})`;
  if(c)c.style.transform=`translateY(${24-12*p}px) scale(${(.90+.04*p).toFixed(4)})`
}
function resetLower(){document.querySelectorAll('#swipeStage .swipe-card[data-depth="1"],#swipeStage .swipe-card[data-depth="2"]').forEach(card=>card.style.transform='')}
function completeSwipe(direction){
  if(swipeAnimating||swipeFlipped)return;
  const top=$('#swipeStage .swipe-card[data-depth="0"]');if(!top)return;
  swipeAnimating=true;setStackReveal(direction);const distance=(window.innerWidth||430)*1.35*direction;
  top.classList.remove('dragging');top.classList.add('throwing');top.style.transform=`translate(${distance}px,${Math.abs(distance)*.045}px) rotate(${distance*.06}deg)`;top.style.opacity='0';animateLower(1,direction);
  setTimeout(()=>{swipeDayIdx=(swipeDayIdx+(direction>0?1:-1)+days.length)%days.length;store.set('chengduSwipeDay',String(swipeDayIdx));swipeAnimating=false;resetLower();renderSwipeStack(swipeDayIdx)},320)
}
function springBack(){const top=$('#swipeStage .swipe-card[data-depth="0"]');if(top){top.classList.remove('dragging');top.style.transform='';top.style.opacity=''}resetLower()}
function bindSwipeTop(){
  const top=$('#swipeStage .swipe-card[data-depth="0"]');if(!top)return;
  const start=e=>{
    if(swipeAnimating)return;
    const p=e.touches?e.touches[0]:e;
    dragState={x:p.clientX,y:p.clientY,lastX:p.clientX,lastY:p.clientY,moved:false,wasFlipped:swipeFlipped,pointerId:e.pointerId??null};
    if(dragState.pointerId!==null&&top.setPointerCapture)top.setPointerCapture(dragState.pointerId);
    if(!swipeFlipped)top.classList.add('dragging')
  };
  const move=e=>{
    if(!dragState)return;
    const p=e.touches?e.touches[0]:e,dx=p.clientX-dragState.x,dy=p.clientY-dragState.y;
    dragState.lastX=p.clientX;dragState.lastY=p.clientY;
    if(Math.hypot(dx,dy)>7)dragState.moved=true;
    if(dragState.wasFlipped)return;
    if(Math.abs(dx)>Math.abs(dy)&&e.cancelable)e.preventDefault();
    top.style.transform=`translateX(${dx}px) rotate(${(dx*.06).toFixed(2)}deg)`;
    if(dx!==0)animateLower(Math.min(1,Math.abs(dx)/(top.clientWidth*SWIPE_THRESHOLD)),dx>0?1:-1)
  };
  const end=()=>{
    if(!dragState)return;
    const dx=dragState.lastX-dragState.x,moved=dragState.moved,wasFlipped=dragState.wasFlipped,pointerId=dragState.pointerId;
    if(pointerId!==null&&top.hasPointerCapture?.(pointerId))top.releasePointerCapture(pointerId);
    dragState=null;
    if(wasFlipped){
      if(!moved)flipTopCard(false);
      return
    }
    if(Math.abs(dx)>top.clientWidth*SWIPE_THRESHOLD){completeSwipe(dx>0?1:-1);return}
    springBack();
    if(!moved)setTimeout(()=>flipTopCard(true),0)
  };
  if(window.PointerEvent){
    top.addEventListener('pointerdown',start);
    top.addEventListener('pointermove',move);
    top.addEventListener('pointerup',end);
    top.addEventListener('pointercancel',()=>{dragState=null;springBack()})
  }else{
    top.addEventListener('touchstart',start,{passive:true});
    top.addEventListener('touchmove',move,{passive:false});
    top.addEventListener('touchend',end);
    top.addEventListener('mousedown',start);
    window.addEventListener('mousemove',move);
    window.addEventListener('mouseup',end)
  }
}
function renderHome(forcedIndex=null){
  const hero=DATA.images.panda_portrait.replace(/w=\d+/,'w=1000');
  swipeDayIdx=forcedIndex===null||forcedIndex===undefined?initialSwipeIndex():forcedIndex;
  $('#home').innerHTML=`
   <div class="home-top"><div><div class="greeting" id="greet">${greeting()}</div><div class="greeting-en" id="greetEn"></div><div class="home-poem">${L('home_line')}</div></div>
     <div class="home-tools"><button class="lang-toggle" onclick="toggleLang()" aria-label="${L('switch_lang')}"><span style="${lang==='zh'?'font-weight:800':'opacity:.55'}">中</span> | <span style="${lang==='en'?'font-weight:800':'opacity:.55'}">EN</span></button><div class="wx"><div class="wx-row" id="wxIcon">${wxIcon(wx?wx.code:null)}<span class="wx-temp" id="wxTemp">${wx?Math.round(wx.t)+'°C':'—°C'}</span></div><small id="wxPlace">${L(wx?.city||weatherContext().key)} · ${wx?weatherCN(wx.code):L('weather_loading')}</small></div></div></div>
   <div class="hero"><img src="${hero}" alt="${lang==='zh'?'竹林中的大熊猫':'A giant panda resting on a wooden log'}" onerror="this.style.display='none'"><div class="hero-copy"><div class="cn1">${L('hero_1')}</div><div class="cn2">${L('hero_2')}</div></div></div>
   <div class="sheet"><div class="swipe-shell">
      <button class="stack-arrow prev" onclick="completeSwipe(-1)" aria-label="${lang==='zh'?'前一天':'Previous day'}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      <button class="stack-arrow next" onclick="completeSwipe(1)" aria-label="${lang==='zh'?'后一天':'Next day'}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      <div class="swipe-stage" id="swipeStage"></div><div class="stack-dots" id="stackDots"></div>
      <div class="stack-help">${lang==='zh'?'← 左滑前一天　·　轻触翻面　·　右滑后一天 →':'← Swipe left: previous · Tap: flip · Swipe right: next →'}</div>
   </div></div>`;
  renderSwipeStack(swipeDayIdx)
}
function sizeSwipe(){}

async function loadWeather(){
  try{
    const c=weatherContext(),r=await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lat}&longitude=${c.lon}&current=temperature_2m,weather_code&timezone=Asia%2FShanghai`);
    const j=await r.json();wx={t:j.current.temperature_2m,code:j.current.weather_code,city:c.key};
    const t=$('#wxTemp'),ic=$('#wxIcon svg');
    if(t){t.textContent=Math.round(wx.t)+'°C';ic.outerHTML=wxIcon(wx.code);const p=$('#wxPlace');if(p)p.textContent=L(wx.city)+' · '+weatherCN(wx.code)}
  }catch(e){}
}

function weatherContext(){
  const n=chinaNow(),d=currentDay(),minutes=n.h*60+n.m;
  const cq=d===2||(d===1&&minutes>=14*60)||(d===3&&minutes<17*60+30);
  return cq?{key:'chongqing',lat:29.5630,lon:106.5516}:{key:'chengdu',lat:30.5728,lon:104.0668};
}

'''
