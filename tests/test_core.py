# backend/tests/test_core.py

import pytest
from oaa.api.v1.endpoints import extract_dependencies
from oaa.core.project_manager import generate_project
import os
import shutil
import os
import shutil


# 測試 extract_dependencies 函數
def test_extract_dependencies_basic():
    """測試從基本程式碼中提取依賴。"""
    code = """
import os
import requests
import sys
from fastapi import FastAPI
"""
    dependencies = extract_dependencies(code)
    assert "requests" in dependencies
    assert "fastapi" in dependencies
    assert "os" not in dependencies  # 確保忽略內建庫
    assert "sys" not in dependencies
    assert len(dependencies) == 2


def test_extract_dependencies_from():
    """測試 from ... import ... 語法。"""
    code = """
from pydantic import BaseModel
from sqlalchemy.orm import Session
"""
    dependencies = extract_dependencies(code)
    assert "pydantic" in dependencies
    assert "sqlalchemy" in dependencies
    assert len(dependencies) == 2


def test_extract_dependencies_no_imports():
    """測試不包含任何 import 語句的程式碼。"""
    code = """
def hello_world():
    print("Hello, world!")
"""
    dependencies = extract_dependencies(code)
    assert len(dependencies) == 0


# 測試 generate_project 函數
@pytest.fixture(scope="function")
def temp_project_dir(tmp_path):
    """pytest 內建的 fixture，用於創建臨時目錄。"""
    return tmp_path


def test_generate_project_success(temp_project_dir):
    """測試成功生成專案。"""
    from oaa.core.project_manager import ProjectRequest

    project_name = "test_project_success"
    project_path = str(temp_project_dir)
    source_code = "import requests\nprint('Hello')"
    dependencies = ["requests"]

    request = ProjectRequest(project_name=project_name, project_path=project_path, source_code=source_code)

    full_path = generate_project(request, dependencies)

    assert os.path.isdir(full_path)
    assert os.path.exists(os.path.join(full_path, "main.py"))
    assert os.path.exists(os.path.join(full_path, "requirements.txt"))
    assert os.path.exists(os.path.join(full_path, "README.md"))

    with open(os.path.join(full_path, "requirements.txt"), "r") as f:
        content = f.read()
        assert "requests\n" in content


def test_generate_project_exists(temp_project_dir):
    """測試當專案目錄已存在時是否拋出異常。"""
    from oaa.core.project_manager import ProjectRequest
    from fastapi import HTTPException

    project_name = "existing_project"
    project_path = str(temp_project_dir)
    os.makedirs(os.path.join(project_path, project_name))

    request = ProjectRequest(project_name=project_name, project_path=project_path, source_code="...")

    with pytest.raises(HTTPException):
        generate_project(request, [])