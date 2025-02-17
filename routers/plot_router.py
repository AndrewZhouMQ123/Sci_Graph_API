from fastapi import APIRouter, File, UploadFile, Form, HTTPException
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
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 2:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.scatter(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=scatter.pdf"})

@plot_router.post("/errbar1x")
async def generate_errbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 3:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.errbar1x(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar1x.pdf"})

@plot_router.post("/errbar1y")
async def generate_errbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 3:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.errbar1y(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar1y.pdf"})

@plot_router.post("/errbar2xy")
async def generate_errbar2xy_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 4:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.errbar2xy(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errbar2xy.pdf"})

@plot_router.post("/eqhist")
async def generate_eqhist_plot(
  files: List[UploadFile] = File(...), 
  bins: int | list[int] = Form(...),
  xlabel: str = Form(...),
  ylabel: str = Form(...),
  size: str = Form(...)
  ) -> StreamingResponse:
  contents_data = await files[0].read()
  file_extdata = files[0].filename.split(".")[-1].lower()
  data, _ = helper.load_data(file_extdata, contents_data)
  weights = None
  if len(files) > 1:
    contents_weights = await files[1].read()
    file_extweights = files[1].filename.split(".")[-1].lower()
    weights, _ = helper.load_data(file_extweights, contents_weights)
  try:
    pdf_buffer = pltpdf.eqhist(data, weights, bins, xlabel, ylabel, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=eqhist.pdf"})

@plot_router.post("/varyhist")
async def generate_varyhist_plot(
  files: List[UploadFile] = File(...),
  xlabel: str = Form(...),
  ylabel: str = Form(...),
  size: str = Form(...)
  ) -> StreamingResponse:
  contents_data = await files[0].read()
  file_extdata = files[0].filename.split(".")[-1].lower()
  data, h1 = helper.load_data(file_extdata, contents_data)
  weights = None
  h2 = None
  if len(files) > 1:
    contents_weights = await files[1].read()
    file_extweights = files[1].filename.split(".")[-1].lower()
    weights, h2 = helper.load_data(file_extweights, contents_weights)
    if len(h2) != 2:
      raise HTTPException(status_code=400, detail="Missing column or data!")
  if h2 is None:
    h2 = []
  if len(h1) != 2:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.varyhist(data, weights, xlabel, ylabel, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=varyhist.pdf"})

@plot_router.post("/bar")
async def generate_bar_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 2:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.bar(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=bar.pdf"})

@plot_router.post("/pie")
async def generate_pie_plot(file: UploadFile = File(...), size: str = Form(...), categories: list[str] = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) != 1:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.pie(data, categories, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pie.pdf"})

@plot_router.post("/boxplot")
async def generate_boxplot_plot(file: UploadFile = File(...), size: str = Form(...), categories: list[str] = Form(...),
  xlabel: str = Form(...), ylabel: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, _ = helper.load_data(file_ext, contents)
  if categories is None or xlabel is None or ylabel is None:
    raise HTTPException(status_code=400, detail="Missing column or data!")
  try:
    pdf_buffer = pltpdf.boxplot(data, categories, size, xlabel, ylabel)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=boxplot.pdf"})

@plot_router.post("/imshowhmap")
async def generate_imshowhmap_plot(file: UploadFile = File(...), title: str = Form(...), cmap: str = Form(...), origin: str = Form(...),
  size: str = Form(...), useAnnotation: bool = Form(...), normalization: str = Form(...), missing_values: str = Form(...),
  xlabel: str = Form(...), ylabel: str = Form(...), zlabel: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, _ = helper.load_data(file_ext, contents)
  data = helper.normalize_data(data, method=normalization)
  data = helper.handle_missing_values(data, strategy=missing_values)
  headers = [xlabel, ylabel, zlabel]
  pdf_buffer = pltpdf.imshowhmap(data, headers, title, cmap, origin, size, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=imshowhmap.pdf"})

@plot_router.post("/pmhmap")
async def generate_pmhmap_plot(file: UploadFile = File(...), title: str = Form(...), cmap: str = Form(...), shading: str = Form(...),
  size: str = Form(...), useAnnotation: bool = Form(...), normalization: str = Form(...), missing_values: str = Form(...),
  xlabel: str = Form(...), ylabel: str = Form(...), zlabel: str = Form(...)) -> StreamingResponse:
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, _ = helper.load_data(file_ext, contents)
  data = helper.normalize_data(data, method=normalization)
  data = helper.handle_missing_values(data, strategy=missing_values)
  headers = [xlabel, ylabel, zlabel]
  pdf_buffer = pltpdf.pmhmap(data, headers, title, cmap, shading, size, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmhmap.pdf"})

@plot_router.post("/pmChmap")
async def generate_pmChmap_plot(files: List[UploadFile] = File(...), title: str = Form(...), cmap: str = Form(...), shading: str = Form(...),
  size: str = Form(...), useAnnotation: bool = Form(...), normalization: str = Form(...), missing_values: str = Form(...),
  xlabel: str = Form(...), ylabel: str = Form(...), zlabel: str = Form(...)) -> StreamingResponse:
  contents_data = await files[0].read()
  contents_coord = await files[1].read()
  file_extdata = files[0].filename.split(".")[-1].lower()
  file_extcoord = files[1].filename.split(".")[-1].lower()
  data, _ = helper.load_data(file_extdata, contents_data)
  coord, _ = helper.load_data(file_extcoord, contents_coord)
  data = helper.normalize_data(data, method=normalization)
  data = helper.handle_missing_values(data, strategy=missing_values)
  headers = [xlabel, ylabel, zlabel]
  pdf_buffer = pltpdf.pmChmap(data, coord, headers, title, cmap, shading, size, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmChmap.pdf"})

@plot_router.post("/pmfhmap")
async def generate_pmfhmap_plot(files: List[UploadFile] = File(...), title: str = Form(...), cmap: str = Form(...), func: str = Form(...),
  shading: str = Form(...), size: str = Form(...), useAnnotation: bool = Form(...), normalization: str = Form(...), 
  missing_values: str = Form(...), xlabel: str = Form(...), ylabel: str = Form(...), zlabel: str = Form(...)) -> StreamingResponse:
  if len(files) != 2:
    raise ValueError("Missing required files.")
  contents_X = await files[0].read()
  contents_Y = await files[1].read()
  file_extX = files[0].filename.split(".")[-1].lower()
  file_extY = files[1].filename.split(".")[-1].lower()
  X, _ = helper.load_data(file_extX, contents_X)
  Y, _ = helper.load_data(file_extY, contents_Y)
  X = helper.normalize_data(X, method=normalization)
  X = helper.handle_missing_values(X, strategy=missing_values)
  Y = helper.normalize_data(Y, method=normalization)
  Y = helper.handle_missing_values(Y, strategy=missing_values)
  headers = [xlabel, ylabel, zlabel]
  pdf_buffer = pltpdf.pmfhmap(X, Y, headers, title, cmap, shading, func, size, useAnnotation)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmfhmap.pdf"})

@plot_router.post("/contour")
async def generate_contour_plot(files: List[UploadFile] = File(...), title: str = Form(...), cmap: str = Form(...), 
  levels: int | list[int] = Form(...), func: str = Form(...), size: str = Form(...), normalization: str = Form(...),
  missing_values: str = Form(...), xlabel: str = Form(...), ylabel: str = Form(...), zlabel: str = Form(...)) -> StreamingResponse:
  if len(files) != 2:
    raise ValueError("Missing required files.")
  contents_X = await files[0].read()
  contents_Y = await files[1].read()
  file_extX = files[0].filename.split(".")[-1].lower()
  file_extY = files[1].filename.split(".")[-1].lower()
  X, _ = helper.load_data(file_extX, contents_X)
  Y, _ = helper.load_data(file_extY, contents_Y)
  X = helper.normalize_data(X, method=normalization)
  X = helper.handle_missing_values(X, strategy=missing_values)
  Y = helper.normalize_data(Y, method=normalization)
  Y = helper.handle_missing_values(Y, strategy=missing_values)
  headers = [xlabel, ylabel, zlabel]
  pdf_buffer = pltpdf.contourmap(X, Y, title, cmap, levels, func, size, headers)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=contour.pdf"})