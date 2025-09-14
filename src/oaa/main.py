# backend/src/oaa/main.py

from fastapi import FastAPI
from .api.v1 import endpoints

app = FastAPI(
    title="編碼僕人 - Vibe Coder Helper",
    description="一個幫助使用者快速將 AI 代碼部署到 IDE 的工具。",
    version="0.2.0-feature-code-gen"
)

app.include_router(endpoints.router, prefix="/api/v1")

# 在這裡我們可以添加根路徑的歡迎訊息
@app.get("/")
def read_root():
    return {"message": "歡迎使用 編碼僕人 API！請前往 /docs 查看 API 文件。"}