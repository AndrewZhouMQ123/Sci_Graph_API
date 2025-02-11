from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import json
from io import StringIO
import pandas as pd
import plot as pltpdf
from helper import normalize_data, handle_missing_values, load_data
from typing import List

plot_router = APIRouter(prefix="/plot")

@plot_router.get("/line")
def generate_line_plot(params: str = Form(...)) -> StreamingResponse:
    data = json.loads(params)
    a = data["a"]
    b = data["b"]
    domain = data["domain"]
    yrange = data["yrange"]
    num = data["num"]
    pdf_buffer =  pltpdf.line(a, b, domain, yrange, num)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=line.pdf"})

@plot_router.get("/quadratic")
def generate_quadratic_plot(params: str = Form(...)) -> StreamingResponse:
    data = json.loads(params)
    a = data["a"]
    b = data["b"]
    c = data["c"]
    domain = data["domain"]
    yrange = data["yrange"]
    num = data["num"]
    pdf_buffer = pltpdf.quadratic(a, b, c, domain, yrange, num)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=quadratic.pdf"})

@plot_router.get("/scatter")
async def generate_scatter_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    if df is None or len(headers) < 2:
        return {"error": "Incorrect data format"}
    pdf_buffer = pltpdf.scatter(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=scatter.pdf"})

@plot_router.get("/errorbar1x")
async def generate_errorbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    if df is None or len(headers) < 2:
        return {"error": "Incorrect data format"}
    pdf_buffer = pltpdf.errorbar1x(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errorbar1x.pdf"})

@plot_router.get("/errorbar1y")
async def generate_errorbar1x_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    if df is None or len(headers) < 2:
        return {"error": "Incorrect data format"}
    pdf_buffer = pltpdf.errorbar1y(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errorbar1y.pdf"})

@plot_router.get("/errorbar2xy")
async def generate_errorbar2xy_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    if df is None or len(headers) < 2:
        return {"error": "Incorrect data format"}
    pdf_buffer = pltpdf.errorbar2xy(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=errorbar2xy.pdf"})

@plot_router.get("/eqhistogram")
async def generate_eqhistogram_plot(
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
    pdf_buffer = pltpdf.eqhistogram(data, bins, xlabel, ylabel, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=eqhistogram.pdf"})

@plot_router.get("/varyhistogram")
async def generate_varyhistogram_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    pdf_buffer = pltpdf.varyhistogram(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=varyhistogram.pdf"})

@plot_router.get("/bar")
async def generate_bar_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    pdf_buffer = pltpdf.bar(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=bar.pdf"})

@plot_router.get("/pie")
async def generate_pie_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    pdf_buffer = pltpdf.pie(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pie.pdf"})

@plot_router.get("/boxplot")
async def generate_boxplot_plot(file: UploadFile = File(...), size: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    string_io = StringIO(contents.decode("utf-8"))
    df = pd.read_csv(string_io)
    headers = df.columns.tolist()
    pdf_buffer = pltpdf.boxplot(df, headers, size)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=boxplot.pdf"})

@plot_router.get("/imshowhmap")
async def generate_imshowhmap_plot(file: UploadFile = File(...), params: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    file_ext = file.filename.split(".")[-1].lower()
    data = load_data(file_ext, contents)

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

    data = normalize_data(data, method=normalization)
    data = handle_missing_values(data, strategy=missing_values)
    pdf_buffer = pltpdf.imshowhmap(data, title, cmap, origin, size, xlabel, ylabel, useAnnotation)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=imshowhmap.pdf"})

@plot_router.get("/pmeshhmap")
async def generate_pmeshhmap_plot(file: UploadFile = File(...), params: str = Form(...)) -> StreamingResponse:
    contents = await file.read()
    file_ext = file.filename.split(".")[-1].lower()
    data = load_data(file_ext, contents)

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

    data = normalize_data(data, method=normalization)
    data = handle_missing_values(data, strategy=missing_values)
    pdf_buffer = pltpdf.pmeshhmap(data, title, cmap, shading, size, xlabel, ylabel, useAnnotation)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmhmap.pdf"})

@plot_router.get("/pmeshfunchmap")
async def generate_pmeshfunchmap_plot(files: List[UploadFile] = File(...), params: str = Form(...)) -> StreamingResponse:
    if len(files) != 2:
        raise ValueError("Two files required: one for X and one for Y.")
    contents_X = await files[0].read()
    contents_Y = await files[1].read()
    file_extX = files[0].filename.split(".")[-1].lower()
    file_extY = files[1].filename.split(".")[-1].lower()
    X = load_data(file_extX, contents_X)
    Y = load_data(file_extY, contents_Y)

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

    X = normalize_data(X, method=normalization)
    X = handle_missing_values(X, strategy=missing_values)
    Y = normalize_data(Y, method=normalization)
    Y = handle_missing_values(Y, strategy=missing_values)
    pdf_buffer = pltpdf.pmeshfunchmap(X, Y, title, cmap, shading, func, size, xlabel, ylabel, useAnnotation)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=pmfhmap.pdf"})

@plot_router.get("/contour")
async def generate_contour_plot(files: List[UploadFile] = File(...), params: str = Form(...)) -> StreamingResponse:
    if len(files) != 2:
        raise ValueError("Two files required: one for X and one for Y.")
    contents_X = await files[0].read()
    contents_Y = await files[1].read()
    file_extX = files[0].filename.split(".")[-1].lower()
    file_extY = files[1].filename.split(".")[-1].lower()
    X = load_data(file_extX, contents_X)
    Y = load_data(file_extY, contents_Y)

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
    X = normalize_data(X, method=normalization)
    X = handle_missing_values(X, strategy=missing_values)
    Y = normalize_data(Y, method=normalization)
    Y = handle_missing_values(Y, strategy=missing_values)
    pdf_buffer = pltpdf.contourmap(X, Y, title, cmap, levels, func, size, xlabel, ylabel, zlabel)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=contour.pdf"})