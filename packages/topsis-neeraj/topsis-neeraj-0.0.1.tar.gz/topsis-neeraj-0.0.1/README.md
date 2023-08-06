# Topsis Analysis

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install topsis.

```bash
pip install topsis-neeraj
```

## Usage

Following query on terminal will provide you the topsis analysis for input csv file.

```
topsis -n "dataset-name" -w "w1,w2,w3,w4,..." -i "i1,i2,i3,i4,..."

```

Do not mention the file format, 'csv', as part of dataset-name.
w1,w2,w3,w4 represent weights, and i1,i2,i3,i4 represent impacts where 1 is used for maximize and 0 for minimize. 
Size of w and i is equal to number of features. 

Note that the first row and first column of dataset is dropped

Rank 1 signifies best decision

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)