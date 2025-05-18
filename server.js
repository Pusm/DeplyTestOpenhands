const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const BRANCH_NAME = 'openhands-dynamic-feature-branch';

app.get('/', (req, res) => {
  const pageHtml = `
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenHands デプロイテスト (Branch: ${BRANCH_NAME} on Heroku)</title>
        <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: linear-gradient(to right, #6dd5ed, #2193b0); color: #fff; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
        .container { text-align: center; padding: 50px; background-color: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); color: #333; }
        h1 { color: #0d47a1; margin-bottom: 0.5em;}
        p { font-size: 1.15em; line-height: 1.6; }
        .branch-info { font-weight: bold; color: #1565c0; }
        .timestamp { margin-top: 30px; padding: 12px; background-color: #e3f2fd; border-left: 6px solid #1e88e5; color: #0d47a1; border-radius: 0 8px 8px 0; }
        </style>
    </head>
    <body>
    <div class="container">
    <h1>こんにちは、OpenHandsです！</h1>
    <p>このページは、<span class="branch-info">${BRANCH_NAME}</span> ブランチからデプロイされた<br>Node.js (Express) アプリケーションによって動的に生成されました。</p>
    <div class="timestamp">
    サーバー時刻 (UTC): ${new Date().toISOString()}<br>
    リクエストされたパス: ${req.path}
    </div>
    </div>
    </body>
    </html>
  `;
  res.send(pageHtml);
});

app.listen(PORT, () => {
  console.log(`Node.js dynamic test server (from branch ${BRANCH_NAME}) is running on port ${PORT}`);
});