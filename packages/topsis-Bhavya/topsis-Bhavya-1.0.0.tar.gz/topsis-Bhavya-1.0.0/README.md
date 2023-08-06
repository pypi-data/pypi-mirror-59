# Topsis Analysis

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install topsis-Bhavya.

```bash
pip install topsis-Bhavya
```

## Usage

Following query on terminal will provide you the topsis analysis for input csv file.

```
topsisB -a "dataset-name" -b "w1,w2,w3,w4,..." -c "i1,i2,i3,i4,..."

```

Do not mention the file format, 'csv', as part of dataset-name.
w1,w2,w3,w4 represent weights, and i1,i2,i3,i4 represent impacts where 1 is used for maximize and 0 for minimize. 
Size of w and i is equal to number of features. 

Note that the first row and first column of dataset is dropped

The item attributed rank 1 is the best choice.

## License
[MIT](https://choosealicense.com/licenses/mit/)