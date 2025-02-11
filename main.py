from routers.plot_router import plot_router
from routers.fit_router import fit_router
from routers.multiplot_router import multiplot_router

from fastapi import FastAPI

app = FastAPI()
# Register routers
app.include_router(plot_router)
app.include_router(fit_router)
app.include_router(multiplot_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)