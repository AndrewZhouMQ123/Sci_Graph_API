# SCIENTIFIC GRAPH API
- plots from given parameters or csv data
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
### Single Histogram
- API endpoints: /plot/eqhistogram, /plot/varyhistogram
- Data, #no of bins for equal bin steps, xlabel, ylabel
- Bins (list, varying steps) : Frequencies
### Bar graph
- API endpoint: /plot/bar
- data : labels
### Pie Chart
- API endpoint: /plot/pie
- category, percentage
### Boxplot CSV Format
- API endpoint: /plot/boxplot
- category, value
### Heatmap and Contour map CSV Format
- API endpoints: /plot/imshowhmap, /plot/pmeshhmap, /plot/pmeshfunchmap, /plot/imshowhmap, /plot/contour,
- csv numeric matrix, npy, npz, HDF5, JSON
- require all matrices have single header value as "m" to distinguish it from ordinary data 
- Normalization: "minmax" or "zscore"
- Fill Missing Values Strategy: "mean", "median" or 0
- choose cmap: https://matplotlib.org/stable/users/explain/colors/colormaps.html
## Best Fit API
### 

## Multi Plot
- Plots multiple sets of data in one graph
- Each curve is labeled based on file name.
### Multi Scatter
- API endpoint: /multiplot/multiscatter