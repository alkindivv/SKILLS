# Worked examples / contoh penerapan

These are original examples authored and reviewed during skill construction.
They illustrate intended behavior; they are not independent model runs, blind
reviews, or evidence of a measured quality improvement. Some outputs correctly
leave the source unchanged. All product names and example scenarios are
illustrative, not externally verified customer cases.

## Contents

- W01: Homepage: fakta lebih dahulu
- W02: Laporan: penjualan bukan laba
- W03: Terjemahan: modalitas dan cakupan
- W04: Terjemahan: izin bukan kewajiban
- W05: Tidak perlu memaksa kalimat aktif
- W06: Kontras yang memang menjelaskan hak akses
- W07: Email: usulan tidak menjadi keputusan
- W08: String UI: token tetap utuh
- W09: Ringkasan: dukungan tidak bulat
- W10: Puisi: pertahankan pengulangan
- W11: JSON: terjemahkan nilai saja
- W12: Headline dengan batas kata

## W01 - Homepage: fakta lebih dahulu

**Task:** Tulis headline dan satu kalimat pendukung. Fakta tersedia: Draftroom menyimpan draf, menyediakan komentar, dan menjadwalkan publikasi.

**Input:**

```text
Buka potensi tanpa batas dengan solusi revolusioner untuk mentransformasi perjalanan konten Anda.
```

**Output:**

```text
Atur draf dan jadwal publikasi di Draftroom.
Simpan draf, beri komentar, dan tentukan kapan artikel diterbitkan.
```

**Review:** Copy menyebut fitur yang diberikan. Tidak menambah jumlah pengguna, integrasi, penghematan waktu, atau jaminan.

## W02 - Laporan: penjualan bukan laba

**Task:** Perbaiki interpretasi berdasarkan data: penjualan Juli Rp120 juta, Agustus Rp126 juta, biaya tidak tersedia.

**Input:**

```text
Penjualan meningkat dan membuktikan bahwa laba perusahaan melonjak.
```

**Output:**

```text
Penjualan naik dari Rp120 juta pada Juli menjadi Rp126 juta pada Agustus, atau 5%. Perubahan laba belum dapat ditentukan karena data biaya tidak tersedia.
```

**Review:** 5% dihitung sebagai (126 - 120) / 120. Penjualan dan laba dibedakan; tidak ada penyebab kenaikan yang direka.

## W03 - Terjemahan: modalitas dan cakupan

**Task:** Terjemahkan ke bahasa Indonesia, hanya hasilnya.

**Input:**

```text
The update may reduce processing time by up to 18% in internal tests.
```

**Output:**

```text
Dalam pengujian internal, pembaruan ini mungkin mengurangi waktu pemrosesan hingga 18%.
```

**Review:** Mungkin = ketidakpastian; hingga = batas atas; pengujian internal = konteks. Tidak diubah menjadi hasil yang pasti.

## W04 - Terjemahan: izin bukan kewajiban

**Task:** Terjemahkan ke bahasa Indonesia.

**Input:**

```text
You may cancel unless the invoice has already been paid.
```

**Output:**

```text
Anda boleh membatalkan, kecuali jika tagihan sudah dibayar.
```

**Review:** Boleh mempertahankan izin. Kecuali mempertahankan pengecualian.

## W05 - Tidak perlu memaksa kalimat aktif

**Task:** Copyedit only if needed. Keep the sample-focused scientific register.

**Input:**

```text
Samples were stored at 4 degrees Celsius until analysis.
```

**Output:**

```text
Samples were stored at 4 degrees Celsius until analysis.
```

**Review:** Tidak ada perbaikan yang diperlukan. Menambah peneliti sebagai subjek akan menciptakan detail yang tidak diberikan.

## W06 - Kontras yang memang menjelaskan hak akses

**Task:** Rapikan bila perlu.

**Input:**

```text
Akun tamu dapat membaca laporan, tetapi tidak dapat mengeditnya.
```

**Output:**

```text
Akun tamu dapat membaca laporan, tetapi tidak dapat mengeditnya.
```

**Review:** Kontras menjelaskan batas akses. Ini bukan pola kosong yang perlu dihapus.

## W07 - Email: usulan tidak menjadi keputusan

**Task:** Padatkan tanpa mengubah status tenggat yang masih berupa usulan.

**Input:**

```text
Saya ingin menyampaikan bahwa kami mengusulkan agar ulasan diberikan paling lambat Jumat, apabila jadwal tersebut memungkinkan bagi Anda.
```

**Output:**

```text
Kami mengusulkan tenggat ulasan pada Jumat. Apakah jadwal ini memungkinkan bagi Anda?
```

**Review:** Tenggat tetap merupakan usulan, bukan tenggat yang telah disetujui atau dijamin.

## W08 - String UI: token tetap utuh

**Task:** Terjemahkan label tanpa mengubah placeholder.

**Input:**

```text
Save changes to {project_name}?
```

**Output:**

```text
Simpan perubahan pada {project_name}?
```

**Review:** Hanya prosa diterjemahkan. Token dan tanda tanya tetap dipertahankan.

## W09 - Ringkasan: dukungan tidak bulat

**Task:** Ringkas menjadi satu kalimat tanpa menghilangkan keberatan utama.

**Input:**

```text
Komite terdiri atas tujuh anggota. Lima mendukung uji coba. Dua menolak karena biaya belum dihitung. Keputusan peluncuran penuh ditunda.
```

**Output:**

```text
Lima dari tujuh anggota komite mendukung uji coba, tetapi dua menolak karena biaya belum dihitung; keputusan peluncuran penuh ditunda.
```

**Review:** Ruang lingkup dukungan, jumlah anggota, keberatan biaya, dan penundaan peluncuran tetap ada.

## W10 - Puisi: pertahankan pengulangan

**Task:** Periksa tanpa merusak anafora yang disengaja; boleh tidak diubah.

**Input:**

```text
Aku menunggu hujan. Aku menunggu kabar. Aku menunggu namamu berhenti menjadi pintu.
```

**Output:**

```text
Aku menunggu hujan. Aku menunggu kabar. Aku menunggu namamu berhenti menjadi pintu.
```

**Review:** Pengulangan merupakan pilihan bentuk dan makna, bukan bukti slop. Tidak ditambahkan disclosure atau ringkasan.

## W11 - JSON: terjemahkan nilai saja

**Task:** Kembalikan JSON valid, terjemahkan nilainya, jangan ubah kunci.

**Input:**

```text
{"save":"Save changes","project":"Open {project_name}"}
```

**Output:**

```text
{"save":"Simpan perubahan","project":"Buka {project_name}"}
```

**Review:** Kunci dan placeholder tetap; hasil dapat diparse sebagai JSON. Pemeriksa literal sendiri tidak memvalidasi sintaks JSON.

## W12 - Headline dengan batas kata

**Task:** Tulis headline tepat tujuh kata tentang mengatur draf dan jadwal publikasi.

**Input:**

```text
Sebuah solusi terbaik untuk segala kebutuhan konten.
```

**Output:**

```text
Atur draf dan jadwal publikasi artikel Anda.
```

**Review:** Tujuh kata menurut pemisahan spasi; fungsinya jelas tanpa klaim superioritas.

## How these were checked

The companion JSON stores the same examples plus explicit literal constraints.
A construction-time check tested those constraints, parsed the JSON example,
counted W12's words, and ran the integrity checker on eligible pairs. Editorial
review separately examined the stated meaning risks. A passing literal check
cannot prove translation correctness, style quality, or factual truth.
