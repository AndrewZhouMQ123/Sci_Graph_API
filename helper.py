from fastapi import HTTPException
import numpy as np
import pandas as pd
import io
import json
import h5py

def normalize_data(data: np.ndarray, method: str = "minmax") -> np.ndarray:
  if method == "minmax":
    data_min, data_max = np.nanmin(data), np.nanmax(data)
    return (data - data_min) / (data_max - data_min + 1e-8)
  elif method == "zscore":
    mean, std = np.nanmean(data), np.nanstd(data)
    return (data - mean) / (std + 1e-8)
  return data

def handle_missing_values(data: np.ndarray, strategy: str) -> np.ndarray:
  if np.all(np.isnan(data)):
    return np.zeros_like(data)
  if strategy == "mean":
    fill_value = np.nanmean(data)
  elif strategy == "median":
    fill_value = np.nanmedian(data)
  return np.nan_to_num(data, nan=fill_value)

def load_data(file_ext: str, contents: bytes) -> np.ndarray:
  try:
    if file_ext == "csv":
      string_io = io.StringIO(contents.decode("utf-8"))
      df = pd.read_csv(string_io)
      headers = df.columns.tolist()
      data = df.to_numpy(dtype=float).T
    elif file_ext == "npy":
      buf = io.BytesIO(contents)
      data = np.load(buf)
      headers = ["x", "y"]
    elif file_ext == "npz":
      buf = io.BytesIO(contents)
      npz_data = np.load(buf)
      data = npz_data[npz_data.files[0]]
      headers = ["x", "y"]
    elif file_ext in ["h5", "hdf5"]:
      buf = io.BytesIO(contents)
      with h5py.File(buf, "r") as f:
        first_dataset = list(f.keys())[0]
        data = np.array(f[first_dataset])
        headers = [first_dataset]
    elif file_ext == "json":
      json_data = json.loads(contents.decode("utf-8"))
      headers = list(json_data.keys())
      data = np.array([json_data[key] for key in headers])
    else:
      raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV, NPY, NPZ, or HDF5.")
  except UnicodeDecodeError:
    raise HTTPException(status_code=400, detail="Invalid file encoding (use UTF-8)")
  except pd.errors.EmptyDataError:
    raise HTTPException(status_code=400, detail="Empty CSV file")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")
  return data, headers