## CASE1
# 🚀 Çalışan Ayrılma (Attrition) Tahmini Projesi

Bu proje, çalışanların şirkette kalıp kalmayacağını (Attrition: Yes/No) tahmin etmek için bir sınıflandırma modeli geliştirmeyi hedefler. Şirketin insan kaynakları karar destek süreçlerini veri odaklı hale getirerek, ayrılma riskini erken tespit etmeyi amaçlamaktadır.

---

## 📊 Veri Seti

- Şirket çalışan verileri (demografik bilgiler, iş memnuniyeti, performans ölçütleri vb.)
- Hedef sütun: **Attrition** (Yes/No, binary sınıf)

---

## ⚙️ Ana Aşamalar

✅ **Veri İncelemesi ve Temizleme**  
- Eksik veri bulunmuyor, aykırı değerler anlamlı → modele doğrudan dahil edildi.  
- Korelasyon (ısı haritası) ve dağılım analizi yapıldı.

✅ **Feature Engineering**  
- Oran bazlı ve etkileşimli yeni özellikler oluşturuldu:  
  - `YearsInCurrentRoleRatio`, `Age_YearsAtCompany`, `EnvJobSatisfaction` vb.  
- Kategorik değişkenler **One-Hot Encoding** ile sayısallaştırıldı.

✅ **Modelleme ve Threshold Tuning**  
- Kullanılan modeller: Logistic Regression, Random Forest, XGBoost  
- Threshold tuning ile özellikle **Recall** ve **F1-Score** optimize edildi.  
- Performans metrikleri: Accuracy, Precision, Recall, F1-Score, ROC-AUC

✅ **Sonuçlar ve Karşılaştırmalar**  
- **Logistic Regression** Recall ve F1-Score’da en iyi performansı gösterdi.  
- **Random Forest** ve **XGBoost** alternatif olarak test edildi.  
- Yeni feature’lar Logistic Regression’ın recall ve F1’ini daha da iyileştirdi.  
- ROC-AUC tüm modellerde stabil (~0.8) – genel ayırt edicilik yüksek.

---


## CASE2 

# Araç Finansmanı Chatbot

Bu proje, araç finansmanı ön başvurusu ve SSS için chatbot API’sidir. Kullanıcıdan aldığı mesajı vektör tabanlı ChromaDB ile eşleştirir, Ollama LLM kullanarak akıcı yanıt döndürür.

## Özellikler
✅ Yeni/ikinci el finansman başvuru akışı  

✅ SSS veritabanı: ChromaDB + SentenceTransformer  

✅ Ollama LLM ile akıcı yanıtlar  

✅ FastAPI tabanlı REST API  

## Kurulum ve Çalıştırma

1. Ortamı oluştur

python -m venv chatbot_env


2. Ortamı aktifleştir

chatbot_env\Scripts\activate  # Windows

source chatbot_env/bin/activate  # Linux/macOS


3. Gereksinimleri yükle

pip install -r requirements.txt


4. Embedding verilerini yükle

python db_setup.py


5. Ollama sunucusunu başlat

ollama serve


6. API’yi başlat

uvicorn app:app --host 0.0.0.0 --port 8000
