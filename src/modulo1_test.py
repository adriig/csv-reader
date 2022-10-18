import datetime
import os
from modulo1 import lee_personas
#os.chdir('C:\\Users\\sonto\\Desktop\\Python-Uni\\proyecto-python-1c-adriig')
#print(os.getcwd())
feedback=lee_personas('./proyecto-python-1c-adriig/data/personas.csv')
print('''
Primeros 3 registros: 
    {}
            
Últimos 3 registros:
    {}
            
Cantidad de Elementos Leídos: {}'''.format(feedback[0],feedback[1],feedback[2]))
