# あおいの本棚 公開手順

このzipの中身は検証済みの完成品です。コードの修正は不要です。
中身: index.html / style.css / books.json / covers/（表紙27枚）/ build.py（更新用）/ このファイル

## 公開方法A（推奨・Codex不要・個人情報リスクなし）
1. ブラウザで github.com にログインし、リポジトリ aoi-books を開く（なければ New repository で作成、Public）
2. 「Add file →Upload files」で、このzipの中身を全部ドラッグ＆ドロップ（coversフォルダごと）
3. 「Commit changes」を押す
4. Settings → Pages → Branch を main / (root) にして Save
5. 数分後、https://aoi-kurochan.github.io/aoi-books/ で公開されます

## 公開方法B（Codexに任せる場合）
Codexには次の文言だけ渡してください。
「リポジトリの中身をこのフォルダのファイルで丸ごと置き換えてください。コードの修正・生成は一切不要です。commit前に、全ファイルに実名・メールアドレス・ローカルパスが含まれないことをgrepで確認して結果を提示し、git configのuser.name / user.emailの値を提示して、私の承認を待ってからpushしてください。」

## 公開後の確認3点
- 1番目の本『ChatGPTを使って7日でKindle出版！』＝白い表紙
- 画像生成の4冊目『Claude Designの教科書』＝ターコイズの表紙
- 最後の本『本業月収を超えた私の話』＝紫の表紙

## 新刊が出たときの更新手順
1. books.json の books 配列に1冊分を追記（既存の1冊をコピーして書き換えるのが簡単）
2. covers/ に表紙を追加（次の番号.jpg）
3. python3 build.py を実行（index.htmlが再生成され、検証も自動で走る）
4. 変更ファイルをアップロード（方法Aなら該当ファイルを再アップするだけ）
CodexやClaudeに「books.jsonに新刊を1冊追加してbuild.pyを実行して」と頼んでもOKです。
