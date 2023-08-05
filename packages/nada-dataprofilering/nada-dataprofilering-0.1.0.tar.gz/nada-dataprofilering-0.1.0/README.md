# nada-dataprofilering
Python package that generates sql scripts for data profiling + connectors.

# Columns Metrics
Each metric function computes generate script that computes a metric and updates the value in NADA_PROFILERING_PROD.

The implemented metrics are

## Standard metrics
`standard_metric_functions.py`

| Metric                  | Function name    |
|-------------------------|------------------|
|Number of observations   |num_rows          |
|Number of nulls          |num_nulls         |
|Number of nulls %        |num_nulls_pct     |
|Number of unique values  |count_distinct    |
|Number of unique values %|count_distinct_pct|


## Number metrics
`number_metric_functions.py`

### Quantile metrics

| Metric                  | Function name    |
|-------------------------|------------------|
|Min                      |min_number        |
|`p-th` percentile        |quantile          |
|Max                      |max_number        |
|Range                    |value_range       |
|Interquartile range      |iqr               |

### Descriptive metrics

| Metric                  | Function name    |
|-------------------------|------------------|
|Standard deviation       |std_number        |
|Coef of variation        |coef_variation    |
|Kurtosis                 |kurtosis_value    |
|Mean                     |mean_number       |
|MAD                      |mad_value         |
|Skewness                 |skewness_value    |
|Sum                      |value_sum         |
|Variance                 |value_variance    |
|Number of zero           |num_zero          |


## Date metrics
`date_metric_functions.py`

| Metric                  | Function name    |
|-------------------------|------------------|
|Min                      |min_date          |
|Median                   |median_date       |
|Max                      |max_date          |


## varchar2 metrics
`varchar2_metric_functions.py`

### Quantile metrics

| Metric                  | Function name    |
|-------------------------|------------------|
|Min length               |min_date          |
|Median length            |median_date       |
|Max length               |max_date          |

### Descriptive metrics
| Metric                     | Function name    |
|----------------------------|------------------|
|Mean length                 |mean_len          |
|Standard deviation length   |std_len           |
