# X 投稿専用ページ

Wikiの記事を抽選し、**見出し（項）ひとつ分を全文抜粋**して、投稿文と画像をXへ手動投稿するためのページです。記事内画像に加えて、記事本文内のリンク先ページをたどり、そのページにある画像も取得します。関連性による画像選別は行いません。複数画像は結合コピーとZIP保存ができます。文字数による省略はしません。投稿は自動送信されません。

<div id="xp">
  <p><button id="xp-next" class="md-button md-button--primary">次の投稿候補を抽選</button> <label><input type="checkbox" id="xp-repeat"> 投稿済みも抽選</label></p>
  <p id="xp-message" role="status" aria-live="polite">記事一覧を読み込んでいます…</p>
  <section id="xp-post" hidden>
    <h2 id="xp-title"></h2>
    <p>記事：<a id="xp-link" target="_blank" rel="noopener noreferrer"></a></p>
    <label for="xp-text"><strong>投稿文（編集可能）</strong></label>
    <textarea id="xp-text" rows="7" style="display:block;width:100%;box-sizing:border-box"></textarea>
    <p id="xp-count"></p>
    <p><small>※ 抜粋は見出し単位で全文を取得します。Xの投稿文字数上限を超える場合は、投稿前に編集するか分割してください。</small></p>
    <div class="xp-buttons">
      <button id="xp-both" class="md-button md-button--primary">一括コピー（本文＋全画像の結合画像）</button>
      <button id="xp-text-copy" class="md-button">本文をコピー</button>
      <a href="https://x.com/compose/post" class="md-button" target="_blank" rel="noopener noreferrer">X投稿画面</a>
    </div>
    <p><small>※ 一括コピーでは本文と全画像を1枚に結合したPNG画像を格納します。Xが本文と画像を同時に貼り付けるとは限りません。画像を個別に添付する場合はZIP保存をご利用ください。</small></p>
    <h3>添付画像</h3>
    <div id="xp-images"></div>
    <div class="xp-buttons">
      <button id="xp-image-copy" class="md-button">選択画像をコピー</button>
      <button id="xp-images-copy" class="md-button md-button--primary">全画像をコピー（1枚に結合）</button>
      <button id="xp-image-save" class="md-button">選択画像を保存</button>
      <button id="xp-images-save" class="md-button">全画像を保存（ZIP）</button>
    </div>
    <div class="xp-buttons">
      <button id="xp-done" class="md-button md-button--primary">投稿済みにする</button>
      <button id="xp-undo" class="md-button">未投稿に戻す</button>
      <span id="xp-state"></span>
    </div>
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
const app=document.getElementById('xp');if(!app||app.dataset.initialized)return;app.dataset.initialized='yes';
const $=id=>document.getElementById('xp-'+id), base=new URL('../',location.href);
const store='sekigahara-posted-articles-v1';let pages=[],current=null;
let posted;try{posted=new Set(JSON.parse(localStorage.getItem(store)||'[]'))}catch{posted=new Set()}
const say=message=>$('message').textContent=message;
const count=()=>$('count').textContent=Array.from($('text').value).length+'文字（XのURL文字数カウントとは異なる場合があります）';
function eligible(u){const p=decodeURIComponent(u.pathname.slice(base.pathname.length)).replace(/\/$/,'');
return /^(game|gameplay|systems|formations|experiments|scenarios|commanders)\//.test(p)&&!p.startsWith('en/')}
async function loadList(){let r=await fetch(new URL('sitemap.xml',base));if(!r.ok)throw Error('サイトマップを取得できません');
const xml=new DOMParser().parseFromString(await r.text(),'text/xml');if(xml.querySelector('parsererror'))throw Error('サイトマップの形式が不正です');
return [...new Set([...xml.querySelectorAll('url > loc')].map(el=>{try{let u=new URL(el.textContent.trim());return u.origin===location.origin&&u.pathname.startsWith(base.pathname)&&eligible(u)?u.origin+u.pathname:null}catch{return null}}).filter(Boolean))]}
async function loadArticle(url){let r=await fetch(url);if(!r.ok)throw Error('記事が見つかりません');
let doc=new DOMParser().parseFromString(await r.text(),'text/html'),box=doc.querySelector('article.md-content__inner, .md-content__inner');if(!box)throw Error('記事本文がありません');
let title=(box.querySelector('h1')?.textContent||doc.title).replace(/[¶#]\s*$/,'').trim();
// h2/h3 の見出し単位で内容を取得する。少なくとも1項を全文取得し、文字数による切り詰めは行わない。
// h2 の項は次の h2 まで（h3 等の小項も含む）、h3 は次の h2/h3 まで。
function extractSection(root){
  const headings=[...root.querySelectorAll('h2,h3')];
  const sections=[];
  for(const heading of headings){
    const level=Number(heading.tagName[1]);
    const parts=[];
    let node=heading.nextElementSibling;
    while(node){
      if(/^H[1-6]$/.test(node.tagName)&&Number(node.tagName[1])<=level)break;
      // MkDocs の編集UI等は除去するが、本文の段落・リスト・表は残す。
      const copy=node.cloneNode(true);
      copy.querySelectorAll('script,style,.headerlink,.md-source-file,button').forEach(e=>e.remove());
      const lines=[];
      function read(el){
        if(el.nodeType===3)return el.textContent.replace(/\s+/g,' ');
        if(el.nodeType!==1)return '';
        if(['SCRIPT','STYLE','IMG','SVG'].includes(el.tagName))return '';
        if(el.matches('li'))return '・'+[...el.childNodes].map(read).join('').trim()+'\n';
        if(el.matches('tr'))return [...el.querySelectorAll(':scope > th,:scope > td')].map(c=>c.textContent.replace(/\s+/g,' ').trim()).join(' | ')+'\n';
        if(el.matches('table'))return [...el.querySelectorAll('tr')].map(read).join('');
        if(el.matches('p,h3,h4,h5,h6,dt,dd,blockquote'))return [...el.childNodes].map(read).join('').trim()+'\n';
        return [...el.childNodes].map(read).join('');
      }
      let part=read(copy).replace(/[ \t]+\n/g,'\n').trim();
      if(part)parts.push(part);
      node=node.nextElementSibling;
    }
    const headingName=heading.textContent.replace(/¶/g,'').trim();
    if(headingName&&parts.length)sections.push({heading:headingName,body:parts.join('\n\n')});
  }
  // h2/h3 がない記事は記事本文を「ひとつの項」として全文抜粋する。
  if(!sections.length){
    const fallback=root.cloneNode(true);
    fallback.querySelectorAll('script,style,.headerlink,.md-source-file,h1,a[href*="/en/"],img').forEach(e=>e.remove());
    const whole=fallback.innerText||fallback.textContent||'';
    return {heading:'',body:whole.trim()};
  }
  return sections[Math.floor(Math.random()*sections.length)];
}
const section=extractSection(box);
let images=[...box.querySelectorAll('img')].map(e=>{try{let src=e.getAttribute('src');if(!src||src.startsWith('data:'))return null;let u=new URL(src,url);return u.origin===location.origin?{src:u.href,alt:e.alt||'記事の画像'}:null}catch{return null}}).filter(Boolean);
// 記事本文に書かれたリンク先（同じWiki内）をたどり、見つかった画像をすべて追加する。
// 武将名・alt・ファイル名による関連性チェックは行わない。
// ヘッダーやサイドバーではなく、記事本文のリンクだけを対象にする。
const visited=new Set([new URL(url).href]);
const linkedPages=[...box.querySelectorAll('a[href]')].map(a=>{
  try {
    const href=a.getAttribute('href');
    if(!href || href.startsWith('#') || /^(mailto:|javascript:|tel:)/i.test(href))return null;
    const link=new URL(href,url);
    link.hash='';link.search='';
    // Wiki外へのアクセスとファイルへの誤アクセスだけを防ぐ。
    if(link.origin!==base.origin || !link.pathname.startsWith(base.pathname))return null;
    if(/\.(?:png|jpe?g|gif|webp|svg|pdf|zip|mp4|webm)$/i.test(link.pathname))return null;
    if(!link.pathname.endsWith('/'))return null;
    return link.href;
  }catch{return null}
}).filter(Boolean);
// 一つのページから直接たどれるリンクを検索する。無限巡回を防ぐためリンク先のリンクは追わない。
for(const linkedUrl of linkedPages){
  if(visited.has(linkedUrl))continue;
  visited.add(linkedUrl);
  try{
    const response=await fetch(linkedUrl);
    if(!response.ok)continue;
    const linkedDoc=new DOMParser().parseFromString(await response.text(),'text/html');
    const linkedBody=linkedDoc.querySelector('article.md-content__inner, .md-content__inner');
    if(!linkedBody)continue;
    for(const image of linkedBody.querySelectorAll('img')){
      const src=image.getAttribute('src');
      if(!src || src.startsWith('data:'))continue;
      try{
        const imageUrl=new URL(src,linkedUrl);
        if(imageUrl.origin===location.origin)images.push({src:imageUrl.href,alt:image.alt || 'リンク先の画像'});
      }catch{}
    }
  }catch(error){console.warn('リンク先の画像を取得できませんでした',linkedUrl,error)}
}
images=images.filter((e,i)=>images.findIndex(x=>x.src===e.src)===i);
return {url,title,section,images}}
function postText(a){
 const heading=a.section.heading&&a.section.heading!==a.title?'【'+a.section.heading+'】\n\n':'';
 return a.title+'\n\n'+heading+a.section.body+'\n\n'+a.url;
}
function selected(){return document.querySelector('#xp input[name="xp-image"]:checked')?.value||null}
function state(){return $('state').textContent=posted.has(current.url)?'投稿済み':'未投稿'}
function show(a){current=a;$('post').hidden=false;$('title').textContent=a.title;$('link').textContent=a.url;$('link').href=a.url;$('text').value=postText(a);count();
$('images').replaceChildren();if(!a.images.length)$('images').textContent='この記事には画像がありません。';
a.images.forEach((im,i)=>{let label=document.createElement('label');label.className='xp-img';let radio=document.createElement('input');radio.type='radio';radio.name='xp-image';radio.value=im.src;radio.checked=i===0;
let span=document.createElement('span');span.textContent=' 画像 '+(i+1)+'：'+im.alt;let img=document.createElement('img');img.src=im.src;img.alt=im.alt;img.loading='lazy';label.append(radio,span,img);$('images').append(label)});
for(let id of ['image-copy','images-copy','image-save','images-save'])$(id).disabled=!a.images.length;state()}
async function next(){let pool=pages.filter(x=>$('repeat').checked||!posted.has(x));if(!pool.length){say('未投稿の記事がありません。投稿済みも抽選を選択してください。');return}
$('next').disabled=true;say('記事を読み込み中…');try{for(let tries=0;tries<Math.min(pool.length,8);tries++){
let i=Math.floor(Math.random()*pool.length),url=pool.splice(i,1)[0];if(url===current?.url&&pool.length)continue;
try{show(await loadArticle(url));say('投稿候補を表示しました。');return}catch(err){console.warn(err)}}throw Error('記事の読み込みに失敗しました')}
catch(err){say(err.message)}finally{$('next').disabled=false}}
async function png(src){let r=await fetch(src);if(!r.ok)throw Error('画像を取得できません');let bitmap=await createImageBitmap(await r.blob());try{let canvas=document.createElement('canvas');canvas.width=bitmap.width;canvas.height=bitmap.height;canvas.getContext('2d').drawImage(bitmap,0,0);return await new Promise((ok,no)=>canvas.toBlob(b=>b?ok(b):no(Error('PNG変換に失敗')),'image/png'))}finally{bitmap.close()}}
// 全画像を縦方向に連結して1枚のPNGにする（クリップボードは複数の独立画像を保証しない）。
async function combinedPng(){
 if(!current?.images.length)throw Error('画像がありません');
 const bitmaps=[];
 try{
  for(const im of current.images){
   const r=await fetch(im.src);if(!r.ok)throw Error('画像の取得に失敗：'+im.src);
   bitmaps.push(await createImageBitmap(await r.blob()));
  }
  const maxWidth=1600, width=Math.min(maxWidth,Math.max(...bitmaps.map(b=>b.width)));
  const padding=16, heights=bitmaps.map(b=>Math.round(b.height*width/b.width));
  const totalHeight=heights.reduce((a,b)=>a+b,0)+padding*(bitmaps.length-1);
  if(width*totalHeight>80000000 || totalHeight>32767)throw Error('全画像が大きすぎるため結合できません。ZIP保存で個別画像を使用してください');
  const canvas=document.createElement('canvas');canvas.width=width;canvas.height=totalHeight;
  const ctx=canvas.getContext('2d');ctx.fillStyle='#ffffff';ctx.fillRect(0,0,width,totalHeight);
  let y=0;bitmaps.forEach((b,i)=>{ctx.drawImage(b,0,y,width,heights[i]);y+=heights[i]+padding});
  return await new Promise((ok,no)=>canvas.toBlob(b=>b?ok(b):no(Error('画像結合に失敗しました')),'image/png'));
 }finally{bitmaps.forEach(b=>b.close())}
}
function download(blob,name){
 const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;
 document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),30000);
}
function fileName(index,ext){return 'sekigahara-'+(current.url.split('/').filter(Boolean).pop()||'post')+'-'+index+'.'+ext}
async function save(src,index){
 const r=await fetch(src);if(!r.ok)throw Error('画像を取得できません');
 const blob=await r.blob();const ext=blob.type==='image/png'?'png':blob.type==='image/webp'?'webp':blob.type==='image/gif'?'gif':'jpg';
 download(blob,fileName(index,ext));
}
// 依存ライブラリや外部CDNを使わないZIP(STORE形式)作成。
const encoder=new TextEncoder();
const crcTable=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=(c&1)?(0xedb88320^(c>>>1)):(c>>>1);return c>>>0});
function crc32(bytes){let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return(c^0xffffffff)>>>0}
function zipFiles(files){
 const pieces=[],central=[];let offset=0;
 for(const {name,bytes} of files){
  const nameBytes=encoder.encode(name),crc=crc32(bytes),n=bytes.length;
  const local=new Uint8Array(30+nameBytes.length),v=new DataView(local.buffer);
  v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x0800,true);
  v.setUint32(14,crc,true);v.setUint32(18,n,true);v.setUint32(22,n,true);v.setUint16(26,nameBytes.length,true);
  local.set(nameBytes,30);pieces.push(local,bytes);
  const cd=new Uint8Array(46+nameBytes.length),w=new DataView(cd.buffer);
  w.setUint32(0,0x02014b50,true);w.setUint16(4,20,true);w.setUint16(6,20,true);w.setUint16(8,0x0800,true);
  w.setUint32(16,crc,true);w.setUint32(20,n,true);w.setUint32(24,n,true);
  w.setUint16(28,nameBytes.length,true);w.setUint32(42,offset,true);cd.set(nameBytes,46);
  central.push(cd);offset+=local.length+bytes.length;
 }
 const centralSize=central.reduce((s,b)=>s+b.length,0),end=new Uint8Array(22),v=new DataView(end.buffer);
 v.setUint32(0,0x06054b50,true);v.setUint16(8,files.length,true);v.setUint16(10,files.length,true);
 v.setUint32(12,centralSize,true);v.setUint32(16,offset,true);
 return new Blob([...pieces,...central,end],{type:'application/zip'});
}
async function saveAll(){
 const files=[];
 for(let i=0;i<current.images.length;i++){
  const src=current.images[i].src,r=await fetch(src);if(!r.ok)throw Error('画像を取得できません：'+src);
  const blob=await r.blob(),bytes=new Uint8Array(await blob.arrayBuffer());
  const ext=blob.type==='image/png'?'png':blob.type==='image/webp'?'webp':blob.type==='image/gif'?'gif':'jpg';
  files.push({name:fileName(i+1,ext),bytes});
 }
 download(zipFiles(files),'sekigahara-'+(current.url.split('/').filter(Boolean).pop()||'post')+'-all-images.zip');
}
async function run(fn){try{await fn()}catch(e){say('失敗：'+e.message+'。画像保存や本文コピーをお試しください。')}}
$('next').onclick=next;$('text').oninput=count;
$('text-copy').onclick=()=>run(async()=>{await navigator.clipboard.writeText($('text').value);say('本文をコピーしました。')});
$('image-copy').onclick=()=>run(async()=>{let src=selected();if(!src)throw Error('画像がありません');let item=new ClipboardItem({'image/png':png(src)});await navigator.clipboard.write([item]);say('画像をコピーしました。')});
$('images-copy').onclick=()=>run(async()=>{
 if(!current.images.length)throw Error('画像がありません');
 await navigator.clipboard.write([new ClipboardItem({'image/png':combinedPng()})]);
 say('全'+current.images.length+'枚を1枚のPNGに結合してコピーしました。');
});
$('both').onclick=()=>run(async()=>{
 if(!current.images.length){await navigator.clipboard.writeText($('text').value);say('画像がないため本文のみコピーしました。');return}
 const item=new ClipboardItem({'text/plain':new Blob([$('text').value],{type:'text/plain'}),'image/png':combinedPng()});
 await navigator.clipboard.write([item]);
 say('本文＋全画像を結合したPNGをコピーしました。Xで両方が貼り付いたか確認してください。');
});
$('image-save').onclick=()=>run(async()=>{let src=selected();if(!src)throw Error('画像がありません');await save(src,1);say('画像の保存を開始しました。')});
$('images-save').onclick=()=>run(async()=>{await saveAll();say('全'+current.images.length+'枚の画像をZIPに保存しました。')});
function mark(yes){if(!current)return;yes?posted.add(current.url):posted.delete(current.url);localStorage.setItem(store,JSON.stringify([...posted]));state();say(yes?'投稿済みにしました。':'未投稿に戻しました。')}
$('done').onclick=()=>mark(true);$('undo').onclick=()=>mark(false);
loadList().then(list=>{pages=list;if(!list.length)throw Error('対象の記事がありません');next()}).catch(e=>say('記事一覧の取得に失敗：'+e.message));
})();
</script>
