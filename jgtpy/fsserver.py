from flask import Flask, jsonify, request
#from jgtpy import sc,up,h,stay

from subprocess import check_output
import shlex


app = Flask(__name__)
#stayConnectedSetter(True)


@app.route('/run_jgtcli', methods=['POST'])
def run_jgtcli():
    data = request.json
    instrument = data['instrument']
    timeframe = data['timeframe']

    # Optional parameters with default values
    datefrom = data.get('datefrom', None)
    dateto = data.get('dateto', None)
    #output = '-o' if data.get('output', False) else ''
    cds = '-cds' if data.get('cds', False) else ''
    verbose = '-v %s' % data.get('verbose', 0)

    # Construct the command
    cmd = f'jgtcli -i {instrument} -t {timeframe} -o {cds} {verbose}'


    if datefrom:
        cmd += f' -s "{datefrom}"'
    if dateto:
        cmd += f' -e "{dateto}"'

    # Execute the command
    print("==================CLI===================")
    print(cmd)
    print("========================================")

    try:
        result = check_output(shlex.split(cmd)).decode('utf-8')
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})



# More routes for other functions...

if __name__ == '__main__':
    app.run(debug=True)


