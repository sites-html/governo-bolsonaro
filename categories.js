/* Categorias editoriais; os estados de denúncia/investigação permanecem nas fichas. */
(function(root){
 const themes=[
  {id:'democracia',name:'Golpe e democracia',color:'#e9897c'},
  {id:'covid',name:'Covid-19',color:'#b5a0e8'},
  {id:'corrupcao',name:'Corrupção e suspeitas',color:'#e0a769'},
  {id:'economia',name:'Economia',color:'#d0c182'},
  {id:'ambiente',name:'Meio ambiente',color:'#91b99a'},
  {id:'direitos',name:'Direitos e intolerância',color:'#8fbbd8'},
  {id:'governo',name:'Crises de governo',color:'#b7bdc7'}
 ];
 function classify(e){
  const themes=[];
  if(e.category==='Democracia')themes.push('democracia');
  if(e.category==='Saúde'||/covaxin|cpi.*pandemia|cpi.*covid/i.test(e.title))themes.push('covid');
  if(/joias|covaxin|pastor|pastores|milton ribeiro|orçamento secreto|emendas opacas|rachadinh|queiroz|flávio.*(?:denúncia|peculato|lavagem)|(?:denúncia|peculato|lavagem).*flávio/i.test(e.title))themes.unshift('corrupcao');
  const original={'Economia':'economia','Meio ambiente':'ambiente','Direitos':'direitos','Governo':'governo'}[e.category];
  if(original)themes.push(original);
  return [...new Set(themes.length?themes:['governo'])];
 }
 const api={themes,classify};
 if(typeof module==='object'&&module.exports)module.exports=api;else root.ArchiveCategories=api;
})(typeof window==='object'?window:globalThis);
