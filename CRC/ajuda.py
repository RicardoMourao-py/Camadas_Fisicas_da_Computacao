lista = []
for i in range(1,1200):
    lista.append(i)
lista2 = [lista[i:i + 114] for i in range(0, len(lista), 114)]
print(lista2)

lista = []
for i in range(0, len(lista), 114):
    lista.append(lista[i:i + 114])