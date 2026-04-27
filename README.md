# ⚙️ FSM Simulator - Tugas Praktikum #2

Sebuah aplikasi Desktop (GUI) berbasis Python yang dirancang untuk melakukan simulasi dari FSM atau Finite State Machine pada kode sumber program. Dibangun dengan library customtkinter, aplikasi ini menyediakan antarmuka modern untuk menentukan transisi antar kondisi berdasarkan input.

## ✨ Fitur Utama
- Antarmuka Modern : Desain UI yang memanjakan mata menggunakan CustomTkinter.
- Input String Biner : Hanya akan memproses karakter 0 dan 1, selain karakter tersebut akan muncul perinatan dan tidak akan dieksekusi
- Jejak Transisi State : Menampilkan urutan perpindahan state secara visual. Lalu state terakhir akan berubah warna menjadi hijau (diterima) atau merah (ditolak)
- Diagram FSM Interaktif : Diagram menampilkan semua transisi, self-loop, dan menandai state accept (B) dengan lingkaran ganda

## 🛠️ Persyaratan Sistem (Prerequisites)
Sebelum menjalankan aplikasi ini, pastikan telah menginstal Python di komputer (versi 3.7 ke atas disarankan). Kita juga perlu menginstal pustaka pihak ketiga yang digunakan untuk GUI.

Jalankan perintah berikut di Terminal atau Command Prompt:
```
pip install customtkinter
```

## 📖 Cara Penggunaan
1. Input String Biner: Masukkan string biner ke dalam kotak teks di sebelah kiri.
2. Contoh test case: Jika ingin langsung mmencoba contoh test case yang sudah teruji.
3. Simulasi: Klik tombol jalankan untuk mensimulasikan FSM.
4. Lihat Hasil: Hasil simulasi akan muncul di tabel bawah lengkap dengan hasil dan state akhirnya.
5. Reset: Untuk mereset aplikasi, klik tombol reset di sebelah tombol jalankan.

## 🧠 Struktur Logika
Program ini menggunakan tabel transisi yang mendefinisikan perilaku mesin. Tabel tersebut menyimpan aturan perpindahan state, misalnya jika mesin sedang di state S dan membaca karakter 0, maka mesin berpindah ke state A. Fungsi `run_fsm()` menggunakan tabel ini untuk memproses string karakter demi karakter dari kiri ke kanan, dimulai dari state awal S. Setiap langkah perpindahan direkam ke dalam daftar trace. Setelah semua karakter selesai dibaca, fungsi ini mengecek apakah state terakhir adalah B, satu-satunya state yang menerima string. Hasil akhirnya yaitu diterima atau ditolak, dan jejak lengkap perpindahan state.

