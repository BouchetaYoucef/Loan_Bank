import streamlit as st
from PIL import Image
import pickle

model = pickle.load(open('model_pkl.pickle', 'rb'))

img1 = Image.open('image4.jpg')
img1 = img1.resize((600, 200))
st.image(img1, use_column_width=False)

## --- SELECTIONS DES DONNEES --- ## 

# For gender
gen_display = ('Female', 'Male')
gen_options = list(range(len(gen_display)))
gen = st.selectbox("Gender", gen_options, format_func=lambda x: gen_display[x])


# For Marital Status
mar_display = ('No', 'Yes')
mar_options = list(range(len(mar_display)))
mar = st.selectbox("Married", mar_options,
                   format_func=lambda x: mar_display[x])


# No of dependets
dep_display = ('No', 'One', 'Two', 'More than Two')
dep_options = list(range(len(dep_display)))
dep = st.selectbox("Dependents", dep_options,
                   format_func=lambda x: dep_display[x])


# For edu
edu_display = ('Not Graduate', 'Graduate')
edu_options = list(range(len(edu_display)))
edu = st.selectbox("Education", edu_options,
                   format_func=lambda x: edu_display[x])


# For emp status
emp_display = ('Yes', 'No')
emp_options = list(range(len(emp_display)))
emp = st.selectbox("Self_Employed", emp_options,
                   format_func=lambda x: emp_display[x])


# For Property status
prop_display = ('Rural', 'Semi-Urban', 'Urban')
prop_options = list(range(len(prop_display)))
prop = st.selectbox("Property Area", prop_options,
                    format_func=lambda x: prop_display[x])


# For Credit Score
cred_display = ('Between 300 to 500', 'Above 500')
cred_options = list(range(len(cred_display)))
cred = st.selectbox("Credit_History", cred_options,
                    format_func=lambda x: cred_display[x])


# Applicant Monthly Income
mon_income = st.number_input("ApplicantIncome($)", value=0)


# Co-Applicant Monthly Income
co_mon_income = st.number_input("CoapplicantIncome($)", value=0)


# Loan AMount
loan_amt = st.number_input("Loan Amount", value=0)


# loan duration
dur_display = [12, 65, 342, 360, 480, 600]
dur_options = range(len(dur_display))
dur = st.selectbox("Loan_Amount_Term", dur_options,
                   format_func=lambda x: dur_display[x])

## ----------------------------------------------------- ## 

## --- TRAITEMENT DES DONNEES --- ##





## ------------------------------ ##



if st.button("Submit"):
    duration = 0


