/* Cronologia compacta, com datas reais e espaço suficiente para cada manchete. */
(function(root){
 'use strict';
 const DAY=86400000,START=Date.parse('2019-01-01T00:00:00Z'),END=Date.parse('2023-01-08T00:00:00Z'),TOTAL=(END-START)/DAY;
 const ordinal=date=>(Date.parse(date+'T00:00:00Z')-START)/DAY;
 function height(e,width,mobile){
  const font=mobile?(e.highlight?34:12):(e.highlight?49:16),chars=Math.max(10,Math.floor(width/(font*.55))),lines=Math.ceil(e.title.length/chars)+1;
  return 24+lines*font*1.3+(e.highlight&&(e.image||e.video)?width*.64+9:0);
 }
 function layout(events,width,mobile,measured={}){
  const months=[];for(let y=2019;y<=2023;y++)for(let m=1;m<=12;m++){const day=ordinal(`${y}-${String(m).padStart(2,'0')}-01`);if(day<=TOTAL)months.push(day);}
  const days=[...new Set([0,TOTAL,...months,...events.map(e=>ordinal(e.date))])].sort((a,b)=>a-b);
  const cards=[],points=[],ticks=[],bottoms=[0,0];let y=55,priorDay=0,priorCard=-100;
  for(const day of days){
   y+=(day-priorDay)*1.2;priorDay=day;
   const d=new Date(START+day*DAY),year=months.includes(day)&&d.getUTCMonth()===0;
   const month=months.includes(day);
   if(year){y=Math.max(y,...bottoms.map(b=>b+40));ticks.push({day,y,year:true});points.push({day,y});y+=60;}else if(month){y=Math.max(y,priorCard+16);ticks.push({day,y,year:false});points.push({day,y});y+=16;}
   const same=events.filter(e=>ordinal(e.date)===day);
   for(const e of same){const side=bottoms[0]<=bottoms[1]?0:1;y=Math.max(y,bottoms[side]+16,priorCard+22);const h=measured[e.id]||height(e,width,mobile);cards.push({event:e,day,y,height:h,side});bottoms[side]=y+h;priorCard=y;}
   if(!month)points.push({day,y});
  }
  function position(day){const after=points.findIndex(p=>p.day>=day);if(after<=0)return points[0].y;const a=points[after-1],b=points[after];return a.y+(day-a.day)/(b.day-a.day)*(b.y-a.y);}
  function dayAt(positionY){const after=points.findIndex(p=>p.y>=positionY);if(after<0)return TOTAL;if(after===0)return 0;const a=points[after-1],b=points[after];return Math.max(0,Math.min(TOTAL,a.day+(positionY-a.y)/(b.y-a.y)*(b.day-a.day)));}
  return {cards,ticks,position,dayAt,height:Math.max(y,...bottoms)+70};
 }
 const api={DAY,START,END,TOTAL,ordinal,height,layout};if(typeof module==='object'&&module.exports)module.exports=api;else root.TimelineEngine=api;
})(typeof window==='object'?window:globalThis);
