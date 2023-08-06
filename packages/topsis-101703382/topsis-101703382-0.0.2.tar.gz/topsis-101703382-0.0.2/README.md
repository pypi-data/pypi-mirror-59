# TOPSIS implementation 
```
Class project for DATA ANALYSIS AND VISUALISATION 2020 - UCS633 Thapar University, Patiala
Submitted by: Paras Arora
101703382 (COE 18)

```
Output is a dataframe with 3 columns
 - **Alternatives** 
 - **Score**
 - **Rank**

## Installation
`pip install topsis-101703382`


## To use via command line
`topsis-101703382-cli data.csv 25,25,25,25 -+++`

First argument after run.py is filename with .csv extension. The .csv file is assumed to have a structure similar to one provided in topsis-101703382/data.csv

That is, the .csv file should have a header with column names and first column should only list alternatives and not attribute values.

## To use in .py script
```
from topsis-101703382 import topsis
"""
decision_matrix is 2D numpy array, weights is a 1D array and impacts is a string of the form +-+-- 
where + implies benefit and - implies cost
"""
output_dataframe = topsis(decision_matrix,weights,impacts)
```
