import matplotlib
matplotlib.use('Agg')  # Force non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import pandas as pd
import scipy

def line(a: float, b: float, domain: list[float], range: list[float], num: int):
  x = np.linspace(domain[0], domain[1], num)
  fig = plt.figure(1, figsize=(3.375, 3))
  ax = fig.add_subplot(111)
  ax.plot(x, a*x + b)
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.set_title("y = ax + b")
  ax.set_xlim(domain[0], domain[1])
  ax.set_ylim(range[0], range[1])
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf", bbox_inches='tight')
  buf.seek(0)
  plt.close(fig)
  return buf

def quadratic(a: float, b: float, c: float, domain: list[float], range: list[float], num: int):
  x = np.linspace(domain[0], domain[1], num)
  fig = plt.figure(1, figsize=(3.375, 3))
  ax = fig.add_subplot(111)
  ax.plot(x, a*x**2 + b*x + c)
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.set_title("y = ax^2 + bx + c")
  ax.set_xlim(domain[0], domain[1])
  ax.set_ylim(range[0], range[1])
  ax.grid()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def scatter(data: np.ndarray, headers: list[str], size: str):
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

def errbar1x(data: np.ndarray, headers: list[str], size: str):
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

def errbar1y(data: np.ndarray, headers: list[str], size: str):
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

def errbar2xy(data: np.ndarray, headers: list[str], size: str):
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

def eqhist(data: list[int], bins: int, xlabel: str, ylabel: str, size: str):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
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

def varyhist(df: pd.DataFrame, headers: list[str], size: str):
  bins = df[headers[0]].to_numpy()
  counts = df[headers[1]].to_numpy()
  if len(counts) != len(bins):
    raise ValueError("Columns must have the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.hist(counts, bins=bins)
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.set_title(f"Histogram of {headers[0]} vs {headers[1]}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def bar(df: pd.DataFrame, headers: list[str], size: str):
  x = df[headers[0]].to_numpy()
  y = df[headers[1]].to_numpy()
  if len(x) != len(y):
    raise ValueError("X and Y lists must be the same length")
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

def pie(df: pd.DataFrame, headers: list[str], size: str):
  category = df[headers[0]].to_numpy()
  percentages = df[headers[1]].to_numpy()
  if len(category) != len(percentages):
    raise ValueError("Category and percentages lists must be the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.pie(percentages, labels=category, autopct='%1.1f%%')
  ax.set_title(f"Pie Graph of {category.tolist().join(', ')}")
  ax.legend()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def boxplot(df: pd.DataFrame, headers: list[str], size: str):
  category = df[headers[0]].to_numpy()
  value = df[headers[1]].to_numpy()
  if len(category) != len(value):
    raise ValueError("Category and value lists must be the same length")
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.boxplot(value)
  ax.set_xticklabels(category)
  ax.set_xlabel("Categories")
  ax.set_ylabel("Values")
  ax.set_title(f"Box Plot of {headers[1]} by {headers[0]}")
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def imshowhmap(data: np.ndarray, title: str, cmap: str, origin: str, size: str, 
               xlabel: str, ylabel: str, useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  im = ax.imshow(data, cmap=cmap, origin=origin)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = data.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
  fig.colorbar(im, ax=ax)
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf
        
def pmeshhmap(data: np.ndarray, title: str, cmap: str, shading: str, size: str,
              xlabel: str, ylabel: str, useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  im = ax.pcolormesh(data, cmap=cmap, shading=shading)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = data.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
  fig.colorbar(im, ax=ax)
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def pmeshfunchmap(X: np.ndarray, Y: np.ndarray, title: str, cmap: str, shading: str, func: str, size: str,
                  xlabel: str, ylabel: str, useAnnotation: bool = False):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if func:
    try:
      if func.startswith("np."):
        transformation = eval(func, {"np": np})
      else:
        transformation = eval(f"lambda x, y: {func}", {"np": np, "sp": scipy})
    except Exception as e:
      raise ValueError(f"Error applying function {func}: {e}")
  Z = transformation(X , Y)
  im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading=shading)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  if useAnnotation:
    num_rows, num_cols = Z.shape
    for i in range(num_rows):
      for j in range(num_cols):
        ax.text(X[i, j], Y[i, j], f"{Z[i, j]:.2f}", ha="center", va="center", color="black")
  fig.colorbar(im, ax=ax)
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf

def contourmap(X: np.ndarray, Y: np.ndarray, title: str, cmap: str, levels: str, 
               func: str, size: str, xlabel: str, ylabel: str, zlabel: str):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  if func:
    try:
      if func.startswith("np."):
        transformation = eval(func, {"np": np})
      else:
        transformation = eval(f"lambda x, y: {func}", {"np": np, "sp": scipy})
    except Exception as e:
      raise ValueError(f"Error applying function {func}: {e}")
  Z = transformation(X , Y)
  contour_filled = ax.contourf(X, Y, Z, levels=levels, cmap=cmap)
  contour_lines = ax.contour(X, Y, Z, colors="black", levels=levels)
  ax.clabel(contour_lines, inline=True, fontsize=8)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.set_xticks(np.linspace(X.min(), X.max(), num=10))
  ax.set_yticks(np.linspace(Y.min(), Y.max(), num=10))
  ax.grid()
  cbar = plt.colorbar(contour_filled)
  cbar.set_label(zlabel)
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf