# X 投稿専用ページ

Wikiの記事を抽選し、投稿文と画像をXへ手動投稿するためのページです。投稿は自動送信されません。

<div id="xp">
  <p><button id="xp-next" class="md-button md-button--primary">次の投稿候補を抽選</button> <label><input type="checkbox" id="xp-repeat"> 投稿済みも抽選</label></p>
  <p id="xp-message" role="status" aria-live="polite">記事一覧を読み込んでいます…</p>
  <section id="xp-post" hidden>
    <h2 id="xp-title"></h2>
    <p>記事：<a id="xp-link" target="_blank" rel="noopener noreferrer"></a></p>
    <label for="xp-text"><strong>投稿文（編集可能）</strong></label>
    <textarea id="xp-text" rows="7" style="display:block;width:100%;box-sizing:border-box"></textarea>
    <p id="xp-count"></p>
    <div class="xp-buttons">
      <button id="xp-both" class="md-button md-button--primary">一括コピー（本文＋画像）</button>
      <button id="xp-text-copy" class="md-button">本文をコピー</button>
      <a href="https://x.com/compose/post" class="md-button" target="_blank" rel="noopener noreferrer">X投稿画面</a>
    </div>
    <p><small>※ 一括コピーでは本文＋選択画像1枚をクリップボードに格納します。Xが両方同時に貼り付けるとは限りません。貼り付け後に確認してください。</small></p>
    <h3>添付画像</h3>
    <div id="xp-images"></div>
    <div class="xp-buttons">
      <button id="xp-image-copy" class="md-button">画像をコピー</button>
      <button id="xp-image-save" class="md-button">画像を保存</button>
      <button id="xp-images-save" class="md-button">全画像を保存</button>
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
let title=box.querySelector('h1')?.textContent.trim()||doc.title;
let paragraphs=[...box.querySelectorAll('p')].map(e=>e.textContent.replace(/\s+/g,' ').trim()).filter(t=>t.length>20&&!/^English version|^日本語版/.test(t));
let images=[...box.querySelectorAll('img')].map(e=>{try{let src=e.getAttribute('src');if(!src||src.startsWith('data:'))return null;let u=new URL(src,url);return u.origin===location.origin?{src:u.href,alt:e.alt||'記事の画像'}:null}catch{return null}}).filter(Boolean);
images=images.filter((e,i)=>images.findIndex(x=>x.src===e.src)===i);return {url,title,summary:paragraphs.slice(0,2).join('\n'),images}}
function postText(a){let prefix=a.title+'\n\n',tail='\n\n'+a.url,body=a.summary;
while(Array.from(prefix+body+tail).length>245&&body.length)body=body.slice(0,-1);
if(body.length<a.summary.length)body=body.replace(/[、。\s]+$/,'')+'…';return prefix+(body?body+tail:a.url)}
function selected(){return document.querySelector('#xp input[name="xp-image"]:checked')?.value||null}
function state(){return $('state').textContent=posted.has(current.url)?'投稿済み':'未投稿'}
function show(a){current=a;$('post').hidden=false;$('title').textContent=a.title;$('link').textContent=a.url;$('link').href=a.url;$('text').value=postText(a);count();
$('images').replaceChildren();if(!a.images.length)$('images').textContent='この記事には画像がありません。';
a.images.forEach((im,i)=>{let label=document.createElement('label');label.className='xp-img';let radio=document.createElement('input');radio.type='radio';radio.name='xp-image';radio.value=im.src;radio.checked=i===0;
let span=document.createElement('span');span.textContent=' 画像 '+(i+1)+'：'+im.alt;let img=document.createElement('img');img.src=im.src;img.alt=im.alt;img.loading='lazy';label.append(radio,span,img);$('images').append(label)});
for(let id of ['image-copy','image-save','images-save'])$(id).disabled=!a.images.length;state()}
async function next(){let pool=pages.filter(x=>$('repeat').checked||!posted.has(x));if(!pool.length){say('未投稿の記事がありません。投稿済みも抽選を選択してください。');return}
$('next').disabled=true;say('記事を読み込み中…');try{for(let tries=0;tries<Math.min(pool.length,8);tries++){
let i=Math.floor(Math.random()*pool.length),url=pool.splice(i,1)[0];if(url===current?.url&&pool.length)continue;
try{show(await loadArticle(url));say('投稿候補を表示しました。');return}catch(err){console.warn(err)}}throw Error('記事の読み込みに失敗しました')}
catch(err){say(err.message)}finally{$('next').disabled=false}}
async function png(src){let r=await fetch(src);if(!r.ok)throw Error('画像を取得できません');let bitmap=await createImageBitmap(await r.blob());try{let canvas=document.createElement('canvas');canvas.width=bitmap.width;canvas.height=bitmap.height;canvas.getContext('2d').drawImage(bitmap,0,0);return await new Promise((ok,no)=>canvas.toBlob(b=>b?ok(b):no(Error('PNG変換に失敗')),'image/png'))}finally{bitmap.close()}}
async function save(src,index){let r=await fetch(src);if(!r.ok)throw Error('画像を取得できません');let blob=await r.blob();let ext=blob.type==='image/png'?'png':blob.type==='image/webp'?'webp':blob.type==='image/gif'?'gif':'jpg';
let objectUrl=URL.createObjectURL(blob),a=document.createElement('a');a.href=objectUrl;a.download='sekigahara-'+(current.url.split('/').filter(Boolean).pop()||'post')+'-'+index+'.'+ext;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(objectUrl),10000)}
async function run(fn){try{await fn()}catch(e){say('失敗：'+e.message+'。画像保存や本文コピーをお試しください。')}}
$('next').onclick=next;$('text').oninput=count;
$('text-copy').onclick=()=>run(async()=>{await navigator.clipboard.writeText($('text').value);say('本文をコピーしました。')});
$('image-copy').onclick=()=>run(async()=>{let src=selected();if(!src)throw Error('画像がありません');let item=new ClipboardItem({'image/png':png(src)});await navigator.clipboard.write([item]);say('画像をコピーしました。')});
$('both').onclick=()=>run(async()=>{let src=selected();if(!src){await navigator.clipboard.writeText($('text').value);say('画像がないため本文のみコピーしました。');return}
let item=new ClipboardItem({'text/plain':new Blob([$('text').value],{type:'text/plain'}),'image/png':png(src)});await navigator.clipboard.write([item]);say('本文＋画像を一括コピーしました。Xの投稿欄で両方が貼り付いたか確認してください。')});
$('image-save').onclick=()=>run(async()=>{let src=selected();if(!src)throw Error('画像がありません');await save(src,1);say('画像の保存を開始しました。')});
$('images-save').onclick=()=>run(async()=>{for(let i=0;i<current.images.length;i++)await save(current.images[i].src,i+1);say('全画像の保存を開始しました。複数ダウンロードの許可が必要な場合があります。')});
function mark(yes){if(!current)return;yes?posted.add(current.url):posted.delete(current.url);localStorage.setItem(store,JSON.stringify([...posted]));state();say(yes?'投稿済みにしました。':'未投稿に戻しました。')}
$('done').onclick=()=>mark(true);$('undo').onclick=()=>mark(false);
loadList().then(list=>{pages=list;if(!list.length)throw Error('対象の記事がありません');next()}).catch(e=>say('記事一覧の取得に失敗：'+e.message));
})();
</script>
