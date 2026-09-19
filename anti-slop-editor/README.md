# Anti-Slop Editor

Satu skill editorial untuk artikel, laporan, naskah PDF/DOCX, halaman website,
UI copy, email, dokumentasi, ringkasan, skrip, dan terjemahan. Versi paket: 1.0.0.
Tanggal penyusunan: 20 September 2026.

Tujuannya adalah tulisan yang jelas, spesifik, akurat terhadap sumber, dan sesuai
pembacanya. Bukan menebak penulisnya atau menjanjikan lolos detektor AI.

## Mulai

Unggah `skill.zip` melalui alur Skills di ChatGPT, atau ekstrak folder
`anti-slop-editor` ke lokasi skill yang didukung agent Anda. Lihat
[petunjuk instalasi](references/installation.md) untuk ChatGPT, Hermes, dan Codex.
Paket ini belum otomatis terpasang hanya karena file sudah dibuat.

Contoh pemanggilan:

> Gunakan anti-slop-editor untuk menyunting artikel ini. Pertahankan argumen,
> fakta, kutipan, dan gaya penulis. Kembalikan naskah final saja.

> Gunakan anti-slop-editor untuk menerjemahkan teks ini ke bahasa Indonesia
> formal yang natural. Jangan hilangkan batasan, angka, atau pengecualian.

> Gunakan anti-slop-editor untuk copy homepage berdasarkan spesifikasi produk
> ini. Jangan tambahkan metrik, testimoni, atau fitur yang tidak tersedia.

## Jadikan pedoman utama

Gabungkan isi [DEFAULT_INSTRUCTIONS.txt](assets/DEFAULT_INSTRUCTIONS.txt) ke
instruksi persisten yang didukung host. Tersedia juga
[versi bahasa Indonesia](assets/DEFAULT_INSTRUCTIONS_ID.txt). Jangan menimpa konfigurasi yang sudah
ada. Skill memakai pemanggilan sesuai konteks, bukan tombol ajaib yang dapat
memaksa semua LLM membacanya pada setiap respons.

Untuk host tanpa dukungan folder skill, tersedia
[PORTABLE_INSTRUCTIONS.md](assets/PORTABLE_INSTRUCTIONS.md). Ini versi mandiri
yang lebih ringkas; bukan seluruh modul lengkap.

## Isi paket

`SKILL.md` adalah inti. Direktori `references` berisi panduan berdasarkan medium,
fidelitas, bahasa, terjemahan, voice, dan pemeriksaan kualitas. Panduan dimuat
hanya ketika relevan, bukan semuanya pada setiap tugas.

[Source catalog](references/source-catalog.md) memetakan 16 proyek publik,
batas akses sumber, aturan yang dipilih, dan aturan yang ditolak. Daftar ini
bukan inventaris seluruh internet. [sources.json](references/sources.json)
menyimpan catatan yang sama dalam bentuk terstruktur.

`evals/cases.json` berisi skenario regresi. `evals/worked-examples.md` menunjukkan
contoh hasil dan pemeriksaan makna. Lihat [laporan validasi](evals/validation-report.md) untuk membedakan
pengujian perangkat pemeriksa dari evaluasi kualitas tulisan lintas model.

## Pemeriksaan opsional

Tidak perlu Python untuk memakai panduan editorial. Untuk membandingkan file:

```bash
python scripts/check_integrity.py --source sebelum.txt --target sesudah.txt
python scripts/check_integrity.py --source sebelum.txt --target sesudah.txt --manifest manifest.json
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/run_checks.py
```

Mulai manifest dari `assets/fidelity-manifest.example.json`, lalu sesuaikan token
yang benar-benar ada di sumber. `pass` berarti pemeriksaan literal terpilih lolos,
bukan bukti akurasi atau kesetaraan makna. `review` menandai perbedaan yang perlu
diperiksa, misalnya format angka. `fail` menandai pelanggaran literal yang
dikonfigurasi. Kode keluar: 0 untuk pass/review, 1 untuk fail, 2 untuk input tidak
valid. Baca JSON hasilnya; jangan menafsirkan kode 0 sebagai persetujuan publikasi.

## Batas yang sengaja dipertahankan

Tidak ada larangan mutlak atas tanda baca, kalimat pasif, istilah teknis, atau
daftar tiga butir. Tidak ada statistik, pengalaman pribadi, sumber, dan janji
produk yang direka untuk membuat tulisan lebih menarik. Tulisan formal tidak
otomatis diubah menjadi bahasa gaul; terjemahan tidak otomatis diringkas.

Panduan terperinci berfokus pada bahasa Indonesia dan Inggris. Prinsip fidelitas
bisa dipakai untuk bahasa lain, tetapi paket ini tidak mengklaim peninjauan native
untuk semua bahasa. Layout, aksesibilitas, ekspor file, dan validasi teknis tetap
memerlukan kemampuan serta pemeriksaan khusus dari host.
