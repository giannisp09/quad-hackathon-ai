from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import torch  # or `import tensorflow as tf`
import pandas as pd
from typing import List
# import yfinance 


from stable_baselines3 import PPO  # Replace PPO with your specific algorithm if different

# Define the constant dictionary
test_prediction = {
            "tickers": ["AAPL", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "GS", "HD", "HON", "IBM", "INTC", "JNJ",
                        "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"],
            "probs": [0.071527, 0.033112, 0.052824, 0.033112, 0.036220, 0.036897, 0.033112, 0.033112, 0.033112,
                      0.034724, 0.036590, 0.033112, 0.037261, 0.037598, 0.033112, 0.033112, 0.036398, 0.033112,
                      0.050686, 0.033112, 0.036492, 0.033112, 0.033112, 0.033112, 0.033112, 0.033112, 0.036101],
            "projected_portfolio_value": 1122421.21,
            "sdg_alignment":  0.73,

        }



# Load the policy model
def load_model():
    model = PPO.load("model/trained_ppo.zip")
    return model

model = load_model()
app = FastAPI()

# Define the input data model
class UserInput(BaseModel):
    risk_level: int
    sdgs_preferences: List[float]


# def get_state(covs, ti, data):
#         obs = np.append(np.array(self.covs), [data[tech].values.tolist() for tech in tech_indicator_list ], axis=0)
#         obs = np.append(obs, [self.data[tech].values.tolist() for tech in ['SDG_' +str(i) for i in range(1,18)] ],  axis=0)
#         duplicated_array = np.tile(self.user_sdg_preferences, (27,1))
#         # print(obs.shape)
#         # print(duplicated_array.shape)

#         obs = np.append(obs, duplicated_array.T,  axis=0)
#         return obs


@app.post("/predict/")
async def predict(user_input: UserInput):
    try:
        # # Prepare the input data
        # input_data = np.array([[user_input.risk_level, user_input.esg_priority]], dtype=np.float32)
        # input_tensor = torch.tensor(input_data)

        #get state
        #state = get_state()


        state = np.load('obj/state.npy')

       # Get prediction from the model
        action, _states = model.predict(state)
        
        # Convert the prediction to a readable format (depends on your model output)
        result = action.tolist()

        #return {"prediction": result}

        return test_prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)