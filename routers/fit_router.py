from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import helper
import fit
from typing import Literal

fit_router = APIRouter(prefix="/fit")

@fit_router.post("/polyfit")
async def generate_polyfit(
  file: UploadFile = File(...), 
  poly_degree: int = Form(..., ge=0), 
  size: Literal["small", "large"] = Form(...)
  ):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.polyfit(data, headers, poly_degree, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=polyfit.pdf"})

@fit_router.post("/expfit")
async def generate_expfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.expfit(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=expfit.pdf"})

@fit_router.post("/logfit")
async def generate_logfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.logfit(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=logfit.pdf"})

@fit_router.post("/gaussfit")
async def generate_gaussfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.gaussfit(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=gaussfit.pdf"})

@fit_router.post("/powfit")
async def generate_powfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.powfit(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=powfit.pdf"})

@fit_router.post("/poissonfit")
async def generate_poissonfit(file: UploadFile = File(...), size: str = Form(...)):
  contents = await file.read()
  file_ext = file.filename.split(".")[-1].lower()
  data, headers = helper.load_data(file_ext, contents)
  if len(headers) < 2 or size is None:
    raise HTTPException(status_code=400, detail="CSV must contain at least 2 columns")
  try:
    pdf_buffer = fit.poissonfit(data, headers, size)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=poissonfit.pdf"})