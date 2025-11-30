import os
import joblib
import pandas as pd
import numpy as np
from config import Config

class LotteryPredictor:
    def __init__(self):
        # Simpan state di memori (Cache)
        self.model = None
        self.feature_cols = None
        self.test_df = None
        self.target_cols = None  # Cache nama kolom target
        self.date_cache = ([], []) # Cache data dropdown
        self._load_resources()

    def _load_resources(self):
        try:
            if not all(os.path.exists(p) for p in [Config.MODEL_PATH, Config.FEATURES_PATH, Config.TEST_DATA_PATH]):
                raise FileNotFoundError("File aset tidak lengkap.")

            self.model = joblib.load(Config.MODEL_PATH)
            self.feature_cols = joblib.load(Config.FEATURES_PATH)
            
            # Load Dataframe
            df = pd.read_csv(Config.TEST_DATA_PATH, index_col=0)
            df.index = pd.to_datetime(df.index)
            self.test_df = df

            # OPTIMASI 1: Pre-calculate Target Columns
            # Biar gak perlu searching string 'num_' tiap kali prediksi
            self.target_cols = [c for c in df.columns if 'num_' in c or 'target_' in c]

            # OPTIMASI 2: Pre-calculate Dropdown Data
            # Biar gak sorting ulang tiap refresh halaman
            dates = df.index.sort_values(ascending=False)
            years = sorted(dates.year.unique(), reverse=True)
            valid_dates = [d.strftime('%Y-%m-%d') for d in dates]
            self.date_cache = (years, valid_dates)
            
            print("✅ [Service] Resources loaded & cached.")
            
        except Exception as e:
            print(f"❌ [Service] Error: {e}")

    def get_available_dates(self):
        # Tinggal return data yang sudah dihitung di awal (Instant!)
        return self.date_cache

    def predict(self, date_str):
        if self.model is None: raise Exception("Model not loaded")
        
        # Pandas lookup (Hash lookup) sangat cepat
        try:
            row = self.test_df.loc[[date_str]]
        except KeyError:
            raise KeyError("Tanggal tidak ditemukan.")

        # 1. Input Features
        X_input = row[self.feature_cols]

        # 2. Ground Truth (Pakai kolom yang sudah dicache)
        # Flattening numpy array lebih cepat drpd iterasi
        true_balls = np.where(row[self.target_cols].values.flatten() == 1)[0] + 1

        # 3. Predict
        probs = self.model.predict_proba(X_input)
        
        # 4. Sorting Cepat (Vectorized)
        # Ambil probabilitas kelas positif (index 1) untuk semua 49 output
        # Hasil probs adalah list of (n_samples, 2), kita butuh (n_samples, 49)
        # Kita pakai list comprehension karena struktur output RF sklearn agak unik
        final_probs = np.array([p[0, 1] for p in probs]) # Ambil baris pertama, kelas 1
        
        # argpartition lebih cepat dari argsort untuk mengambil Top-K
        # Tapi karena N=49 (kecil), argsort biasa sudah cukup cepat (-6 artinya ambil 6 terakhir)
        pred_balls = np.argsort(final_probs)[-6:][::-1] + 1

        return sorted(pred_balls), sorted(true_balls)