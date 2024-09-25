from sqlalchemy import create_engine, text
import csv
import json

conexion = create_engine('mysql+pymysql://adsantafe_pruebarest:GUxFoJG(2;}#@www.vallesantafe.com.pe:3306/adsantafe_pruebarest')

def DescargarDatos():
    with conexion.connect() as conn:
        consulta = text("SELECT * FROM reporte")
        result = conn.execute(consulta)
        columnas = result.keys()
        with open('resultados.csv', 'w', newline='', encoding='utf-8') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(columnas)
          for fila in result:
              writer.writerow(fila)
          print("Datos exportados a resultados.csv")

def JsonVentas():
  with conexion.connect() as conn:
    consulta = text("SELECT * FROM JsonVentas")
    result = conn.execute(consulta)
    ventas = []
    for row in result:
      ventas.append(json.loads(row[0]))
    return ventas
  # print(json.loads(ventas[1]))
  
def Jsonproductosxdia():
  with conexion.connect() as conn:
    consulta = text("SELECT * FROM Productoxdia")
    result = conn.execute(consulta)
    ventas = []
    for row in result:
      ventas.append(json.loads(row[0]))
    return ventas


def JsonVentasxMes():
  with conexion.connect() as conn:
    consulta = text("SELECT * FROM ventasxdia")
    result = conn.execute(consulta)
    ventas = []
    for row in result:
      val = row[0].decode('utf-8')
      ventas.append(json.loads(val))
    return ventas


def JsonTotal():
  consultas = (
    {
      "name":"ventasPorDia",
     "consulta":"SELECT * FROM NewVentasxDia"
     },
    {
      "name":"ventasPorProducto",
     "consulta":"SELECT * FROM Productoxdia"
     }
    )
  Arrayjson = {}
  for consul in consultas:
    with conexion.connect() as conn:
      consulta = text(f"{consul['consulta']}")
      result = conn.execute(consulta)
      datos = []
      for row in result:
        try:
            val = row[0].decode('utf-8')
        except:
          val=row[0]
        datos.append(json.loads(val))
        Arrayjson[f"{consul['name']}"] = datos
  return Arrayjson
  
      


    

# JsonTotal()
  



        
