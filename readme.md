<div align="center">

# 🛡️ BlaBla Sigorta – Gemini Chatbot

**FastAPI + Google Gemini + PHP/MySQL**  
Hasar sorgu, kasko & trafik teklifi; müşteri tanıma ve canlı chat kutusu ile tam entegre demo.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-4B8BBE)](https://www.uvicorn.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20GenerativeAI-Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![PHP](https://img.shields.io/badge/PHP-8.x-777BB4?logo=php&logoColor=white)](https://www.php.net/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Swagger](https://img.shields.io/badge/Swagger-OpenAPI%203-85EA2D?logo=swagger&logoColor=white)](https://swagger.io/)
[![License](https://img.shields.io/badge/License-MIT-informational)](#-license)

</div>

---

## ✨ Önizleme

<p align="center">
  <!-- Kendi ekran görüntülerini /static altına koyup yolu güncelle -->
  <img src="app/static/preview-hero.png" alt="Site Önizleme" width="860" />
  <br />
  <sub>Minimal, açık temalı kurumsal demo site + sağ altta chat baloncuğu</sub>
</p>

---

## 🧭 İçindekiler
- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Kurulum (Hızlı Başlangıç)](#-kurulum-hızlı-başlangıç)

---

## 🚀 Özellikler
- **Niyet Algılama & Yönlendirme:** `general → hasar_sorgula / kasko_teklif / trafik_teklif / off_topic`
- **Müşteri Tanıma:** TCKN ile `hasar_detay` sorgusu (PHP API + MySQL JOIN)
- **Çift Baloncuk Yanıtı:** İlk baloncuk “bilgiler alındı”, ikinci baloncuk **API’den gelen detay** (`follow_up`)
- **Swagger Dokümantasyon:** FastAPI (`/swagger`) + PHP API (`swagger.html`)
- **Sade Modern UI:** `app/static/index.html` – açık tema, smooth chat, unread badge
- **Configurable:** `.env` ile `GEMINI_API_KEY`, `API_BASE`, CORS, model adı…

---

## 🏗 Mimari

FastAPI (Python)
├─ /chat ← Gemini yönlendirme + payload doğrulama
│ └─ PHP API'ye GET → hasar_detay (TCKN)
│ └─ MySQL (sigorta_chatbot)
└─ /swagger (OpenAPI UI)

PHP API (api.php)
├─ /api.php?table=musteri
├─ /api.php?table=hasar_dosya
└─ /api.php?table=hasar_detay&tckn=... ← JOIN + son kayıt

Static Frontend
└─ app/static/index.html ← Chat bubble, iki baloncuk desteği


---

## Kurulum (Hızlı Başlangıç)

### 1) Python (FastAPI)
```bash
# repo kökünde
pip install -r requirements.txt

# .env örneğini çoğalt, anahtarı gir
cp .env.example .env

# dev sunucu
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# http://localhost:8000/swagger
```

<p> <a href="mailto:ucarkacar231415@gmail.com"><img src="https://img.shields.io/badge/E--mail-Contact-informational?logo=gmail&logoColor=white" /></a> <a href="https://x.com/yefeblgn"><img src="https://img.shields.io/badge/Twitter-@yefeblgn-1DA1F2?logo=x&logoColor=white" /></a> </p>


