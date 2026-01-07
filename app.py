import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import time
from datetime import date

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Teman Jurusan", page_icon="🎓", layout="centered")

# --- CUSTOM CSS UNTUK TAMPILAN MODERN & SERTIFIKAT ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    
    /* Tombol Custom */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3.2em;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Style Sertifikat */
    .certificate-container {
        border: 10px solid #1E88E5;
        border-double: 4px;
        padding: 40px;
        background-color: white;
        text-align: center;
        font-family: 'Georgia', serif;
        position: relative;
        color: #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .cert-header { color: #1E88E5; font-size: 35px; font-weight: bold; margin-bottom: 0px; }
    .cert-sub { font-size: 16px; letter-spacing: 2px; text-transform: uppercase; color: #555; }
    .cert-name { font-size: 30px; font-weight: bold; border-bottom: 2px solid #333; display: inline-block; padding: 0 20px; margin: 15px 0; color: #111; }
    .cert-text { font-size: 16px; line-height: 1.5; margin: 15px 40px; }
    .cert-result { font-size: 26px; font-weight: bold; color: #1565C0; background: #e3f2fd; padding: 15px; border-radius: 10px; border: 1px dashed #1E88E5; }
    .cert-footer { margin-top: 30px; font-size: 12px; font-style: italic; color: #777; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE DESKRIPSI JURUSAN ---
deskripsi_jurusan = {
    'Pendidikan Teknologi Informasi': {'desc': 'Fokus pada pengajaran IT, pemrograman, dan sistem informasi.', 'prospek': 'Guru TIK, IT Trainer, EdTech Developer.'},
    'Pendidikan Matematika': {'desc': 'Mempelajari metode pengajaran matematika yang efektif dan logika angka.', 'prospek': 'Guru Matematika, Peneliti Pendidikan, Analis Data.'},
    'Pendidikan Biologi': {'desc': 'Mempelajari mahluk hidup dan teknik pengajaran laboratorium biologi.', 'prospek': 'Guru Biologi, Peneliti, Konsultan Lingkungan.'},
    'Pendidikan Fisika': {'desc': 'Mendalami konsep energi, materi, dan alam untuk dunia pendidikan.', 'prospek': 'Guru Fisika, Teknisi Laboratorium.'},
    'Sistem Operasi': {'desc': 'Arsitektur software pengelola hardware komputer dan keamanan sistem.', 'prospek': 'System Administrator, Cloud Engineer, IT Support.'},
    'Pendidikan Bahasa dan Sastra Indonesia': {'desc': 'Tata bahasa, sastra, dan teknik komunikasi bahasa Indonesia.', 'prospek': 'Guru B.Indo, Penulis, Editor, Jurnalis.'},
    'Pendidikan Bahasa Inggris': {'desc': 'Kemampuan internasional dan metode mengajar bahasa asing.', 'prospek': 'Guru B.Inggris, Translator, Diplomat.'},
    'Pendidikan Guru Sekolah Dasar': {'desc': 'Membimbing anak usia emas sekolah dasar secara holistik.', 'prospek': 'Guru SD, Pengembang Kurikulum Dasar.'},
    'Pendidikan IPS': {'desc': 'Hubungan sosial, sejarah, geografi, dan ekonomi masyarakat.', 'prospek': 'Guru IPS, Peneliti Sosial.'},
    'Pendidikan PKN': {'desc': 'Hukum, norma, demokrasi, dan nilai kewarganegaraan.', 'prospek': 'Guru PKN, Staf Pemerintah, Aktivis.'}
}

# --- 3. AI ENGINE (DECISION TREE) ---
# Data latih buatan untuk memberikan logika pada model AI
data_latih = {
    'MTK': [95, 80, 85, 60, 95, 45, 75, 55, 65, 88, 40, 50, 92, 70, 60],
    'IPA': [90, 50, 95, 40, 85, 30, 40, 85, 30, 85, 80, 20, 90, 40, 30],
    'IPS': [30, 95, 40, 85, 30, 80, 90, 40, 80, 50, 20, 95, 35, 85, 90],
    'Inggris': [75, 85, 65, 95, 75, 85, 85, 70, 95, 65, 60, 90, 70, 95, 85],
    'Target': [
        'Pendidikan Matematika', 'Pendidikan IPS', 'Pendidikan Biologi', 
        'Pendidikan Bahasa Inggris', 'Sistem Operasi', 'Pendidikan Guru Sekolah Dasar',
        'Pendidikan PKN', 'Pendidikan Fisika', 'Pendidikan Bahasa dan Sastra Indonesia',
        'Pendidikan Teknologi Informasi', 'Pendidikan Biologi', 'Pendidikan IPS',
        'Pendidikan Teknologi Informasi', 'Pendidikan Bahasa Inggris', 'Pendidikan IPS'
    ]
}
df = pd.DataFrame(data_latih)
model = DecisionTreeClassifier()
model.fit(df[['MTK', 'IPA', 'IPS', 'Inggris']], df['Target'])

# --- 4. SESSION STATE & SIDEBAR ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2102/2102633.png", width=80)
    st.title("Teman Jurusan")
    st.write("---")
    steps = {"welcome": 0, "identitas": 33, "nilai": 66, "hasil": 100}
    st.progress(steps[st.session_state.page])
    st.caption(f"Langkah: {st.session_state.page.capitalize()}")
    st.write("---")
    st.info("AI Teman Jurusan menganalisis pola nilai ijazah untuk memberikan saran masa depan.")

def change_page(page_name):
    st.session_state.page = page_name

# --- 5. HALAMAN 1: WELCOME ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🎓 Teman Jurusan</h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co.com/mrftg5d8/IMG-20260107-WA0009.jpg", use_container_width=True)
    st.markdown("<h4 style='text-align: center;'>Partner Setia Memilih Masa Depan</h4>", unsafe_allow_html=True)
    st.write("Selamat datang! Aplikasi ini akan membantumu menentukan jurusan kuliah terbaik berdasarkan data akademikmu.")
    if st.button("Mulai Konsultasi 🚀"):
        change_page('identitas')

# --- 6. HALAMAN 2: IDENTITAS & SEKOLAH ---
elif st.session_state.page == 'identitas':
    st.title("👤 Profil Siswa")
    with st.container(border=True):
        nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama sesuai ijazah")
        col1, col2 = st.columns(2)
        with col1:
            sekolah = st.radio("Asal Sekolah", ["SMA", "SMK"], horizontal=True)
        with col2:
            if sekolah == "SMA":
                jur_asal = st.selectbox("Jurusan SMA", ["IPA", "IPS"])
            else:
                jur_asal = st.selectbox("Jurusan SMK", ["TIK", "Kesehatan", "Manajemen", "Akuntansi", "Pariwisata", "Otomotif", "Seni", "Pertanian"])
    
    if st.button("Lanjut ke Pengisian Nilai ➡️"):
        if nama:
            st.session_state.nama = nama
            st.session_state.asal = f"{sekolah} - {jur_asal}"
            change_page('nilai')
        else:
            st.error("Nama wajib diisi!")

# --- 7. HALAMAN 3: INPUT NILAI ---
elif st.session_state.page == 'nilai':
    st.title("📝 Input Nilai Ijazah")
    st.write(f"Halo **{st.session_state.nama}**, silakan masukkan nilai rata-rata mata pelajaranmu:")
    
    with st.container(border=True):
        st.subheader("📊 Daftar Mata Pelajaran")
        c1, c2, c3 = st.columns(3)
        with c1:
            pai = st.number_input("PAI", 0, 100, 85)
            pkn = st.number_input("PKN", 0, 100, 85)
            indo = st.number_input("B. Indonesia", 0, 100, 85)
            ing = st.number_input("B. Inggris", 0, 100, 85)
        with c2:
            pjok = st.number_input("PJOK", 0, 100, 85)
            mtk = st.number_input("Matematika", 0, 100, 85)
            sunda = st.number_input("B. Sunda", 0, 100, 80)
            ipa = st.number_input("IPA", 0, 100, 80)
        with c3:
            ips = st.number_input("IPS", 0, 100, 80)
            tik = st.number_input("TIK", 0, 100, 80)
            seni = st.number_input("Seni Budaya", 0, 100, 80)

    if st.button("Proses Analisis AI 🔍"):
        with st.spinner("AI Teman Jurusan sedang menghitung kecocokan..."):
            time.sleep(2)
            # Prediksi berdasarkan fitur kunci (MTK, IPA, IPS, Inggris)
            prediksi = model.predict([[mtk, ipa, ips, ing]])
            st.session_state.hasil = prediksi[0]
            change_page('hasil')

# --- 8. HALAMAN 4: HASIL (SERTIFIKAT DIGITAL) ---
elif st.session_state.page == 'hasil':
    st.balloons()
    res = st.session_state.hasil
    tgl = date.today().strftime("%d %B %Y")
    
    st.markdown("<h2 style='text-align: center;'>✨ Hasil Rekomendasi</h2>", unsafe_allow_html=True)
    
    # Tampilan Sertifikat
    st.markdown(f"""
        <div class="certificate-container">
            <div class="cert-sub">Official Recommendation Certificate</div>
            <div class="cert-header">Teman Jurusan AI</div>
            <br>
            <div style="font-size: 18px;">Diberikan Kepada:</div>
            <div class="cert-name">{st.session_state.nama.upper()}</div>
            <div class="cert-text">
                Berdasarkan analisis cerdas terhadap performa akademik dan latar belakang sekolah <b>{st.session_state.asal}</b>, sistem AI Teman Jurusan merekomendasikan siswa untuk melanjutkan ke jenjang:
            </div>
            <div class="cert-result">{res}</div>
            <div class="cert-footer">
                Diterbitkan secara otomatis pada {tgl}<br>
                Digital Verification ID: TJ-{int(time.time())}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    with st.expander("📖 Lihat Penjelasan Jurusan"):
        info = deskripsi_jurusan.get(res, {'desc': '-', 'prospek': '-'})
        st.write(f"**Tentang Jurusan:** {info['desc']}")
        st.write(f"**Prospek Karir:** {info['prospek']}")

    if st.button("Konsultasi Ulang 🔄"):
        change_page('welcome')