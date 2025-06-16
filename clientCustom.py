import socket
import sys
import os

def list_files(host, port, directory_path):
    """Mengirim permintaan GET untuk melihat daftar file."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        request = f"GET {directory_path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        sock.sendall(request.encode())

        response = sock.recv(4096).decode()
        print("--- Server Response ---")
        print(response)
    finally:
        sock.close()

def upload_file(host, port, file_path):
    """Mengirim permintaan POST untuk mengunggah file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            file_content = f.read()

        boundary = b"----ClientBoundary123"
        
        # Bangun body request dalam bentuk bytes
        body_parts = [
            b'--' + boundary,
            f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode(),
            b'Content-Type: application/octet-stream',
            b'',
            file_content,
            b'--' + boundary + b'--',
            b''
        ]
        body = b'\r\n'.join(body_parts)

        # Bangun header request
        headers_str = "\r\n".join([
            f"POST /upload HTTP/1.1",
            f"Host: {host}",
            f"Content-Type: multipart/form-data; boundary={boundary.decode()}",
            f"Content-Length: {len(body)}"
        ])
        request = headers_str.encode() + b"\r\n\r\n" + body
        
        sock.sendall(request)

        response = sock.recv(4096).decode()
        print("--- Server Response ---")
        print(response)

    finally:
        sock.close()

def delete_file(host, port, file_path_on_server):
    """Mengirim permintaan DELETE untuk menghapus file."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        request = f"DELETE {file_path_on_server} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        sock.sendall(request.encode())

        response = sock.recv(4096).decode()
        print("--- Server Response ---")
        print(response)
    finally:
        sock.close()

def main():
    if len(sys.argv) < 5:
        print("Penggunaan: python client_custom.py <host> <port> <command> [args]")
        print("Perintah:")
        print("  list   <directory_path>     -> Melihat daftar file di direktori")
        print("  upload <local_file_path>     -> Mengunggah file ke server")
        print("  delete <server_file_path>    -> Menghapus file di server")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]
    path = sys.argv[4]

    if command == 'list':
        list_files(host, port, path)
    elif command == 'upload':
        upload_file(host, port, path)
    elif command == 'delete':
        delete_file(host, port, path)
    else:
        print(f"Perintah '{command}' tidak valid.")
        sys.exit(1)

if __name__ == "__main__":
    main()