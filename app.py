"""
E-VOTE MAHASISWA - versi APLIKASI DESKTOP (GUI Tkinter)

Memakai database & fungsi yang sama dengan main.py, jadi:
  - taruh app.py dan main.py di folder yang sama
  - jalankan:  python app.py
  - data tersimpan di evote_mahasiswa.db (sama dengan versi terminal)

Akun admin bawaan: admin / admin123
Fitur bonus: grafik hasil voting + audit log.
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import main as core  # fungsi database & logika dari main.py

# ---------- Warna & font ----------
BIRU = "#1F3A5F"
BIRU_MUDA = "#2F5D9B"
ABU = "#F3F5F8"
PUTIH = "#FFFFFF"
HIJAU = "#2E8B57"
MERAH = "#C0392B"
FONT = "Segoe UI"
WARNA_BAR = ["#2F5D9B", "#E07A5F", "#3D9970", "#F2B134", "#8E6BBF", "#4DB6AC"]


def terapkan_gaya(root):
    gaya = ttk.Style(root)
    try:
        gaya.theme_use("clam")
    except tk.TclError:
        pass
    root.configure(bg=ABU)
    gaya.configure(".", font=(FONT, 10), background=ABU)
    gaya.configure("TFrame", background=ABU)
    gaya.configure("Card.TFrame", background=PUTIH)
    gaya.configure("TLabel", background=ABU)
    gaya.configure("Card.TLabel", background=PUTIH)
    gaya.configure("Judul.TLabel", font=(FONT, 20, "bold"), foreground=BIRU, background=ABU)
    gaya.configure("Sub.TLabel", font=(FONT, 10), foreground="#666666", background=ABU)
    gaya.configure("H2.TLabel", font=(FONT, 13, "bold"), foreground=BIRU, background=PUTIH)
    gaya.configure("TButton", padding=(12, 6))
    gaya.configure("Utama.TButton", background=BIRU_MUDA, foreground=PUTIH,
                   font=(FONT, 10, "bold"), padding=(14, 8))
    gaya.map("Utama.TButton", background=[("active", BIRU)])
    gaya.configure("Bahaya.TButton", background=MERAH, foreground=PUTIH,
                   font=(FONT, 10, "bold"))
    gaya.map("Bahaya.TButton", background=[("active", "#962D22")])
    gaya.configure("Treeview", rowheight=26, font=(FONT, 10))
    gaya.configure("Treeview.Heading", font=(FONT, 10, "bold"))
    gaya.configure("TNotebook.Tab", padding=(14, 8), font=(FONT, 10, "bold"))
    gaya.configure("Horizontal.TProgressbar", thickness=22)


def buat_tabel_tree(parent, kolom, lebar, tinggi=12):
    """Membuat Treeview + scrollbar. kolom = list nama, lebar = list lebar."""
    bingkai = ttk.Frame(parent)
    tree = ttk.Treeview(bingkai, columns=kolom, show="headings", height=tinggi)
    for k, w in zip(kolom, lebar):
        tree.heading(k, text=k)
        tree.column(k, width=w, anchor="w")
    sb = ttk.Scrollbar(bingkai, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return bingkai, tree


# =====================================================================
# APLIKASI UTAMA (mengganti-ganti halaman)
# =====================================================================
class AplikasiEVote(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-VOTE MAHASISWA - Pemilihan Ketua Himpunan")
        self.geometry("980x640")
        self.minsize(900, 600)
        terapkan_gaya(self)
        self.halaman = None
        self.tampil_login()

    def ganti_halaman(self, kelas, *args):
        if self.halaman is not None:
            self.halaman.destroy()
        self.halaman = kelas(self, *args)
        self.halaman.pack(fill="both", expand=True)

    def tampil_login(self):
        self.ganti_halaman(HalamanLogin)

    def tampil_mahasiswa(self, pemilih):
        self.ganti_halaman(HalamanMahasiswa, pemilih)

    def tampil_admin(self, username):
        self.ganti_halaman(HalamanAdmin, username)


# =====================================================================
# HALAMAN LOGIN
# =====================================================================
class HalamanLogin(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        ttk.Label(self, text="🗳  E-VOTE MAHASISWA", style="Judul.TLabel").pack(pady=(50, 2))
        ttk.Label(self, text="Pemilihan Ketua Himpunan Mahasiswa Informatika",
                  style="Sub.TLabel").pack(pady=(0, 20))

        kartu = ttk.Frame(self, style="Card.TFrame", padding=24)
        kartu.pack()
        tab = ttk.Notebook(kartu)
        tab.pack()

        # --- Tab mahasiswa ---
        f1 = ttk.Frame(tab, style="Card.TFrame", padding=20)
        tab.add(f1, text="  Mahasiswa  ")
        ttk.Label(f1, text="Masuk dengan NPM", style="H2.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        ttk.Label(f1, text="NPM", style="Card.TLabel").grid(row=1, column=0, sticky="w")
        self.ent_nim = ttk.Entry(f1, width=32)
        self.ent_nim.grid(row=1, column=1, padx=10, pady=6)
        self.ent_nim.bind("<Return>", lambda e: self.login_mhs())
        ttk.Button(f1, text="Login", style="Utama.TButton",
                   command=self.login_mhs).grid(row=2, column=0, columnspan=2, pady=(14, 0), sticky="ew")

        # --- Tab admin ---
        f2 = ttk.Frame(tab, style="Card.TFrame", padding=20)
        tab.add(f2, text="  Admin  ")
        ttk.Label(f2, text="Masuk sebagai panitia", style="H2.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        ttk.Label(f2, text="Username", style="Card.TLabel").grid(row=1, column=0, sticky="w")
        self.ent_user = ttk.Entry(f2, width=32)
        self.ent_user.grid(row=1, column=1, padx=10, pady=6)
        ttk.Label(f2, text="Password", style="Card.TLabel").grid(row=2, column=0, sticky="w")
        self.ent_pass = ttk.Entry(f2, width=32, show="•")
        self.ent_pass.grid(row=2, column=1, padx=10, pady=6)
        self.ent_pass.bind("<Return>", lambda e: self.login_admin())
        ttk.Button(f2, text="Login", style="Utama.TButton",
                   command=self.login_admin).grid(row=3, column=0, columnspan=2, pady=(14, 0), sticky="ew")

        self.gagal_admin = 0
        self.ent_nim.focus_set()

    def login_mhs(self):
        nim = self.ent_nim.get().strip()
        conn = core.koneksi()
        pemilih = conn.execute("SELECT * FROM pemilih WHERE nim = ?", (nim,)).fetchone()
        conn.close()
        if pemilih is None:
            core.catat_log(nim or "(kosong)", "LOGIN_GAGAL_MHS", "NIM tidak terdaftar")
            messagebox.showerror("ERROR", "NIM tidak terdaftar")
            return
        core.catat_log(nim, "LOGIN_MHS", pemilih["nama"])
        self.app.tampil_mahasiswa(pemilih)

    def login_admin(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get()
        conn = core.koneksi()
        admin = conn.execute(
            "SELECT * FROM admin WHERE username = ? AND password = ?",
            (username, core.hash_password(password))).fetchone()
        conn.close()
        if admin:
            core.catat_log(username, "LOGIN_ADMIN", "")
            self.app.tampil_admin(username)
            return
        self.gagal_admin += 1
        core.catat_log(username or "(kosong)", "LOGIN_GAGAL_ADMIN", f"percobaan ke-{self.gagal_admin}")
        if self.gagal_admin >= 3:
            messagebox.showerror("Terkunci", "Terlalu banyak percobaan gagal.\nAplikasi akan ditutup.")
            self.app.destroy()
        else:
            messagebox.showerror("ERROR", f"Username atau password salah ({self.gagal_admin}/3)")


# =====================================================================
# HALAMAN MAHASISWA
# =====================================================================
class HalamanMahasiswa(ttk.Frame):
    def __init__(self, app, pemilih):
        super().__init__(app)
        self.app = app
        self.nim = pemilih["nim"]
        self.pilihan = tk.IntVar(value=0)

        atas = ttk.Frame(self, padding=(20, 14))
        atas.pack(fill="x")
        ttk.Label(atas, text="MENU PEMILIH", style="Judul.TLabel").pack(side="left")
        ttk.Button(atas, text="Logout", command=self.logout).pack(side="right")

        self.lbl_info = ttk.Label(self, style="Sub.TLabel")
        self.lbl_info.pack(anchor="w", padx=22)

        tab = ttk.Notebook(self)
        tab.pack(fill="both", expand=True, padx=20, pady=12)
        self.tab_kandidat = ttk.Frame(tab, padding=14)
        self.tab_voting = ttk.Frame(tab, padding=14)
        self.tab_status = ttk.Frame(tab, padding=14)
        tab.add(self.tab_kandidat, text="  Lihat Kandidat  ")
        tab.add(self.tab_voting, text="  Voting  ")
        tab.add(self.tab_status, text="  Status Voting  ")
        tab.bind("<<NotebookTabChanged>>", lambda e: self.segarkan())
        self.segarkan()

    def segarkan(self):
        p = core.cek_status_pemilih(self.nim)
        self.lbl_info.config(text=f"{p['nama']}  •  NIM {p['nim']}  •  Pemilu: {core.ambil_status_pemilu()}")
        self.isi_kandidat()
        self.isi_voting()
        self.isi_status()

    @staticmethod
    def kosongkan(frame):
        for w in frame.winfo_children():
            w.destroy()

    # --- Lihat kandidat (profil, visi, misi) ---
    def isi_kandidat(self):
        self.kosongkan(self.tab_kandidat)
        data = core.ambil_semua_kandidat()
        if not data:
            ttk.Label(self.tab_kandidat, text="Belum ada kandidat.").pack()
            return
        teks = tk.Text(self.tab_kandidat, wrap="word", font=(FONT, 10), bg=PUTIH,
                       relief="flat", padx=14, pady=10)
        teks.pack(fill="both", expand=True)
        teks.tag_configure("nama", font=(FONT, 13, "bold"), foreground=BIRU)
        teks.tag_configure("label", font=(FONT, 10, "bold"))
        for no, k in enumerate(data, start=1):
            teks.insert("end", f"{no}. {k['nama_calon']}\n", "nama")
            teks.insert("end", "Prodi / Angkatan : ", "label")
            teks.insert("end", f"{k['program_studi']} / {k['angkatan']}\n")
            teks.insert("end", "Visi : ", "label")
            teks.insert("end", f"{k['visi']}\n")
            teks.insert("end", "Misi :\n", "label")
            teks.insert("end", f"{k['misi']}\n\n")
        teks.config(state="disabled")

    # --- Voting ---
    def isi_voting(self):
        self.kosongkan(self.tab_voting)
        f = self.tab_voting
        if not core.pemilu_aktif():
            ttk.Label(f, text="Pemungutan suara telah ditutup.", foreground=MERAH,
                      font=(FONT, 13, "bold")).pack(pady=40)
            return
        p = core.cek_status_pemilih(self.nim)
        if p["sudah_memilih"] == 1:
            ttk.Label(f, text="AKSES DITOLAK", foreground=MERAH,
                      font=(FONT, 15, "bold")).pack(pady=(40, 4))
            ttk.Label(f, text="Anda sudah menggunakan hak suara.").pack()
            return
        data = core.ambil_semua_kandidat()
        if not data:
            ttk.Label(f, text="Belum ada kandidat yang terdaftar.").pack(pady=40)
            return
        ttk.Label(f, text="Pilih satu kandidat:", font=(FONT, 12, "bold")).pack(anchor="w", pady=(0, 8))
        self.pilihan.set(0)
        self.peta_kandidat = {}
        for k in data:
            self.peta_kandidat[k["id_kandidat"]] = k["nama_calon"]
            ttk.Radiobutton(
                f, text=f"  {k['nama_calon']}  —  {k['program_studi']} {k['angkatan']}",
                variable=self.pilihan, value=k["id_kandidat"]).pack(anchor="w", pady=5)
        ttk.Button(f, text="Kirim Suara", style="Utama.TButton",
                   command=self.kirim_suara).pack(anchor="w", pady=20)

    def kirim_suara(self):
        id_k = self.pilihan.get()
        if id_k == 0:
            messagebox.showwarning("Belum memilih", "Pilih salah satu kandidat dulu.")
            return
        if not core.pemilu_aktif():
            messagebox.showerror("Ditutup", "Pemungutan suara telah ditutup.")
            self.segarkan()
            return
        nama = self.peta_kandidat[id_k]
        if not messagebox.askyesno("Konfirmasi", f"Anda memilih:\n\n{nama}\n\nYakin?\n"
                                   "Pilihan tidak dapat diubah setelah dikirim."):
            return
        if core.proses_voting(self.nim, id_k):
            core.catat_log(self.nim, "VOTING", "suara tercatat")
            messagebox.showinfo("Berhasil", "Terima kasih.\nSuara Anda berhasil direkam.")
        else:
            core.catat_log(self.nim, "VOTING_DITOLAK", "mencoba voting ganda")
            messagebox.showerror("AKSES DITOLAK", "Anda sudah menggunakan hak suara.")
        self.segarkan()

    # --- Status ---
    def isi_status(self):
        self.kosongkan(self.tab_status)
        p = core.cek_status_pemilih(self.nim)
        f = self.tab_status
        baris = [("NIM", p["nim"]), ("Nama", p["nama"]),
                 ("Program Studi", p["program_studi"] or "-"),
                 ("Status Pemilih", "SUDAH MEMILIH" if p["sudah_memilih"] else "BELUM MEMILIH"),
                 ("Waktu Memilih", p["tanggal_vote"] or "-"),
                 ("Status Pemilu", core.ambil_status_pemilu())]
        for i, (a, b) in enumerate(baris):
            ttk.Label(f, text=a, font=(FONT, 10, "bold")).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 30))
            warna = HIJAU if (a == "Status Pemilih" and p["sudah_memilih"]) else "black"
            ttk.Label(f, text=b, foreground=warna).grid(row=i, column=1, sticky="w")

    def logout(self):
        core.catat_log(self.nim, "LOGOUT_MHS", "")
        self.app.tampil_login()


# =====================================================================
# HALAMAN ADMIN
# =====================================================================
class HalamanAdmin(ttk.Frame):
    def __init__(self, app, username):
        super().__init__(app)
        self.app = app
        self.admin = username

        atas = ttk.Frame(self, padding=(20, 14))
        atas.pack(fill="x")
        ttk.Label(atas, text="DASHBOARD ADMIN", style="Judul.TLabel").pack(side="left")
        ttk.Button(atas, text="Logout", command=self.logout).pack(side="right")
        self.btn_tutup = ttk.Button(atas, text="Tutup Pemilu", style="Bahaya.TButton",
                                    command=self.tutup_pemilu)
        self.btn_tutup.pack(side="right", padx=8)
        self.lbl_status = ttk.Label(atas, font=(FONT, 11, "bold"))
        self.lbl_status.pack(side="right", padx=8)

        self.tab = ttk.Notebook(self)
        self.tab.pack(fill="both", expand=True, padx=20, pady=(0, 14))
        self.f_hasil = ttk.Frame(self.tab, padding=12)
        self.f_stat = ttk.Frame(self.tab, padding=12)
        self.f_kand = ttk.Frame(self.tab, padding=12)
        self.f_pemilih = ttk.Frame(self.tab, padding=12)
        self.f_log = ttk.Frame(self.tab, padding=12)
        self.tab.add(self.f_hasil, text="Hasil Voting")
        self.tab.add(self.f_stat, text="Statistik")
        self.tab.add(self.f_kand, text="Kelola Kandidat")
        self.tab.add(self.f_pemilih, text="Data Pemilih")
        self.tab.add(self.f_log, text="Audit Log")

        self.bangun_hasil()
        self.bangun_statistik()
        self.bangun_kandidat()
        self.bangun_pemilih()
        self.bangun_log()
        self.tab.bind("<<NotebookTabChanged>>", lambda e: self.segarkan_semua())
        self.segarkan_semua()

    def segarkan_semua(self):
        self.segarkan_status()
        self.segarkan_hasil()
        self.segarkan_statistik()
        self.segarkan_kandidat()
        self.segarkan_pemilih()
        self.segarkan_log()

    def segarkan_status(self):
        aktif = core.pemilu_aktif()
        self.lbl_status.config(text=f"Status: {core.ambil_status_pemilu()}",
                               foreground=HIJAU if aktif else MERAH)
        self.btn_tutup.config(state="normal" if aktif else "disabled")

    # ---------------- Hasil voting (+ grafik) ----------------
    def bangun_hasil(self):
        bingkai, self.tree_hasil = buat_tabel_tree(
            self.f_hasil, ("Rank", "Kandidat", "Suara", "Persentase"), (60, 280, 100, 120), tinggi=6)
        bingkai.pack(fill="x")
        self.canvas = tk.Canvas(self.f_hasil, bg=PUTIH, height=230, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.gambar_grafik())
        self.lbl_pemenang = ttk.Label(self.f_hasil, font=(FONT, 11, "bold"), foreground=HIJAU)
        self.lbl_pemenang.pack(anchor="w")
        ttk.Button(self.f_hasil, text="Export Hasil ke CSV",
                   command=self.export_csv).pack(anchor="e")

    def data_hasil(self):
        data = sorted(core.ambil_semua_kandidat(), key=lambda k: k["total_suara"], reverse=True)
        return data, core.total_suara_masuk()

    def segarkan_hasil(self):
        self.tree_hasil.delete(*self.tree_hasil.get_children())
        data, total = self.data_hasil()
        for rank, k in enumerate(data, start=1):
            persen = core.hitung_persentase(k["total_suara"], total)
            self.tree_hasil.insert("", "end", values=(rank, k["nama_calon"], k["total_suara"], f"{persen:.1f}%"))
        self.gambar_grafik()
        # Pemenang hanya diumumkan setelah pemilu ditutup
        if not core.pemilu_aktif() and data and total > 0:
            tertinggi = data[0]["total_suara"]
            menang = [k["nama_calon"] for k in data if k["total_suara"] == tertinggi]
            if len(menang) == 1:
                p = core.hitung_persentase(tertinggi, total)
                self.lbl_pemenang.config(text=f"🏆 Pemenang: {menang[0]}  •  {tertinggi} suara  •  {p:.0f}%")
            else:
                self.lbl_pemenang.config(text="SERI antara: " + ", ".join(menang))
        else:
            self.lbl_pemenang.config(text="")

    def gambar_grafik(self):
        c = self.canvas
        c.delete("all")
        data = core.ambil_semua_kandidat()
        total = core.total_suara_masuk()
        lebar = max(c.winfo_width(), 400)
        c.create_text(14, 14, anchor="w", text="Grafik Hasil Voting", font=(FONT, 12, "bold"), fill=BIRU)
        if not data or total == 0:
            c.create_text(lebar / 2, 110, text="Belum ada suara masuk", fill="#888", font=(FONT, 11))
            return
        kiri, kanan, y, tinggi_bar, jarak = 170, 110, 45, 26, 14
        maks = lebar - kiri - kanan
        for i, k in enumerate(data):
            persen = core.hitung_persentase(k["total_suara"], total)
            panjang = max(persen / 100 * maks, 2)
            warna = WARNA_BAR[i % len(WARNA_BAR)]
            c.create_text(kiri - 10, y + tinggi_bar / 2, anchor="e", text=k["nama_calon"], font=(FONT, 10))
            c.create_rectangle(kiri, y, kiri + panjang, y + tinggi_bar, fill=warna, outline="")
            c.create_text(kiri + panjang + 8, y + tinggi_bar / 2, anchor="w",
                          text=f"{persen:.0f}% ({k['total_suara']})", font=(FONT, 10, "bold"))
            y += tinggi_bar + jarak

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="hasil_voting.csv",
                                            filetypes=[("CSV", "*.csv")])
        if not path:
            return
        data, total = self.data_hasil()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Rank", "Kandidat", "Suara", "Persentase"])
            for rank, k in enumerate(data, start=1):
                w.writerow([rank, k["nama_calon"], k["total_suara"],
                            f"{core.hitung_persentase(k['total_suara'], total):.1f}%"])
        core.catat_log(self.admin, "EXPORT_CSV", path)
        messagebox.showinfo("Berhasil", f"Hasil disimpan ke:\n{path}")

    # ---------------- Statistik ----------------
    def bangun_statistik(self):
        self.lbl_stat = {}
        for i, nama in enumerate(["Total Pemilih Terdaftar", "Sudah Memilih",
                                  "Belum Memilih", "Tingkat Partisipasi"]):
            ttk.Label(self.f_stat, text=nama, font=(FONT, 11)).grid(row=i, column=0, sticky="w", pady=8, padx=(0, 40))
            lbl = ttk.Label(self.f_stat, font=(FONT, 14, "bold"), foreground=BIRU)
            lbl.grid(row=i, column=1, sticky="w")
            self.lbl_stat[nama] = lbl
        self.bar = ttk.Progressbar(self.f_stat, length=500, maximum=100)
        self.bar.grid(row=5, column=0, columnspan=2, sticky="w", pady=20)

    def segarkan_statistik(self):
        total, sudah, belum, persen = core.hitung_statistik()
        self.lbl_stat["Total Pemilih Terdaftar"].config(text=str(total))
        self.lbl_stat["Sudah Memilih"].config(text=str(sudah))
        self.lbl_stat["Belum Memilih"].config(text=str(belum))
        self.lbl_stat["Tingkat Partisipasi"].config(text=f"{persen:.0f}%")
        self.bar["value"] = persen

    # ---------------- Kelola kandidat ----------------
    def bangun_kandidat(self):
        bingkai, self.tree_kand = buat_tabel_tree(
            self.f_kand, ("ID", "Nama", "Prodi", "Angkatan", "Suara"), (50, 240, 160, 90, 80), tinggi=7)
        bingkai.pack(fill="x")
        self.tree_kand.bind("<<TreeviewSelect>>", lambda e: self.isi_form_kandidat())

        form = ttk.Frame(self.f_kand, padding=(0, 10))
        form.pack(fill="x")
        self.v_nama, self.v_prodi, self.v_angkatan, self.v_visi = (tk.StringVar() for _ in range(4))
        label_entry = [("Nama Calon", self.v_nama), ("Prodi", self.v_prodi),
                       ("Angkatan", self.v_angkatan), ("Visi", self.v_visi)]
        for i, (lab, var) in enumerate(label_entry):
            ttk.Label(form, text=lab).grid(row=i, column=0, sticky="w", pady=3)
            ttk.Entry(form, textvariable=var, width=60).grid(row=i, column=1, sticky="w", padx=10)
        ttk.Label(form, text="Misi (1 per baris)").grid(row=4, column=0, sticky="nw", pady=3)
        self.txt_misi = tk.Text(form, width=58, height=4, font=(FONT, 10))
        self.txt_misi.grid(row=4, column=1, sticky="w", padx=10)

        tombol = ttk.Frame(self.f_kand)
        tombol.pack(fill="x")
        ttk.Button(tombol, text="Tambah", style="Utama.TButton", command=self.tambah_kandidat).pack(side="left")
        ttk.Button(tombol, text="Simpan Perubahan", command=self.ubah_kandidat).pack(side="left", padx=8)
        ttk.Button(tombol, text="Hapus", style="Bahaya.TButton", command=self.hapus_kandidat).pack(side="left")
        ttk.Button(tombol, text="Kosongkan Form", command=self.kosongkan_form).pack(side="right")

    def segarkan_kandidat(self):
        self.tree_kand.delete(*self.tree_kand.get_children())
        for k in core.ambil_semua_kandidat():
            self.tree_kand.insert("", "end", iid=str(k["id_kandidat"]),
                                  values=(k["id_kandidat"], k["nama_calon"], k["program_studi"],
                                          k["angkatan"], k["total_suara"]))

    def kosongkan_form(self):
        for v in (self.v_nama, self.v_prodi, self.v_angkatan, self.v_visi):
            v.set("")
        self.txt_misi.delete("1.0", "end")
        self.tree_kand.selection_remove(self.tree_kand.selection())

    def isi_form_kandidat(self):
        pilih = self.tree_kand.selection()
        if not pilih:
            return
        conn = core.koneksi()
        k = conn.execute("SELECT * FROM kandidat WHERE id_kandidat = ?", (int(pilih[0]),)).fetchone()
        conn.close()
        if k is None:
            return
        self.v_nama.set(k["nama_calon"])
        self.v_prodi.set(k["program_studi"])
        self.v_angkatan.set(k["angkatan"])
        self.v_visi.set(k["visi"])
        self.txt_misi.delete("1.0", "end")
        # tampilkan misi tanpa nomor di depannya agar mudah diedit
        baris = [b.split(". ", 1)[-1] for b in (k["misi"] or "").split("\n")]
        self.txt_misi.insert("1.0", "\n".join(baris))

    def baca_form(self):
        """Validasi form. Mengembalikan tuple data atau None jika tidak valid."""
        nama, prodi = self.v_nama.get().strip(), self.v_prodi.get().strip()
        visi = self.v_visi.get().strip()
        angk = self.v_angkatan.get().strip()
        misi_baris = [b.strip() for b in self.txt_misi.get("1.0", "end").split("\n") if b.strip()]
        if not (nama and prodi and visi and misi_baris):
            messagebox.showwarning("Data kurang", "Semua kolom wajib diisi.")
            return None
        if not angk.isdigit() or not (2000 <= int(angk) <= 2100):
            messagebox.showwarning("Angkatan salah", "Angkatan harus berupa tahun, mis. 2023.")
            return None
        misi = "\n".join(f"{i}. {m}" for i, m in enumerate(misi_baris, start=1))
        return nama, prodi, int(angk), visi, misi

    def tambah_kandidat(self):
        d = self.baca_form()
        if d is None:
            return
        conn = core.koneksi()
        conn.execute("INSERT INTO kandidat (nama_calon, program_studi, angkatan, visi, misi) "
                     "VALUES (?, ?, ?, ?, ?)", d)
        conn.commit()
        conn.close()
        core.catat_log(self.admin, "TAMBAH_KANDIDAT", d[0])
        self.kosongkan_form()
        self.segarkan_semua()

    def ubah_kandidat(self):
        pilih = self.tree_kand.selection()
        if not pilih:
            messagebox.showwarning("Pilih data", "Klik kandidat di tabel dulu.")
            return
        d = self.baca_form()
        if d is None:
            return
        conn = core.koneksi()
        conn.execute("UPDATE kandidat SET nama_calon=?, program_studi=?, angkatan=?, visi=?, misi=? "
                     "WHERE id_kandidat=?", d + (int(pilih[0]),))
        conn.commit()
        conn.close()
        core.catat_log(self.admin, "UBAH_KANDIDAT", f"id={pilih[0]} {d[0]}")
        self.segarkan_semua()
        messagebox.showinfo("Berhasil", "Data kandidat diperbarui.")

    def hapus_kandidat(self):
        pilih = self.tree_kand.selection()
        if not pilih:
            messagebox.showwarning("Pilih data", "Klik kandidat di tabel dulu.")
            return
        if core.total_suara_masuk() > 0:
            messagebox.showerror("DITOLAK", "Pemungutan suara sudah berjalan (ada suara masuk).\n"
                                 "Kandidat tidak boleh dihapus.")
            return
        nama = self.tree_kand.item(pilih[0], "values")[1]
        if messagebox.askyesno("Konfirmasi", f"Yakin menghapus '{nama}'?"):
            conn = core.koneksi()
            conn.execute("DELETE FROM kandidat WHERE id_kandidat = ?", (int(pilih[0]),))
            conn.commit()
            conn.close()
            core.catat_log(self.admin, "HAPUS_KANDIDAT", f"id={pilih[0]} {nama}")
            self.kosongkan_form()
            self.segarkan_semua()

    # ---------------- Data pemilih ----------------
    def bangun_pemilih(self):
        bar = ttk.Frame(self.f_pemilih)
        bar.pack(fill="x", pady=(0, 8))
        ttk.Label(bar, text="Filter:").pack(side="left")
        self.filter_pemilih = ttk.Combobox(bar, state="readonly", width=16,
                                           values=["Semua", "Sudah memilih", "Belum memilih"])
        self.filter_pemilih.current(0)
        self.filter_pemilih.pack(side="left", padx=8)
        self.filter_pemilih.bind("<<ComboboxSelected>>", lambda e: self.segarkan_pemilih())
        ttk.Button(bar, text="+ Tambah Pemilih", style="Utama.TButton",
                   command=self.dialog_tambah_pemilih).pack(side="right")
        self.lbl_jumlah = ttk.Label(bar)
        self.lbl_jumlah.pack(side="right", padx=14)
        bingkai, self.tree_pemilih = buat_tabel_tree(
            self.f_pemilih, ("NIM", "Nama", "Prodi", "Angkatan", "Status", "Waktu Vote"),
            (140, 200, 130, 80, 130, 150), tinggi=14)
        bingkai.pack(fill="both", expand=True)

    def segarkan_pemilih(self):
        sql = "SELECT * FROM pemilih"
        pilih = self.filter_pemilih.get()
        if pilih == "Sudah memilih":
            sql += " WHERE sudah_memilih = 1"
        elif pilih == "Belum memilih":
            sql += " WHERE sudah_memilih = 0"
        sql += " ORDER BY nim"
        conn = core.koneksi()
        data = conn.execute(sql).fetchall()
        conn.close()
        self.tree_pemilih.delete(*self.tree_pemilih.get_children())
        for p in data:
            status = "SUDAH MEMILIH" if p["sudah_memilih"] else "BELUM MEMILIH"
            self.tree_pemilih.insert("", "end", values=(p["nim"], p["nama"], p["program_studi"] or "",
                                                        p["angkatan"] or "", status, p["tanggal_vote"] or "-"))
        self.lbl_jumlah.config(text=f"{len(data)} pemilih")

    def dialog_tambah_pemilih(self):
        win = tk.Toplevel(self)
        win.title("Tambah Pemilih")
        win.transient(self)
        win.grab_set()
        win.configure(bg=ABU)
        frm = ttk.Frame(win, padding=20)
        frm.pack()
        entri = {}
        for i, lab in enumerate(["NIM", "Nama", "Program Studi", "Angkatan"]):
            ttk.Label(frm, text=lab).grid(row=i, column=0, sticky="w", pady=5)
            e = ttk.Entry(frm, width=34)
            e.grid(row=i, column=1, padx=10)
            entri[lab] = e

        def simpan():
            nim = entri["NIM"].get().strip()
            nama = entri["Nama"].get().strip()
            prodi = entri["Program Studi"].get().strip()
            angk = entri["Angkatan"].get().strip()
            if not (nim and nama and prodi and angk):
                messagebox.showwarning("Data kurang", "Semua kolom wajib diisi.", parent=win)
                return
            if not nim.isdigit() or not angk.isdigit():
                messagebox.showwarning("Salah format", "NIM dan angkatan harus angka.", parent=win)
                return
            conn = core.koneksi()
            if conn.execute("SELECT 1 FROM pemilih WHERE nim = ?", (nim,)).fetchone():
                conn.close()
                messagebox.showerror("ERROR", "NIM sudah terdaftar.", parent=win)
                return
            conn.execute("INSERT INTO pemilih (nim, nama, program_studi, angkatan) VALUES (?, ?, ?, ?)",
                         (nim, nama, prodi, int(angk)))
            conn.commit()
            conn.close()
            core.catat_log(self.admin, "TAMBAH_PEMILIH", f"{nim} {nama}")
            win.destroy()
            self.segarkan_semua()

        ttk.Button(frm, text="Simpan", style="Utama.TButton", command=simpan).grid(
            row=4, column=0, columnspan=2, pady=(14, 0), sticky="ew")

    # ---------------- Audit log ----------------
    def bangun_log(self):
        bar = ttk.Frame(self.f_log)
        bar.pack(fill="x", pady=(0, 8))
        ttk.Label(bar, text="Filter:").pack(side="left")
        self.filter_log = ttk.Combobox(bar, state="readonly", width=20,
                                       values=["100 terakhir", "Semua", "Hanya VOTING", "Hanya login gagal"])
        self.filter_log.current(0)
        self.filter_log.pack(side="left", padx=8)
        self.filter_log.bind("<<ComboboxSelected>>", lambda e: self.segarkan_log())
        bingkai, self.tree_log = buat_tabel_tree(
            self.f_log, ("Waktu", "Aktor", "Aksi", "Keterangan"), (160, 130, 170, 360), tinggi=14)
        bingkai.pack(fill="both", expand=True)

    def segarkan_log(self):
        pilih = self.filter_log.get()
        sql, params = "SELECT * FROM audit_log", ()
        if pilih == "Hanya VOTING":
            sql += " WHERE aksi = ?"
            params = ("VOTING",)
        elif pilih == "Hanya login gagal":
            sql += " WHERE aksi IN ('LOGIN_GAGAL_MHS', 'LOGIN_GAGAL_ADMIN')"
        sql += " ORDER BY id DESC"
        if pilih == "100 terakhir":
            sql += " LIMIT 100"
        conn = core.koneksi()
        data = conn.execute(sql, params).fetchall()
        conn.close()
        self.tree_log.delete(*self.tree_log.get_children())
        for b in data:
            self.tree_log.insert("", "end", values=(b["waktu"], b["aktor"], b["aksi"], b["keterangan"]))

    # ---------------- Tutup pemilu & logout ----------------
    def tutup_pemilu(self):
        if not core.pemilu_aktif():
            return
        if not messagebox.askyesno("Tutup Pemilu",
                                   "Setelah ditutup, mahasiswa tidak bisa memberi suara lagi.\n"
                                   "Tindakan ini tidak dapat dibatalkan dari aplikasi.\n\nYakin menutup pemilu?"):
            return
        conn = core.koneksi()
        conn.execute("UPDATE pengaturan_pemilu SET status_pemilu = ? WHERE id = 1", (core.STATUS_DITUTUP,))
        conn.commit()
        conn.close()
        core.catat_log(self.admin, "TUTUP_PEMILU", "status AKTIF -> DITUTUP")
        self.segarkan_semua()
        self.tab.select(self.f_hasil)
        self.tampilkan_pengumuman()

    def tampilkan_pengumuman(self):
        data, total = self.data_hasil()
        if not data or total == 0:
            messagebox.showinfo("HASIL PEMILIHAN", "Pemungutan suara telah ditutup.\n\n"
                                "Tidak ada suara masuk, pemenang tidak dapat ditentukan.")
            return
        tertinggi = data[0]["total_suara"]
        menang = [k["nama_calon"] for k in data if k["total_suara"] == tertinggi]
        if len(menang) > 1:
            isi = "PEMILIHAN SERI antara:\n" + "\n".join(f"  - {n}" for n in menang)
        else:
            p = core.hitung_persentase(tertinggi, total)
            isi = f"Pemenang :\n{menang[0]}\n\nTotal Suara : {tertinggi}\nPersentase  : {p:.0f}%"
        messagebox.showinfo("HASIL PEMILIHAN", "Pemungutan suara telah ditutup.\n\n" + isi)

    def logout(self):
        core.catat_log(self.admin, "LOGOUT_ADMIN", "")
        self.app.tampil_login()


if __name__ == "__main__":
    core.buat_tabel()
    AplikasiEVote().mainloop()
