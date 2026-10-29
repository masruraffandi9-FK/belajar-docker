# 1. Gunakan Python versi resmi
FROM python:3.10-slim

# 2. Tentukan direktori kerja di dalam container
WORKDIR /app

# 3. Salin requirements.txt dan install library yang dibutuhkan
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Salin seluruh kode proyek ke dalam container
COPY . .

# 5. Buka port 5000 (port standar Flask)
EXPOSE 5000

# 6. Perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]