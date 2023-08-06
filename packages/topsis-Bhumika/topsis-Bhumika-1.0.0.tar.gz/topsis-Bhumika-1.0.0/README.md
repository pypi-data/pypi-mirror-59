# Topsis Analysis

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install topsis-Bhumika.

```bash
pip install topsis-Bhumika
```

## Usage

Following query on terminal will provide you the topsis analysis for input csv file.

```
topsisBG -x "dataset-name" -y "w1,w2,w3,w4,..." -z "i1,i2,i3,i4,..."

```

Do not mention the file format, 'csv', as part of dataset-name.

w1,w2,w3,w4 represent weights (w), not already normalised will be normalised later in the code.

i1,i2,i3,i4.... represent information of benefit positive(1) or negative(0) impact criteria.

Note that the first row and first column of dataset is dropped

Rank 1 item denotes the best choice.

## License
[MIT](https://choosealicense.com/licenses/mit/)