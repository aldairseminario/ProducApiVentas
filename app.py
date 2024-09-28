from flask import Flask , jsonify, send_file, Response , request
from functions import CargarFiltros , NewConsultas
from flask_cors import CORS



app = Flask(__name__)

CORS(app)

@app.route('/f',methods=['POST'])
def filtro():
    data = request.get_json()
    c,z,t = CargarFiltros(data)
    return jsonify({"z":z,"c":c,"t":t})

@app.route('/NewProc', methods=['POST'])
def Newfiltro():
    data = request.get_json()
    newdata = NewConsultas(data)
    return jsonify(newdata)


@app.route('/')
def index():
    return "Que haces aqui :/"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
