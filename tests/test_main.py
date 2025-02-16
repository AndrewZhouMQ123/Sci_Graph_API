import matplotlib
matplotlib.use('Agg')
from fastapi.testclient import TestClient
from main import app
import pytest
import os
import json
from mydb import init_db
from main import app, verify_api_key

app.dependency_overrides[verify_api_key] = lambda: True
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def initialize_test_db():
  init_db()

def test_read_main():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"msg": "Hello World"}

def test_line():
  params = {"a": 1, "b": 2, "domain": [0, 4], "range": [0, 4], "num": 4}
  response = client.post("/plot/line", data={"params": json.dumps(params)})
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=line.pdf" in response.headers["Content-Disposition"]

def test_quadratic():
  params = {"a": 1, "b": 2, "c": 3, "domain": [0, 4], "range": [0, 4], "num": 4}
  response = client.post("plot/quadratic", data={"params": json.dumps(params)})
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=quadratic.pdf" in response.headers["Content-Disposition"]

def test_polyfit_data():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/polyfit",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"poly_degree": "1", "size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=polyfit.pdf" in response.headers["Content-Disposition"]

def test_polyfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/polyfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"poly_degree": "1", "size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_expfit():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/expfit",
      files={"file": ("data.csv", csv_file, "test/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=expfit.pdf" in response.headers["Content-Disposition"]

def test_expfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/expfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_logfit():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/logfit",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=logfit.pdf" in response.headers["Content-Disposition"]

def test_logfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/logfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_gaussfit():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/gaussfit",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=gaussfit.pdf" in response.headers["Content-Disposition"]

def test_gaussfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/gaussfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_powfit():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/powfit",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=powfit.pdf" in response.headers["Content-Disposition"]

def test_powfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/powfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_poissonfit():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/poissonfit",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=poissonfit.pdf" in response.headers["Content-Disposition"]

def test_poissonfit_singlecolumn():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/fit/poissonfit",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 400
  assert response.json()["detail"] == "Missing column or data!"

def test_scatter():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/scatter",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=scatter.pdf" in response.headers["Content-Disposition"]