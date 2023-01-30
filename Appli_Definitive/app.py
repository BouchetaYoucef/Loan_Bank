import streamlit as st
from PIL import Image
import pickle
import pandas as pd

## Variables d'environnement (secrets sur streamlit cloud) ##
valid_login = st.secrets["VALID_LOGIN"]
valid_password = st.secrets["VALID_PASSWORD"]

## Fonctions ##
def loading_model():
    infile = open('./model.pkl','rb')
    model = pickle.load(infile)
    infile.close()
    return model

def create_user_dataframe(data):
        COLUMNS_NAMES = ['Gender', 'Married', 'Dependents', 'Education',
                         'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                         'Loan_Amount_Term', 'Credit_History', 'Property_Area']

        if data[-2] == "Yes":
            data[-2]  = 1.0
        if data[-2]  == "No":
            data[-2]  = 0.0

        df = pd.DataFrame([data], columns=COLUMNS_NAMES)

        return df

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == valid_password and st.session_state["login"] == valid_login:
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
        st.error("😕 Identifiants incorrects, veuillez réessayer")
        return False
    else:
        # Password correct.
        return True

## Login ##
if check_password():

    ## Application ##
    img1 = Image.open('image4.jpg')
    img1 = img1.resize((600, 200))
    st.image(img1, use_column_width=False)

    ## --- SELECTIONS DES DONNEES --- ## 

    # For gender
    gen_display = ('Female', 'Male')
    gen = st.selectbox("Genre", gen_display)

    # For Marital Status
    mar_display = ('Yes', 'No')
    mar = st.selectbox("Marrié", mar_display)

    # No of dependets
    dep_display = ('0', '1', '2', '3+')
    dep = st.selectbox("Nombre de salarié(s)", dep_display)

    # For edu
    edu_display = ('Not Graduate', 'Graduate')
    edu = st.selectbox("Education", edu_display)

    # For emp status
    emp_display = ('Yes', 'No')
    emp = st.selectbox("Travailleur indépendant", emp_display)

    # For Property status
    prop_display = ('Rural', 'Semiurban', 'Urban')
    prop = st.selectbox("Zone d'habitation", prop_display)

    # Applicant Monthly Income
    mon_income = float(st.number_input("Revenus demandeur", value=0))

    # Credit history
    credit_hst_display = ('Yes', 'No')
    credit_history = st.selectbox("Historique de crédit", credit_hst_display)         

    # Co-Applicant Monthly Income
    co_mon_income = float(st.number_input("Revenues co-demandeur", value=0))

    # Loan AMount
    loan_amt = float(st.number_input("Montant du credit", value=0))

    # loan duration
    dur = float(st.number_input("Durée du credit", value=0))

    ## ----------------------------------------------------- ## 

    if st.button("Demande de crédit"):
        model = loading_model()

        data = [gen, mar, dep, edu, emp, mon_income, 
                co_mon_income, loan_amt, dur, credit_history, prop]

        df = create_user_dataframe(data)
        
        ## --- PREDICTION --- ##
        pred = model.predict(df)
        proba = model.predict_proba(df)
        proba_yes_class = round(proba[0][1], 2) * 100
        proba_no_class = round(proba[0][0], 2) * 100

        if pred == "Y":
            st.success(f"Le demandeur est éligble au credit avec un indicateur de confiance de {int(proba_yes_class)} %")
        else:
            st.warning(f"Le demandeur n'est pas éligble au credit avec un indicateur de confiance de {int(proba_no_class)} %")
        
        # Ajout de la prédiction au tableau de l'utilisateur
        df["LoanStatus"] = pred

        # Télécharge la prediction
        st.download_button("Télécharger les données d'utilisateur",
                            df.to_csv(index=False).encode('utf-8'),
                            "User_data.csv",
                            "text/csv")