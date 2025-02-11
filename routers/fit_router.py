from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from io import StringIO
import pandas as pd
import fit

fit_router = APIRouter(prefix="/fit")

@fit_router.get("/polyfit")
async def generate_polyfit(file: UploadFile = File(...), poly_degree: int = Form(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
      return {"error": "Incorrect data format"}
  pdf_buffer = fit.polyfit(df, headers, poly_degree, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=polyfit.pdf"})

@fit_router.get("/expfit")
async def generate_expfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = fit.expfit(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=expfit.pdf"})

@fit_router.get("/logfit")
async def generate_logfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = fit.logfit(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=logfit.pdf"})

@fit_router.get("/gaussfit")
async def generate_gaussfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = fit.gaussfit(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=gaussfit.pdf"})

@fit_router.get("/powfit")
async def generate_powfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = fit.powfit(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=powfit.pdf"})

@fit_router.get("/poissonfit")
async def generate_poissonfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  string_io = StringIO(contents.decode("utf-8"))
  df = pd.read_csv(string_io)
  headers = df.columns.tolist()
  if df is None or len(headers) < 2:
    return {"error": "Incorrect data format"}
  pdf_buffer = fit.poissonfit(df, headers, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=poissonfit.pdf"})