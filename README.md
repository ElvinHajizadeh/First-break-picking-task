# Seismic First Break Picking
## Seysmik İlk Gəliş Zamanlarının Avtomatik Müəyyən Edilməsi

Bu layihə seysmik məlumatlardan **first break** zamanlarını avtomatik tapmaq üçün hibrid bir alqoritm inkişaf etdirir. Bandpass filtr, AIC picker və median hamarlamanın kombinasiyasına əsaslanır.

---

## 📁 Fayl Strukturu

```
First-break-picking-task-main/
│
├── 📄 final_solution.py          # ← Əsas icra faylı (bütün pipeline burada)
│
├── 🔬 Picker İnkişaf Mərhələləri
│   ├── stalta_picker.py          # STA/LTA metodu ilə ilk cəhd
│   ├── aic_picker.py             # AIC əsaslı picker
│   ├── improved_picker.py        # Təkmilləşdirilmiş versiya
│   ├── robust_picker.py          # Daha davamlı versiya
│   ├── line_picker.py            # Xətt əsaslı picker
│   └── final_picker.py           # Final picker məntiqi
│
├── 🗂️ Data Təşkili Skriptləri
│   ├── explore_data.py           # HDF5 faylına ilkin baxış
│   ├── check_organization.py     # Data strukturunu yoxlama
│   ├── organize_gathers.py       # Shot gather-ları qovluqlara ayırma
│   ├── organize_by_lines.py      # DBSCAN ilə receiver xəttlərinə görə təşkil
│   ├── better_organization.py    # Təkmilləşdirilmiş təşkil skripti
│   └── visualize_gather.py       # Shot gather vizuallaşdırması
│
├── 📊 Nəticə Şəkilləri
│   ├── receiver_lines.png        # DBSCAN ilə tapılan receiver xəttləri
│   ├── shot_gather_visualization.png
│   ├── stalta_results.png
│   ├── aic_results.png
│   ├── hybrid_results.png
│   ├── line_results.png
│   ├── robust_results.png
│   ├── final_results.png
│   └── final_robust_results.png  # ← Son nəticə (sarı xətt = alqoritm, qırmızı nöqtə = həqiqi)
│
└── 📋 Sənədlər
    ├── Automated Algorithm Development for Seismic First Break Picking.md
    ├── Automated Algorithm Development for Seismic First Break Picking.pptx
    └── Firstbreakpickingtasksdescription.pdf
```

---

## 🎯 Problem Təsviri

**First break** — seysmik dalğanın yerüstü mənbədən çıxıb qeydedici (receiver) stansiyasına çatdığı ilk an deməkdir. Bu zamanlar:

- Seysmik refraksiyon tədqiqatlarında
- Yer qabığı tomografiyasında
- Mədən səsmiğinin emalında

əsas girdi məlumatı kimi istifadə olunur. Əl ilə işarələmə (manual picking) son dərəcə vaxt apardığından avtomatlaşdırma vacibdir.

---

## 📊 Dataset

**Halfmile** seysmik aktivinin HDF5 faylından istifadə edilmişdir.

| Sahə         | Təsvir                                                        |
|--------------|---------------------------------------------------------------|
| `data_array` | Bütün seysmik izlər — 2D massiv (iz sayı × nümunə sayı)      |
| `SHOTID`     | Shot identifikatorları                                        |
| `REC_X`      | Receiver X koordinatı                                         |
| `REC_Y`      | Receiver Y koordinatı                                         |
| `SAMP_RATE`  | Nümunəalma tezliyi (mikrosan)                                 |
| `SPARE1`     | First break zamanları (ms). 0 və ya -1 = işarəsiz iz          |

> **Qeyd:** Data faylı (`seismic_data/Halfmile.hdf5`) depoya daxil deyil — ayrıca əldə edilməlidir.

---

## ⚙️ Alqoritm Pipeline-ı

```
HDF5 Data Faylı
       │
       ▼
  Data Yüklənməsi
  (h5py, SHOTID, REC_X, REC_Y, SPARE1)
       │
       ▼
  Xəttlərə Görə Qruplaşdırma
  (DBSCAN clustering — receiver koordinatlarına görə)
       │
       ▼
  Bandpass Filtr
  (5–80 Hz, Butterworth 5-ci dərəcə, filtfilt)
       │
       ▼
  AIC Picker
  (hər iz üçün dispersiya dəyişkənliyi minimumu tapılır)
       │
       ▼
  Outlier Rədd Edilməsi
  (median filtr ilə ətrafdakılardan >30 nümunə fərqli olanlar korreksiya edilir)
       │
       ▼
  Yekun Hamarlaşdırma
  (medfilt, kernel_size=11)
       │
       ▼
  First Break Zamanları (ms)
```

---

## 📈 Nəticələr

Alqoritm **Halfmile** datasetinin ilk 10 xətti üzərində sınaqdan keçirilmişdir:

| Metrika                       | Dəyər      |
|-------------------------------|------------|
| **Orta Mütləq Xəta (MAE)**    | 85.83 ms   |
| **Median Mütləq Xəta (MdAE)** | **8.00 ms** |

Median xəta daha real göstəricidir — əksər izlərdə alqoritm son dərəcə dəqiqdir. MAE isə bəzi küylü izlərdəki böyük kənarlaşmalardan təsirlənir.

---

## 🚀 İstifadə

### 1. Asılılıqları quraşdırın

```bash
pip install numpy scipy matplotlib h5py scikit-learn
```

### 2. Data faylını yerləşdirin

```
seismic_data/
└── Halfmile.hdf5
```

### 3. Data strukturunu yoxlayın

```bash
python explore_data.py
python check_organization.py
```

### 4. Data-nı xəttlərə görə təşkil edin

```bash
python organize_by_lines.py
```

Bu skript `lines/` qovluğunu yaradır və hər shot-xətt cütü üçün `.npy` faylları saxlayır.

### 5. Əsas pipeline-ı işə salın

```bash
python final_solution.py
```

Çıxış:
```
Overall Median Absolute Error: 8.00 ms
Overall Mean Absolute Error: 85.83 ms
```

Vizuallaşdırma `final_robust_results.png` faylında saxlanılır.

---

## 🔬 İnkişaf Mərhələləri

| Skript              | Metod                            |
|---------------------|----------------------------------|
| `stalta_picker.py`  | STA/LTA nisbəti (klassik metod)  |
| `aic_picker.py`     | Akaike Information Criterion     |
| `improved_picker.py`| AIC + ilk filtr cəhdi            |
| `robust_picker.py`  | AIC + outlier rəddi              |
| `line_picker.py`    | Xətt əsaslı spatial analiz       |
| `final_solution.py` | Tam hibrid pipeline (son versiya)|

---

## 🔮 Gələcək İşlər

- Digər datasetlər (Brunswick, Lalor, Sudbury) üzərində sınaq
- Parametrlərin optimallaşdırılması
- ML/DL əsaslı yanaşmaların araşdırılması (CNN, U-Net)
- Real-vaxt emal üçün optimallaşdırma
