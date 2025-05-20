# Node.js環境ベース
FROM node:18

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY package.json package-lock.json ./

# 依存関係インストール
RUN npm install
RUN npm install next react react-dom

# アプリケーションコードをコピー
COPY . .

# 開発サーバー起動
EXPOSE 3000
CMD ["npm", "run", "dev"]