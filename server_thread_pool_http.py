from socket import *
import socket
import time
import sys
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

httpserver = HttpServer()

#untuk menggunakan threadpool executor, karena tidak mendukung subclassing pada process,
#maka class ProcessTheClient dirubah dulu menjadi function, tanpda memodifikasi behaviour didalamnya

def ProcessTheClient(connection,address):
    try:
        header_data = b''
        content_length = 0
        body = b''
        
        while True:
            chunk = connection.recv(1024)
            if not chunk:
                break
                
            header_data += chunk
            
            if b'\r\n\r\n' in header_data:
                headers_part, body_part = header_data.split(b'\r\n\r\n', 1)
                headers_text = headers_part.decode('utf-8')
                
                for line in headers_text.split('\r\n'):
                    if line.lower().startswith('content-length:'):
                        content_length = int(line.split(':', 1)[1].strip())
                        break
                
                body = body_part
                break
        
        if content_length > 0:
            while len(body) < content_length:
                chunk = connection.recv(min(65535, content_length - len(body)))
                if not chunk:
                    break
                body += chunk
        
        complete_data = headers_part + b'\r\n\r\n' + body
        
        hasil = httpserver.proses(complete_data)
        
        hasil = hasil + b"\r\n\r\n"
        connection.sendall(hasil)
    except Exception as e:
        print(f"Error processing client: {e}")
    finally:
        connection.close()



def Server():
	the_clients = []
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	my_socket.bind(('0.0.0.0', 8885)) 
	my_socket.listen(10)
    
	logging.warning("Server is listening on port 8885")
	with ThreadPoolExecutor(20) as executor:
		while True:
			connection, client_address = my_socket.accept()
			logging.warning(f"connection from {client_address}")
			p = executor.submit(ProcessTheClient, connection, client_address)
			the_clients.append(p)
			# Menampilkan jumlah thread yang sedang aktif
			jumlah = ['x' for i in the_clients if i.running()==True]
			print(jumlah)





def main():
    Server()

if __name__=="__main__":
    main()