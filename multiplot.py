import matplotlib.pyplot as plt
from typing import List
from io import BytesIO

def multi_scatter(datasets: List[dict], title: str, size: str):
  fig_size = (7, 3) if size == "large" else (3.375, 3)
  fig, ax = plt.subplots(figsize=fig_size)
  for dataset in datasets:
    df = dataset.get("data")
    headers = dataset.get("headers", [])
    label = dataset.get("labels", "")
    if df is None or len(headers) < 2:
      continue
    x = df[headers[0]].to_numpy()
    y = df[headers[1]].to_numpy()
    if len(x) != len(y):
      raise ValueError("X and Y lists must be the same length for each dataset")
    ax.scatter(x, y, fmt='o', capsize=5, label=label)
  if datasets and datasets[0].get("headers", []):
    ax.set_xlabel(datasets[0]["headers"][0])
    ax.set_ylabel(datasets[0]["headers"][1])
  ax.set_title(title)
  ax.grid()
  ax.legend()
  fig.tight_layout()
  buf = BytesIO()
  fig.savefig(buf, format="pdf")
  buf.seek(0)
  plt.close(fig)
  return buf