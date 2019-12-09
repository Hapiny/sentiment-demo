import pickle
from models.logistic_regression import LogisticRegressionModel
from models.naive_bayes import NaiveBayesModel
from models.base_model import BaseModel

import fire
from flask import Flask, jsonify, request

app = Flask(__name__)
MODEL = None


def run_server(
        model_name: str,
        model_params_path: str,
        host: str = "0.0.0.0",
        port: str = "5001",
        debug: bool = False
):
    with open(model_params_path, "rb") as fp:
        global MODEL
        MODEL = pickle.load(fp)
        MODEL.name = model_name
    app.run(host=host, port=port, debug=debug)


@app.route("/predict", methods=["POST"])
def predict():
    sentences = request.json["data"]
    predicted = MODEL.predict(sentences)
    response = {
        "model": MODEL.name,
        "response": predicted
    }
    return jsonify(response)


if __name__ == "__main__":
    fire.Fire(run_server)
