関ヶ原IF布陣シミュレータ Wiki：大谷吉勝・木下頼継の表示レイアウト修正

対象：次の4つのMarkdownファイルのみ（日本語版・英語版）。
- docs/commanders/western/otani-yoshikatsu.md
- docs/commanders/western/kinoshita-yoritsugu.md
- docs/en/commanders/western/otani-yoshikatsu.md
- docs/en/commanders/western/kinoshita-yoritsugu.md

変更点：既存武将と同じ「肖像画／旗印／能力値表」の3列グリッドを使うように、
commander-data-layout has-portrait クラスと figure.commander-portrait を採用。
既存CSS（docs/assets/stylesheets/commander-portraits.css）をそのまま利用します。
能力値、紹介文、画像参照先は変更していません。

アップロード：ZIPを解凍し、4ファイルをGitHubの同じパスに上書きするだけ。
画像やCSSファイルの追加・変更は不要です。
注意：ページ本文幅640px以下では、既存CSSの仕様により表は画像の下に配置されます。
