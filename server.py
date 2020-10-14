from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS
from entry_point import run
import json
app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/', methods=['POST'])
def get_query_string():
    query = request.get_json()["params"]
    return {
        run(query.search_keyword, "", 1000, query.pdf_min_num_page, query.num_years)
    }



if __name__ == "__main__":
    app.run(debug=True)

# run to start environment .\env\Scripts\Activate.ps1 
# then run py server.py