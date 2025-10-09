from fastapi import APIRouter
from app.schemas import ChatInput
from app.flows import (
    build_system_prompt,
    parse_gemini_json,
    validate_payload,
    off_topic_response,
    format_hasar_followup,
)
from app.gemini_client import generate_json

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
def chat(body: ChatInput):
    system_prompt = build_system_prompt()
    raw = generate_json(system_prompt, body.text)

    try:
        parsed = parse_gemini_json(raw)
    except Exception:
        return off_topic_response()

    if parsed.type == "off_topic":
        return parsed.model_dump()

    try:
        validate_payload(parsed)
    except Exception:
        return parsed.model_dump()

    if parsed.type == "hasar_sorgula":
        tckn = parsed.fields.get("tckn")
        follow_up = format_hasar_followup(tckn)
        return {
            "type": parsed.type,
            "fields": parsed.fields,
            "message": parsed.message or "Hasar sorgulaması için bilgiler alındı.",
            "follow_up": follow_up
        }

    if parsed.type == "kasko_teklif":
        return {"type": parsed.type, "fields": parsed.fields, "message": "Kasko teklifiniz hesaplanıyor, lütfen bekleyin."}

    if parsed.type == "trafik_teklif":
        return {"type": parsed.type, "fields": parsed.fields, "message": "Trafik teklifiniz hazırlanıyor, birkaç saniye içinde yanıtlanacak."}

    return parsed.model_dump()
