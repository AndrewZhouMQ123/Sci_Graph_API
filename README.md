# SCIENTIFIC GRAPH API
- generates static plots / charts from given parameters or csv data
- fits csv data from given guess parameters and returns generated plot of best fit with fit parameters
- plots and fits are available as downloadable pdfs (best format for latex)

## General Guidelines
- First row of csv should be the headers / labels
- Relevant Title, detailed captions and legends in all plots (possibly use AI to prompt a response in future)
- Size Option: Single Column Plot (3.375 inches * 3 inches), Double Column Plot (7 inches * 3 inches)
- If csv columns incorrect format, then will not plot as expected
- Try to not have duplicate headers, Pandas automatically appends numbers to duplicate colummns, so if that is not what you want, try to have unique column headers
## Plot API
### Line and Quadratic
- API endpoints: /plot/line, /plot/quadratic
- Provide required parameters, domain of x and range of y
- Plots line and quadratic within domain and range with roots solved
### Scatter plot CSV Format
- API endpoint: /plot/scatter
- x : y
### Errorbar plot CSV Format
- API endpoints: /plot/errorbar1x, /plot/errorbar1y, /plot/errorbar2xy
- x : y : error x
- x : y : error y
- x : y : error x : error y
### Bar graph
- API endpoint: /plot/bar
- data : labels
### Pie Chart
- API endpoint: /plot/pie
- category, percentage
### Boxplot CSV Format
- API endpoint: /plot/boxplot
- category, value
### Single Histogram
- API endpoints: /plot/eqhistogram, /plot/varyhistogram
- Data, #no of bins for equal bin steps, xlabel, ylabel
- Bins (list, varying steps) : Frequencies
### Heatmap and Contour map CSV Format
- API endpoints: /plot/imshowhmap, /plot/pmeshhmap, /plot/pmeshfunchmap, /plot/imshowhmap, /plot/contour,
- csv numeric matrix, npy, npz, HDF5, JSON
- require all matrices have single header value as "m" to distinguish it from ordinary data 
- Normalization: "minmax" or "zscore"
- Fill Missing Values Strategy: "mean", "median" or 0
- choose cmap: https://matplotlib.org/stable/users/explain/colors/colormaps.html
- Using an integer (e.g., levels=10): Matplotlib automatically generates that many contour levels, evenly spaced between the minimum and maximum values of the data (or between specified vmin and vmax if provided). This is useful when you want a general overview of the data distribution without worrying about the exact threshold values.
- Using a list of numbers (e.g., levels=[-1, 0, 1]): Matplotlib uses these exact numbers as the contour levels. This gives you precise control over which data values are highlighted, which is especially useful if you have specific thresholds or boundaries of interest.
## Best Fit API
### 

## Multi Plot
- Plots multiple sets of data in one graph
- Each curve is labeled based on file name.
### Multi Scatter
- API endpoint: /multiplot/multiscatter