#lista = [n*n for n in range(100000000)]

lista = (n*n for n in range(100000000))

for i, x in enumerate(lista):
    print(i,x)