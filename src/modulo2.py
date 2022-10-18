import datetime
from select import select
from typing import Dict


def createQuery():
    print("Asistente de creación de Query, introduzca valor para cada campo o en caso de no querer utilizarlo introzuca N\n")

    complexQuery = dict()

    if input("¿Quiere introducir un filtro para pais Y/N: ") == "Y":
        complexQuery["pais['enabled']"]=True
        pais=input("Introduzca valor para pais: ")
        complexQuery["pais['name']"]= pais
        if input("Quiere filtrar según ese país o todos menos ese país 1/2: ") == "1":
            complexQuery["pais['condition']"]=True
        else:
            complexQuery["pais['condition']"]=False
    else: 
        complexQuery["pais['enabled']"]=False

    if input("¿Quiere introducir un filtro para edad Y/N: ") == "Y":
        complexQuery["edad['enabled']"]=True
        edad=int(input("Introduzca valor para edad: "))
        complexQuery["edad['name']"]= edad
        if input("Quiere filtrar con esa edad como máximo o como mínimo 1/2") == "1":
            complexQuery["edad['condition']"]=True
        else:
            complexQuery["edad['condition']"]=False
    else: 
        complexQuery["edad['enabled']"]=False

    if input("¿Quiere introducir un filtro para peso Y/N: ") == "Y":
        complexQuery["peso['enabled']"]=True
        peso=int(input("Introduzca valor para peso: "))
        complexQuery["peso['name']"]= peso
        if input("Quiere filtrar con ese peso como máximo o como mínimo 1/2") == "1":
            complexQuery["peso['condition']"]=True
        else:
            complexQuery["peso['condition']"]=False
    else: 
        complexQuery["peso['enabled']"]=False

    return complexQuery

def customQuery(fichero, query):
    personas=[]
    with open(fichero, encoding='utf-8') as f:
        next(f, None)
        for linea in f:
            selectable=True
            _id, nombre, apellido, genero, pais, nacimiento, altura, peso, hobbies = linea.split(';')
            if query["pais['enabled']"]==True:
                if query["pais['condition]"]==True:
                    if pais != query["pais['name']"]:
                        selectable=False
                else:
                    if pais == query["pais['name']"]:
                        selectable=False
            
            if query["edad['enabled']"]==True:
                nacimiento = datetime.datetime.strptime(nacimiento.replace('/','-'), '%d-%m-%Y')
                today = datetime.date.today()
                edad = today.year - nacimiento.year - ((today.month, today.day) < (nacimiento.month, nacimiento.day))
                if query["edad['condition']"]==True:                    
                    if query["edad['name']"] < edad:
                        selectable=False
                else:
                    if query["edad['name']"] > edad:
                        selectable=False
            if(selectable==True):
                tupla=(_id, nombre, apellido, genero, pais, nacimiento, altura, peso, hobbies)
                personas.append(tupla)
    return personas