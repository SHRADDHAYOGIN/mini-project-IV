# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy
import pickle

app = Flask(__name__)
api = Api(app)

class RawFeats:
    def __init__(self, feats):
        self.feats = feats

    def fit(self, X, y=None):
        pass


    def transform(self, X, y=None):
        return X[self.feats]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)
    
model = pickle.load( open( "model.f","rb") )

class Status(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        # getting predictions from our model
        res = model.predict(df)
        # convert predictions to "Yes" or "No"
        res = ["Yes" if val == 1 else "No" for val in res]
        return res
    
# assign endpoint
api.add_resource(Status, '/status')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)