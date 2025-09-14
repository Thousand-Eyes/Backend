# backend/src/oaa/core/ide_connector.py

import os
import httpx
from fastapi import HTTPException

# 從 .env.example 讀取 PyCharm API URL
PYCHARM_API_URL = os.environ.get("PYCHARM_API_URL", "http://localhost:63342")

def open_project_in_pycharm(project_path: str):
    """
    使用 PyCharm 的 REST API 自動打開指定路徑的專案。
    """
    endpoint = f"{PYCHARM_API_URL}/api/vcs/checkout"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "url": project_path,
        "parentDirectory": os.path.dirname(project_path),
        "name": os.path.basename(project_path)
    }

    try:
        # 使用 httpx 進行非同步 POST 請求
        response = httpx.post(endpoint, headers=headers, json=data, timeout=10)
        response.raise_for_status() # 如果請求失敗，拋出異常
        return {"status": "success", "message": "Successfully sent request to PyCharm."}
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"與 PyCharm API 通訊失敗。請檢查 PyCharm 是否已開啟並啟用 API 存取權限。錯誤: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"PyCharm API 服務器返回錯誤：{e.response.text}"
        )