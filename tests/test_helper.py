import numpy as np
import pytest
from helper import normalize_data, handle_missing_values, load_data
import io
import h5py
import json
import os

def test_normalize_data_minmax():
  data = np.array([[1, 2], [3, 4]])
  normalized = normalize_data(data, method="minmax")
  expected = np.array([[0., (2 - 1) / (4 - 1 + 1e-8)], [(3 - 1) / (4 - 1 + 1e-8), 1.]])
  assert np.allclose(normalized, expected)

def test_normalize_data_zscore():
  data = np.array([[1, 2], [3, 4]])
  normalized = normalize_data(data, method="zscore")
  mean, std = np.nanmean(data), np.nanstd(data)
  expected = (data - mean) / (std + 1e-8)
  assert np.allclose(normalized, expected)

def test_normalize_data_constant_array():
  data = np.array([[1, 1], [1, 1]])
  normalized = normalize_data(data, method="minmax")
  assert np.allclose(normalized, np.zeros_like(data))

def test_handle_missing_values_mean():
  data = np.array([[1, np.nan], [3, 4]])
  filled = handle_missing_values(data, strategy="mean")
  expected = np.array([[1., 8/3], [3., 4.]])
  assert np.allclose(filled, expected)

def test_handle_missing_values_median():
  data = np.array([[1, np.nan], [3, 4]])
  filled = handle_missing_values(data, strategy="median")
  expected = np.array([[1., 3.], [3., 4.]])
  assert np.allclose(filled, expected)

def test_handle_missing_values_no_nans():
  data = np.array([[1, 2], [3, 4]])
  filled = handle_missing_values(data, strategy="mean")
  assert np.allclose(filled, data)

def test_handle_missing_values_all_nans():
  data = np.array([[np.nan, np.nan], [np.nan, np.nan]])
  filled = handle_missing_values(data, strategy="")
  assert np.allclose(filled, np.zeros_like(data))

def test_load_data_csv():
  csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
  with open(csv_path, "rb") as csv_file:
    contents = csv_file.read()
    data, headers = load_data("csv", contents)
  expected = np.array([[1, 2, 3], [2, 3, 4]])
  assert headers == ["x", "y"]
  assert np.allclose(data, expected)

def test_load_data_npy():
  npy_contents = io.BytesIO()
  np.save(npy_contents, np.array([[1, 2], [3, 4]]))
  npy_contents.seek(0)
  data, headers = load_data("npy", npy_contents.getvalue())
  expected = np.array([[1, 2], [3, 4]])
  assert headers == ["x", "y"]
  assert np.allclose(data, expected)

def test_load_data_npz():
  npz_contents = io.BytesIO()
  np.savez(npz_contents, arr=np.array([[1, 2], [3, 4]]))
  npz_contents.seek(0)
  data, headers = load_data("npz", npz_contents.getvalue())
  expected = np.array([[1, 2], [3, 4]])
  assert headers == ["x", "y"]
  assert np.allclose(data, expected)

def test_load_data_hdf5():
  hdf5_contents = io.BytesIO()
  with h5py.File(hdf5_contents, "w") as f:
    f.create_dataset("data", data=np.array([[1, 2], [3, 4]]))
  hdf5_contents.seek(0)
  data, headers = load_data("h5", hdf5_contents.getvalue())
  expected = np.array([[1, 2], [3, 4]])
  assert np.allclose(data, expected)

def test_load_data_json():
  json_contents = json.dumps({"x": [1, 2], "y": [3, 4]}).encode("utf-8")
  data, headers = load_data("json", json_contents)
  expected = np.array([[1, 2], [3, 4]])
  assert headers == ["x", "y"]
  assert np.allclose(data, expected)