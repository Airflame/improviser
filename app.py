import os
from flask import *
from random import randint
from synth import Synth

app = Flask(__name__)
ip_set = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.remote_addr not in ip_set:
        oid = randint(100000, 999999)
        ip_set[request.remote_addr] = oid
        s = Synth()
        if request.args.get("length") is not None:
            s.set_length(request.args.get("length"))
        if request.args.get("meter") is not None:
            s.set_meter(request.args.get("meter"))
        if request.args.get("scale") is not None:
            if request.args.get("tonic") is not None:
                s.set_scale(request.args.get("scale"), request.args.get("tonic"))
            else:
                s.set_scale(request.args.get("scale"), "C")
        if request.args.get("tempo") is not None:
            s.set_tempo(request.args.get("tempo"))
        if request.args.get("instrument") is not None:
            s.set_instrument(request.args.get("instrument"))
        s.create(oid)
        ip_set.pop(request.remote_addr)
    else:
        oid = ip_set[request.remote_addr]
        while request.remote_addr in ip_set:
            pass
    path = '/wav/' + str(oid) + '.wav'
    return redirect(path, code=302)


@app.route('/wav/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='wav', filename=filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
