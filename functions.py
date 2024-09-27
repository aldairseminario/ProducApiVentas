from conect import Consultar , EjecutarConsulta
import json

def tablatemp(s):
  if s == "mezqal":
    s = "ventas"
  elif s == "qarbon":
    s = "ventasQarbon"
  else:
    s = ""
  return s

def CargarFiltros(d):
    d = tablatemp(d)
    consulta = f"""SELECT DISTINCT Categoria, ZONA, TIPO FROM {d} WHERE `Tipodoc.` != "Nota de credito Boleta" AND `Tipodoc.` = "Nota de credito Factura";"""
    resp = Consultar(consulta)
    categorias = [row["Categoria"] for row in resp]
    zonas = [row["ZONA"] for row in resp]
    tipos = [row["TIPO"] for row in resp]
    # eliminar duplicados 
    categorias = list(set(categorias))
    zonas = list(set(zonas))
    tipos = list(set(tipos))
    #odenar
    categorias.sort()
    zonas.sort()
    tipos.sort()

    return categorias,zonas,tipos

def GenerarFiltro(data):
    f1 , f2 , d , c , z , t , s = data.get('fechaInicial') , data.get('fechaFinal') , data.get('dominio') , data.get('categorias') , data.get('zonas') , data.get('tipos') , data.get('dias')
    filtros = f"""WHERE `Tipodoc.` != "Nota de credito Boleta" AND `Tipodoc.` = "Nota de credito Factura" AND FECHAREAL BETWEEN '{f1}' AND '{f2}'"""
    if z != []:
        z = ', '.join(f'\'{zona}\'' for zona in z)
        filtros += f"AND ZONA in ({z})"
    if c != []:
        c = ', '.join(f'\'{categ}\'' for categ in c)
        filtros += f"AND Categoria in ({c})"
    if t != []:
        t = ', '.join(f'\'{tip}\'' for tip in t)
        filtros += f"AND TIPO in ({t})"
    if s != []:
        s = ', '.join(f'\'{dias}\'' for dias in s)
        filtros += f"AND DIASEMANA in ({s})"
    return filtros, d

def NewConsultas(data):
  filtros , d = GenerarFiltro(data)
  d = tablatemp(d)
  ConsulGraficas = (
    {
      "name":"ventasPorDia",
      "consulta":f"""SELECT 
                    concat('{{"fecha": "',date_format(FECHAREAL,'%Y-%m-%d'),'","total": ',sum(VENTABRUTA),',"alimentos": ',sum(case when TIPO = 'ALIMENTOS' then VENTABRUTA else 0 end),',"bebidas": ',sum(case when TIPO = 'BEBIDAS' then VENTABRUTA else 0 end),',"otros":',sum(case when TIPO = 'OTROS' then VENTABRUTA else 0 end),' }}') AS ventasxdia 
                    from {d} {filtros}
                    group by FECHAREAL;"""
     },
    {
      "name":"ventasPorProducto",
      "consulta":f"""SELECT 
                      CONCAT('{{"producto":"', Producto, '", "cantidad":"', SUM(Cantidad), '", "total":"', SUM(VENTABRUTA), '"}}') AS resultado 
                      FROM {d} {filtros} 
                      GROUP BY Producto ;"""
      }
    )
  Arrayjson = {}
  for consul in ConsulGraficas:
      result = EjecutarConsulta(consul['consulta'])
      datos = []
      for row in result:
          val=row[0]
          datos.append(json.loads(val))
          Arrayjson[f"{consul['name']}"] = datos
  return Arrayjson
