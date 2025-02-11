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
    pdf_buffer = fit.polyfit(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=polyfit.pdf"})

@fit_router.get("/Lin_least_squares")
async def generate_lin_least_squares_fit(file: UploadFile = File(...)):
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    # Parse CSV into DataFrame
    df = pd.read_csv(string_io)
    return {"fit": "Lin_least_squares"}

@fit_router.get("/NL_least_squares")
async def generate_nl_least_squares_fit(file: UploadFile = File(...)):
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    # Parse CSV into DataFrame
    df = pd.read_csv(string_io)
    return {"fit": "NL_least_squares"}

@fit_router.get("/curve_fit")
async def generate_curve_fit(file: UploadFile = File(...)):
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    # Parse CSV into DataFrame
    df = pd.read_csv(string_io)
    return {"fit": "curve_fit"}