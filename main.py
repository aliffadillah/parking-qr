def open_image(image_path):
  try:
    img = Image.open(image_path)
    return img
  except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found.")
    return None
  except Exception as e:
    print(f"Error opening image: {e}")
    return None

def create_parking_ticket_jpg(kodParking,kodeTiket,qr_file_path, tgl_masuk, output_file):
    img = np.zeros((400, 400, 3), np.uint8)
    img[:] = 255

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (0, 0, 0)
    now = datetime.datetime.now()
    tanggal = now.strftime("%d %B %Y") 
    waktu = now.strftime("%H:%M:%S")

   
    cv2.putText(img, 'TANDA MASUK - UNIVERSITAS IPWIJA', (50, 50), font, font_scale, color, 2)
    cv2.putText(img,f"="*23,(50, 70), font, font_scale, color, 2)
    cv2.putText(img,f"Nomor Tiket    : {kodeTiket}", (50, 100), font, font_scale, color, 2)
    cv2.putText(img, f"Tanggal Masuk : {tanggal}", (50, 120), font, font_scale, color, 2)
    cv2.putText(img, f"Waktu Masuk   : {waktu}", (50, 140), font, font_scale, color, 2)
    cv2.putText(img, f"           {kodParking}", (50, 320), font, font_scale, color, 2)
    cv2.putText(img,f"="*23,(50, 360), font, font_scale, color, 2)
    cv2.putText(img, "Terima kasih ", (50, 380), font, font_scale, color, 2)

    try:
        qr_img = cv2.imread(qr_file_path)
    except (FileNotFoundError, cv2.error):
        print(f"Error: QR code image '{qr_file_path}' not found or invalid.")
        return 
    
    img_width = 350 
    qr_img = cv2.resize(qr_img, (150, 150))
    qr_x = (img_width - 100) // 2
    qr_y = 150

    img[qr_y:qr_y+150, qr_x:qr_x+150] = qr_img

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  
    draw = ImageDraw.Draw(pil_img)
    pil_img.save(output_file)

def capture(nama_file):
    '''Fungsi Ini Berguna untuk mengambil foto kendaraan saat masuk dan keluar'''
    

def gen_kode_parking(panjang):
    '''Fungsi Ini Berguna untuk membuat kode parkir'''

def check_file(file_path):
    '''Fungsi Ini Berguna untuk melakukan check file'''

def save_parking(parking):
    '''Fungsi Ini Berguna untuk menyimpan data parking ke dalam excel'''

def gen_QRcode (data, filename):
    '''Fungsi Ini Berguna untuk membuat QR Code'''
    
def validate_nomor_kendaraan(nomor_kendaraan):
    '''Fungsi Ini Berguna untuk validasi nomor kenadaraan'''

def masuk(tgl_masuk,nama_petugas):
    '''Fungsi Ini Berguna untuk proses masuk kenadaraan''' 
def keluar_parkir(qrCode):
    '''Fungsi Ini Berguna untuk proses Keluar kenadaraan'''
        
def baca_tiket():
    '''Fungsi Ini Berguna untuk proses membaca Tiker Parkir kenadaraan'''
    

while True:
    print("*"*100)
    print("Ujian Akhir Semester - Dasar Pemrograman")
    print("*"*100)
    print("Nama : Muhammad Maulana Rachman")
    print("Kelas : Rekayasa Perangakt Lunak - RK231")
    print("*"*100,"\n")
    print("*"*100)
    print("Sistem Parking Universitas IPWIJA")
    print("*"*100)
    tanggal_waktu = datetime.datetime.now()
    tgl_masuk = tanggal_waktu.strftime("%Y-%m-%d %H:%M:%S")
    print("Nama Petugas: Muhammad Maulana Rachman")
    nama_petugas = "Muhammad Maulana"
    print("Tanggal Operation: ",tgl_masuk)
    print("*"*100)
    print("1. Parkir Masuk: ")
    print("2. Parkir Keluar: ")
    pilihan = int(input("Masukan Pilihan : "))
    print("*"*100)
    if pilihan == 1:
        masuk(tgl_masuk,nama_petugas)
    elif pilihan == 2:
        baca_tiket()
    else:
        print("Ada salah Masukan Pilihan")