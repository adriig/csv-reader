import datetime

def lee_personas(fichero, lect=False):
    """File reading function

    Args:
        fichero (str): csv file which we will read
        lect (Bool): We will be able to decide what we want the function to return

    Returns:
        If lect==False --> We will get the first 3 and last 3 read elements from our document and the total number of elements read.
        If lect==True --> We will get the whole list.
    """
    personas = []
    
    with open(fichero, encoding='utf-8') as f:
        next(f, None)
        qty=0
        for linea in f:
            qty+=1
            _id, nombre, apellido, genero, pais, nacimiento, altura, peso, hobbies = linea.split(';')
            _id = int(_id) 
            #nacimiento = datetime.datetime.strptime(nacimiento.replace('/','-'), '%d-%m-%Y')
            altura = float(altura.replace(',','.'))
            peso = int(peso)
            tupla=(_id, nombre, apellido, genero, pais, nacimiento, altura, peso, hobbies)
            personas.append(tupla)
    if lect == False:
        return personas[:3],personas[-3:],qty
    else:
        return personas