from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import json
from io import StringIO
import pandas as pd
import plot as pltpdf
import helper
from typing import List

plot_router = APIRouter(prefix="/plot")

@plot_router.post("/line")
def generate_line_plot(params: str = Form(...)) -> StreamingResponse:
  data = json.loads(params)
  a = data["a"]
  b = data["b"]
  domain = data["domain"]
  range = data["range"]
  num = data["num"]
  pdf_buffer =  pltpdf.line(a, b, domain, range, num)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=line.pdf"})

@plot_router.post("/quadratic")
def generate_quadratic_plot(params: str = Form(...)) -> StreamingResponse:
  data = json.loads(params)
  a = data["a"]
  b = data["b"]
  c = data["c"]
  domain = data["domain"]
  range = data["range"]
  num = data["num"]
  pdf_buffer = pltpdf.quadratic(a, b, c, domain, range, num)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=quadratic.pdf"})

@plot_router.post("/scatter")
async def generate_scatter_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = pltpdf.scatter(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=scatter.pdf"})

@plot_router.post("/errbar1x")
async def generate_errbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
      return {"error": "Incorrect data format"}
  pdf_buffer = pltpdf.errbar1x(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar1x.pdf"})

@plot_router.post("/errbar1y")
async def generate_errbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
      return {"error": "Incorrect data format"}
  pdf_buffer = pltpdf.errbar1y(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar1y.pdf"})

@plot_router.post("/errbar2xy")
async def generate_errbar2xy_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = pltpdf.errbar2xy(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar2xy.pdf"})

@plot_router.post("/eqhist")
async def generate_eqhist_plot(
  file: UploadFile = File(...), 
  bins: int = Form(...),
  xlabel: str = Form(...),
  ylabel: str = Form(...),
  size: str = Form(...)
  ) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  data = df[headers[0]].to_numpy(dtype=float)
  pdf_buffer = pltpdf.eqhist(data, bins, xlabel, ylabel, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=eqhist.pdf"})

@plot_router.post("/varyhist")
async def generate_varyhist_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  pdf_buffer = pltpdf.varyhist(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=varyhist.pdf"})

@plot_router.post("/bar")
async def generate_bar_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  pdf_buffer = pltpdf.bar(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=bar.pdf"})

@plot_router.post("/pie")
async def generate_pie_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  pdf_buffer = pltpdf.pie(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pie.pdf"})

@plot_router.post("/boxplot")
async def generate_boxplot_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  pdf_buffer = pltpdf.boxplot(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=boxplot.pdf"})

@plot_router.post("/imshowhmap")
async def generate_imshowhmap_plot(file: UploadFile = File(...), params: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data = helper.load_data(file_ext, contents)

  values = json.loads(params)
  normalization = values["normalization"]
  missing_values = values["missing_values"]
  title = values["title"]
  cmap = values["cmap"]
  origin = values["origin"]
  size = values["size"]
  xlabel = values["x"]
  ylabel = values["y"]
  useAnnotation = values["useAnnotation"]

  data = helper.normalize_data(data, method=normalization)
  data = helper.handle_missing_values(data, strategy=missing_values)
  pdf_buffer = pltpdf.imshowhmap(data, title, cmap, origin, size, xlabel, ylabel, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=imshowhmap.pdf"})

@plot_router.post("/pmeshhmap")
async def generate_pmeshhmap_plot(file: UploadFile = File(...), params: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data = helper.load_data(file_ext, contents)

  values = json.loads(params)
  normalization = values["normalization"]
  missing_values = values["missing_values"]
  title = values["title"]
  cmap = values["cmap"]
  shading = values["shading"]
  size = values["size"]
  xlabel = values["x"]
  ylabel = values["y"]
  useAnnotation = values["useAnnotation"]

  data = helper.normalize_data(data, method=normalization)
  data = helper.handle_missing_values(data, strategy=missing_values)
  pdf_buffer = pltpdf.pmeshhmap(data, title, cmap, shading, size, xlabel, ylabel, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmhmap.pdf"})

@plot_router.post("/pmeshfunchmap")
async def generate_pmeshfunchmap_plot(files: List[UploadFile] = File(...), params: str = Form(...)) -> StreamingResponse:
  if len(files) != 2:
    raise ValueError("Two files required: one for X and one for Y.")
  contents_X = await files[0].read()
  contents_Y = await files[1].read()
  file_extX = files[0].filename.split(".")[-1].lower()
  file_extY = files[1].filename.split(".")[-1].lower()
  X = helper.load_data(file_extX, contents_X)
  Y = helper.load_data(file_extY, contents_Y)

  values = json.loads(params)
  normalization = values["normalization"]
  missing_values = values["missing_values"]
  title = values["title"]
  cmap = values["cmap"]
  func = values["func"]
  shading = values["shading"]
  size = values["size"]
  xlabel = values["x"]
  ylabel = values["y"]
  useAnnotation = values["useAnnotation"]

  X = helper.normalize_data(X, method=normalization)
  X = helper.handle_missing_values(X, strategy=missing_values)
  Y = helper.normalize_data(Y, method=normalization)
  Y = helper.handle_missing_values(Y, strategy=missing_values)
  pdf_buffer = pltpdf.pmeshfunchmap(X, Y, title, cmap, shading, func, size, xlabel, ylabel, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmfhmap.pdf"})

@plot_router.post("/contour")
async def generate_contour_plot(files: List[UploadFile] = File(...), params: str = Form(...)) -> StreamingResponse:
  if len(files) != 2:
    raise ValueError("Two files required: one for X and one for Y.")
  contents_X = await files[0].read()
  contents_Y = await files[1].read()
  file_extX = files[0].filename.split(".")[-1].lower()
  file_extY = files[1].filename.split(".")[-1].lower()
  X = helper.load_data(file_extX, contents_X)
  Y = helper.load_data(file_extY, contents_Y)

  values = json.loads(params)
  title = values["title"]
  cmap = values["cmap"]
  levels = values["levels"]
  func = values["func"]
  size = values["size"]
  xlabel = values["x"]
  ylabel = values["y"]
  zlabel = values["z"]
  normalization = values["normalization"]
  missing_values = values["missing_values"]
  X = helper.normalize_data(X, method=normalization)
  X = helper.handle_missing_values(X, strategy=missing_values)
  Y = helper.normalize_data(Y, method=normalization)
  Y = helper.handle_missing_values(Y, strategy=missing_values)
  pdf_buffer = pltpdf.contourmap(X, Y, title, cmap, levels, func, size, xlabel, ylabel, zlabel)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=contour.pdf"})