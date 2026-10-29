import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Konfigurasi Koneksi MySQL XAMPP
DB_CONFIG = {
    'host': 'db',
    'user': 'root',      # Default user XAMPP
    'password': 'root',      # Default password XAMPP (kosong)
    'database': 'kantin_db'
}

def init_db():
    try:
        # 1. Koneksi awal tanpa database untuk memastikan 'kantin_db' sudah terbuat
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        conn.close()

        # 2. Koneksi ke database kantin_db untuk membuat tabel
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255) NOT NULL,
                harga INT NOT NULL,
                kategori VARCHAR(100) NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pesanan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_pemesan VARCHAR(255) NOT NULL,
                menu_id INT NOT NULL,
                jumlah INT NOT NULL,
                total_harga INT NOT NULL,
                metode_pembayaran VARCHAR(50) DEFAULT 'Tunai',
                status_pembayaran VARCHAR(50) DEFAULT 'Belum Bayar',
                status VARCHAR(50) DEFAULT 'Diproses',
                FOREIGN KEY (menu_id) REFERENCES menu(id) ON DELETE CASCADE
            )
        ''')

        # Tambahkan sampel menu awal jika tabel masih kosong
        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            sample_menu = [
                ('Nasi Goreng Spesial', 18000, 'Makanan'),
                ('Ayam Geprek Sambal Matah', 15000, 'Makanan'),
                ('Mie Ayam Bakso', 13000, 'Makanan'),
                ('Es Teh Manis Jumbo', 5000, 'Minuman'),
                ('Kopi Milk Brown Sugar', 12000, 'Minuman'),
                ('Matcha Latte Ice', 15000, 'Minuman')
            ]
            cursor.executemany("INSERT INTO menu (nama, harga, kategori) VALUES (%s, %s, %s)", sample_menu)

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error Database: {err}")

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu ORDER BY id DESC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/pesan', methods=['POST'])
def pesan():
    nama_pemesan = request.form['nama_pemesan']
    menu_id = int(request.form['menu_id'])
    jumlah = int(request.form['jumlah'])
    metode_pembayaran = request.form['metode_pembayaran']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT harga FROM menu WHERE id = %s", (menu_id,))
    harga = cursor.fetchone()['harga']
    total_harga = harga * jumlah

    cursor.execute('''
        INSERT INTO pesanan (nama_pemesan, menu_id, jumlah, total_harga, metode_pembayaran)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nama_pemesan, menu_id, jumlah, total_harga, metode_pembayaran))

    conn.commit()
    pesanan_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return redirect(url_for('pembayaran', pesanan_id=pesanan_id))

@app.route('/pembayaran/<int:pesanan_id>')
def pembayaran(pesanan_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT pesanan.*, menu.nama AS nama_menu
        FROM pesanan
        JOIN menu ON pesanan.menu_id = menu.id
        WHERE pesanan.id = %s
    ''', (pesanan_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('pembayaran.html', data=data)

@app.route('/konfirmasi-bayar/<int:pesanan_id>')
def konfirmasi_bayar(pesanan_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE pesanan SET status_pembayaran = 'Lunas' WHERE id = %s", (pesanan_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pembayaran', pesanan_id=pesanan_id))

@app.route('/dapur')
def dapur():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil daftar pesanan masuk
    cursor.execute('''
        SELECT pesanan.id, pesanan.nama_pemesan, menu.nama AS nama_menu, 
               pesanan.jumlah, pesanan.total_harga, pesanan.metode_pembayaran,
               pesanan.status_pembayaran, pesanan.status
        FROM pesanan
        JOIN menu ON pesanan.menu_id = menu.id
        ORDER BY pesanan.id DESC
    ''')
    daftar_pesanan = cursor.fetchall()

    # Ambil daftar menu yang tersedia
    cursor.execute("SELECT * FROM menu ORDER BY id DESC")
    daftar_menu = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('dapur.html', daftar_pesanan=daftar_pesanan, daftar_menu=daftar_menu)

@app.route('/selesai/<int:pesanan_id>')
def selesai(pesanan_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE pesanan SET status = 'Selesai' WHERE id = %s", (pesanan_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dapur'))

@app.route('/tambah-menu', methods=['POST'])
def tambah_menu():
    nama = request.form['nama']
    harga = int(request.form['harga'])
    kategori = request.form['kategori']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO menu (nama, harga, kategori)
        VALUES (%s, %s, %s)
    ''', (nama, harga, kategori))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dapur'))

@app.route('/hapus-menu/<int:menu_id>')
def hapus_menu(menu_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id = %s", (menu_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dapur'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)