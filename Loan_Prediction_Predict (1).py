

# In[32]:

# Importer les packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import learning_curve
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imbpipeline
from sklearn.pipeline import Pipeline , make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from transformers import pipeline
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from sklearn.model_selection import GridSearchCV , cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier , AdaBoostClassifier , StackingClassifier , GradientBoostingClassifier
from sklearn.metrics import plot_confusion_matrix , classification_report
from scikitplot.estimators import plot_learning_curve
import scikitplot as skplt
from yellowbrick.model_selection import LearningCurve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import FeatureUnion
import mysql.connector
from sqlalchemy import *
import mlflow.sklearn
import mlflow


if __name__ == "__main__":
    
    #mlflow.set_tracking_uri("http://localhost:5000/%22)
    mlflow.set_experiment(experiment_name='mlflow_loan_pred')
    with mlflow.start_run(run_name='mlflow_loan_prediction') as run :
        data_base = mysql.connector.connect(host="localhost" , user="root" , password="youcef" , database="loan_prediction")
        cur = data_base.cursor(buffered=True)
        query = "select * from loan_prediction.df_clean_train"
        cur.execute(query)
        tables = cur.fetchone()


        df_clean=pd.read_sql(query , data_base)

        df_clean

        df_clean.head()


        lBE = LabelEncoder()
        categ = ["Loan_Status","Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]
        df_clean[categ] = df_clean[categ].apply(lBE.fit_transform)
        df_clean


        df_clean = df_clean.drop(['Loan_ID', 'MyUnknownColumn'], axis=1)

        X = df_clean.drop(["Loan_Status"], axis=1)
        y = df_clean.Loan_Status


        df_clean


        df_clean.dropna(inplace=True)

        y.isnull().sum()


        X_train, X_test, y_train, y_test = train_test_split(X , y , test_size = 0.2 , random_state = 42 )


        # # FEATURE SCALING

        # # Preprocessing


        preprocessing_MinMaxScaler = Pipeline(steps=[
            ("MinMaxscaler", MinMaxScaler())])


        sm = SMOTE(sampling_strategy='auto')


        # # 6) Iteration-Boosting(GradientBoostingClassifier)


        GBC = Pipeline(steps = [['preprocessing_MinMaxScaler', preprocessing_MinMaxScaler],
                                            ['classifier', GradientBoostingClassifier()]])


        GBC.fit(X_train, y_train)


        print("accuracy train : %.3f"%GBC.score(X_train, y_train))
        print("accuracy test : %.3f"%GBC.score(X_test , y_test))


        y_pred_GBC = GBC.predict(X_test) 


        print(classification_report(y_test, y_pred_GBC))


        # # matrice confusion

        def plot_confusion_matrix(y, y_pred):
            cm = confusion_matrix(y, y_pred)
            sns.heatmap(cm, annot=True, fmt=".0f")
            plt.xlabel('y_pred')
            plt.ylabel('y')
            plt.show()

        plot_confusion_matrix(y_test, y_pred_GBC)


        # # learning-Curve

        plot_learning_curve(GBC,X_test , y_test)


        # # roc-auc

        GBC.fit(X_train, y_train)
        y_probas = GBC.predict_proba(X_test)
        skplt.metrics.plot_roc(y_test, y_probas)


        import pickle


        # import pickle
        with open('testing_pickle.plk', 'wb') as f:
            pickle.dump(GBC, f)


        GBC.predict(X_test)
        mlflow.log_metric("accuracy train" , GBC.score(X_train , y_train))
        mlflow.log_metric("accuracy test" , GBC.score(X_test , y_test))

        mlflow.sklearn.log_model(GBC , "model")

        # In[ ]:
        mlflow.end_run()




