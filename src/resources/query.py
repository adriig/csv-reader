import datetime
import re
from collections import namedtuple
#from matplotlib import pylot as plt
from matplotlib import image as img
class Query:

    """Diccionario en el que almacenamos una serie de keys (que funcionarán como operadores) y su respectiva funcionalidad

    Returns:
        En función de la key retornará la función en forma de string (Que luego será interpretada)
    """
    operators={
        'gt':'float({}) < float({})',
        'lt':'float({}) > float({})',
        'gte':'float({}) <= float({})',
        'lte':'float({}) >= float({})',
        'eq':'"{}" == "{}"',
        'in':'"{}" in "{}".split(",")',
        'out':'"{}" not in "{}".split(",")',
        'before':'datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y") > datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y")',
        'after':'datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y") < datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y")'
    }

    checks={
        'gt':'"{}".isnumeric()',
        'lt':'"{}".isnumeric()',
        'gte':'"{}".isnumeric()',
        'lte':'"{}".isnumeric()',
        'eq':'1==1',
        'in':'1==1',
        'out':'1==1',
        'before':'datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y")',
        'after':'datetime.datetime.strptime("{}".replace("/","-"), "%d-%m-%Y")'
    }

    def __init__(self, database : str):
        self.database = database


    """ MÉTODOS PRINCIPALES (find y aggregate) """



    def find(self, query : dict):
        """Método find que iterará el csv establecido y nos permitirá filtrar cualquier campo.

        Args:
            query (dict): Recibirá como parámetro un diccionario que servirá de query, en el que el usuario introducirá key -> value para filtrar

        Returns:
            list(of tuples): Retornará una lista de tuplas en la que cada tupla será una de las líneas que superen el filtro.
        """
        resultado = []
        with open(self.database, encoding='utf-8') as file:
            headers = next(file, None).split(';')
            if (self.__query_check(query,headers)):
                for linea in file:
                    values = linea.split(';')
                    schema = self.__get_schema(headers, values)
                    if(self.__validate_schema_find(schema, query)):
                        resultado.append(schema)
                return resultado
            else:
                return "Formato de Query no válido"

    

    def aggregate(self, query : dict):
        """Método aggregate que funcionará como el find solo que de forma más compleja ya que podremos hacer comparativas complejas y no solamente match. Por ejemplo, podremos seleccionar según que campo sea mayor o menor

        Args:
            query (dict): Recibirá como parámetro un diccionario que servirá de query, en el que el usuario introducirá key -> value para filtrar

        Returns:
            _type_: Retornará una lista de tuplas en la que cada tupla será una de las líneas que superen el filtro.
        """
        resultado = []
        with open(self.database, encoding='utf-8') as file:
            headers = (next(file, None).replace('\n','')).split(';')
            if (self.__query_check_aggregate(query,headers)==True):
                for linea in file: 
                    values = (linea.replace('\n','')).split(';')
                    schema = self.__get_schema(headers, values)
                    if(self.__validate_schema_aggregate(schema, query)):
                        resultado.append(schema)
                return resultado



    """ MÉTODOS GENÉRICOS (__get_schema, __query_check)"""



    def __get_schema(self, headers : list, values: list):
        """Este método lo usaremos tanto para aggregate como para el find, lo usaremos para generar un diccionario key-value en base a los nombres de cada campo y al valor de cada variable dentro de la línea.
        Esta función será llamada línea por línea para así generar de forma ordenada nuestros Schemas con los que realizaremos el filtrado.

        Args:
            headers (list): Lista del nombre de los campos del csv. (Keys)
            values (list): Lista de los valores de una linea (Values)

        Returns:
            Schema(dict): Retornará un diccionario (Schema) compuesto de keys (nombre de campos del archivo csv) y sus respectivos values (valor de una determinada línea para cada uno de sus campos).
        """
        schema = {}
        for i in range (0, len(headers)):
            schema[headers[i]]=values[i]
        return schema

    
    
    def __query_check_find(self, query : dict, headers: list):
        """Gracias a __query_check podremos revisar que la query introducida tiene campos que se encuentran en el archivo csv.

        Args:
            query (dict): Query que realiza el usuario.
            headers (list): Lista de los campos del documento csv

        Returns:
            boolean: Retornará un booleano en función de si la query cumple los estándares. 
        """
        for e in query:
            if e not in headers:
                return False
        return True



    def __query_check_aggregate(self, query : dict, headers: list):
        """Gracias a __query_check podremos revisar que la query introducida tiene campos que se encuentran en el archivo csv.

        Args:
            query (dict): Query que realiza el usuario.
            headers (list): Lista de los campos del documento csv

        Returns:
            boolean: Retornará un booleano en función de si la query cumple los estándares. 
        """
        for e in query:
            if e not in headers:
                print ("Query header {} isn't a header in the csv file".format(e))
                return False
            for i in query[e]:
                try:
                    if (eval(self.checks[str(i['cond'])].format(i['value']))) == False:
                        print ("Incorrect query format: \n field: {} ---- value: {}".format(e, i['value']))
                        return False
                except ValueError:
                    print ("Incorrect query format: \n field: {} ---- value: {}".format(e, i['value']))
                    return False
        return True





    """ MÉTODOS ESPECÍFICOS (__validate_schema_find, __validate_schema_aggregate)"""


    
    def __validate_schema_find(self, schema : dict, query : dict):
        """__validate_schema_find se encargará de ver si el schema (La línea que estemos verificando) es igual o no que lo dispuesto en la query.

        Args:
            schema (dict): Diccionario compuesto de keys (nombre de campos del archivo csv) y sus respectivos values (valor de una determinada línea para cada uno de sus campos)
            query (dict): Query que realiza el usuario

        Returns:
            boolean: Retornará un False en caso de que alguno de las exigencias impuestas en la Query no se cumplan y finalmente un True para el caso de que ninguna de estas exigencias no se cumplan.
        """
        for e in query:
            if query[e] != int(schema[e]):
                return False
        return True



    def __validate_schema_aggregate(self, schema : dict, query : dict):
        """__validate_schema_aggregate se encargará de ver si el schema (La línea que estemos verificando) cumple las condiciones impuestas en la query.

        Args:
            schema (dict): Diccionario compuesto de keys (nombre de campos del archivo csv) y sus respectivos values (valor de una determinada línea para cada uno de sus campos)
            query (dict): Query que realiza el usuario

        Returns:
            _type_: Retornará un False en caso de que alguno de las exigencias impuestas en la Query no se cumplan y finalmente un True para el caso de que ninguna de estas exigencias no se cumplan.
        """
        for e in query:
            for i in query[e]:
                '''Accederemos al diccionario declarado al principio para mediante eval() desarrollar según la key que le pasemos como parámetro, su respectiva función'''
                if (eval(self.operators[str(i['cond'])].format(i['value'],schema[e])) == False):
                    return False 
        return True

    def queryCheck(self, diccionario: dict, headers: list):
        for e in diccionario:
            if e not in headers:
                return "Header {} isn't a header in the csv file".format(e)
            for i in diccionario[e]:
                try:
                    if (eval(self.checks[str(i['cond'])].format(i['value']))) == False:
                        return "Incorrect data format: \n field: {} ---- value: {}".format(e, i['value'])
                except ValueError:
                    return "Incorrect data format: \n field: {} ---- value: {}".format(e, i['value'])
        return True

query = Query('./data/personas.csv')
#print((query.find({'pais':'Norway', 'gender':'Female'})))

myTest={'id':[{'value': 566, 'cond': 'gte'}, {'value':990,'cond':'lte'}], 'fecha_nacimiento':[{'value':'22/06/2002','cond':'before'}], 'hobbies':[{'value':'yoga','cond':'out'}]}
#print(checkIfDate("19/04/2002"))
print(query.aggregate(myTest))
#print(query.queryCheck(myTest))