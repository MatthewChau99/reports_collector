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
    # run(query.search_keyword, "", 1000, query.pdf_min_num_page, query.num_years)
    # f = open('cache/中芯国际/all_search_results.json', "r")
    # data = json.loads(f.read()) 
    # print(data)
    return {
        "list":
            [
                {
                    "source": "36kr",
                    "doc_id": "12397912",
                    "title" : "test1",
                    "date" : "2019-09-17",
                    "org_name" : "刘光",
                    "doc_type" : "NEWS"
                },
                {
                    "source": "36kr",
                    "doc_id": "1239791223123",
                    "title" : "test2",
                    "date" : "2020-07-30",
                    "org_name" : "AI前线",
                    "doc_type" : "NEWS"
                }
            ]
    }



if __name__ == "__main__":
    app.run(debug=True)

# run to start environment .\env\Scripts\Activate.ps1 
# then run py server.py