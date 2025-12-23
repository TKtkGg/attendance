# 勤怠管理アプリ (Attendance Portal)

従業員 30 名規模のオフィスを想定した Django 製勤怠管理アプリです。出勤・欠勤・休憩のステータスをワンタッチで記録し、その結果をリアルタイムに可視化できます。ここでは実際に運用する担当者向けに、使い方と主要コードの位置づけをまとめました。

## できること
- **ワンタッチ打刻**: 従業員を選んでボタンを押すだけでステータスとメモを保存。
- **リアルタイム状況把握**: 全従業員の在席/休憩/欠勤をカードと表で一目で確認。
- **履歴の自動蓄積**: 打刻内容はすべて履歴に残り、管理画面や SQL で後から参照可能。
- **管理画面でのマスタ管理**: Django Admin から従業員の登録・更新が行えます。

## セットアップ
1. 依存関係を準備
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install django
   ```
2. 初期化と管理ユーザー作成
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # 既存の管理者がいない場合
   ```
3. サーバ起動とアクセス
   ```bash
   python manage.py runserver
   ```
   - `http://127.0.0.1:8000/` : ワンタッチ打刻画面
   - `http://127.0.0.1:8000/dashboard/` : ステータスダッシュボード
   - `http://127.0.0.1:8000/admin/` : 従業員マスタ管理

## 利用の流れ
1. **従業員を登録**: 管理画面 `/admin/` で `Employee` を追加します（名前・社員コード・部署など）。
2. **打刻する**: 現場担当者はトップページで従業員を選び、出勤/欠勤/休憩入り/休憩終わりボタンを押します。必要に応じてメモ（遅刻理由など）を残します。
3. **状況を監視**: `/dashboard/` で現在の在席状況や最終更新時刻を確認し、応援依頼やシフト調整に活用します。
4. **履歴を確認**: 打刻カード下部に直近 8 件が表示されるほか、管理画面やデータベースから全履歴を追えます。

## 画面ガイド
### ワンタッチ打刻パネル
- [attendance/views.py](attendance/views.py#L10-L45) の `attendance_panel()` と [templates/attendance/panel.html](templates/attendance/panel.html#L1-L125) で構成。従業員選択、任意メモ、4 種のアクションボタンを 1 画面にまとめています。
- ボタンを押すとフォームの隠しフィールド `status` が書き換わり、送信後に最新 8 件の履歴リストへ即反映されます。
- 右カラムには操作ヒントと直近打刻が表示され、状況共有に使えます。

### ステータスダッシュボード
- [attendance/views.py](attendance/views.py#L47-L74) の `status_dashboard()` が社員ごとの現在ステータスを集計し、[templates/attendance/dashboard.html](templates/attendance/dashboard.html#L1-L69) でカード + テーブル表示します。
- カードの数字は TextChoices をもとにリアルタイム集計した人数、テーブルは部署・社員コード・最終打刻時刻を一覧化します。

## 主要コードの読み方
- **ドメインモデル**: [attendance/models.py](attendance/models.py#L5-L44) で `AttendanceStatus`（選択肢）, `Employee`（従業員属性 + 現在ステータス）, `AttendanceRecord`（履歴）を定義。`Employee.current_status` と `AttendanceRecord` を同時に更新することで、一覧表示と履歴保存を両立しています。
- **打刻フォーム**: [attendance/forms.py](attendance/forms.py#L1-L28) の `AttendanceActionForm` が ModelChoiceField で従業員一覧を並び替え取得し、初期ステータスを出勤に設定します。バリデーションやウィジェット属性もここで制御します。
- **ビュー層**: `attendance_panel()` と `status_dashboard()` は [attendance/views.py](attendance/views.py#L10-L74) にまとまっており、フォーム処理・成功メッセージ・集計クエリなどを担当します。`messages` を使って操作者に結果を即フィードバックします。
- **テンプレートタグとバッジ**: ステータスと Bootstrap 色の対応は [attendance/constants.py](attendance/constants.py#L1-L8) に集約し、[attendance/templatetags/attendance_extras.py](attendance/templatetags/attendance_extras.py#L1-L16) の `status_badge` フィルタでテンプレートから呼び出します。新しいステータスを追加するときはこの 2 か所を更新します。
- **スタイル調整**: 共通の上書きやブランドカラーを適用したい場合は [static/css/app.css](static/css/app.css) を編集し、`base.html` から読み込まれているクラスを拡張します。

## データ投入と運用のヒント
- 従業員マスタは CSV インポートや Django Admin のインライン編集を使うと大量登録が楽になります。
- メモ欄は検索対象になるため、外出先・案件名・連絡先などを一言残すよう周知すると後から追跡しやすくなります。
- `AttendanceRecord` の `recorded_at` は自動でサーバ時刻が入るため、端末の時計ズレの影響を受けません。タイムゾーン調整が必要なら `settings.py` で JST 以外を指定してください。

## 今後の拡張例
1. 従業員本人ログインとセルフ打刻（社内 PC 以外からの利用を想定）
2. 休憩時間や稼働時間を自動集計し、CSV / Slack 連携でレポート送信
3. 部署・役職ごとのフィルタリングや検索条件をダッシュボードに追加

---
このリポジトリは社内利用向けの最小構成です。認証やワークフローは自社ルールに合わせてカスタマイズしてください。
