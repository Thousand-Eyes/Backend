# 使用官方 Python 3.11 作為基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有依賴
RUN pip install --no-cache-dir -r requirements.txt

# 將專案原始碼複製到容器中
COPY src/ /app/src/

# 暴露應用程式運行的端口
EXPOSE 8000

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 容器啟動時執行的命令
CMD ["uvicorn", "src.oaa.main:app", "--host", "0.0.0.0", "--port", "8000"]