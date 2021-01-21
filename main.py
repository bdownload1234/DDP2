import random, string
from prettytable import PrettyTable

#Membuat fungsi membuka rekening. Buka file.
def bukaRekening(filename):
    #Variabel nomor_rekening = Fungsi randomKey ditambah Awalan yaitu REK.
    nomor_rekening = randomKey("REK")
    #Meminta inputan nama
    nama = input("Masukkan nama : ")
    #Meminta inputan saldo awal
    saldo = numSanitize("Masukkan setoran awal: ")
    #Menggunakan fungsi file, dengan meminta nama file, melakukan penulisan file, yaitu nomor rekening(nomor_rekening) ditambah ,(koma) kemudian nama, lalu saldo
    fileFunc(filename, 'a+', nomor_rekening + ',' + nama + ',' + str(saldo) + '\n')
    #Pengembalian data dengan memunculkan pesan Pembukaan rekening dengan nomor sekian atas nama sekian telah berhasil
    return "Pembukaan rekening dengan nomor " + nomor_rekening + " atas nama " + nama + " berhasil."

#Membuat fungsi pengecekan data, untuk menentukan pesan dan fungsi pada input user.
def cekData(filename, no, nominal=0, transaksi='Setor'):
    #Membuat kondisi true
    notFind = True
    #Membuat variabel dengan fungsi pembacaan data
    data = fileFunc(filename, 'r')
    #Membaca dengan index pada data
    for i in range(len(data)):
        #Membuat fungsi untuk membaca setiap data dengan koma
        ls = data[i].split(',')
        #Fungsi menemukan nomor rekening dengan index pertama, yaitu nomor rekening
        if (no == ls[0]):
            #Kondisi notFind = False
            notFind = False
            #Membaca saldo pada index ke 3
            saldo = int(ls[2])
            #Jika inputan = setor
            if (transaksi.lower() == 'setor'):
                #Maka index ke 3 yaitu saldo awal ditambah nominal inputan
                ls[2] = saldo + nominal
            #Jika inputan selain setor = penarikan
            else:
                #Jika nominal lebih besar daripada saldo, maka munculkan pesan
                if (nominal > saldo):
                    return data, "Saldo tidak mencukupi. Transaksi gagal"
                #Jika nominal lebih kecil, maka saldo dikurangi nominal
                ls[2] = saldo - nominal
            #Lakukan penulisan data
            data[i] = ls[0] + ',' + ls[1] + ',' + str(ls[2]) + '\n'
            break
    #Apabila notFind = True, alias data tidak ketemu/cocok
    if (notFind):
        #Munculkan pesan berikut
        return data, "Nomor rekening " + no + " tidak terdaftar. Transaksi gagal"
    return data, ""

#Fungsi editSaldo untuk melakukan penulisan pada saldo
def editSaldo(filename, transaksi):
    #Masukan nomor rekening, inputan tidak perlu menggunakan huruf kapital, karena akan dikapitalkan secara otomatis
    no = input("Masukkan nomor rekening: ").upper()
    #Fungsi memasukan nominal, tergantung dari inputan user, akankah penarikan atau setor saldo
    nominal = numSanitize(
        "Masukkan nominal yang akan di{0}: ".format(transaksi.lower()))
    #Melakukan pengecekan data dengan format filename(user) nomor rekening(index pertama) nominal(variabel nominal) dan jenis transaksi
    data = cekData(filename, no, nominal, transaksi)
    error = cekData(filename, no, nominal, transaksi)
    if (error != ""):
        #Apabila ada kesalahan, muncul error pada pengecekan data, yaitu saldo tidak mencukupi
        return error
    else:
        #Lakukan penulisan data
        fileFunc(filename, 'w+', data)
        #Melakukan pencetakan pesan yaitu jenis transaksi, ditambah pesan, dst dst
        return transaksi + " tunai sebesar " + str(nominal) + " di rekening " + no + " berhasil."

