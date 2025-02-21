# SCIENTIFIC GRAPH API
- Generates data graphs and best fits plots by calling API endpoints with data files and parameters
- Plots and fits are available as downloadable pdfs (best format for latex)
- Hosted on Heroku, URL: https://sci-graph-api-5df4e4bebbdd.herokuapp.com/
- Web version hosted on Vercel, URL: https://web-goodies.vercel.app/

## General Guidelines
- Acceptable data formats: csv, npy, npz, HDF5, JSON
- First row of csv should be the headers (x labels, y labels etc)
- Size Option: Single Column Plot (3.375 inches * 3 inches), Double Column Plot (7 inches * 3 inches)
- Try to not have duplicate headers, Pandas automatically appends numbers to duplicate colummns, so if that is not what you want, try to have unique column headers

# Plot API

## Scatter Plot
- **Endpoint:** `/plot/scatter`
- **Format:** `x : y`
- **Example Data:**  
  ![data](/public/data.png)

## Errorbar Plot
- **Endpoints:**  
  - `/plot/errorbar1x` → `x : y : error x`
  - `/plot/errorbar1y` → `x : y : error y`
  - `/plot/errorbar2xy` → `x : y : error x : error y`

## Bar Graph
- **Endpoint:** `/plot/bar`
- **Format:**
  - Column 1: Data
  - Column 2: Labels

## Pie Chart
- **Endpoint:** `/plot/pie`
- **Format:**
  - Column 1: Category
  - Column 2: Percentage

## Boxplot
- **Endpoint:** `/plot/boxplot`
- **Format:**
  - Column 1: Category
  - Column 2: Value

## Single Histogram
- **Endpoints:**  
  - `/plot/eqhistogram`
  - `/plot/varyhistogram`
- **Formats:**  
  - Single file → Data → Counts/Frequencies
  - Two files → Data, Weights → Counts/Frequencies : Bins
- **Other Parameters:**  
  - `bins`:  
    - Integer (e.g., `bins=10`): Automatically bins data into evenly spaced intervals.
    - List (e.g., `bins=[1, 2, 5]`): Uses exact numbers for bin spacings.

## Heatmap and Contour Map (CSV Format)
- **Endpoints:**  
  - `/plot/imshowhmap`
  - `/plot/pmeshhmap`
  - `/plot/pmeshfunchmap`
  - `/plot/imshowhmap`
  - `/plot/contour`
- **Data Format:**  
  - Matrices must have a single header value `"m"` to distinguish them from ordinary data.
  - **Example Data:**  
    ![matrix](/public/matrix.png)
- **Normalization:**  
  - `"minmax"` or `"zscore"`
- **Missing Values Handling:**  
  - `"mean"`, `"median"`, or `0`
- **Colormap Selection:**  
  - Choose from: [Matplotlib Colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- **Contour Levels:**  
  - Integer (e.g., `levels=10`): Automatically generates evenly spaced contour levels.
  - List (e.g., `levels=[-1, 0, 1]`): Uses exact numbers as contour levels.

## Best Fit API
###
