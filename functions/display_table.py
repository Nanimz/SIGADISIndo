import pandas as pd
from datetime import datetime

loaded_df = None
valid_filter_columns = {}

FILTER_COLUMN_MAP = {
    "Jenjang Sekolah": "JENJANG SEKOLAH",
    "Status Pegawai": "STATUS PEGAWAI",
    "Golongan": "GOLONGAN",
    "Jenis Kelamin": "JENIS KELAMIN",
    "Sertifikasi": "SERTIFIKASI",
    "Inpassing": "INPASSING",
    "Pensiun": "PENSIUN",
    "Masa Kerja": "TANGGAL TMT PENDIDIK",
    "Usia": "USIA"
}

def load_data(file_path):
    global loaded_df, valid_filter_columns
    try:
        if file_path.endswith(".csv"):
            loaded_df = pd.read_csv(file_path, dtype=str)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            loaded_df = pd.read_excel(file_path, dtype=str)
        else:
            loaded_df = None
    except Exception as e:
        print(f"⚠️ Gagal memuat file: {e}")
        loaded_df = None
        return

    if loaded_df is not None:
        # 🧼 Bersihkan nilai
        loaded_df.fillna("nan", inplace=True)
        cols_to_clean = ["NUPTK", "NRG", "NIP", "NIK", "NO SK DIRJEN"]
        for col in cols_to_clean:
            if col in loaded_df.columns:
                loaded_df[col] = loaded_df[col].astype(str).str.replace(r'\\.0$', '', regex=True)

        # 🔁 Normalisasi kolom ke lowercase untuk pemrosesan
        lower_columns = [col.lower() for col in loaded_df.columns]
        loaded_df.columns = lower_columns

        # 🧠 Petakan filter hanya yang tersedia (pakai lowercase)
        valid_filter_columns = {label: col.lower() for label, col in FILTER_COLUMN_MAP.items() if col.lower() in loaded_df.columns}


def get_loaded_data():
    global loaded_df
    return loaded_df.copy() if loaded_df is not None else None

def filter_data(filters):
    df = get_loaded_data()
    if df is None:
        return pd.DataFrame()

    today = pd.Timestamp.today()

    for label, value in filters.items():
        column = valid_filter_columns.get(label)
        if column:
            if label == "Usia" and "-" in value:
                try:
                    lower, upper = map(int, value.split("-"))
                    df[column] = pd.to_numeric(df[column], errors='coerce')
                    df = df[df[column].between(lower, upper, inclusive="left")]
                except ValueError:
                    continue

            elif label == "Masa Kerja" and "-" in value:
                try:
                    lower, upper = map(int, value.split("-"))
                    df[column] = pd.to_datetime(df[column], errors="coerce")
                    df["MASA_KERJA_TAHUN"] = (today - df[column]).dt.days // 365
                    df = df[df["MASA_KERJA_TAHUN"].between(lower, upper, inclusive="left")]
                except Exception as e:
                    print(f"❌ Gagal menghitung masa kerja: {e}")
                    continue

            else:
                df = df[df[column] == value]
    return df