import streamlit as st
from PIL import Image
import pickle
# model = pickle.load(open('model1.pkl', 'rb'))

def run():
    img1 = Image.open('image4.jpg')
    img1 = img1.resize((190, 190))
    st.image(img1, use_column_width=False)


    new_title = '<p style="font-family:sans-serif; color:red; font-size: 20px;"></p>'
    st.markdown(new_title, unsafe_allow_html=True)
    title = '<p style="font-family:sans-serif; color:red; font-size: 30px;">BANK SIMPLONIEN</p>'

    # st.markdown(title,unsafe_allow_html=True)

    # fn = st.text_input('Full Name')
    # account_no = st.text_input('Account number')

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
df=pd.read_csv('train.csv')
credit_input=df.drop(columns=['Loan_ID','Loan_Status'])
# donnee_entree=pd.concat([input_df,credit_input],axis=0)

# encodage des données
var_cat=['Gender', 'Married', 'Dependents', 'Education','Self_Employed','Credit_History', 'Property_Area']
for col in var_cat:
    dummy=pd.get_dummies(donnee_entree[col],drop_first=True)
    donnee_entree=pd.concat([dummy,donnee_entree],axis=1)
    del donnee_entree[col]
#prendre uniquement la premiere ligne
donnee_entree=donnee_entree[:1]

#afficher les données transformées
st.subheader('Les caracteristiques transformés')
st.write(donnee_entree)

#importer le modèle
load_model=pickle.load(open('prevision_credit.pkl','rb'))

#appliquer le modèle sur le profil d'entrée
prevision=load_model.predict(donnee_entree)

st.subheader('Résultat de la prévision')
st.write(prevision)
dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
dur_options = range(len(dur_display))
dur = st.selectbox("Loan Duration", dur_options, format_func=lambda x: dur_display[x])
if st.button("Submit"):
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
features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
print(features)
prediction = model.predict(features)
lc = [str(i) for i in prediction]
ans = int("".join(lc))
if ans == 0:
            st.error(
                "Hello " + fn +' you will not get a loan as per the calculations of the bank.'
            )
else:
            st.success(
                "Hello " + fn + ' '+' Congratulations!! you will get the loan from Bank'
            )
run()