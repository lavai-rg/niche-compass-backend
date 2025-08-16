# Niche Compass Backend

Backend API untuk aplikasi Niche Compass - platform analisis niche dan riset produk Etsy.

## Teknologi
- Python 3.11
- Flask
- Azure Cosmos DB (MongoDB API)
- Azure Cognitive Services

## Setup Lokal
1. Clone repository ini
2. Buat virtual environment: `python -m venv venv`
3. Aktifkan virtual environment: `source venv/bin/activate` (Linux/Mac) atau `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Konfigurasi file `.env` dengan kredensial Azure Anda
6. Jalankan server: `python src/main.py`

## API Endpoints
- `/api/health` - Health check
- `/api/keywords/analyze` - Analisis keyword
- `/api/niches/analyze` - Analisis niche
- `/api/products/analyze` - Analisis produk
