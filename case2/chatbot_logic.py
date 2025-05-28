from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel
from vehicle_finance import YeniTasitFinansman, IkinciElFinansman

class ChatState(Enum):
    INITIAL = "initial"
    ARAC_TURU = "arac_turu"
    YENI_ARAC_BILGI = "yeni_arac_bilgi"
    IKINCI_EL_BILGI = "ikinci_el_bilgi"
    TEYIT = "teyit"
    HGS = "hgs"
    COMPLETED = "completed"

class ChatSession(BaseModel):
    state: ChatState = ChatState.INITIAL
    data: Dict[str, Any] = {}
    current_field: Optional[str] = None

class ChatbotLogic:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}

    def get_session(self, session_id: str) -> ChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession()
        return self.sessions[session_id]

    def get_session_context(self, session_id: str) -> str:
        """Oturum bağlamını döndürür"""
        session = self.get_session(session_id)
        context = f"Mevcut Durum: {session.state.value}\n"
        
        if session.data:
            context += "Toplanan Bilgiler:\n"
            for key, value in session.data.items():
                context += f"- {key}: {value}\n"
                
        if session.current_field:
            context += f"\nŞu an istenen bilgi: {session.current_field}"
            
        return context

    def process_message(self, session_id: str, message: str) -> str:
        session = self.get_session(session_id)
        
        if session.state == ChatState.INITIAL:
            return self._handle_initial_state(session)
            
        elif session.state == ChatState.ARAC_TURU:
            return self._handle_arac_turu(session, message)
            
        elif session.state == ChatState.YENI_ARAC_BILGI:
            return self._handle_yeni_arac(session, message)
            
        elif session.state == ChatState.IKINCI_EL_BILGI:
            return self._handle_ikinci_el(session, message)
            
        elif session.state == ChatState.TEYIT:
            return self._handle_teyit(session, message)
            
        elif session.state == ChatState.HGS:
            return self._handle_hgs(session, message)
            
        return "Üzgünüm, bir hata oluştu. Başvuruyu yeniden başlatabilir miyiz?"

    def _handle_initial_state(self, session: ChatSession) -> str:
        session.state = ChatState.ARAC_TURU
        return "Araç finansmanı başvurunuz için hoş geldiniz! Yeni araç için mi, yoksa ikinci el araç için mi başvuru yapmak istersiniz? (Yeni/İkinci El)"

    def _handle_arac_turu(self, session: ChatSession, message: str) -> str:
        lower_msg = message.lower()
        if "yeni" in lower_msg:
            session.data["arac_turu"] = "yeni"
            session.state = ChatState.YENI_ARAC_BILGI
            session.current_field = "proforma_deger"
            return "Lütfen araç proforma fatura değerini giriniz (TL):"
        elif "ikinci" in lower_msg or "2." in lower_msg:
            session.data["arac_turu"] = "ikinci_el"
            session.state = ChatState.IKINCI_EL_BILGI
            session.current_field = "kasko_degeri"
            return "Lütfen araç kasko değerini giriniz (TL):"
        else:
            return "Lütfen 'Yeni' veya 'İkinci El' seçeneklerinden birini belirtiniz."

    def _handle_yeni_arac(self, session: ChatSession, message: str) -> str:
        try:
            if session.current_field == "proforma_deger":
                session.data["proforma_deger"] = float(message)
                session.current_field = "arac_modeli"
                return "Lütfen araç modelini giriniz:"
                
            elif session.current_field == "arac_modeli":
                session.data["arac_modeli"] = message
                if session.data["proforma_deger"] >= 5000000:
                    session.current_field = "kefil_tckn"
                    return "5M TL ve üzeri araçlar için kefil gereklidir. Lütfen kefil TC kimlik numarasını giriniz:"
                else:
                    session.current_field = "finansman_tutari"
                    return f"Lütfen talep ettiğiniz finansman tutarını giriniz (maksimum {session.data['proforma_deger'] * 0.6:,.2f} TL):"
                    
            elif session.current_field == "kefil_tckn":
                session.data["kefil_tckn"] = message
                session.current_field = "finansman_tutari"
                return f"Lütfen talep ettiğiniz finansman tutarını giriniz (maksimum {session.data['proforma_deger'] * 0.6:,.2f} TL):"
                
            elif session.current_field == "finansman_tutari":
                session.data["finansman_tutari"] = float(message)
                # Validasyon
                YeniTasitFinansman(**session.data)
                session.state = ChatState.TEYIT
                return self._generate_teyit_mesaji(session)
                
        except ValueError as e:
            return f"Hata: {str(e)}. Lütfen tekrar deneyiniz."
            
        return "Bir hata oluştu, lütfen tekrar deneyiniz."

    def _handle_ikinci_el(self, session: ChatSession, message: str) -> str:
        try:
            if session.current_field == "kasko_degeri":
                session.data["kasko_degeri"] = float(message)
                session.current_field = "arac_yasi"
                return "Lütfen araç yaşını giriniz:"
                
            elif session.current_field == "arac_yasi":
                session.data["arac_yasi"] = int(message)
                session.current_field = "finansman_tutari"
                max_tutar = min(session.data["kasko_degeri"] * 0.4, 3000000)
                return f"Lütfen talep ettiğiniz finansman tutarını giriniz (maksimum {max_tutar:,.2f} TL):"
                
            elif session.current_field == "finansman_tutari":
                session.data["finansman_tutari"] = float(message)
                session.current_field = "satici_tckn"
                return "Satıcı TC kimlik numarasını girebilirsiniz (opsiyonel, boş bırakılabilir):"
                
            elif session.current_field == "satici_tckn":
                if message.strip():
                    session.data["satici_tckn"] = message
                # Validasyon
                IkinciElFinansman(**session.data)
                session.state = ChatState.TEYIT
                return self._generate_teyit_mesaji(session)
                
        except ValueError as e:
            return f"Hata: {str(e)}. Lütfen tekrar deneyiniz."
            
        return "Bir hata oluştu, lütfen tekrar deneyiniz."

    def _handle_teyit(self, session: ChatSession, message: str) -> str:
        if "evet" in message.lower():
            session.state = ChatState.HGS
            return "Başvurunuz başarıyla kaydedildi! HGS ürünü almak ister misiniz? (Evet/Hayır)"
        elif "hayır" in message.lower():
            session.state = ChatState.INITIAL
            session.data = {}
            return "Başvuruyu yeniden başlatıyoruz. " + self._handle_initial_state(session)
        else:
            return "Lütfen 'Evet' veya 'Hayır' şeklinde yanıt veriniz."

    def _handle_hgs(self, session: ChatSession, message: str) -> str:
        if "evet" in message.lower():
            session.state = ChatState.COMPLETED
            return "HGS talebiniz kaydedildi. Başvurunuz tamamlandı, teşekkür ederiz!"
        elif "hayır" in message.lower():
            session.state = ChatState.COMPLETED
            return "Başvurunuz tamamlandı, teşekkür ederiz!"
        else:
            return "Lütfen 'Evet' veya 'Hayır' şeklinde yanıt veriniz."

    def _generate_teyit_mesaji(self, session: ChatSession) -> str:
        if session.data["arac_turu"] == "yeni":
            return f"""
Lütfen bilgilerinizi teyit ediniz:
- Araç Türü: Yeni
- Proforma Değeri: {session.data['proforma_deger']:,.2f} TL
- Araç Modeli: {session.data['arac_modeli']}
- Kefil TCKN: {session.data.get('kefil_tckn', 'Gerekli değil')}
- Finansman Tutarı: {session.data['finansman_tutari']:,.2f} TL

Bilgiler doğru mu? (Evet/Hayır)
"""
        else:
            return f"""
Lütfen bilgilerinizi teyit ediniz:
- Araç Türü: İkinci El
- Kasko Değeri: {session.data['kasko_degeri']:,.2f} TL
- Araç Yaşı: {session.data['arac_yasi']}
- Finansman Tutarı: {session.data['finansman_tutari']:,.2f} TL
- Satıcı TCKN: {session.data.get('satici_tckn', 'Belirtilmedi')}

Bilgiler doğru mu? (Evet/Hayır)
""" 