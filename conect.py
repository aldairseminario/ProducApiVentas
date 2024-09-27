from sqlalchemy import create_engine, text
import json

conexion = create_engine('mysql+pymysql://adsantafe_pruebarest:GUxFoJG(2;}#@www.vallesantafe.com.pe:3306/adsantafe_pruebarest')

def EjecutarConsulta(c):
    with conexion.connect() as conn:
        consulta = text(c)
        result = conn.execute(consulta)
    # rows = result.fetchall()
    # result = [row for row in rows]
    return result

def Consultar(c ,tipo=1):
    with conexion.connect() as conn:
        consulta = text(c)
        result = conn.execute(consulta)
        result_data = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    if int(tipo) == 0 and result_data:
        return result_data[0]
    return result_data
