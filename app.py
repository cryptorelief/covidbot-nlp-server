from flask import Flask, request
from model import Model
import json

app = Flask(__name__)

latest_version = 2
model = Model(latest_version)

# The process method should get a json in this format: 
# {'messages': [{'metadata': ['some group name maybe'],
#                'text': 'I need an icu bed urgently. I am in hyderabad now. Call me at 3432746283'}]}
@app.post("/process")
def process():
    # TODO: Error handling
    messages = request.json['messages']
    return json.dumps([model.processMessage(i['text'], i['metadata']) for i in messages])

if __name__ == "__main__":
    app.run(debug=True)
