GELİŞTİRME SÜRECİ
1. Temel Altyapı
- FastAPI web uygulaması kurulumu
- ChromaDB ve Mistral 7B entegrasyonu
- Temel endpoint'lerin oluşturulması

2. Veri Hazırlığı
- SSS veritabanı oluşturma
- Araç finansmanı kurallarının tanımlanması
- Training verilerinin hazırlanması

3. Chatbot Mantığı
- Yanıt önceliklendirme sistemi
- Durum yönetimi
- Kullanıcı oturum takibi

4. Test ve Optimizasyon
- Performans testleri
- Kullanıcı testleri
- Sistem optimizasyonları

CHATBOT WORKFLOW

1. Karşılama ve Kimlik Doğrulama
- Müşteri girişi ve kimlik doğrulama
- Önceki başvuru kontrolü
- Müşteri segmenti belirleme (bireysel/kurumsal)

2. Araç Bilgileri Toplama
- Araç tipi (yeni/ikinci el)
- Marka/model/yıl bilgileri
- Fiyat bilgisi
LLM: Araç değerleme kontrolü ve uygunluk analizi

3. Finansman Koşulları
- Ödeme planı tercihi
- Peşinat miktarı
- Vade seçimi
LLM: Finansman şartlarının değerlendirilmesi

4. Başvuru Tamamlama
- Belge talepleri
- Onay süreci bilgilendirme
- Sonraki adımlar


 Chatbot inference maliyeti düşürme yöntemleri

## 1. Katmanlı Mimari Yaklaşımı
## 2. Model Optimizasyonları
### Quantization
## 3. Sistem Seviyesi Optimizasyonlar
### Önbellekleme Stratejisi
### Batch Processing
## 4. Donanım Optimizasyonları
### GPU Kullanımı
### CPU Fallback
## 5. Prompt Mühendisliği
### Prompt Optimizasyonu
- min token sayısı,max context
## 6. Ölçeklendirme Stratejileri
### Load Balancing
### Dinamik Ölçeklendirme

