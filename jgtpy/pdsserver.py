from flask import Flask, jsonify, request
from jgtpy.JGTPDS import getPH, mk_fn, mk_fullpath,stayConnectedSetter

app = Flask(__name__)
stayConnectedSetter(True)

@app.route('/getPH', methods=['POST'])
def fetch_getPH():
    data = request.json
    instrument = data['instrument']
    timeframe = data['timeframe']
    result = getPH(instrument, timeframe)
    return jsonify(result)  # Assuming the result can be serialized into JSON

@app.route('/mk_fn', methods=['GET'])
def fetch_mk_fn():
    instrument = request.args.get('instrument')
    timeframe = request.args.get('timeframe')
    ext = request.args.get('ext')
    result = mk_fn(instrument, timeframe, ext)
    return jsonify({'filename': result})

# More routes for other functions...

if __name__ == '__main__':
    app.run(debug=True)


