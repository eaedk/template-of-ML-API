from fastapi import FastAPI
import os, joblib, uvicorn
from typing import List, Literal
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
app = FastAPI(
    title="",  # something like "Credit Card Churn Prediction"
    version=1.0,
    description="", # something like "Classification Machine Learning Prediction"
)

# INPUT MODELING
class ModelInput(BaseModel):
    """Modeling of one input data in a type-restricted dictionary-like format

    column_name : variable type # strictly respect the name in the dataframe header.

    eg.:
    =========
    customer_age : int
    gender : Literal['male', 'female', 'other']
    """


class ModelInputs(BaseModel):
    """Modeling of multiple inputs"""

    inputs: List[ModelInput]


# ENDPOINTS

## API STATUS
@app.post("/status")  
async def status():
    return{"message": "online"}
@app.get("/status")  
async def status():
    return{"message": "online"}


## PREDICT
@app.post(
    "/__endpoint_link__" # something like "/credit_card_churn_prediction"
)  # the string in the post methode is the endpoint link
async def predict(input: ModelInput):
    "Function that receive the posted input data for inference and return an output prediction/error message"
    output = None

    # try to execute the inference loop
    try:
        # create a dataset-like (with the dataset header) dataframe
        df = pd.DataFrame([input.dict()])
        print(f"[Info] Dataframe created with header: {list(df.columns)}\n")

        # apply the preprocessing used during ml model development
        final_input = preprocessor.transform(df)
        print(f"[Info] Input data transformed:\n")

        # predict using the loaded, trained ml model
        prediction = model.predict(final_input)

        # format the prediction as output
        output = {"prediction": prediction.tolist()}

    except ValueError as e:
        output = {"error": str(e)}

    except Exception as e:
        output = {"error": f"Oops something went wrong:\n{e}"}
    finally:
        return output  # output must be json serializable


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
