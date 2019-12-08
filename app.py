from flask import Flask, jsonify, request
from requests import post
import fire
import json

from models.utils import parallel_requests

app = Flask(__name__)


MODEL_TO_PORT = {
    "log_reg": "5001",
    "bayes":   "5002",
    "base":    "5003"
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "OK"})


@app.route("/predict", methods=["POST"])
def predict():
    def make_predict_request(args):
        _sentences, _model_name = args
        payload = json.dumps({
            "data": _sentences
        })
        headers = {"Content-Type": "application/json"}
        url = f"http://0.0.0.0:{MODEL_TO_PORT[_model_name]}/predict"
        return post(url=url, data=payload, headers=headers)

    sentences = request.json["data"]
    all_models = list(MODEL_TO_PORT.keys())
    all_args = [(sentences, model) for model in all_models]
    model_responses = parallel_requests(num_threads=len(all_models),
                                        task=make_predict_request,
                                        args=all_args)
    return jsonify(model_responses)


def run_server(host="0.0.0.0", port="5000", debug=False):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    fire.Fire(run_server)