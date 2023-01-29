import streamlit as st
from PIL import Image
import pickle
from sklearn.preprocessing import LabelEncoder
from PIL import Image
from preprocessor import cleaner, pipeline_constructor, feature_encoder, feature_engineering
import pickle
import pandas as pd
import numpy as np
import joblib
import numpy

import yaml
from pathlib import Path

##### Functions #####

# def première_fonction(df):
def features_encoding(data):
   lBE = LabelEncoder()
   categ = ["Loan_Status","Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]
   data[categ] = data[categ].apply(lBE.fit_transform)
   return data    

# def deuxième_fonction(df):
def target_encoding(data):
   le = LabelEncoder()
   df['Loan_Status'] = le.fit_transform(df['Loan_Status'])
   return df

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

valid_login = config['credentials']['username']
valid_pwd = config['credentials']['password']

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if  st.session_state["password"] == valid_pwd and st.session_state["login"] == valid_login:
            st.session_state["password_correct"] = True 
            del st.session_state["password"]  # don't store password
            del st.session_state["login"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Login", on_change=password_entered, key="login"
        )
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Login", on_change=password_entered, key="login"
        )
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Username/password is incorrect")
        return False
    else:
        # Password correct.
        return True

        st.session_state["data"] = {}

if check_password():
    # model = pickle.load(open('../classifier.pkl', 'rb'))
    st.title("Prédiction de prêt bancaire")

    ## --- SELECTIONS DES DONNEES --- ## 

    # For gender
    gen_display = ('Female', 'Male')
    gen_options = list(range(len(gen_display)))
    gen = st.selectbox("Genre", gen_options, format_func=lambda x: gen_display[x])

    # For Marital Status
    mar_display = ('No', 'Yes')
    mar_options = list(range(len(mar_display)))
    mar = st.selectbox("Status civil", mar_options,
                    format_func=lambda x: mar_display[x])

    # No of dependets
    dep_display = ('0', '1', '2', '3+')
    dep_options = list(range(len(dep_display)))
    dep = st.selectbox("Nombre d'enfant(s)", dep_options,
                    format_func=lambda x: dep_display[x])

    # For edu
    edu_display = ('Not Graduate', 'Graduate')
    edu_options = list(range(len(edu_display)))
    edu = st.selectbox("Education", edu_options,
                    format_func=lambda x: edu_display[x])

    # For emp status
    emp_display = ('Yes', 'No')
    emp_options = list(range(len(emp_display)))
    emp = st.selectbox("Travailleur independant", emp_options,
                    format_func=lambda x: emp_display[x])

    # For Property status
    prop_display = ('Rural', 'Semi-Urban', 'Urban')
    prop_options = list(range(len(prop_display)))
    prop = st.selectbox("Zone d'habitation", prop_options,
                        format_func=lambda x: prop_display[x])

    # Applicant Monthly Income
    mon_income = (st.number_input("Revenus demandeur", value=0))
    # Credit history
    credit_display = ('Yes', 'No')
    credit_hst_options = list(range(len(credit_display)))
    credit_hst = st.selectbox("Autre crédit en cours", credit_hst_options,
                            format_func=lambda x: credit_display[x])
    # Co-Applicant Monthly Income
    co_mon_income = (st.number_input("Revenues co-demandeur", value=0))
    # Loan AMount
    loan_amt = (st.number_input("Montant du credit", value=0))
    # loan duration
    dur = (st.number_input("Durée du credit", value=0))
    
    #########################################################################
    
    if st.button("Prédiction du prêt"):
        duration = 0
        if dur == 0:
            duration = 60
        if dur == 1:
            duration = 180
        if dur == 2:
            duration = 240
        if dur == 3:
            duration = 360
        if dur == 4:
            duration = 480

        ## --- TRAITEMENT DES DONNEES --- ##
        model = joblib.load('./models/clf_model.joblib')
        COLUMNS_NAMES = ['Gender', 'Married', 'Dependents', 'Education',
        'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
        'Loan_Amount_Term', 'Credit_History', 'Property_Area'
        ]
        # dep = 3 if dep == "3+" else int(dep)
        df = pd.DataFrame(data=[[gen, mar, dep, edu, emp, mon_income, 
                                co_mon_income, loan_amt, dur, credit_hst, prop]], columns=COLUMNS_NAMES)

        # Process raw data
        data = cleaner(df)
        data_prcd = feature_encoder(data)
        data_prcd.columns = data_prcd.columns.astype(str)

        st.table(data_prcd)

        # preds, probas = feature_engineering(X, y, lg_pipe)
        ## ------------------------------ ##
        
        # ##### TODO #####
        # # exécuter les fonctions de preprocessing
        # # def première_fonction(features):
        # def features_encoding(df_clean):
        #    lBE = LabelEncoder()
        #    categ = ["Loan_Status","Gender", "Married", "Dependents",
        #             "Education", "Self_Employed", "Property_Area"]
        #    df_clean[categ] = df_clean[categ].apply(lBE.fit_transform)
        #    return df_clean  
       
        # # def deuxième_fonction(features):
        # def target_encoding(df_clean_encoded):
        #    le = LabelEncoder()
        #    df_clean_encoded['Loan_Status'] = le.fit_transform(df_clean_encoded['Loan_Status'])
        #    return df_clean_encoded
        
        ## --- RETURNER LA PREDICTION AVEC UNE ALERTE PERTINENTE --- ###
        pred = model.predict(data_prcd)
        proba = model.predict_proba(data_prcd)
        
        if pred == 0:
            st.error('Suite à nos calcul vous ne pouvez pas prétendre à un prêt bancaire.')
            st.text(f"Taux de confiance : {proba}")
        else:
            st.success('Félécitations! Vous pouvez prétendre à un prêt bancaire !' )
            st.text(f"Taux de confiance : {proba}")
        ## --------------------------------------------------------- ###
            
            

