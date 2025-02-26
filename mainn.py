import datetime
import pandas as pd
import openpyxl as op
import os
import qrcode
from PIL import Image
import string
import random as rd
from pyzbar.pyzbar import decode
import cv2
import re
import numpy as np


# Helper Functions
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


def create_parking_ticket_jpg(KodParking, KodeTiket, qr_file_path, tgl_masuk, output_file):
    img = np.zeros((400, 400, 3), np.uint8)
    img[:] = 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (0, 0, 0)

    cv2.putText(img, "TANDA MASUK PARKIR", (50, 50), font, font_scale, color, 2)
    cv2.putText(img, f"Nomor Tiket: {KodeTiket}", (50, 100), font, font_scale, color, 2)
    cv2.putText(img, f"Tanggal Masuk: {tgl_masuk}", (50, 120), font, font_scale, color, 2)
    cv2.putText(img, f"Kode Parkir: {KodParking}", (50, 140), font, font_scale, color, 2)

    try:
        qr_img = cv2.imread(qr_file_path)
        if qr_img is None:
            print(f"Error: QR code file '{qr_file_path}' not found.")
            return
        qr_img = cv2.resize(qr_img, (100, 100))
        img[150:250, 150:250] = qr_img
    except Exception as e:
        print(f"Error reading QR code: {e}")
        return

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not output_file.lower().endswith(".jpg"):
        output_file += ".jpg"  # Ensure valid file extension
    pil_img.save(output_file)


def capture(nama_file):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible.")
        return False

    ret, frame = cap.read()
    if ret:
        waktu_sekarang = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, waktu_sekarang, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if not nama_file.lower().endswith(".jpg"):
            nama_file += ".jpg"  
        if cv2.imwrite(nama_file, frame):
            cap.release()
            return True
        else:
            print("Failed to save file.")
    cap.release()
    return False


def gen_kode_parking(panjang):
    karakter = string.ascii_uppercase + string.digits
    kode = ''.join(rd.choice(karakter) for _ in range(panjang))
    return kode


def check_file(file_path):
    return os.path.exists(file_path)


def save_parking(parking):
    path = "database"
    fileName = "Data_Parking.xlsx"
    if not os.path.exists(path):
        os.makedirs(path)

    dfParking = pd.DataFrame(parking)
    try:
        dfEx = pd.read_excel(f"{path}/{fileName}")
        dfParking = pd.concat([dfEx, dfParking], ignore_index=True)
    except FileNotFoundError:
        pass
    dfParking.to_excel(f"{path}/{fileName}", index=False, sheet_name="Data_Parking")


def genQrcode(data, fileName):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    if not fileName.lower().endswith(".png"):
        fileName += ".png"  # Ensure valid file extension
    img_qr.save(fileName)


def validate_nomor_kendaraan(nomor_kendaraan):
    pattern = r'^[A-Z]{1}\d{4}[A-Z]{3}$'
    # Hilangkan spasi sebelum validasi
    nomor_kendaraan = nomor_kendaraan.replace(" ", "").upper()
    return bool(re.match(pattern, nomor_kendaraan))


# Main Functions
def masuk(tgl_masuk, nama_petugas):
    kodParking = gen_kode_parking(12)
    kodTiket = gen_kode_parking(4)
    NoKendaraan = input("Masukkan Nomor Kendaraan: ").replace(" ", "").upper()
    
    if validate_nomor_kendaraan(NoKendaraan):
        path = "qrcode"
        pathCapture = "capture"
        pathTiket = "karcis"

        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(pathCapture):
            os.makedirs(pathCapture)
        if not os.path.exists(pathTiket):
            os.makedirs(pathTiket)

        nameQr = f"{kodParking}.png"
        nameFile = os.path.join(path, nameQr)
        nameCapture = os.path.join(pathCapture, f"{kodParking}.jpg")
        namaTicket = f"{kodTiket}.jpg"
        fileTiket = os.path.join(pathTiket, namaTicket)

        genQrcode(kodParking, nameFile)
        capture(nameCapture)
        create_parking_ticket_jpg(kodParking, kodTiket, nameFile, tgl_masuk, fileTiket)

        parking = {
            'Kode_parking': [kodParking],
            'No_kendaraan': [NoKendaraan],
            'jenis_kendaraan': [""],
            'Waktu_masuk': [tgl_masuk],
            'Waktu_keluar': [""],
            'Durasi': [""],
            'Biaya': [""],
            'Nama_petugas': [nama_petugas],
            'Foto_masuk': [nameCapture],
            'Foto_keluar': [""],
        }

        save_parking(parking)
        print("Ticket generated successfully!")
    else:
        print("Nomor kendaraan tidak valid. Harap masukkan nomor kendaraan tanpa spasi atau karakter tambahan.")

