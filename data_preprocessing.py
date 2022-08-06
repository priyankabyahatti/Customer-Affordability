""" This script used for data preprocessing in transforming text variables, dummy-fying some variables and
data normalization """
import re
import sqlite3
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas import DataFrame
from scipy import stats
import datetime as dt
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler


def clean_weekly_restock_vals(customer_df) -> pd.DataFrame:
    """ This function normalises weekly restock values by cleaning values inside it
    Args:
        customer_df: input dataframe consisting affordability data """
    customer_df['weekly_restock'] = customer_df['weekly_restock'].str.strip() \
        .str.replace("Once|once|Omce|0nce|Weekl", "1", regex=True)
    customer_df['weekly_restock'] = customer_df['weekly_restock'].str.strip() \
        .str.replace("Twice|Two|twice", "2", regex=True)
    customer_df['weekly_restock'] = customer_df['weekly_restock'].str.strip() \
        .str.replace("Thric|Three|three|thric", "3", regex=True)
    customer_df['weekly_restock'] = customer_df['weekly_restock'].str.strip() \
        .str.replace("Daily|Dail", "7", regex=True)
    freq_df = customer_df['weekly_restock'].value_counts().rename_axis('weekly_restock').reset_index(name='counts')
    # keep frequent weekly restock values and map everything else to Other
    freq_business_list = [business for business in freq_df[freq_df['counts'] > 1000]['weekly_restock']]
    customer_df['weekly_restock'] = customer_df['weekly_restock'].apply(lambda x: x if x in freq_business_list else 'Other')
    return customer_df


def clean_business_category_vals(customer_df) -> pd.DataFrame:
    """ This function normalises business category values by cleaning values inside it
    Args:
        customer_df: input dataframe consisting affordability data """
    customer_df['business_category'] = customer_df['business_category'].str.strip() \
        .str.replace("services|service|Services|Service|SErvices", "Services", regex=True)
    customer_df['business_category'] = customer_df['business_category'].str.strip() \
        .str.replace("FMCG|fMCG|FCMG", "FMCG", regex=True)
    customer_df['business_category'] = customer_df['business_category'].str.strip() \
        .str.replace("Agri|AGRI|agri", "Agri", regex=True)
    customer_df['business_category'] = customer_df['business_category'].str.strip() \
        .str.replace("Others|other|Other", "Others", regex=True)
    return customer_df


def clean_business_type_vals(customer_df) -> pd.DataFrame:
    """ This function normalises business type values by cleaning values inside it
    Args:
        customer_df: input dataframe consisting affordability data """
    customer_df['business_type'] = customer_df['business_type'].str.strip() \
        .str.replace("Retails|retails|Retailer|retailer|retailers|Retailers", "Retail", regex=True)
    customer_df['business_type'] = customer_df['business_type'].str.strip() \
        .str.replace("Wholesaler|Wholesale|wholesaler", "Wholesale", regex=True)
    customer_df['business_type'] = customer_df['business_type'].\
        str.replace("Retails", "Retail", regex=True)
    return customer_df


def clean_business_names(customer_df) -> pd.DataFrame:
    """ This function normalises business name values by cleaning values inside it
    Args:
        customer_df: input dataframe consisting affordability data """
    rename_list = [('Kiosk', 'kiosk'), ('Groceries', 'grocery'), ('Fruits & Vegetables', 'fruit'),
                   ('Fruits & Vegetables', 'vegetable'), ('Clothing & Accessories', 'cloth'),
                   ('General Stores', 'general'), ('Electronics', 'electronic'), ('Electronics', 'hardware'),
                   ('Electronics', 'phone'), ('Salon', 'salon'), ('Fish Seller', 'fish'), ('Milk & Diary', 'milk'),
                   ('Milk & Diary', 'dairy'), ('Agri-Business', 'agro'), ('Cyber', 'cyber'), ('Furniture', 'furniture'),
                   ('Furniture', 'timber'), ('Auto Repairs', 'auto'), ('Auto Repairs', 'spare'), ('Barber', 'barber'),
                   ('Poultry', 'poultry'), ('Poultry', 'chicken'), ('Eggs', 'egg')]
    for name in rename_list:
        customer_df['business'] = [name[0] if (name[1] in item.lower()) else item for item in customer_df['business']]
    freq_df = customer_df['business'].value_counts().rename_axis('business').reset_index(name='counts')
    # keep most frequent occurring business and rest everything to Other
    freq_business_list = [business for business in freq_df[freq_df['counts'] > 800]['business']]
    customer_df['business'] = customer_df['business'].apply(lambda x: x if x in freq_business_list else 'Other')
    return customer_df


def data_preprocess() -> pd.DataFrame:
    """ This function gets the data from database, and does data preprocessing, and does one hot encoding """
    # get data from DB
    connection = sqlite3.connect('4g_capital.db')
    customer_df = pd.read_sql('SELECT * FROM customer_affordability;', connection)
    customer_df = customer_df.drop('index', axis=1)
    customer_df = customer_df.drop('employees', axis=1)
    # clean text variables
    clean_business_category_vals(customer_df)
    clean_business_type_vals(customer_df)
    clean_business_names(customer_df)
    clean_weekly_restock_vals(customer_df)
    # encode data
    customer_df['loan_date'] = pd.to_datetime(customer_df['loan_date'])
    customer_df['loan_date'] = customer_df['loan_date'].map(dt.datetime.toordinal)
    # one hot encoding
    customer_df = pd.get_dummies(customer_df)
    return customer_df
