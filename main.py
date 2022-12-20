import streamlit as st
from PIL import Image
import pickle
# model = pickle.load(open('model1.pkl', 'rb'))

def run():
    img1 = Image.open('image4.jpg')
    img1 = img1.resize((200, 200))
    st.image(img1, use_column_width=False)

    st.sidebar.header("L'application qui prédit l'accord du crédit")

    new_title = '<p style="font-family:sans-serif; color:red; font-size: 20px;">BANK SIMPLONIEN</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    # title = '<p style="font-family:sans-serif; color:orange; font-size: 30px;">B SIMPLONIEN</p>'
   
    gen_display = ('Female','Male')
    gen_options = list(range(len(gen_display)))
    gen = st.selectbox("Gender",gen_options, format_func=lambda x: gen_display[x])
    
    mar_display = ('No', 'Yes')
    mar_options = list(range(len(mar_display)))
    mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])
    
    dep_display = ('No', '1', '2', '3+')
    dep_options = list(range(len(dep_display)))
    dep = st.selectbox("Dependents", dep_options, format_func=lambda x: dep_display[x])

    edu_display = ('Not Graduate', 'Graduate')
    edu_options = list(range(len(edu_display)))
    edu = st.selectbox("Education", edu_options, format_func=lambda x: edu_display[x])
    
    emp_display = ('Yes', 'No')
    emp_options = list(range(len(emp_display)))
    emp = st.selectbox("Self_Employed", emp_options, format_func=lambda x: emp_display[x])

    prop_display = ('Rural', 'Semi-Urban', 'Urban')
    prop_options = list(range(len(prop_display)))
    prop = st.selectbox("Property Area", prop_options, format_func=lambda x: prop_display[x])
    
    cred_display = ('1.0', '0.0')
    cred_options = list(range(len(cred_display)))
    cred = st.selectbox("Credit History", cred_options, format_func=lambda x: cred_display[x])
    
    mon_income = st.number_input("Applicant Income($)", value=0)

    co_mon_income = st.number_input("CoApplicant Income($)", value=0)

    loan_amt = st.number_input("Loan Amount", value=0)

    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month', '360 Month']
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