# Import Neptune
import os, joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

from sklearn.metrics import precision_score, recall_score

# //////////////////////////////////////////////////// #

# --- COLUMNS NAMES --- #
COLUMNS_NAMES = ['Loan_ID', 'Gender', 'Married', 'Dependents', 'Education',
    'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
    'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status'
]

categorical_fts = [
    "gender", "married", "education", "self_employed",
    "credit_history", "property_area"
]
numerical_fts_eng = ['dependents', 'loanamount', 'totalincome', 'loan_amount_term_months']
numerical_fts = ['dependents', 'applicantincome', 'coapplicantincome', 'loanamount', 'loan_amount_term']

# ---- Multi Columns Label Enconder ---- #
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit_transform(self, X):
        """
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        """
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    # def fit_transform(self,X):
    #     return self.fit(X).transform(X)
# ---------------------------------------- #

def cleaner(data):
    # assert all(x in COLUMNS_NAMES for x in data.columns)

    # data = data.drop(["Loan_ID"], axis=1)
    # data = data.dropna()
    data.columns = data.columns.str.lower()
    data = (data.replace({"3+": 3, "0": 0, "1": 1, "2": 2}))

    return data

def splitter_balancer(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
    sm = SMOTE(random_state=0)

    X_train, y_train = sm.fit_resample(X_train, y_train)
    X_test, y_test = sm.fit_resample(X_test, y_test)

    return X_train, X_test, y_train, y_test

def feature_encoder(X, ctg_fts = categorical_fts):
    le = LabelEncoder()
    one_hot = OneHotEncoder()

    onehot_df = one_hot.fit_transform(X[ctg_fts[-1]].reshape(1, -1))
    return onehot_df
    label_df = MultiColumnLabelEncoder(columns = ctg_fts[:-1]).fit_transform(X)
    label_df = label_df.drop(ctg_fts[-1], axis=1)

    X = label_df.join(onehot_df)
    # y = le.fit_transform(y)

    return X

def feature_engineering(X, y, pipe):
    # Converting the scale of loan term from months to years
    X["loan_amount_term_months"] = (X["loan_amount_term"] / 12)

    # Combining applicant and co-applicant income to get the total income per application
    X["totalincome"] = X["applicantincome"] + X["coapplicantincome"]

    # Dropping the columns as we created a new column which captures the same information
    X.drop(columns=["applicantincome", "coapplicantincome"], inplace=True)

    X_train, X_test, y_train, y_test = splitter_balancer(X, y)

    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_probas = pipe.predict_proba(X_test)
    
    return y_pred, y_probas
    
def hyperparameter_optimizer(pipe, X_eng, y):
    params = {'C': 10,
        'class_weight': 'balanced',
        'dual': False,
        'multi_class': 'auto',
        'penalty': 'l2',
        'solver': 'lbfgs'
    }

    X_train, X_test, y_train, y_test = splitter_balancer(X_eng, y)

    pipe[-1].set_params(**params)
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_probas = pipe.predict_proba(X_test)

def pipeline_constructor(lg_model, num_fts_l = numerical_fts):
    column_transformer = ColumnTransformer([
        ("scaler", StandardScaler(), num_fts_l)
    ], remainder="passthrough")

    return Pipeline([("datafeed", column_transformer), ("classifier", lg_model)])


