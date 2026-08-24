# Servis Kurulumu

## Gereksinimler

Uygulamayı çalıştırmadan önce Python'un sistemde kurulu olması gerekir.

Proje bağımlılıklarının requirements.txt dosyasından yüklenmesi önerilir.

## Sanal Ortam

Proje klasöründe sanal ortam oluşturmak için:

python -m venv .venv

Windows ortamında sanal ortamı etkinleştirmek için:

.venv\Scripts\activate

## Paketlerin Yüklenmesi

Gerekli Python paketleri aşağıdaki komutla yüklenebilir:

pip install -r requirements.txt

## Uygulamayı Çalıştırma

Python uygulaması aşağıdaki komutla başlatılabilir:

python app.py

Eğer uygulama Streamlit kullanıyorsa:

streamlit run app.py

komutu kullanılabilir.

## Hata Kontrolü

Uygulama başlamıyorsa Python sürümü, sanal ortam ve gerekli paketlerin kurulu olup olmadığı kontrol edilmelidir.