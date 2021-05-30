from flask import Flask, request

app = Flask(__name__)


@app.get("/process")
def process():
    args = request.args.to_dict()
    pass


if __name__ == "__main__":
    app.run(debug=True)
