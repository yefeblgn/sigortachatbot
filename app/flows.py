import json
import requests
from datetime import datetime
from app.schemas import ParsedOutput, HasarSorguPayload, KaskoTeklifPayload, TrafikTeklifPayload
from app.config import settings

OFF_TOPIC_MESSAGE = (
    "Konu dışı isteğe yardımcı olamıyorum. "
    "Sigorta ile ilgili hasar sorgu, kasko teklif veya trafik teklif konularında ilerleyebiliriz."
)

SYSTEM_CORE = """Yalnızca JSON üret. Şema:
{
  "type": "hasar_sorgula" | "kasko_teklif" | "trafik_teklif" | "general" | "off_topic",
  "fields": {},
  "message": "<kısa, net, Türkçe yönlendirme/cevap>"
}
Konu dışıysa "type":"off_topic" ve "message":"Konu dışı ..." döndür.
General modunda kullanıcının niyetini teşhis et, uygun flow'u ve eksik alanları belirterek yönlendirici kısa mesaj yaz.
Zorunlu alanlar:
hasar_sorgula: dosya_no(7-9 rakam), tckn(11 rakam), tutanak(evet|hayir, opsiyonel)
kasko_teklif: tckn(11 rakam), plaka, model_yili(4 rakam), marka
trafik_teklif: tckn(11 rakam), plaka
Yanıtın yalnızca JSON olsun."""

FEWSHOT = [
    {
        "user": "Hasar dosyası bakmak istiyorum, dosya numaram 12345678, TCKN 12345678901, tutanak var.",
        "out": {
            "type": "hasar_sorgula",
            "fields": {"dosya_no": "12345678", "tckn": "12345678901", "tutanak": "evet"},
            "message": "Hasar sorgulaması için bilgiler alındı."
        }
    },
    {
        "user": "Aracım için kasko fiyatı alayım, TCKN 11122233344, plaka 34ABC123, 2019 model, marka Honda.",
        "out": {
            "type": "kasko_teklif",
            "fields": {"tckn": "11122233344", "plaka": "34ABC123", "model_yili": "2019", "marka": "Honda"},
            "message": "Kasko teklifi için bilgiler alındı."
        }
    },
    {
        "user": "Trafik sigortası teklifi lazım, TCKN 44433322211, plaka 35XYZ35.",
        "out": {
            "type": "trafik_teklif",
            "fields": {"tckn": "44433322211", "plaka": "35XYZ35"},
            "message": "Trafik teklifi için bilgiler alındı."
        }
    },
    {"user": "Selam nasılsın, oyun önerir misin?", "out": {"type": "off_topic", "fields": {}, "message": OFF_TOPIC_MESSAGE}}
]

def fetch_api_data(params: dict):
    try:
        res = requests.get(settings.api_base, params=params, timeout=8)
        res.raise_for_status()
        return res.json().get("data", None)
    except Exception as e:
        print(f"[API ERROR] {e}")
        return None

def build_system_prompt():
    s = [SYSTEM_CORE, "Eğitim örnekleri:"]
    for ex in FEWSHOT:
        s.append("Kullanıcı: " + ex["user"])
        s.append("JSON: " + json.dumps(ex["out"], ensure_ascii=False))
    return "\n".join(s)

def parse_gemini_json(text: str) -> ParsedOutput:
    cleaned = text.strip().strip("`")
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()
    obj = json.loads(cleaned)
    return ParsedOutput(**obj)

def validate_payload(parsed: ParsedOutput):
    if parsed.type == "hasar_sorgula":
        HasarSorguPayload(**parsed.fields)
    elif parsed.type == "kasko_teklif":
        KaskoTeklifPayload(**parsed.fields)
    elif parsed.type == "trafik_teklif":
        TrafikTeklifPayload(**parsed.fields)

def _fmt_dt(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
    except Exception:
        return value or "Bilinmiyor"

def format_hasar_followup(tckn: str) -> str:
    """
    TCKN ile PHP API'den hasar_detay çekip kullanıcıya okunur bir özet döndürür.
    """
    data = fetch_api_data({"table": "hasar_detay", "tckn": tckn})
    if not data:
        return "Girilen TCKN'ye ait herhangi bir hasar kaydı bulunamadı."

    if isinstance(data, list):
        data = data[0]

    ad = (data.get("ad") or "Bilinmiyor").strip()
    soyad = (data.get("soyad") or "").strip()
    musteri = f"{ad} {soyad}".strip()

    dosya_no = data.get("dosya_no", "-")
    police_no = data.get("police_no", "-")
    durum = (data.get("durum") or "bilinmiyor").capitalize()
    tutanak = (data.get("tutanak") or "bilinmiyor").capitalize()
    tarih_str = _fmt_dt(data.get("tarih") or "")

    return (
        "—\n"
        "Dosya Durumu Bilgisi\n"
        f"Dosya No: {dosya_no}\n"
        f"Poliçe No: {police_no}\n"
        f"Müşteri: {musteri}\n"
        f"Durum: {durum}\n"
        f"Tutanak Kaydı: {tutanak}\n"
        f"Son Güncelleme: {tarih_str}\n"
        f"{dosya_no} numaralı dosyanız şu anda \"{durum}\" durumundadır. "
        "İşlemler tamamlandığında veya yeni bir aşamaya geçildiğinde dosya durumu güncellenecektir."
    )

def off_topic_response():
    return {"type": "off_topic", "fields": {}, "message": OFF_TOPIC_MESSAGE}
