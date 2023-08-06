# Project UCS633

Name **Kriti Pandey** 

Roll no **101703292**

Group **3COE13**


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TOPSIS-ANALYSIS-kriti.

```bash
pip install TOPSIS-ANALYSIS-kriti
```

## Usage
Enter csv filename followed by .csv extentsion, then enter the weights vector with vector values separated by commas, followed by the impacts vector with comma separated signs (+,-)

```python
TOPO_101703292 data.csv [1,1,1,1] [+,+,-,+]
```
## Sample dataset

| ID | EYES | NOSE | FOREHEAD | LIPS  | CHIN |
|----|------|------|----------|-------|------|
| S1 | 0.79 | 0.62 | 1.25     | 60.89 | 11   |
| S2 | 0.66 | 0.44 | 2.89     | 63.07 | 20   |
| S3 | 0.56 | 0.31 | 1.57     | 62.87 | 16   |
| S4 | 0.82 | 0.67 | 2.68     | 70.19 | 16   |
| S5 | 0.75 | 0.56 | 1.3      | 80.39 | 20   |

## Input

```bash
TOPO_101703292 PhotogenicFace.csv [1,1,1,1,1] [+,-,+,+,+]
```
 ## Result

```bash
Topsis Selection of DATA

Model | Rank
_______________

1     | 5

2     | 1

3     | 3

4     | 2

5     | 4
_______________
```

## Constraint 
*Your csv file should not have categorical data*



## License
[MIT](https://choosealicense.com/licenses/mit/)