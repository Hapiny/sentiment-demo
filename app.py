from flask import Flask, jsonify 
import fire


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status" : "OK"})

def run_server(host="0.0.0.0", port="5000", debug=False):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    fire.Fire(run_server)