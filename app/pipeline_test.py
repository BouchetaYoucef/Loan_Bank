from preprocessor import cleaner, pipeline_constructor, feature_encoder, feature_engineering
import os
import pickle
import joblib 
import pandas as pd

test_data = pd.read_csv("./data/test.csv")

model_path = os.path.join("./models/clf_model.joblib")
model = joblib.load(model_path)

lg_pipe = pipeline_constructor(lg_model=model)

# Process raw data
X, y = cleaner(test_data)
X, y = feature_encoder(X, y)

# Apply feature engineering model improvement and return predictions with probability #
preds, probas = feature_engineering(X, y, lg_pipe)

print(preds, probas)

