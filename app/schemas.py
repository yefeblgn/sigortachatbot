from pydantic import BaseModel, Field, constr
from typing import Optional, Literal, Dict, Any

FlowType = Literal["general", "hasar_sorgu", "kasko_teklif", "trafik_teklif"]

class ChatInput(BaseModel):
    type: FlowType
    text: constr(strip_whitespace=True, min_length=1)
    meta: Optional[Dict[str, Any]] = None

class ParsedOutput(BaseModel):
    type: Literal["hasar_sorgula","kasko_teklif","trafik_teklif","off_topic","general"]
    fields: Dict[str, Any] = Field(default_factory=dict)
    message: str

class HasarSorguPayload(BaseModel):
    dosya_no: constr(pattern=r"^\d{7,9}$")
    tckn: constr(pattern=r"^\d{11}$")
    tutanak: Optional[Literal["evet","hayir"]] = None

class KaskoTeklifPayload(BaseModel):
    tckn: constr(pattern=r"^\d{11}$")
    plaka: constr(strip_whitespace=True, min_length=4)
    model_yili: constr(pattern=r"^\d{4}$")
    marka: constr(strip_whitespace=True, min_length=2)

class TrafikTeklifPayload(BaseModel):
    tckn: constr(pattern=r"^\d{11}$")
    plaka: constr(strip_whitespace=True, min_length=4)
