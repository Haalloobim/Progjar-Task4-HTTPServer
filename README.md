# 🕸️ HTTP Server with Thread and Process Pool

## 📋 Deskripsi

Proyek ini mengimplementasikan HTTP Server menggunakan Python `socket`, yang mendukung penanganan koneksi secara *concurrent* baik dengan **thread pool** maupun **process pool**. Server ini dirancang untuk melayani permintaan HTTP dasar seperti `GET`, `POST` (unggah file), dan `DELETE`.

---

## 🧩 Fitur

- Server mendengarkan koneksi pada port yang dapat dikonfigurasi:
  - `8885` untuk *Thread Pool*
  - `8889` untuk *Process Pool*
- Mendukung metode:
  - `GET` → Mengambil file atau melihat isi direktori
  - `POST` → Mengunggah file ke server
  - `DELETE` → Menghapus file dari server
- Penanganan konkurensi menggunakan:
  - **`ThreadPoolExecutor`** → `server_thread_pool_http.py`
  - **`ProcessPoolExecutor`** → `server_process_pool_http.py`
- Penanganan permintaan HTTP dan pembuatan respons dikelola oleh kelas `HttpServer`

---

## 🚀 Cara Menjalankan Program

### 1. Jalankan Server

🔹 **Menggunakan Thread Pool (Port 8885)**

    python Progjar-Task4-HTTPServer/server_thread_pool_http.py

> Output akan menampilkan log koneksi yang masuk dan jumlah thread aktif.

🔹 **Menggunakan Process Pool (Port 8889)**

    python Progjar-Task4-HTTPServer/server_process_pool_http.py

> Output akan menampilkan jumlah proses yang aktif.

---

### 2. Jalankan Client

Gunakan `clientCustom.py` untuk berinteraksi dengan server. Format perintah:

    python Progjar-Task4-HTTPServer/clientCustom.py <host> <port> <command> [args]

#### 📘 Perintah yang Tersedia

- `list <directory_path>`  
  Melihat daftar file di direktori server  
  Contoh:  
      python clientCustom.py localhost 8885 list upload

- `upload <local_file_path>`  
  Mengunggah file dari lokasi lokal ke server  
  Contoh:  
      python clientCustom.py localhost 8885 upload src/test.txt

- `delete <server_file_path>`  
  Menghapus file di server  
  Contoh:  
      python clientCustom.py localhost 8885 delete test.txt

---

## 📦 Contoh Output (Client)

### 🔼 Mengunggah File (POST)

    python clientCustom.py localhost 8885 upload src/test.txt

**Output:**

    HTTP/1.0 200 OK
    Date: Fri Jun 20 11:11:50 2025
    Connection: close
    Server: myserver/1.0
    Content-Length: 33
    Content-type: text/plain

    File test.txt uploaded successfully

---

### 📂 Melihat Daftar File (GET)

    python clientCustom.py localhost 8885 list upload

**Output:**

    HTTP/1.0 200 OK
    Date: Fri Jun 20 11:11:50 2025
    Connection: close
    Server: myserver/1.0
    Content-Length: 26
    Content-type: text/html

    isi dir upload: <br>test.txt

---

### ❌ Menghapus File (DELETE)

    python clientCustom.py localhost 8885 delete test.txt

**Output:**

    HTTP/1.0 200 OK
    Date: Fri Jun 20 11:11:50 2025
    Connection: close
    Server: myserver/1.0
    Content-Length: 7

    Deleted

---

## 🔒 Catatan Keamanan

> Untuk penggunaan di lingkungan produksi:
- Pastikan port server tidak diekspos ke publik tanpa alasan yang jelas
- Gunakan autentikasi dan enkripsi untuk meningkatkan keamanan

---

## 👨‍💻 Author

- **Nama**: Muhammad Bimatara Indianto 
- **Tugas**: Implementasi HTTP Server dengan Thread dan Process Pool  
- **Mata Kuliah**: Pemrograman Jaringan
