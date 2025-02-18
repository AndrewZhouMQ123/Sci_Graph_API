import matplotlib
matplotlib.use('Agg') # Force non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import scipy
from typing import Optional

def scatter(data: np.ndarray, headers: list[str], size: Optional[str]):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, marker='o')
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Scatter Plot of {headers[0]} vs {headers[1]}")
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def errbar1x(data: np.ndarray, headers: list[str], size: Optional[str]):
  x, y, error = data[0], data[1], data[2]
  if len(x) != len(y) or len(x) != len(error):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.errorbar(x, y, xerr=error, marker='o')
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Errorbar Plot of {headers[0]} vs {headers[1]}")
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def errbar1y(data: np.ndarray, headers: list[str], size: Optional[str]):
  x, y, error = data[0], data[1], data[2]
  if len(x) != len(y) or len(x) != len(error):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.errorbar(x, y, yerr=error, marker='o')
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Errorbar Plot of {headers[0]} vs {headers[1]}")
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def errbar2xy(data: np.ndarray, headers: list[str], size: Optional[str]):
  x, y, error_x, error_y = data[0], data[1], data[2], data[3]
  if len(x) != len(y) or len(x) != len(error_x) or len(x) != len(error_y):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.errorbar(x, y, xerr=error_x, yerr=error_y, marker='o')
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Errorbar Plot of {headers[0]} vs {headers[1]}")
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def eqhist(data: np.ndarray, weights: Optional[np.ndarray], bins: int | list[int], xlabel: str, ylabel: str, size: Optional[str]):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if data.ndim > 1:
    data = data.flatten()
  if weights is not None:
    if len(data) != len(weights):
      raise ValueError("Columns must have the same length")
    ax.hist(data, bins=bins, weights=weights)
  else:
    ax.hist(data, bins=bins)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(f"Histogram of {xlabel} vs {ylabel}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def varyhist(data: np.ndarray, weights: Optional[np.ndarray], xlabel: str, ylabel: str, size: Optional[str]):
  bins, counts = data[0], data[1]
  if len(counts) != len(bins):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if weights is not None:
    if len(counts) != len(weights):
      raise ValueError("Columns must have the same length")
    ax.hist(counts, bins=bins, weights=weights)
  else:
    ax.hist(counts, bins=bins)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(f"Histogram of {xlabel} vs {ylabel}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def bar(data: np.ndarray, headers: list[str], size: Optional[str]):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.bar(x, y)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Bar Graph of {headers[0]} vs {headers[1]}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def pie(data: np.ndarray, categories: list[str], size: Optional[str]):
  percentages = data[0]
  if len(categories) != len(percentages):
    raise ValueError("Columns must be the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.pie(percentages, labels=categories, autopct='%1.1f%%')
  ax.set_title(f"Pie Graph of {np.char.join(',', categories)}")
  ax.legend()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def boxplot(data: np.ndarray, categories: list[str], size: Optional[str], xlabel: str, ylabel: str):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if len(categories) == 1:
    data = data[0]
  ax.boxplot(data, tick_labels=categories)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(f"Box Plot of {np.char.join(',', categories)}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def imshowhmap(data: np.ndarray, headers: list[str], title: str, cmap: str, origin: str, size: Optional[str], useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  im = ax.imshow(data, cmap=cmap, origin=origin)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = data.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
  cbar = fig.colorbar(im, ax=ax)
  cbar.set_label(headers[2])
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf
        
def pmhmap(data: np.ndarray, headers: list[str], title: str, cmap: str, shading: str, size: Optional[str], useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  im = ax.pcolormesh(data, cmap=cmap, shading=shading)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = data.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
  cbar = fig.colorbar(im, ax=ax)
  cbar.set_label(headers[2])
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def pmChmap(data: np.ndarray, coords: np.ndarray, headers: list[str], title: str, cmap: str, shading: str, size: Optional[str], 
  useAnnotation: bool = False
          ):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  x, y = coords[0], coords[1]
  X, Y = np.meshgrid(x, y)
  im = ax.pcolormesh(X, Y, data, cmap=cmap, shading=shading)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = data.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
  cbar = fig.colorbar(im, ax=ax)
  cbar.set_label(headers[2])
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def pmfhmap(X: np.ndarray, Y: np.ndarray, headers: list[str], title: str, cmap: str, 
  shading: str, func: str, size: Optional[str], useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if func:
    try:
      transformation = eval(f"lambda x, y: {func}", {"np": np, "sp": scipy, "__builtins__": __builtins__})
    except Exception as e:
      raise ValueError(f"Error applying function {func}: {e}")
  Z = transformation(X , Y)
  im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading=shading)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = Z.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(X[i, j], Y[i, j], f"{Z[i, j]:.2f}", ha="center", va="center", color="black")
  cbar = fig.colorbar(im, ax=ax)
  cbar.set_label(headers[2])
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def contourmap(X: np.ndarray, Y: np.ndarray, title: str, cmap: str, levels: int | list[int], 
               func: str, size: Optional[str], headers: list[str]):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if func:
    try:
      transformation = eval(f"lambda x, y: {func}", {"np": np, "sp": scipy, "__builtins__": __builtins__})
    except Exception as e:
      raise ValueError(f"Error applying function {func}: {e}")
  Z = transformation(X , Y)
  contour_filled = ax.contourf(X, Y, Z, levels=levels, cmap=cmap)
  contour_lines = ax.contour(X, Y, Z, colors="black", levels=levels)
  ax.clabel(contour_lines, inline=True, fontsize=8)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(title)
  ax.set_xticks(np.linspace(X.min(), X.max(), num=10))
  ax.set_yticks(np.linspace(Y.min(), Y.max(), num=10))
  ax.grid()
  cbar = plt.colorbar(contour_filled)
  cbar.set_label(headers[2])
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf