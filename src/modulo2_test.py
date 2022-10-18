from modulo2 import createQuery
from modulo1 import lee_personas
from modulo2 import customQuery

# query=createQuery()
# list=lee_personas('./proyecto-python-1c-adriig/data/personas.csv')
# customQuery(list, query)

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print( n, 'equals', x, '*', n/x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')