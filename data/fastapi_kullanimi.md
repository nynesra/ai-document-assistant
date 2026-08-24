# FastAPI Kullanımı

## FastAPI Nedir?

FastAPI, Python ile API geliştirmek için kullanılabilen bir web framework'üdür.

Python type hint yapılarıyla birlikte çalışabilir ve API endpointlerinin tanımlanmasını kolaylaştırır.

## Basit Uygulama

Basit bir FastAPI uygulaması şu şekilde oluşturulabilir:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Uygulama çalışıyor"}

## Uygulamayı Çalıştırma

FastAPI uygulamaları bir ASGI sunucusu kullanılarak çalıştırılabilir.

Örneğin uygulama app.py dosyasındaysa uvicorn ile:

uvicorn app:app --reload

komutu kullanılabilir.

## Endpoint

Endpoint, API üzerinden erişilebilen belirli bir adres ve işlemi temsil eder.

Örneğin:

GET /documents

sistemde bulunan dokümanların listesini döndüren bir endpoint olarak tasarlanabilir.

## Doküman Asistanında Kullanımı

AI Doküman Asistanı ilerleyen aşamada API üzerinden kullanılmak istenirse FastAPI ile soru alma, doküman listeleme ve cevap döndürme endpointleri oluşturulabilir.

Bu proje için ilk kullanıcı arayüzü CLI veya Streamlit olarak geliştirilebilir; FastAPI ise alternatif bir servis katmanı olarak değerlendirilebilir.