# Ranking System Using Topsis

**Project 1 : UCS633**


Submitted By: **Rajat Gupta 101703427**

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Ranking system.

```bash
pip install topsis-RajatGupta-101703427
```

<br>

## How to use this package:

topsis-RajatGupta-101703427 can be run as done below:



### In Command Prompt
```
>> topsis data.csv "1,1,1,1" "+,+,-,+"
```
<br>

### In Python IDLE:
```python
>>> import pandas as pd
>>> import topsis
>>> data = pd.read_csv('data.csv').values
>>> data = data[:,1:]
>>> w = [1,1,1,1]
>>> impacts = ["+" , "+" , "-" , "+" ]
>>> topsis.topsis(data,w,impacts)
```

<br>

## Sample dataset

The decision matrix should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R<sup>2</sup>, Root Mean Squared Error, Correlation, and many more.

Model | Correlation | R<sup>2</sup> | RMSE | Accuracy
:------------: | :-------------:| :------------: | :-------------: | :------------:
M1 |	0.79 | 0.62	| 1.25 | 60.89
M2 |  0.66 | 0.44	| 2.89 | 63.07
M3 |	0.56 | 0.31	| 1.57 | 62.87
M4 |	0.82 | 0.67	| 2.68 | 70.19
M5 |	0.75 | 0.56	| 1.3	 | 80.39

Weights list is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.

<br>

## Output

```
Model   Score    Rank
-----  --------  ----
  1    0.77221     2
  2    0.225599    5
  3    0.438897    4
  4    0.523878    3
  5    0.811389    1
```
<br>

The rankings are displayed in the form of a table using a package 'tabulate', with the 1st rank offering us the best decision, and last rank offering the worst decision making, according to TOPSIS method.