def update_data_parkir(fileExcel,id_parkir, jenis_kendaraan, waktu_keluar, durasi, biaya, foto_keluar):
    dfparkir = pd.read_excel(fileExcel,sheet_name="Data_Parking")
    dfparkir['Jenis_Kendaraan'] = dfparkir['Jenis_kendaraan'].astype('object')

    #cari data berdasarkan ID parkir
    index = dfparkir[dfparkir['kode_parking'] == id_parkir].index
    if index.empty:
        print("\n")
        print("+"*100)
        print("\t\t\tData Parkir tidak ditemukan.")
        print("+"*100)
        print("\n")

        return
    
    dfparkir.loc[index, 'jenis kendaraan'] = jenis_kendaraan
    dfparkir.loc[index, 'waktu keluar'] = waktu_keluar
    dfparkir.loc[index, 'Durasi'] = durasi
    dfparkir.loc[index, 'Biaya'] = biaya
    dfparkir.loc[index, 'foto_keluar'] = foto_keluar
    dfparkir.to_excel(fileExcel, sheet_name="Data_parking", index=False)

def keluar_parkir():
    print("Proses keluar parkir dimulai...")
    baca_qr_code()

# Fungsi untuk membaca QR code kendaraan
def baca_qr_code():
    import cv2
    from pyzbar.pyzbar import decode
    import time

    cap = cv2.VideoCapture(0)
    no_qr_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error saat membaca frame dari kamera.")
            break

        cv2.putText(frame, "Sedang membaca QR code...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)

        decoded_objects = decode(frame)

        if decoded_objects:
            no_qr_count = 0
            for obj in decoded_objects:
                cv2.rectangle(frame, obj.rect, (0, 255, 0), 3)
                qr_data = obj.data.decode("utf-8")
                cv2.putText(frame, qr_data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            print(f"QR code ditemukan: {qr_data}")
            cap.release()
            cv2.destroyAllWindows()
            proses_keluar_parkir(qr_data)
            return
        else:
            no_qr_count += 1
            if time.time() - start_time >= 30:
                print("Tidak terdeteksi QR code. Mematikan kamera dalam 10 detik ...")
                cap.release()
                cv2.destroyAllWindows()
                return

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fungsi untuk memproses keluar parkir
# Fungsi untuk memproses keluar parkir
def proses_keluar_parkir(qr_data):
    path = "database"
    fileExcel = "Data_Parking.xlsx"
    file_path = os.path.join(path, fileExcel)

    if not os.path.exists(file_path):
        print("Data parkir tidak ditemukan.")
        return

    df = pd.read_excel(file_path, sheet_name="Data_Parking")
    data_kendaraan = df[df['Kode_parking'] == qr_data]

    if data_kendaraan.empty:
        print("Data parkir tidak ditemukan untuk QR code tersebut.")
        return

    waktu_keluar = datetime.datetime.now()
    waktu_keluar_str = waktu_keluar.strftime("%Y-%m-%d %H:%M:%S")
    waktu_masuk = pd.to_datetime(data_kendaraan.iloc[0]['Waktu_masuk'])

    durasi = (waktu_keluar - waktu_masuk).total_seconds()
    jam = durasi // 3600
    menit = (durasi % 3600) // 60
    biaya = 2000 if data_kendaraan.iloc[0]['jenis_kendaraan'] == "Motor" else 4000
    if jam > 1:
        biaya += (jam - 1) * biaya

    print(f"Durasi parkir: {int(jam)} jam {int(menit)} menit")
    print(f"Biaya parkir: Rp {int(biaya)}")

    # Update data di Excel
    index = data_kendaraan.index[0]
    df.at[index, 'Waktu_keluar'] = waktu_keluar_str
    df.at[index, 'Durasi'] = f"{int(jam)} jam {int(menit)} menit"
    df.at[index, 'Biaya'] = biaya

    # Hitung total biaya
    total_biaya = df['Biaya'].fillna(0).sum()

    # Simpan data ke file Excel
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Data_Parking", index=False)

        # Tambahkan total biaya ke sheet baru
        total_df = pd.DataFrame({"Keterangan": ["Total Biaya"], "Nilai": [total_biaya]})
        total_df.to_excel(writer, sheet_name="Total_Biaya", index=False)

    print("Data parkir berhasil diperbarui.")
    print(f"Total biaya parkir saat ini: Rp {int(total_biaya)}")


# Main menu
while True:
    print("*" * 100)
    print("Sistem Parkir")
    print("*" * 100)
    tgl_masuk = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nama_petugas = "Praditya Wahyu Saputra"
    print(f"Nama Petugas: {nama_petugas}")
    print(f"Tanggal Masuk: {tgl_masuk}")
    print("1. Parkir Masuk")
    print("2. Keluar")
    pilihan = int(input("Masukkan pilihan: "))
    print("*" * 100)
    if pilihan == 1:
        masuk(tgl_masuk, nama_petugas)
    elif pilihan == 2:
        keluar_parkir()
    else:
        print("Pilihan tidak valid.")
