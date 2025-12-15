# Lottery Prediction App

Aplikasi prediksi hasil lotere (HK Lottery) menggunakan algoritma Random Forest.

## Persyaratan
*   Python 3.7+
*   Pip package manager

## Instalasi

1.  **Ekstrak** folder proyek (jika dari zip).
2.  **Buka Terminal** atau Command Prompt (CMD/PowerShell) dan arahkan ke direktori utama proyek (folder yang berisi `requirements.txt`).
3.  **Instal library** yang dibutuhkan dengan perintah:
    ```bash
    pip install -r requirements.txt
    ```

## Cara Menjalankan Aplikasi

1.  Pastikan Anda berada di direktori utama proyek.
2.  Jalankan aplikasi dengan perintah:
    ```bash
    python app/app.py
    ```
3.  Tunggu hingga muncul pesan seperti:
    ```
    Running on http://127.0.0.1:5000
    ```
4.  Buka browser Anda dan akses alamat: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Struktur Folde
*   `app/`: Berisi kode utama aplikasi (`app.py`), konfigurasi, dan file model `.pkl` dan `.py`.
    *   **PENTING**: Pastikan file `lottery_model.pkl` dan `model_features.pkl` ada di folder ini agar aplikasi dapat melakukan prediksi.
*   `data/`: Berisi dataset latih dan uji.
*   `templates/`: Berisi file HTML (`index.html`).
*   `static/`: Berisi file statis seperti CSS dan gambar.
