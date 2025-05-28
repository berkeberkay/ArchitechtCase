import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Genişletilmiş SSS verisi
sss_data = [
    {"id": "1", "soru": "Araç yaşı kaç olabilir?", "cevap": "İkinci el araç finansmanında araç yaşı en fazla 5 olabilir."},
    {"id": "2", "soru": "HGS başvurusu nasıl yapılır?", "cevap": "Araç finansmanı başvurunuz onaylandıktan sonra HGS başvurunuzu da yapabilirsiniz."},
    {"id": "3", "soru": "Finansman oranı nedir?", "cevap": "Yeni araçlarda araç bedelinin %60'ına, ikinci el araçlarda ise kasko değerinin %40'ına kadar finansman sağlanabilir."},
    {"id": "4", "soru": "Kefil gerekli mi?", "cevap": "5 milyon TL ve üzeri araç değeri olan başvurularda kefil zorunludur."},
    {"id": "5", "soru": "Ticari araç için başvuru yapabilir miyim?", "cevap": "Hayır, ticari araçlar için finansman başvurusu kabul edilmemektedir."},
    {"id": "6", "soru": "Maksimum finansman tutarı nedir?", "cevap": "İkinci el araçlarda maksimum finansman tutarı 3 milyon TL'dir. Yeni araçlarda ise araç değerinin %60'ı kadardır."},
    {"id": "7", "soru": "Satıcı TCKN zorunlu mu?", "cevap": "İkinci el araç finansmanında satıcı TCKN bilgisi opsiyoneldir, zorunlu değildir."},
    {"id": "8", "soru": "Başvuru sonucunu nasıl öğrenebilirim?", "cevap": "Başvurunuz tamamlandıktan sonra size SMS ile bilgilendirme yapılacaktır."},
    {"id": "9", "soru": "Başvurumu iptal edebilir miyim?", "cevap": "Evet, başvurunuzu herhangi bir aşamada iptal edebilirsiniz."},
    {"id": "10", "soru": "Proforma fatura gerekli mi?", "cevap": "Evet, yeni araç finansmanı için proforma fatura gereklidir."}
]

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("sss_collection")
embed_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Verileri ekle
for item in sss_data:
    text = f"Soru: {item['soru']} Cevap: {item['cevap']}"
    embedding = embed_model.encode(text).tolist()
    collection.add(
        documents=[text],
        ids=[item["id"]],
        embeddings=[embedding]
    )

print(" SSS verileri ChromaDB'ye eklendi!")
