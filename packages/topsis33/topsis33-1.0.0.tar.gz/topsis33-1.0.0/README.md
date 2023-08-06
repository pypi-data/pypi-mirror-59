# topsis-python
Topsis analysis of a csv file in python


## About Topsis

It is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion. An assumption of TOPSIS is that the criteria are monotonically increasing or decreasing. Normalisation is usually required as the parameters or criteria are often of incongruous dimensions in multi-criteria problems

## Installation


```bash
pip install topsis33
```

## Usage

Query on terminal will provide you the topsis analysis for input csv file.

```
topsis33 -n "dataset-name.csv" -w "w1,w2,w3,w4,..." -i "i1,i2,i3,i4,..."

```

w1,w2,w3,w4 represent weights, and i1,i2,i3,i4 represent impacts where 1 is used for maximize and 0 for minimize. 
Size of w and i is equal to number of features. 

Note that the first row and first column of dataset is dropped

Rank 1 signifies best decision


## License
[MIT](https://choosealicense.com/licenses/mit/)
