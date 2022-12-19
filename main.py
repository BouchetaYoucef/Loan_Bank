import streamlit as st
import pandas as pds
import numpy as np
from PIL import Image 
import pickle

model = pickle.load(open('model.pkl', 'rb'))

st.write("L'application qui prédit l'accord du crédit")

#Collecter le profil d'entrée
st.sidebar.header("Les caracteristiques du client")

img1 = Image.open('image4.jpg')
img1 = img1.resize((180, 180))
st.image(img1, use_column_width=False)
    
def client_caract_entree():
    Gender=st.sidebar.selectbox('Sexe',('Male','Female'))
    Married=st.sidebar.selectbox('Marié',('Yes','No'))
    Dependents=st.sidebar.selectbox('Enfants',('0','1','2','3+'))
    Education=st.sidebar.selectbox('Education',('Graduate','Not Graduate'))
    Self_Employed=st.sidebar.selectbox('Salarié ou Entrepreneur',('Yes','No'))
    ApplicantIncome=st.sidebar.slider('Salaire du client',150,4000,200)
    CoapplicantIncome=st.sidebar.slider('Salaire du conjoint',0,40000,2000)
    LoanAmount=st.sidebar.slider('Montant du crédit en Kdollar',9.0,700.0,200.0)
    Loan_Amount_Term=st.sidebar.selectbox('Durée du crédit',(360.0,120.0,240.0,180.0,60.0,300.0,36.0,84.0,12.0))
    Credit_History=st.sidebar.selectbox('Credit_History',(1.0,0.0))
    Property_Area=st.sidebar.selectbox('Property_Area',('Urban','Rural','Semiurban'))

    data={
    'Gender':Gender,
    'Married':Married,
    'Dependents':Dependents,
    'Education':Education,
    'Self_Employed':Self_Employed,
    'ApplicantIncome':ApplicantIncome,
    'CoapplicantIncome':CoapplicantIncome,
    'LoanAmount':LoanAmount,
    'Loan_Amount_Term':Loan_Amount_Term,
    'Credit_History':Credit_History,
    'Property_Area':Property_Area
    }

    profil_client=pd.DataFrame(data,index=[0])
    return profil_client

# input_df=client_caract_entree()

#Transformer les données d'entrée en données adaptées à notre modèle
#importer la base de données
df_clean=pd.read_csv('train.csv')
credit_input=df_clean.drop(columns=['Loan_ID','Loan_Status'])
donnee_entree=pd.concat([input_df,credit_input],axis=0)

# # encodage des données
var_cat=['Gender', 'Married', 'Dependents', 'Education','Self_Employed','Credit_History', 'Property_Area']
for col in var_cat:
    dummy=pd.lBE(donnee_entree[col],drop_first=True)
    donnee_entree=pd.concat([dummy,donnee_entree],axis=1)
    del donnee_entree[col]
#prendre uniquement la premiere ligne
donnee_entree=donnee_entree[:1]

# #afficher les données transformées
# st.subheader('Les caracteristiques transformés')
# st.write(donnee_entree)


# #importer le modèle
# load_model=pickle.load(open('prevision_credit.pkl','rb'))


# #appliquer le modèle sur le profil d'entrée
# prevision=load_model.predict(donnee_entree)

# st.subheader('Résultat de la prévision')
# st.write(prevision)
            