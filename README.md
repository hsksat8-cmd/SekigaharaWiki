# 関ヶ原IF布陣シミュレータ Wiki

Xアーカイブの `tweets.js` を基礎資料として整理した、MkDocs Material製の公式Wikiです。

## 公開前に必ず変更する項目

### 1. GitHubユーザー名

`mkdocs.yml` の次の2か所を変更してください。

```yaml
site_url: https://hsksat8-cmd.github.io/SekigaharaWiki/
repo_url: https://github.com/hsksat8-cmd/SekigaharaWiki
```

### 2. Cloudflare Web Analyticsトークン

`overrides/main.html` の次の文字列を、Cloudflareで発行されたトークンに置き換えます。

```text
YOUR_CLOUDFLARE_WEB_ANALYTICS_TOKEN
```

トークン設定前に公開する場合は、対象の `<script>` をコメントアウトしてください。

## GitHub Pagesへの公開

1. GitHubで `SekigaharaWiki` リポジトリを作成します。
2. このフォルダー内のファイルをすべてアップロードします。
3. 既定ブランチを `main` にします。
4. GitHubの `Settings → Pages → Build and deployment` で、Sourceを `GitHub Actions` にします。
5. `main` にpushすると自動的にビルド・公開されます。

## PCでの確認

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

ブラウザで `http://127.0.0.1:8000/` を開きます。

## Cloudflare Web Analytics

Cloudflare Dashboardの `Web Analytics` でサイトを追加し、JavaScript Beaconのトークンを取得します。
このWikiでは全ページ共通テンプレートにBeaconを配置しているため、1か所の設定で全記事が解析対象になります。

計測対象の例：

- ページビュー
- 訪問者
- 人気ページ
- 参照元
- 国・地域
- ブラウザ、OS、端末種別

外部リンクにはJavaScriptで `data-outbound` 属性を付けています。Cloudflare標準のWeb Analyticsはページビュー中心なので、リンク単位の詳細イベントが必要になった場合は、別のイベント計測サービスを追加してください。

## 内容上の注意

一部のX投稿は、アーカイブ上でも本文末尾が `…` で省略されています。そのため、Wikiでは確認できた範囲のみを記載し、推測で補完していません。

## 英語版

日本語版のURLは変更しません。

- 日本語: `https://hsksat8-cmd.github.io/SekigaharaWiki/`
- English: `https://hsksat8-cmd.github.io/SekigaharaWiki/en/`

Cloudflare Web Analyticsは既存の同じトークンで両言語を計測できます。ダッシュボードでURLパス `/en/` を指定すると英語版だけに絞れます。
