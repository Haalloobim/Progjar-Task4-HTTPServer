import sys
import os.path
import uuid
from glob import glob
from datetime import datetime
import logging

class HttpServer:
	def __init__(self):
		self.sessions={}
		self.types={}
		self.types['.pdf']='application/pdf'
		self.types['.jpg']='image/jpeg'
		self.types['.jpg']='image/jpeg'
		self.types['.txt']='text/plain'
		self.types['.html']='text/html'
  
	def response(self,kode=404, message='Not Found', messagebody=bytes(), headers={}):
		tanggal = datetime.now().strftime('%c')
		resp=[]
		resp.append("HTTP/1.0 {} {}\r\n" . format(kode,message))
		resp.append("Date: {}\r\n" . format(tanggal))
		resp.append("Connection: close\r\n")
		resp.append("Server: myserver/1.0\r\n")
		resp.append("Content-Length: {}\r\n" . format(len(messagebody)))
		for kk in headers:
			resp.append("{}:{}\r\n" . format(kk,headers[kk]))
		resp.append("\r\n")

		response_headers=''
		for i in resp:
			response_headers="{}{}" . format(response_headers,i)
   
		if (type(messagebody) is not bytes):
			messagebody = messagebody.encode()

		response = response_headers.encode() + messagebody
		return response

	def proses(self,data):
		if isinstance(data, bytes):
			if b'\r\n\r\n' in data:
				headers_bytes, body = data.split(b'\r\n\r\n', 1)
				headers = headers_bytes.decode('utf-8')
			else:
				headers = data.decode('utf-8')
				body = b''
		else:
			if '\r\n\r\n' in data:
				headers, body_str = data.split('\r\n\r\n', 1)
				body = body_str.encode('utf-8')
			else:
				headers = data
				body = b''
            
		requests = headers.split("\r\n")
		#print(requests)

		baris = requests[0]
		#print(baris)

		all_headers = [n for n in requests[1:] if n!='']
		#print(all_headers)
		j = baris.split(" ")
		logging.warning(f"request: {j}")
		try:
			method=j[0].upper().strip()
			if (method=='GET'):
				object_address = j[1].strip()
				return self.http_get(object_address, all_headers)
			if (method=='POST'):
				object_address = j[1].strip()
				return self.http_post(object_address, all_headers, body)
			if (method=='DELETE'):
				object_address = j[1].strip()
				return self.http_delete(object_address, all_headers)
			else:
				return self.response(400,'Bad Request','',{})
		except IndexError:
			return self.response(400,'Bad Request','',{})


	def http_get(self,object_address,headers):
		files = glob('./upload/*')
		# print(files)
		thedir='./upload/'
		if (object_address == '/'):
			return self.response(200,'OK','Ini Adalah web Server percobaan',dict())

		if (object_address == '/video'):
			return self.response(302,'Found','',dict(location='https://youtu.be/katoxpnTf04'))
		if (object_address == '/santai'):
			return self.response(200,'OK','santai saja',dict())


		dirs = [item for item in os.listdir(thedir) if os.path.isdir(os.path.join('./', item))]
		object_address = object_address[1:]
        
		if object_address in dirs:
			isi_dir = os.listdir(object_address)
			respon = f"isi dir {object_address}: <br>" + "<br>".join(isi_dir)
			return self.response(200, 'OK', respon, {'Content-type': 'text/html'})
        
		if thedir+object_address not in files:
			return self.response(404, 'Not Found', object_address, {})
        
		fp = open(thedir+object_address,'rb')  # rb => artinya adalah read dalam bentuk binary
        # harus membaca dalam bentuk byte dan BINARY
		isi = fp.read()
        
		fext = os.path.splitext(thedir + object_address)[1]
		content_type = self.types[fext]
        
		headers = {}
		headers['Content-type'] = content_type
        
		return self.response(200, 'OK', isi, headers)


	def http_post(self,object_address,headers,body):
		# print(body)
		print(object_address)
		if object_address == '/upload':
			content_disposition = None
			for header in headers:
				if header.lower().startswith('filename:'):
					filename = header.split(':', 1)[1].strip()
					break
			else:
				filename = f"upload_{str(uuid.uuid4())}"
			print("->" + filename)
			filename = os.path.basename(filename)
			file_path = os.path.join('./upload', filename)
            
			try:
				if isinstance(body, str):
					body_bytes = body.encode()
				else:
					body_bytes = body
                
				with open(file_path, 'wb') as f:
					f.write(body_bytes)
                
				return self.response(200, 'OK', f"File {filename} uploaded successfully", 
                                    {'Content-type': 'text/plain'})
			except Exception as e:
				return self.response(500, 'Internal Server Error', f"Error saving file: {str(e)}", 
                                    {'Content-type': 'text/plain'})
		return self.response(400, 'Bad Request', "Invalid upload endpoint", {'Content-type': 'text/plain'})


	def http_delete(self, object_address, headers):
		files = glob('./upload/*')
		#print(files)
		thedir = './upload/'
        
		object_address = object_address[1:]
		if not os.path.exists(thedir+object_address):
			return self.response(404, 'Not Found', '', {})
		if not os.path.isfile(thedir+object_address):
			return self.response(400, 'Bad Request', 'Not a file', {})

		try:
			os.remove(thedir+object_address)
		except Exception as e:
			return self.response(500, 'Error', e, {})
        
		return self.response(200, 'OK', 'Deleted', headers)
		
			 	
#>>> import os.path
#>>> ext = os.path.splitext('/ak/52.png')

if __name__=="__main__":
	httpserver = HttpServer()
	d = httpserver.proses('GET /testing.txt HTTP/1.0\r\nini header\r\n\r\nini body')
	print(d)
    
	filepath='pokijan.jpg'
	with open(filepath, 'rb') as f:
		file_content = f.read()
	# print(file_content)
	headers_part = f'POST /upload HTTP/1.0\r\nFilename: {filepath}\r\n\r\n'
	d = httpserver.proses(headers_part.encode('utf-8') + file_content)
	print(d)
	#d = httpserver.http_get('testing2.txt',{})
	#print(d)
#	d = httpserver.http_get('testing.txt')
#	print(d)













