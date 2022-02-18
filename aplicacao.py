# Caminhos 

# Endereço da imagem a ser transmitida
imageR = "img/nubank.png"
# Endereço da imagem a ser salva
# imageW = "img/nubankCopia.png"

# lista de bytes com a imagem a ser transmitida

# carrega imagem
print("Carregando imagem para a transmissão :")
print(" - {}".format(imageR))
print("----------------------")
txBuffer = open(imageR, 'rb').read()

# Escreve o arquivo cópia

# print("Salvando dados no arquivo :")
# print(" - {}".format(imageW))
# f = open(imageW, 'wb')
# f.write(rxBuffer)
# # fecha o arquivo de imagem
# f.close()
