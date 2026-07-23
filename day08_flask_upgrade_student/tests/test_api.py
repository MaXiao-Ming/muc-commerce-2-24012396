"""第8天 Flask API 测试"""

import pytest
from app import app


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-key"
    with app.test_client() as client:
        # 先登录
        client.post("/login", data={
            "username": "student",
            "password": "day07"
        })
        yield client


def test_health_endpoint():
    """测试 /health 接口（不需要登录）"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["ok"] is True
        assert data["service"] == "day08-flask-upgrade"


def test_metrics_api_requires_login():
    """测试未登录时 /api/metrics 被拦截"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/api/metrics")
        assert response.status_code == 302  # 重定向到登录页


def test_metrics_api_returns_json(client):
    """测试登录后 /api/metrics 返回正确JSON"""
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert "metrics" in data
    assert len(data["metrics"]) == 4


def test_categories_api_with_filter(client):
    """测试 /api/categories 带筛选参数"""
    response = client.get("/api/categories?category=Fashion")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "Fashion"
    assert "rows" in data


def test_categories_api_all(client):
    """测试 /api/categories 不带参数（返回全部）"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "全部"
    assert len(data["rows"]) == 5  # 5个品类


def test_400_error_handler(client):
    """测试400错误处理返回JSON"""
    response = client.post("/api/ask", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["ok"] is False
    assert "answer" in data
    assert "请输入" in data["answer"] or "问题" in data["answer"]


def test_ask_api_returns_answer(client):
    """测试 /api/ask 返回问答结果"""
    response = client.post("/api/ask", json={
        "question": "系统中一共有多少用户？"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert "answer" in data
    assert "5630" in data["answer"] or "5,630" in data["answer"]