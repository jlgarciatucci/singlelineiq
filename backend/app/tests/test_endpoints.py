from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "SingleLineIQ"


def test_demo_run_endpoint():
    response = client.get("/api/demo/run")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "nodes" in data
    assert "edges" in data
    assert "deterministic_issues" in data
    assert "sld_cross_check_issues" in data
    assert "sld_assets" in data
    assert data["kpis"]["synthetic_disclaimer"] == "All data is synthetic and anonymized."


def test_consumer_list_endpoint():
    response = client.get("/api/consumer-list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_topology_endpoint():
    response = client.get("/api/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert "kpis" in data


def test_load_summary_endpoint():
    response = client.get("/api/load-summary")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_deterministic_issues_endpoint():
    response = client.get("/api/issues/deterministic")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_sld_cross_check_endpoint():
    response = client.get("/api/sld/cross-check")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_sld_pdf_endpoint():
    response = client.get("/api/sld/pdf")
    # Should be 200 since the synthetic pdf file exists
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_report_markdown_endpoint():
    response = client.get("/api/report/markdown")
    assert response.status_code == 200
    text = response.text
    assert "# SingleLineIQ Engineering Review Report" in text


def test_report_issues_csv_endpoint():
    response = client.get("/api/report/issues.csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=singlelineiq_issues.csv" in response.headers["content-disposition"]
