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

def test_errbar1x():
  csv_path = os.path.join(os.path.dirname(__file__), "error.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/errbar1x",
      files={"file": ("error.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=errbar1x.pdf" in response.headers["Content-Disposition"]

def test_errbar1y():
  csv_path = os.path.join(os.path.dirname(__file__), "error.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/errbar1y",
      files={"file": ("error.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=errbar1y.pdf" in response.headers["Content-Disposition"]

def test_errbar2xy():
  csv_path = os.path.join(os.path.dirname(__file__), "error2.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/errbar2xy",
      files={"file": ("error2.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=errbar2xy.pdf" in response.headers["Content-Disposition"]

def test_eqhist():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/eqhist",
      files=[("files", ("singlecolumn.csv", csv_file, "text/csv"))],
      data={"bins": 3, "xlabel": "x", "ylabel": "y", "size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=eqhist.pdf" in response.headers["Content-Disposition"]

def test_varyhist():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/varyhist",
      files=[("files", ("data.csv", csv_file, "text/csv"))],
      data={"xlabel": "x", "ylabel": "y", "size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=varyhist.pdf" in response.headers["Content-Disposition"]

def test_bar():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/bar",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=bar.pdf" in response.headers["Content-Disposition"]

def test_pie():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/pie",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small", "categories": ['A', 'B', 'C', 'D', 'E']}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=pie.pdf" in response.headers["Content-Disposition"]

def test_singleboxplot():
  csv_path = os.path.join(os.path.dirname(__file__), "singlecolumn.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/boxplot",
      files={"file": ("singlecolumn.csv", csv_file, "text/csv")},
      data={"size": "small", "categories": ['A'], "xlabel": "x", "ylabel": "y"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=boxplot.pdf" in response.headers["Content-Disposition"]

def test_multiboxplot():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/boxplot",
      files={"file": ("data.csv", csv_file, "text/csv")},
      data={"size": "small", "categories": ['A', 'B', 'C'], "xlabel": "x", "ylabel": "y"}
    )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=boxplot.pdf" in response.headers["Content-Disposition"]

def test_imshowhmap():
  csv_path = os.path.join(os.path.dirname(__file__), "matrix.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/imshowhmap",
      files={"file": ("matrix.csv", csv_file, "text/csv")},
      data={
        "title": "Test", 
        "cmap": "plasma", 
        "origin": "upper", 
        "size": "small",
        "useAnnotation": True,
        "normalization": "zscore",
        "missing_values": "median",
        "xlabel": "x",
        "ylabel": "y",
        "zlabel": "z",
        }
      )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=imshowhmap.pdf" in response.headers["Content-Disposition"]

def test_pmhmap():
  csv_path = os.path.join(os.path.dirname(__file__), "matrix.csv")
  with open(csv_path, "rb") as csv_file:
    response = client.post(
      "/plot/pmhmap",
      files={"file": ("matrix.csv", csv_file, "text/csv")},
      data={
        "title": "Test", 
        "cmap": "plasma", 
        "shading": "auto", 
        "size": "small",
        "useAnnotation": True,
        "normalization": "zscore",
        "missing_values": "median",
        "xlabel": "x",
        "ylabel": "y",
        "zlabel": "z",
        }
      )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=pmhmap.pdf" in response.headers["Content-Disposition"]

def test_pmChmap():
  xpath = os.path.join(os.path.dirname(__file__), "matrix.csv")
  ypath = os.path.join(os.path.dirname(__file__), "coords.csv")
  with open(xpath, "rb") as xfile, open(ypath, "rb") as yfile:
    files = [
      ("files", ("matrix.csv", xfile, "test/csv")),
      ("files", ("coords.csv", yfile, "test/csv"))
      ]
    response = client.post(
      "/plot/pmChmap",
      files=files,
      data={
        "title": "Test", 
        "cmap": "plasma", 
        "shading": "auto",
        "size": "small",
        "useAnnotation": True,
        "normalization": "zscore",
        "missing_values": "median",
        "xlabel": "x",
        "ylabel": "y",
        "zlabel": "z",
        }
      )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=pmChmap.pdf" in response.headers["Content-Disposition"]

def test_pmfhmap():
  xpath = os.path.join(os.path.dirname(__file__), "cornerX.csv")
  ypath = os.path.join(os.path.dirname(__file__), "cornerY.csv")
  with open(xpath, "rb") as xfile, open(ypath, "rb") as yfile:
    files = [
      ("files", ("cornerX.csv", xfile, "test/csv")),
      ("files", ("cornerY.csv", yfile, "test/csv"))
      ]
    response = client.post(
      "/plot/pmfhmap",
      files=files,
      data={
        "title": "Test", 
        "cmap": "plasma", 
        "func": "np.sin(x) + sp.constants.pi - x * y",
        "shading": "auto",
        "size": "small",
        "zlabel": "heat",
        "useAnnotation": True,
        "normalization": "zscore",
        "missing_values": "median",
        "xlabel": "x",
        "ylabel": "y",
        "zlabel": "z",
        }
      )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=pmfhmap.pdf" in response.headers["Content-Disposition"]

def test_contour():
  xpath = os.path.join(os.path.dirname(__file__), "cornerX.csv")
  ypath = os.path.join(os.path.dirname(__file__), "cornerY.csv")
  with open(xpath, "rb") as xfile, open(ypath, "rb") as yfile:
    files = [
      ("files", ("cornerX.csv", xfile, "test/csv")),
      ("files", ("cornerY.csv", yfile, "test/csv"))
      ]
    response = client.post(
      "/plot/contour",
      files=files,
      data={
        "title": "Test", 
        "cmap": "plasma",
        "levels": [2, 3],
        "func": "np.sin(x) + sp.constants.pi - x * y",
        "size": "small",
        "zlabel": "heat",
        "normalization": "zscore",
        "missing_values": "median",
        "xlabel": "x",
        "ylabel": "y",
        "zlabel": "z",
        }
      )
  assert response.status_code == 200
  assert response.headers["content-type"] == "application/pdf"
  assert "inline; filename=contour.pdf" in response.headers["Content-Disposition"]