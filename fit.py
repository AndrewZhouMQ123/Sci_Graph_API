import matplotlib
matplotlib.use('Agg')  # Force non-GUI backend
import numpy as np
from scipy.special import factorial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from io import BytesIO
from scipy.optimize import curve_fit

def polyfit(data: np.ndarray, headers: list[str], poly_degree: int, size: str):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  coeffs, cov = np.polyfit(x, y, poly_degree, cov=True)
  p = np.poly1d(coeffs)
  x_smooth = np.linspace(x.min(), x.max(), 300)
  y_smooth = p(x_smooth)

  y_pred = p(x)
  residuals = y - y_pred
  rss = np.sum(residuals**2)  # Residual Sum of Squares
  tss = np.sum((y - np.mean(y))**2)  # Total Sum of Squares
  r_squared = 1 - (rss / tss)  # R² score
  rmse = np.sqrt(np.mean(residuals**2))  # Root Mean Square Error
  mae = np.mean(np.abs(residuals))  # Mean Absolute Error
  std_err = np.sqrt(np.diag(cov)) if cov is not None else None  # Standard errors

  coeff_str = " + ".join([f"{c:.3g}x^{i}" if i > 0 else f"{c:.3g}" for i, c in enumerate(reversed(coeffs))])
  cov_str = np.array2string(cov, precision=3, suppress_small=True) if cov is not None else "N/A"
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    fig, ax = plt.subplots(figsize=fig_size)
    ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
    ax.plot(x_smooth, y_smooth, label=f"Fit: {coeff_str}", color="red")
    ax.set_xlabel(headers[0])
    ax.set_ylabel(headers[1])
    ax.legend()
    fig.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Polynomial Fit (Degree {poly_degree}):\n"
      f"Equation: {coeff_str}\n\n"
      f"Statistical Summary:\n"
      f"R² = {r_squared:.4f}\n"
      f"RSS = {rss:.4f}\n"
      f"RMSE = {rmse:.4f}\n"
      f"MAE = {mae:.4f}\n"
    )
    if std_err is not None:
      std_err_str = "\n".join([f"Std. Error (x^{i}): {se:.4g}" for i, se in enumerate(reversed(std_err))])
      stats_text += f"\nStandard Errors:\n{std_err_str}\n"
    stats_text += f"\n\nCovariance Matrix:\n{cov_str}"
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center")
    pdf.savefig(fig)
    plt.close(fig)
  
  pdf_buffer.seek(0)
  return pdf_buffer

def exp_model(x, A, B):
  return A * np.exp(B * x)

def sigmoid(x, A, B, C):
  return A / (1 + np.exp(-B * (x - C)))

def gaussian(x, A, mu, sigma):
  return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

def power_law(x, A, B):
  return A * x**B

def expfit(data: np.ndarray, headers: list[str], size: str):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  params, covariance = curve_fit(exp_model, x, y)
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
  ax.plot(x, exp_model(x, *params), label=f"Fit: Y = {params[0]:.3g} * exp({params[1]:.3g} * X)", color="red")
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.legend()
  fig.tight_layout()
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    pdf.savefig(fig)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Exponential Fit (Y = A * exp(B * X)):\n"
      f"Parameters:\n"
      f"A = {params[0]:.3g}, B = {params[1]:.3g}\n\n"
      f"Covariance Matrix:\n{np.array2string(covariance, precision=3, suppress_small=True)}"
    )
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center", family="monospace")
    pdf.savefig(fig)
  pdf_buffer.seek(0)
  return pdf_buffer
    
def logfit(data: np.ndarray, headers: list[str], size: str):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  params, covariance = curve_fit(sigmoid, x, y)
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
  ax.plot(x, sigmoid(x, *params), label=f"Fit: Y = {params[0]:.3g} / (1 + exp(-{params[1]:.3g} * (X - {params[2]:.3g})))", color="red")
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.legend()
  fig.tight_layout()
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    pdf.savefig(fig)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Logistic Fit (Y = A / (1 + exp(-B * (X - C)))):\n"
      f"Parameters:\n"
      f"A = {params[0]:.3g}, B = {params[1]:.3g}, C = {params[2]:.3g}\n\n"
      f"Covariance Matrix:\n{np.array2string(covariance, precision=3, suppress_small=True)}"
    )
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center", family="monospace")
    pdf.savefig(fig)
  pdf_buffer.seek(0)
  return pdf_buffer
    
def gaussfit(data: np.ndarray, headers: list[str], size: str):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  params, covariance = curve_fit(gaussian, x, y)
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
  ax.plot(x, gaussian(x, *params), label=f"Fit: Y = {params[0]:.3g} * exp(-(X - {params[1]:.3g})^2 / (2 * {params[2]:.3g}^2))", color="red")
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.legend()
  fig.tight_layout()
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    pdf.savefig(fig)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Gaussian Fit (Y = A * exp(-(X - mu)^2 / (2 * sigma^2))):\n"
      f"Parameters:\n"
      f"A = {params[0]:.3g}, mu = {params[1]:.3g}, sigma = {params[2]:.3g}\n\n"
      f"Covariance Matrix:\n{np.array2string(covariance, precision=3, suppress_small=True)}"
    )
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center", family="monospace")
    pdf.savefig(fig)
  pdf_buffer.seek(0)
  return pdf_buffer
    
def powfit(data: np.ndarray, headers: list[str], size: str):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  params, covariance = curve_fit(power_law, x, y)
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
  ax.plot(x, power_law(x, *params), label=f"Fit: Y = {params[0]:.3g} * X^{params[1]:.3g}", color="red")
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.legend()
  fig.tight_layout()
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    pdf.savefig(fig)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Power Law Fit (Y = A * X^B):\n"
      f"Parameters:\n"
      f"A = {params[0]:.3g}, B = {params[1]:.3g}\n\n"
      f"Covariance Matrix:\n{np.array2string(covariance, precision=3, suppress_small=True)}"
    )
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center", family="monospace")
    pdf.savefig(fig)
  pdf_buffer.seek(0)
  return pdf_buffer

def poisson_model(x, lambd):
  return (lambd**x * np.exp(-lambd)) / factorial(x)

def poissonfit(data: np.ndarray, headers: list[str], size: str):
  x, y = data[0], data[1]
  if len(x) != len(y):
    raise ValueError("Columns must have the same length")
  try:
    params, covariance = curve_fit(poisson_model, x, y, p0=[np.mean(x)])
  except Exception as e:
    print(f"Error fitting the model: {e}")
    params = [np.nan]
    covariance = np.nan
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  ax.scatter(x, y, label="Data", color="blue", alpha=0.5)
  x_vals = np.arange(0, x.max() + 1)
  ax.plot(x_vals, poisson_model(x_vals, *params), label=f"Fit: λ = {params[0]:.3g}", color="red")
  ax.set_xlabel(headers[0])
  ax.set_ylabel(headers[1])
  ax.legend()
  fig.tight_layout()
  pdf_buffer = BytesIO()
  with PdfPages(pdf_buffer) as pdf:
    pdf.savefig(fig)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    stats_text = (
      f"Poisson Fit (P(x; λ)):\n"
      f"Parameter:\n"
      f"λ = {params[0]:.3g}\n\n"
      f"Covariance Matrix:\n{np.array2string(covariance, precision=3, suppress_small=True)}"
    )
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment="center", family="monospace")
    pdf.savefig(fig)
  pdf_buffer.seek(0)
  return pdf_buffer