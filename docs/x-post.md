# X 投稿専用ページ

Wikiの記事から投稿候補を抽選し、見出し単位の文章を編集・コピーしてXに手動投稿するページです。**武将ページでは武将画像（肖像）を優先し、旗印・記事内画像も追加します。** 文字数で自動省略はしません。Xへの自動投稿は行いません。

<div id="xp">
  <p><button id="xp-next" class="md-button md-button--primary" type="button">次の投稿候補を抽選</button> <label><input type="checkbox" id="xp-repeat"> 投稿済みも抽選</label></p>
  <p id="xp-message" role="status" aria-live="polite">記事一覧を読み込んでいます…</p>
  <section id="xp-post" hidden>
    <h2 id="xp-title"></h2>
    <p>関ヶ原IF布陣シミュレータ公式wikiから</p>
    <p>抜粋元：<a id="xp-link" target="_blank" rel="noopener noreferrer"></a></p>
    <label for="xp-text"><strong>投稿文（編集可能）</strong></label>
    <textarea id="xp-text" rows="7" style="display:block;width:100%;box-sizing:border-box"></textarea>
    <p id="xp-count"></p>
    <p><small>見出し単位で全文を抽出します。Xの文字数上限を超える場合は編集または分割してください。</small></p>
    <div class="xp-buttons">
      <button type="button" id="xp-both" class="md-button md-button--primary">一括コピー（本文＋全画像の結合画像）</button>
      <button type="button" id="xp-text-copy" class="md-button">本文をコピー</button>
      <a href="https://x.com/compose/post" class="md-button" target="_blank" rel="noopener noreferrer">X投稿画面</a>
    </div>
    <p><small>一括コピーでは全文と、全画像を縦に連結した1枚のPNGをコピーします。Xが両方を同時に貼り付けるとは限りません。貼り付け結果を確認してください。</small></p>
    <h3>添付画像</h3>
    <div id="xp-images"></div>
    <div class="xp-buttons">
      <button type="button" id="xp-image-copy" class="md-button">選択画像をコピー</button>
      <button type="button" id="xp-images-copy" class="md-button md-button--primary">全画像をコピー（1枚に結合）</button>
      <button type="button" id="xp-image-save" class="md-button">選択画像を保存</button>
      <button type="button" id="xp-images-save" class="md-button">全画像を保存（ZIP）</button>
    </div>
    <div class="xp-buttons">
      <button type="button" id="xp-done" class="md-button md-button--primary">投稿済みにする</button>
      <button type="button" id="xp-undo" class="md-button">未投稿に戻す</button>
      <span id="xp-state"></span>
    </div>
    <p><small>投稿済みの記録は、このブラウザ内に保存されます。別ブラウザや別PCとは同期しません。</small></p>
  </section>
</div>
<style>
#xp .xp-buttons{display:flex;flex-wrap:wrap;gap:.5rem;margin:.8rem 0;align-items:center}
#xp button{cursor:pointer}#xp button:disabled{opacity:.5;cursor:not-allowed}
#xp .xp-img{display:block;padding:.6rem;margin:.65rem 0;border:1px solid var(--md-default-fg-color--lightest);border-radius:6px}
#xp .xp-img img{display:block;max-width:100%;max-height:300px;object-fit:contain;margin:.5rem 0}
</style>
<script>
(()=>{
const app=document.getElementById('xp');
if(!app || app.dataset.initialized)return;
app.dataset.initialized='yes';
const $=id=>document.getElementById('xp-'+id);
const base=new URL('../',location.href);
const store='sekigahara-posted-articles-v1';
let pages=[],current=null;
let posted;
try{posted=new Set(JSON.parse(localStorage.getItem(store)||'[]'))}catch{posted=new Set()}
const say=message=>$('message').textContent=message;
const count=()=>$('count').textContent=Array.from($('text').value).length+'文字（XのURL文字数カウントとは異なる場合があります）';
function eligible(u){
 const path=decodeURIComponent(u.pathname.slice(base.pathname.length)).replace(/\/$/,'');
 return /^(game|gameplay|systems|formations|experiments|scenarios|commanders)\//.test(path) && !path.startsWith('en/');
}
async function loadList(){
 const response=await fetch(new URL('sitemap.xml',base));
 if(!response.ok)throw Error('サイトマップを取得できません');
 const xml=new DOMParser().parseFromString(await response.text(),'text/xml');
 if(xml.querySelector('parsererror'))throw Error('サイトマップの形式が不正です');
 return [...new Set([...xml.querySelectorAll('url > loc')].map(el=>{
  try{const u=new URL(el.textContent.trim());return u.origin===location.origin&&u.pathname.startsWith(base.pathname)&&eligible(u)?u.origin+u.pathname:null}
  catch{return null}
 }).filter(Boolean))];
}
function extractSection(root){
 const sections=[];
 const headings=[...root.querySelectorAll('h2,h3')];
 function read(node){
  if(node.nodeType===3)return node.textContent.replace(/\s+/g,' ');
  if(node.nodeType!==1)return '';
  if(['SCRIPT','STYLE','IMG','SVG','BUTTON'].includes(node.tagName) || node.classList.contains('headerlink'))return '';
  if(node.matches('tr'))return [...node.querySelectorAll(':scope > th,:scope > td')].map(c=>c.textContent.replace(/\s+/g,' ').trim()).join(' | ')+'\n';
  if(node.matches('table'))return [...node.querySelectorAll('tr')].map(read).join('');
  if(node.matches('li'))return '・'+[...node.childNodes].map(read).join('').trim()+'\n';
  if(node.matches('p,h3,h4,h5,h6,dt,dd,blockquote'))return [...node.childNodes].map(read).join('').trim()+'\n';
  return [...node.childNodes].map(read).join('');
 }
 for(const heading of headings){
  const level=Number(heading.tagName[1]),parts=[];
  for(let node=heading.nextElementSibling;node;node=node.nextElementSibling){
   if(/^H[1-6]$/.test(node.tagName) && Number(node.tagName[1])<=level)break;
   const chunk=read(node).replace(/[ \t]+\n/g,'\n').trim();
   if(chunk)parts.push(chunk);
  }
  if(parts.length)sections.push({heading:heading.textContent.replace(/¶/g,'').trim(),body:parts.join('\n\n')});
 }
 if(sections.length)return sections[Math.floor(Math.random()*sections.length)];
 const clone=root.cloneNode(true);
 clone.querySelectorAll('script,style,.headerlink,.md-source-file,h1,a[href*="/en/"],img').forEach(e=>e.remove());
 return {heading:'',body:(clone.textContent||'').replace(/\n[ \t]+/g,'\n').trim()};
}
async function loadArticle(url){
 const response=await fetch(url);if(!response.ok)throw Error('記事が見つかりません');
 const doc=new DOMParser().parseFromString(await response.text(),'text/html');
 const box=doc.querySelector('article.md-content__inner, .md-content__inner');
 if(!box)throw Error('記事本文がありません');
 const title=(box.querySelector('h1')?.textContent||doc.title).replace(/[¶#]\s*$/,'').trim();
 const section=extractSection(box);
 // 武将ページはURLのスラッグから肖像画像の固定URLを構成する。
 const path=decodeURIComponent(new URL(url).pathname.slice(base.pathname.length)).replace(/\/$/,'');
 const commander=path.match(/^commanders\/(?:eastern|western|user)\/([a-z0-9-]+)$/);
 let images=[];
 if(commander){
  const portrait=new URL('assets/images/commanders/'+encodeURIComponent(commander[1])+'.png',base);
  try{
   const r=await fetch(portrait.href);
   if(r.ok && (r.headers.get('content-type')||'').startsWith('image/'))images.push({src:portrait.href,alt:title+'の武将画像'});
  }catch(err){console.warn('武将画像を確認できませんでした',portrait.href,err)}
 }
 // 記事中の旗印と画像を追加する。記事内リンク先を巡回しない。
 const articleImages=[...box.querySelectorAll('img')].map(img=>{
  try{
   const src=img.getAttribute('src');if(!src||src.startsWith('data:'))return null;
   const u=new URL(src,url);
   return u.origin===base.origin&&u.pathname.startsWith(base.pathname)?{src:u.href,alt:img.alt||'記事画像'}:null;
  }catch{return null}
 }).filter(Boolean);
 articleImages.sort((a,b)=>Number(/\/images\/flags\//.test(b.src))-Number(/\/images\/flags\//.test(a.src)));
 images.push(...articleImages);
 images=images.filter((img,i)=>images.findIndex(x=>x.src===img.src)===i);
 return {url,title,section,images};
}
function postText(a){
 const h=a.section.heading&&a.section.heading!==a.title?'【'+a.section.heading+'】\n\n':'';
 return a.title+'\n\n'+h+a.section.body+'\n\n関ヶ原IF布陣シミュレータ公式wikiから\n'+a.url;
}
function selected(){return app.querySelector('input[name="xp-image"]:checked')?.value||null}
function state(){$('state').textContent=posted.has(current.url)?'投稿済み':'未投稿'}
function show(a){
 current=a;$('post').hidden=false;$('title').textContent=a.title;
 $('link').textContent=a.url;$('link').href=a.url;
 $('text').value=postText(a);count();
 $('images').replaceChildren();
 if(!a.images.length)$('images').textContent='この記事には画像がありません。';
 a.images.forEach((im,i)=>{
  const label=document.createElement('label');label.className='xp-img';
  const radio=document.createElement('input');radio.type='radio';radio.name='xp-image';radio.value=im.src;radio.checked=i===0;
  const text=document.createElement('span');text.textContent=' 画像 '+(i+1)+'：'+im.alt;
  const img=document.createElement('img');img.src=im.src;img.alt=im.alt;img.loading='lazy';
  label.append(radio,text,img);$('images').append(label);
 });
 for(const id of ['image-copy','images-copy','image-save','images-save'])$(id).disabled=!a.images.length;
 state();
}
async function next(){
 const pool=pages.filter(url=>$('repeat').checked||!posted.has(url));
 if(!pool.length){say('未投稿の記事がありません。「投稿済みも抽選」を選んでください。');return}
 $('next').disabled=true;say('記事を読み込み中…');
 try{
  for(let i=0;i<Math.min(8,pool.length);i++){
   const ix=Math.floor(Math.random()*pool.length),url=pool.splice(ix,1)[0];
   if(url===current?.url && pool.length)continue;
   try{show(await loadArticle(url));say('投稿候補を表示しました。');return}catch(error){console.warn(error)}
  }
  throw Error('記事の読み込みに失敗しました');
 }catch(error){say(error.message)}finally{$('next').disabled=false}
}
async function getBitmap(src){
 const response=await fetch(src);
 if(!response.ok)throw Error('画像の取得に失敗しました：'+src);
 return createImageBitmap(await response.blob());
}
async function blobFromCanvas(canvas){
 return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(Error('PNG画像を生成できません')),'image/png'));
}
async function png(src){
 const bitmap=await getBitmap(src);
 try{
  const canvas=document.createElement('canvas');canvas.width=bitmap.width;canvas.height=bitmap.height;
  const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvasが利用できません');
  ctx.drawImage(bitmap,0,0);return await blobFromCanvas(canvas);
 }finally{bitmap.close()}
}
async function combinedPng(){
 if(!current?.images.length)throw Error('画像がありません');
 const bitmaps=[];
 try{
  for(const im of current.images)bitmaps.push(await getBitmap(im.src));
  const width=Math.min(1600,Math.max(...bitmaps.map(b=>b.width))),gap=16;
  const heights=bitmaps.map(b=>Math.round(b.height*width/b.width));
  const height=heights.reduce((a,b)=>a+b,0)+gap*(bitmaps.length-1);
  if(width*height>80000000||height>32767)throw Error('結合画像が大きすぎます。ZIP保存をご利用ください');
  const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;
  const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvasが利用できません');
  ctx.fillStyle='#fff';ctx.fillRect(0,0,width,height);
  let y=0;bitmaps.forEach((b,i)=>{ctx.drawImage(b,0,y,width,heights[i]);y+=heights[i]+gap});
  return blobFromCanvas(canvas);
 }finally{bitmaps.forEach(b=>b.close())}
}
function download(blob,name){
 const url=URL.createObjectURL(blob),link=document.createElement('a');
 link.href=url;link.download=name;document.body.append(link);link.click();link.remove();
 setTimeout(()=>URL.revokeObjectURL(url),30000);
}
function fileName(index,ext){return 'sekigahara-'+(current.url.split('/').filter(Boolean).pop()||'post')+'-'+index+'.'+ext}
async function getFile(src,index){
 const response=await fetch(src);if(!response.ok)throw Error('画像を取得できません：'+src);
 const blob=await response.blob();
 const ext=blob.type==='image/png'?'png':blob.type==='image/webp'?'webp':blob.type==='image/gif'?'gif':'jpg';
 return {name:fileName(index,ext),bytes:new Uint8Array(await blob.arrayBuffer()),blob};
}
// 外部ライブラリに依存せずZIP（STORE方式）を生成する。
const encoder=new TextEncoder();
const crcTable=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;return c>>>0});
function crc32(bytes){let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0}
function zipFiles(files){
 const parts=[],central=[];let offset=0;
 for(const {name,bytes} of files){
  const n=bytes.length,nameBytes=encoder.encode(name),crc=crc32(bytes);
  const local=new Uint8Array(30+nameBytes.length),v=new DataView(local.buffer);
  v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x0800,true);
  v.setUint32(14,crc,true);v.setUint32(18,n,true);v.setUint32(22,n,true);
  v.setUint16(26,nameBytes.length,true);local.set(nameBytes,30);
  parts.push(local,bytes);
  const cd=new Uint8Array(46+nameBytes.length),w=new DataView(cd.buffer);
  w.setUint32(0,0x02014b50,true);w.setUint16(4,20,true);w.setUint16(6,20,true);w.setUint16(8,0x0800,true);
  w.setUint32(16,crc,true);w.setUint32(20,n,true);w.setUint32(24,n,true);
  w.setUint16(28,nameBytes.length,true);w.setUint32(42,offset,true);cd.set(nameBytes,46);
  central.push(cd);offset+=local.length+bytes.length;
 }
 const centralSize=central.reduce((sum,x)=>sum+x.length,0);
 const end=new Uint8Array(22),v=new DataView(end.buffer);
 v.setUint32(0,0x06054b50,true);v.setUint16(8,files.length,true);v.setUint16(10,files.length,true);
 v.setUint32(12,centralSize,true);v.setUint32(16,offset,true);
 return new Blob([...parts,...central,end],{type:'application/zip'});
}
async function saveAll(){
 const files=[];
 for(let i=0;i<current.images.length;i++)files.push(await getFile(current.images[i].src,i+1));
 download(zipFiles(files),'sekigahara-'+(current.url.split('/').filter(Boolean).pop()||'post')+'-all-images.zip');
}
async function run(fn){try{await fn()}catch(error){say('失敗：'+error.message+'。画像保存や本文コピーをお試しください。')}}
$('next').onclick=next;$('text').oninput=count;
$('text-copy').onclick=()=>run(async()=>{await navigator.clipboard.writeText($('text').value);say('本文をコピーしました。')});
$('image-copy').onclick=()=>run(async()=>{
 const src=selected();if(!src)throw Error('画像がありません');
 await navigator.clipboard.write([new ClipboardItem({'image/png':png(src)})]);
 say('選択画像をコピーしました。');
});
$('images-copy').onclick=()=>run(async()=>{
 await navigator.clipboard.write([new ClipboardItem({'image/png':combinedPng()})]);
 say('全画像を1枚のPNGに結合してコピーしました。');
});
$('both').onclick=()=>run(async()=>{
 if(!current.images.length){await navigator.clipboard.writeText($('text').value);say('本文のみコピーしました。');return}
 await navigator.clipboard.write([new ClipboardItem({
  'text/plain':new Blob([$('text').value],{type:'text/plain'}),
  'image/png':combinedPng()
 })]);
 say('本文と結合画像をコピーしました。Xで両方貼り付いたか確認してください。');
});
$('image-save').onclick=()=>run(async()=>{
 const src=selected();if(!src)throw Error('画像がありません');
 const file=await getFile(src,1);download(file.blob,file.name);say('画像を保存しました。');
});
$('images-save').onclick=()=>run(async()=>{await saveAll();say('全画像のZIP保存を開始しました。')});
function mark(yes){
 if(!current)return;
 yes?posted.add(current.url):posted.delete(current.url);
 localStorage.setItem(store,JSON.stringify([...posted]));state();
 say(yes?'投稿済みにしました。':'未投稿に戻しました。');
}
$('done').onclick=()=>mark(true);$('undo').onclick=()=>mark(false);
loadList().then(list=>{pages=list;if(!pages.length)throw Error('対象の記事がありません');return next()}).catch(error=>say('記事一覧の取得に失敗：'+error.message));
})();
</script>
