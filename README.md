# 勤怠管理アプリ (Attendance Portal)

従業員 30 名規模の会社を想定した Django 製勤怠管理アプリです。打刻(出勤/欠勤/休憩入り/休憩終わり)と管理者向けの状況ダッシュボードを Bootstrap ベースの UI で提供します。

## 機能概要
- **ワンタッチ打刻パネル**: 従業員を選択し、各ステータスボタンで即時記録。任意メモも保存可能。
- **リアルタイムダッシュボード**: 現在の在席/欠勤/休憩状況をカードとテーブルで一覧表示。
- **履歴管理**: 打刻履歴は `AttendanceRecord` に蓄積され、管理画面やリストで確認できます。
- **管理画面**: Django Admin から従業員の登録・編集や履歴確認が可能。

## 技術スタック
- Python 3.13
- Django 6.x
- Bootstrap 5.3 + Bootstrap Icons
- SQLite (デフォルト設定)

## セットアップ手順
1. **仮想環境作成・有効化**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **依存パッケージインストール**
   ```bash
   pip install django
   ```
3. **Django マイグレーション実行**
   ```bash
   python manage.py migrate
   ```
4. **必要に応じて管理ユーザー作成**
   ```bash
   python manage.py createsuperuser
   ```
5. **開発サーバ起動**
   ```bash
   python manage.py runserver
   ```
6. ブラウザで `http://127.0.0.1:8000/` にアクセスすると打刻画面、`/dashboard/` で状況一覧、`/admin/` で管理画面が利用できます。

## 主要ファイル
- `attendance/models.py` : `Employee`, `AttendanceRecord`, `AttendanceStatus` のドメインモデル。
- `attendance/views.py` : 打刻パネルとダッシュボードのビュー。
- `attendance/templates/attendance/*.html` : Bootstrap ベースのフロントエンドテンプレート。
- `attendance/static/css/app.css` : 追加スタイル。
- `attendance/constants.py`, `attendance/templatetags/attendance_extras.py` : ステータスバッジ定義とテンプレートフィルタ。

## データ投入のヒント
- まず Django Admin から従業員を追加すると、打刻フォームで選択可能になります。
- 打刻時のメモは履歴検索のキーとして活用できます。

## 今後の拡張例
1. 従業員本人向けログイン機能を追加し、セルフ打刻を実現。
2. 休憩時間自動集計や CSV エクスポート機能を追加。
3. 部署ごとのフィルタリングや通知連携を実装。

---
社内利用を想定した最小構成です。要件に合わせて認証やワークフローを拡張してください。
