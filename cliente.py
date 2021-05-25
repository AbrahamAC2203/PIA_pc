import socket
import requests
import os
import logging
import argparse




# def metadatos(nombre):
# 	print("aqui va toda la funcion y el nombre del archivo pa abrir es: ", archivo)
def scrap(url):
	r = requests.get(url)

	with open("url.txt", 'w') as pagina:
		pagina.write(r.text)

	with open("url_headers.txt", 'w') as pagina:
		#pagina.write(r.headers)
		for i in r.headers:
			pagina.write(f"{i} : {r.headers[i]}\n")

def connect():
	ip = '127.0.0.1'
	port = 5018
	BUFFER_SIZE = 2048
	logging.basicConfig(filename='historial.log', level=logging.INFO)


	
	while True:
		mensaje = input("#>: ")
		logging.info(f'comando enviado: {mensaje}')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, port))

		if mensaje == 'ss':
			s.send(mensaje.encode())
			with open("ss_recibida.png", 'wb') as file_to_write:
				while True:
					data = s.recv(BUFFER_SIZE)
					if not data:
						break
					file_to_write.write(data)
				file_to_write.close()
		else:
			s.send(mensaje.encode())
			r = s.recv(BUFFER_SIZE).decode()
			logging.info(f'mensaje recibido: {r}')
			print(r)
		s.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS, help="usted puede realizar los siguientes comandos: con -h busca la ayuda de ejecución del programa, con -webscrap y -url ingresa a la función que hace el webscrapping de el url proveído, si no ingresa argumentos, se va a la terminal de PS")
	#parser.add_argument("-webs", "-webscrapping", metavar='webscrap', dest='webscrap', help="este argumento llama a la función para hacer el webscraping")
	parser.add_argument("-url", "-link", metavar='url', dest='url', help="este argumento es necesario cuando se quiere invocar al webscraping")
	args = parser.parse_args()
	url = args.url
	if url:
		args.webscrap = scrap(url)
	else:
		connect()
	
