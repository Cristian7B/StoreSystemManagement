from provisionalInputs import *


def sortStatsWeek(statsWeek):
    data = statsWeek.get("porSemana")
    
    for semana in data:
        semana["articulos"].sort(key = lambda articulo:articulo["total"], reverse = True)
        semana["compradores"].sort(key = lambda comprador:comprador["total"], reverse = True)

    return {"porSemana": data}


def productoRegistrado(data, codigo):
    for i in range(len(data)):
        if data[i]["codigo"] == codigo:
            return i  
    return False 


def valorProducto(codigo):
    for producto in productsGeneral:
        if producto["codigo"] == codigo:
            return producto["valor"]
        

def divideDaysByDate(data_customer):
    dataDate = {}
    arrayFromDay = []
    for customerDay in data_customer:
        fechaActual = customerDay["fecha"]
        if not fechaActual in dataDate:
            dataDate[fechaActual] = len(arrayFromDay)
            arrayFromDay.append({fechaActual: []})
        arrayFromDay[dataDate[fechaActual]][fechaActual].append(customerDay)
    
    return arrayFromDay


def knowTopFromDay(dataDays):
    statsByDay = {"porDia": []}
    for fecha in dataDays:
        for day in fecha.values():
            greatestCustomer = {}
            totalSum = 0
            dulceCantidad = 0
            for dataCustomer in day: 
                if dataCustomer["nombre"]:
                    partialSum = 0
                    for product in dataCustomer["compras"]:
                        cantidadProduct = product["cantidad"]
                        for productCode in productsGeneral:
                            if productCode["codigo"] == product["codigo"]:
                                partialSum += productCode["valor"] * cantidadProduct
                                if cantidadProduct > dulceCantidad:
                                    dulceCantidad = cantidadProduct
                                    greatestCustomer["dulce"] = productCode["nombre"]
                    if partialSum > totalSum:
                        totalSum = partialSum
                        greatestCustomer["nombre"] = dataCustomer["nombre"]
            greatestCustomer["fecha"] = list(fecha.keys())[0]
            statsByDay["porDia"].append(greatestCustomer)
    statsByDay["porDia"].sort(key=lambda day: int(day["fecha"].split("-")[2]))
    return statsByDay

"""
Dividir los días en semanas, se toma como referencia el mes de Octubre de 2024
donde el 1 de Octubre es Martes, y hay 4 Domingos(6, 13, 20, 27)
"""

def divideWeekByDate(dataFromDays):
    sundaysAtMonth = [(1, 6), (7, 13), (14, 20), (21, 27)]
    arrayForWeeks = [[], [], [], []]
    i = 0
    for fecha in dataFromDays:
        fechaArray = list(fecha.keys())[0].split("-")
        for i in range(4):
            if int(fechaArray[2]) >= sundaysAtMonth[i][0] and int(fechaArray[2]) <= sundaysAtMonth[i][1]:
                for day in fecha.values():
                    for customer in day:
                        arrayForWeeks[i].append(customer)
    return arrayForWeeks

def getStatsWeek(dataFromEachWeek):
    weekStats = {"porSemana": []}
    semanaActual = 1
    for i in range(4):  
        semana = {
            "semana": semanaActual, 
            "compradores": [], 
            "articulos": []
        }
        for data in dataFromEachWeek[i]:
            comprador = {
                "nombre": data["nombre"],
                "total": 0
            }
            for compra in data["compras"]:
                codigoProducto = compra["codigo"]
                articuloIndice = productoRegistrado(semana["articulos"], codigoProducto)
                if articuloIndice != False:
                    semana["articulos"][articuloIndice]["total"] += valorProducto(codigoProducto)*compra["cantidad"]
                else:
                    articulo = {
                        "codigo": codigoProducto,
                        "total": valorProducto(codigoProducto)*compra["cantidad"]
                    }
                    semana["articulos"].append(articulo)
                cantidadProduct = compra["cantidad"]
                comprador["total"] += valorProducto(codigoProducto) * cantidadProduct
                    
            semana["compradores"].append(comprador)
        weekStats["porSemana"].append(semana)
        semanaActual += 1
    
    return weekStats

