<!-- GETTING STARTED -->
## Getting Started

Clone the project using (https://github.com/priyankabyahatti/Customer-Affordability.git).

1. Install prerequiste python packages used throughout the task
    `pip install -r requirements.txt`

2. First run the database.py. This creates a database and relevant table inside it to store Affordability data.
    `python3 database.py`

3. Then run the main.py. This builds multiple regression models and evaluates their performance. 
    `python3 main.py`

<!-- Results -->
### Data Preprocessing

This is one of the important step in the data science ML process. Here, textual variables are standardised and then 
encoded using one-hot encoding. The data is also normalised using standard scalar to keep all variables in one unit. 

### Results

Out of the 5 regressors, Tree Regression models outperform the others with following results:

##### Decision Trees
- **r²**: 0.99
- **adjusted r²**: 0.99
- **MAE**: 12.21
- **MSE**: 134278.56
- **RMSE**: 366.44

##### Random Forests Trees
- **r²**: 0.99
- **adjusted r²**: 0.99
- **MAE**: 87.69
- **MSE**: 529621.13
- **RMSE**: 727.75
