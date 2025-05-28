from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal

class YeniTasitFinansman(BaseModel):
    proforma_deger: Decimal
    arac_modeli: str
    kefil_tckn: Optional[str]
    finansman_tutari: Decimal

    @validator('proforma_deger')
    def validate_proforma(cls, v):
        if v > Decimal('7000000'):
            raise ValueError('7M üzeri araçlar için başvuru yapılamaz')
        return v

    @validator('arac_modeli')
    def validate_model(cls, v):
        if 'ticari' in v.lower():
            raise ValueError('Ticari modeller için başvuru yapılamaz')
        return v

    @validator('finansman_tutari')
    def validate_finansman(cls, v, values):
        if 'proforma_deger' in values:
            max_tutar = values['proforma_deger'] * Decimal('0.60')
            if v > max_tutar:
                raise ValueError(f'Finansman tutarı araç değerinin %60\'ını aşamaz (Max: {max_tutar})')
        return v

    @validator('kefil_tckn')
    def validate_kefil(cls, v, values):
        if 'proforma_deger' in values:
            if values['proforma_deger'] >= Decimal('5000000') and not v:
                raise ValueError('5M ve üzeri araçlar için kefil zorunludur')
        return v

class IkinciElFinansman(BaseModel):
    kasko_degeri: Decimal
    arac_yasi: int
    finansman_tutari: Decimal
    satici_tckn: Optional[str]

    @validator('arac_yasi')
    def validate_yas(cls, v):
        if v > 5:
            raise ValueError('5 yaş üstü araçlar için başvuru yapılamaz')
        return v

    @validator('finansman_tutari')
    def validate_finansman(cls, v, values):
        if 'kasko_degeri' in values:
            max_tutar = min(values['kasko_degeri'] * Decimal('0.40'), Decimal('3000000'))
            if v > max_tutar:
                raise ValueError(f'Finansman tutarı kasko değerinin %40\'ını veya 3M\'yi aşamaz (Max: {max_tutar})')
        return v

def validate_tckn(tckn: str) -> bool:
    """TC Kimlik numarası doğrulama"""
    if not tckn or not tckn.isdigit() or len(tckn) != 11:
        return False
    
    digits = [int(d) for d in tckn]
    if digits[0] == 0:
        return False
        
    if not (((sum(digits[0:10:2]) * 7) - sum(digits[1:9:2])) % 10) == digits[9]:
        return False
        
    if not (sum(digits[0:10]) % 10) == digits[10]:
        return False
        
    return True 