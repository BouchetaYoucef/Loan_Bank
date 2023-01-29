import pytest
import pandas as pd
from app import loading_model, create_user_dataframe

def test_loading_model():
    # Test if loading_model() loads the model used in this application
    test_model = loading_model()
    assert test_model != None

def test_create_user_dataframe_length():
    # Test if the dataframe created has the good length
    data = ['Female','Yes', '0', 'Not Graduate',
            "Yes", 0.0, 0.0, 0.0,
            0.0, 1.0, 'Rural']
    test_df = create_user_dataframe(data)
    assert test_df.shape == (1,11)

def test_create_user_dataframe_dtype():
    # Test if 'Credit_History' column has the good type 
    # (because when change it from String to Float in the function)
    data = ['Female','Yes', '0', 'Not Graduate',
            'Yes', 0.0, 0.0, 0.0,
            0.0, 1.0, 'Rural']
    test_df = create_user_dataframe(data)
    assert test_df['Credit_History'].dtype == float