#Membuat fungsi transfer dibutuhkan nomor user, dan fungsi transfer
def transferProses(user, transfer):
    #Variabel ini akan menyimpan data transfer
    idTRF = randomKey("TRANSF")
    #Meminta masukan nomor rekening sumber
    noSumber = input("Masukkan nomor rekening sumber: ").upper()
    #Meminta masukan nomor rekening tujuan
    noTujuan = input("Masukkan nomor rekening tujuan: ").upper()
    #Memasukan nominal
    nominal = numSanitize("Masukkan nominal yang akan ditransfer: ")
    #Fungsi data dan error pertama, yaitu user, nomor sumber, nominal dan string "Tarik"
    data1 = cekData(user, noSumber, nominal, "Tarik")
    error1 = cekData(user, noSumber, nominal, "Tarik")
    #Fungsi data kedua, yaitu penarikan data dari data untuk dikurangi
    data2 = cekData(user, noTujuan)
    error2 = cekData(user, noTujuan)
    if (error1 != ""):
        return error1
    elif (error2 != ""):
        return error2
    else:
        #Menggunakan fungsi ... dengan data inputan user dan melakukan penulisan
        fileFunc(user, 'w+', data1)
        data2, error2 = cekData(user, noTujuan, nominal, "Setor")
        #Melakukan fungsi transfer dengan penulisan sebagai berikut
        fileFunc(user, 'w+', data2)
        fileFunc(transfer, 'a+', (idTRF+','+noSumber +','+noTujuan+','+str(nominal)+'\n'))
        #Melakukan pencetakan hasil proses
        return "Transfer sebesar {0} dari rekening {1} ke rekening {2} berhasil".format(nominal, noSumber, noTujuan)

def showTransfer(user, transfer):
     no = input("Masukkan nomor rekening sumber transfer: ").upper()
     data = cekData(user, no)
     error = cekData(user, no)
     if (error != ""):
         return "Nomor rekening sumber tidak terdaftar. Transfer gagal."
     else:
         data = fileFunc(transfer, 'r')
         lsTrf = []
         for i in range(len(data)):
             ls = data[i].strip().split(',')
             if(ls[1] == no):
                 lsTrf.append(ls)
         if len(lsTrf) == 0:
             return "Tidak ada data yang ditampilkan."
         else:
             print("Daftar transfer dari rekening", no, ":")
             t = PrettyTable(['ID TRF', 'REK SUMBER', 'REK TUJUAN', 'NOMINAL'])
             t.add_rows(lsTrf)
             print(t)
         return ""

#Membuat fungsi menulis atau membaca file, disini dibutuhkan filenya, kemudian operatornya, kemudian datanya
def fileFunc(filename, operator, data=None):
    #Ketika file telah dibuka maka
    with open(filename, operator) as file:
        #Jika operator menunjukan append atau write(tulis)
        if operator == 'a+' or operator == 'w+':
            #Lakukan penulisan data pada file
            data = file.writelines(data)
        #Jika operator menunjukan r, maka
        elif operator == 'r':
            #Lakukan pembacaan data pada file
            data = file.readlines()
    #Kembalikan data
    return data

#Membuat fungsi dengan dibutuhkan pesan(string)
def numSanitize(message):
    #Apabila benar
    while True:
        x = input(message)
        try:
            #Apabila user memasukan angka, maka break, program telah benar
            return int(x)
            break
        #Selain itu, muncul error
        except ValueError:
            print("Mohon pastikan inputan berupa angka!")

#Fungsi untuk membuat angka random
def randomKey(awalan):
    #Masukan awalan ditambah '' (tanpa spasi), maka digabungkan dengan fungsi join, angka random. String ditambah Angka. Dengan range angka tiga digit
    return awalan + ''.join(random.choice(string.digits) for _ in range(3))

user = 'user.txt'
transfer = 'transfer.txt'
pesan = ""
while True:
    print(
        '\n##### SELAMAT DATANG DI NF BANK v0.1 #####\nMENU:\n[1] Buka rekening\n[2] Setoran tunai\n[3] Tarik tunai\n[4] Transfer\n[5] Lihat Mutasi Transfer\n[6] Keluar\n'
    )
    menu = numSanitize("Masukkan menu pilihan Anda: ")
    if menu == 1:
        print('### BUKA REKENING ###')
        pesan = bukaRekening(user)
    elif menu == 2:
        print('### SETORAN TUNAI ###')
        pesan = editSaldo(user, "Setor")
    elif menu == 3:
        print('### TARIK TUNAI ###')
        pesan = editSaldo(user, "Tarik")
    elif menu == 4:
        print('### TRANSFER ###')
        pesan = transferProses(user, transfer)
    elif menu == 5:
         print('### LIHAT DATA TRANSFER ###')
         pesan = showTransfer(user, transfer)
    elif menu == 6:
        break
        pesan = "Terima kasih atas kunjungan Anda..."
    else:
        pesan = "Pilihan Anda tidak terdaftar. Ulangi"
    print(pesan + "\n")
