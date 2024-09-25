from flask import Flask , jsonify, send_file, Response
from base import DescargarDatos , JsonVentas,JsonVentasxMes , Jsonproductosxdia , JsonTotal
from flask_cors import CORS
import pandas as pd



app = Flask(__name__)

CORS(app)

@app.route('/datos')
def EnviarDatos():
    #return send_file("resultados.csv", mimetype='text/csv')
    df = pd.read_csv('resultados.csv')
    text_output = df.to_string(index=False)
    return Response(text_output, mimetype='text/plain')

@app.route('/json')
def DatosJson():
    ventas = JsonVentas()
    return jsonify(ventas)

@app.route('/ventasxmes')
def ventasxmes():
    ventas = JsonVentasxMes()
    return jsonify(ventas)

@app.route('/productosxdia')
def productosxdia():
    ventas = Jsonproductosxdia()
    return jsonify(ventas)

@app.route('/total')
def total():
    ventas = JsonTotal()
    return jsonify(ventas)
    

@app.route('/')
def index():
    return "Que haces aqui :/"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
