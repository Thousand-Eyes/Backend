# backend/src/oaa/core/project_manager.py

import os
import shutil
import subprocess
from fastapi import HTTPException
from pydantic import BaseModel


def install_dependencies(project_path: str):
    """
    在指定的專案路徑下執行 'pip install -r requirements.txt'。
    """
    requirements_path = os.path.join(project_path, "requirements.txt")
    if not os.path.exists(requirements_path):
        return {"message": "requirements.txt file not found. Skipping installation."}

    try:
        result = subprocess.run(
            ["pip", "install", "-r", requirements_path],
            check=True,
            capture_output=True,
            text=True,
            cwd=project_path,
            shell=True
        )
        return {"status": "success", "message": "Dependencies installed successfully."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to install dependencies. Error: {e.stderr}"
        )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An unexpected error occurred during dependency installation: {str(e)}")