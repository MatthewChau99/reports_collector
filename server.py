from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS
from ../reports_collector/entry_point.py import *
app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/', methods=['POST'])
def get_query_string():
    query = request.get_json()
    return {
        "params": query
    }



if __name__ == "__main__":
    app.run(debug=True)

# run to start environment .\env\Scripts\Activate.ps1 
# then run py server.py