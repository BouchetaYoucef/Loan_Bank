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
        
    v
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