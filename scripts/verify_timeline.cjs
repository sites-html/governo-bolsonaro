const assert=require('node:assert/strict');
const E=require('../timeline-engine.js'),C=require('../categories.js'),events=require('../events.json'),fs=require('node:fs');
assert.equal(new Date(E.END).toISOString().slice(0,10),'2023-01-08');
for(const [viewport,mobile] of [[320,true],[375,true],[768,true],[1200,false]]){
 const width=mobile?viewport/2-34:415,l=E.layout(events,width,mobile);
 assert.deepEqual(l.cards.map(c=>c.event.id),events.map(e=>e.id));assert.equal(l.ticks.length,49);
 assert.equal(l.ticks.filter(t=>t.year).length,5);
 for(let i=1;i<l.cards.length;i++)assert(l.cards[i].y>l.cards[i-1].y);
 for(const test of [l,E.layout(events,width,mobile,Object.fromEntries(l.cards.map(c=>[c.event.id,c.height*1.5])))]){
  const prev=[null,null];for(const c of test.cards){if(prev[c.side])assert(c.y>=prev[c.side].y+prev[c.side].height+16);prev[c.side]=c;}
  for(const t of test.ticks.filter(t=>t.year))for(const c of test.cards.filter(c=>c.day<t.day))assert(c.y+c.height<=t.y-40+1e-7);
 }
 for(let day=0;day<=E.TOTAL;day+=13)assert(Math.abs(l.dayAt(l.position(day))-day)<1e-8);
}
for(const e of events)assert(C.classify(e).every(id=>C.themes.some(t=>t.id===id)));
assert.equal(new Set(C.themes.map(t=>t.color)).size,7);
assert(!fs.readFileSync('index.html','utf8').includes('id="theme-bar"'));
assert.equal(events.at(-1).date,'2023-01-08');assert(events.at(-1).title.includes('Planalto'));
assert(events.some(e=>e.title.includes('MPRJ denuncia Flávio')&&e.date==='2020-10-19'));
assert(events.some(e=>e.title.includes('Plano para matar')&&e.date==='2022-11-09'));
assert(events.some(e=>e.title.includes('Copa 2022')&&e.date==='2022-12-15'));
assert.equal(E.ordinal('2020-01-01'),365);assert.equal(E.ordinal('2021-01-01'),731);
console.log('OK: manchetes conservadas, layout compacto sem sobreposição em quatro larguras, anos livres e49meses; Flávio e golpe nas datas dos atos; final8janeiro.');
