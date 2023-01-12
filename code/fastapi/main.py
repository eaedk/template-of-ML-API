from fastapi import FastAPI
import os, joblib, uvicorn
from pydantic import BaseModel
import pandas as pd
import numpy as np

# SETTINGS
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIRECTORY = os.path.join(CURRENT_FILE_DIRECTORY, "assets")
MODEL_FILEPATH = os.path.join(ASSETS_DIRECTORY, ".pkl")
PREPROCESSOR_FILEPATH = os.path.join(ASSETS_DIRECTORY, ".pkl")

# LOADING
## model
model = joblib.load(MODEL_FILEPATH)

## preprocessor
preprocessor = joblib.load(PREPROCESSOR_FILEPATH)


# CONFIG
app = FastAPI(title ='Credit Card Churn Prediction', version = 1.0, description = 'Classification Machine Learning Prediction')

# INPUT MODELING
class ModelInput(BaseModel):
    """Modeling of the input data in a type-restricted dictionary-like format
    
    column_name : variable type # strictly respect the name in the dataframe header.

    eg.:
    =========
    customer_age : int
    gender : str
    """
    


# ENDPOINTS

## PREDICT
@app.post("/credit_card_churn_prediction")
async def predict(input:ModelInput):
    prediction = None
    try:

        df = pd.DataFrame([input.dict()])
        print(f"[Info] Dataframe created with header: {list(df.columns)}\n")

        final_input = preprocessor.transform(df)
        print(f"[Info] Input data transformed:\n")

        prediction = model.predict(final_input).tolist()
        print(prediction)

        return {"prediction":prediction}
    
    except ValueError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"Oops something went wrong:\n{e}"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload = True)