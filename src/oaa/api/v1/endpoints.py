# backend/src/oaa/api/v1/endpoints.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import shutil
import ast
import re

from ...core import ide_connector
from ...core import project_manager

router = APIRouter()


# 請求模型
class ProjectRequest(BaseModel):
    project_name: str
    source_code: str


# 定義一個安全的根目錄
# 請將這裡的路徑替換為你希望存放專案的實際路徑
SAFE_PROJECT_ROOT = "D:\\Users\\侑成\\PycharmProjects\\coding-butler-projects"
if not os.path.exists(SAFE_PROJECT_ROOT):
    os.makedirs(SAFE_PROJECT_ROOT)


def generate_project(request: ProjectRequest, dependencies: list[str]):
    """
    根據請求和依賴列表生成專案文件。
    專案只會在 SAFE_PROJECT_ROOT 下創建。
    """
    full_path = os.path.join(SAFE_PROJECT_ROOT, request.project_name)

    if os.path.exists(full_path):
        raise HTTPException(status_code=409, detail=f"Project directory '{request.project_name}' already exists.")

    try:
        os.makedirs(full_path)

        main_file_path = os.path.join(full_path, "main.py")
        with open(main_file_path, "w", encoding="utf-8") as f:
            f.write(request.source_code)

        req_file_path = os.path.join(full_path, "requirements.txt")
        with open(req_file_path, "w", encoding="utf-8") as f:
            for dep in dependencies:
                f.write(f"{dep}\n")

        readme_content = f"""
# {request.project_name}

這是一個由「編碼僕人」自動生成的專案。

### 如何運行

1.  確保您已安裝 Python {os.environ.get('PYTHON_VERSION', '3.11')}.
2.  安裝依賴庫：
    ```bash
    pip install -r requirements.txt
    ```
3.  運行主程式：
    ```bash
    python main.py
    ```
"""
        readme_file_path = os.path.join(full_path, "README.md")
        with open(readme_file_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        return full_path

    except Exception as e:
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
        raise HTTPException(status_code=500, detail=f"Failed to generate project: {str(e)}")


# 輔助函數：解析 Python 代碼，提取依賴庫
def extract_dependencies(code: str) -> list[str]:
    dependencies = set()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not alias.name.startswith("os") and not alias.name.startswith("sys"):
                    dependencies.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and not node.module.startswith("os") and not node.module.startswith("sys"):
                dependencies.add(node.module.split('.')[0])
    return sorted(list(dependencies))


# 主要 API 端點
@router.post("/projects")
def create_project(request: ProjectRequest):
    """
    接收代碼並自動生成一個包含依賴的專案。
    """
    try:
        dependencies = extract_dependencies(request.source_code)

        project_path = generate_project(request, dependencies)

        installation_result = project_manager.install_dependencies(project_path)

        ide_connector.open_project_in_pycharm(project_path)

        return {
            "status": "success",
            "message": f"專案 '{request.project_name}' 已成功創建，並已嘗試在 PyCharm 中開啟。",
            "data": {
                "project_name": request.project_name,
                "project_path": project_path,
                "dependencies_found": dependencies,
                "installation_result": installation_result
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")