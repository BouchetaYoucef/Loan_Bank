import streamlit as st
from PIL import Image
import pickle

# model = pickle.load(open('./classifier.pickle.pkl', 'rb'))

def run():
    img1 = Image.open('image4.jpg')
    img1 = img1.resize((600,200))
    st.image(img1,use_column_width=False)
    # st.title("Bank Simplonien ")
run()

def prediction(Gender, Married, Dependents, Employment_Status, ApplicantIncome, CoapplicantIncome,LoanAmount, Credit_History):
        
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

    input_df=client_caract_entree()
    # if st.button("Submit"):
    
    # Making predictions
    prediction = classifier.predict(
        [[Gender, Married, Dependents, Employment_Status, ApplicantIncome, CoapplicantIncome, LoanAmount, Credit_History]])
    
    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return pred

# this is the main function in which we define our webpage
    def main():
    # front end elements of the web page
     html_temp = """
    <div style ="background-color:blue;padding:13px">
    <h1 style ="color:white;text-align:center;">Bank Simplonien</h1>
    </div>
    """
    
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html= True)
    
    # following lines create boxes in which user can enter data required to make prediction
    Gender = st.selectbox('Gender',('Male','Female'))
    Married = st.selectbox('Marital Status',('Unmarried','Maried'))
    Dependents = st.selectbox('Dependents', ('1', '2', '3', '+' ))
    Employment_Status = st.selectbox('Employment Status',('Job','Business'))
    ApplicantIncome = st.number_input('Applicants monthly income')
    LoanAmount = st.number_input('Total loan amount')
    Credit_History = st.selectbox('Credit_History',('Unclear Debts','No Unclear Debts'))
    result =""
    
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"):
        result = prediction(Gender, Married, Dependents, Employment_Status, ApplicantIncome, LoanAmount, Credit_History)
        st.success('Your loan is {}'.format(result))
        print(LoanAmount)
        
    if __name__=='__main__':
     main()