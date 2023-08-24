import pandas as pd
import pickle
from flask             import Flask, request, Response
from rossmann.Rossmann import Rossmann


# loading model
model = pickle.load( open( 'C:/Users/filip/Documents/Repos/Python/rossman_project/rossman_store_predict/model/model_xgb_tuned.pickle', 'rb' ) )

# Initialize API
app = Flask(__name__)

@app.route( '/rossmann/predict', methods=['POST'] )
def rossman_predict():
    test_json = request.get_json()
    
    if test_json: # if there's data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # instantiante Rossmann Class
        pipeline = Rossmann()
        
        # data cleaning
        df1 = pipeline.data_cleaning( test_raw )
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # predict
        df_response = pipeline.get_prediction( model, test_raw, df3 )
        
        return df_response
        
    else:
        return Response( '{}', status = 200, mimetype='application/json')

if __name__ == '__main__':
    app.run( '0.0.0.0' )