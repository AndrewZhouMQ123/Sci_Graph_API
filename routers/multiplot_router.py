from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import List
from multiplot import multi_scatter
import pandas as pd

multiplot_router = APIRouter(prefix="/multiplot")

@multiplot_router.get("/multiscatter")
async def generate_multiscatter_plot(files: List[UploadFile] = File(...), size: str = Form(...), title: str = Form(...)):
  datasets = []
  for file in files:
    df = pd.read_csv(file.file)
    header = df.columns.tolist()
    datasets.append({
        "data": df,
        "headers": header,
        "labels": file.filename
    })
  pdf_buffer = multi_scatter(datasets, title, size)
  return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=multiscatter.pdf"})