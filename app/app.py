import streamlit as st
from PIL import Image
from preprocessor import cleaner, pipeline_constructor, feature_encoder, feature_engineering
import pickle
import pandas as pd
import numpy as np
import joblib
import numpy

img1 = Image.open('image4.jpg')
img1 = img1.resize((600, 200))
st.image(img1, use_column_width=False)

## --- SELECTIONS DES DONNEES --- ## 

# For gender
gen_display = ('Female', 'Male')
gen_options = list(range(len(gen_display)))
gen = st.selectbox("Genre", gen_options, format_func=lambda x: gen_display[x])

# For Marital Status
mar_display = ('No', 'Yes')
mar_options = list(range(len(mar_display)))
mar = st.selectbox("Mariée", mar_options,
                   format_func=lambda x: mar_display[x])

# No of dependets
dep_display = ('0', '1', '2', '3+')
dep_options = list(range(len(dep_display)))
dep = st.selectbox("Nombre de salariés", dep_options,
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
mon_income = float(st.number_input("Revenus demandeur", value=0))
# Credit history
# credit_display = ('Yes', 'No')
credit_display = "Yes"
# credit_hst_options = list(range(len(credit_display)))
# credit_hst = st.selectbox("Travailleur independant", credit_hst_options,
#                         format_func=lambda x: credit_display[x])
# Co-Applicant Monthly Income
co_mon_income = float(st.number_input("Revenues co-demandeur", value=0))
# Loan AMount
loan_amt = float(st.number_input("Montant du credit", value=0))
# loan duration
dur = float(st.number_input("Durée du credit", value=0))

## ----------------------------------------------------- ## 

if st.button("Submit"):
    ## --- TRAITEMENT DES DONNEES --- ##
    model = joblib.load('./models/clf_model.joblib')
    lg_pipe = pipeline_constructor(lg_model=model)
    COLUMNS_NAMES = ['Gender', 'Married', 'Dependents', 'Education',
    'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
    'Loan_Amount_Term', 'Credit_History', 'Property_Area'
    ]
    # dep = 3 if dep == "3+" else int(dep)
    df = pd.DataFrame(data=[gen, mar, dep, edu, emp, mon_income, 
                            co_mon_income, loan_amt, dur, credit_display, prop], columns=COLUMNS_NAMES)

    # Process raw data
    data = cleaner(df)
    data_prcd = feature_encoder(data)

    # Unit testing on first feature engineering model improvement exp run #
    # preds, probas = feature_engineering(X, y, lg_pipe)
    ## ------------------------------ ##
    
    ## --- PREDICTION --- ##
    pred = lg_pipe.predict(data_prcd)
    proba = lg_pipe.predict_proba(data_prcd)
    
    if not pred == 0:
        st.text(f"Le demandeur est eligble au credit avec un indicateur de confiance de {proba}")
    else:
        st.text(f"Le demandeur n'est pas eligble au credit avec un indicateur de confiance de {proba}")


