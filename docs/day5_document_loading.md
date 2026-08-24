# 5. Gün - Doküman Yükleme ve Metin Temizleme

## 1. Günün Amacı

AI Doküman Asistanının gerçek Markdown ve TXT dokümanlarıyla
çalışabilmesi için doküman yükleme ve metin temizleme altyapısı
geliştirilmiştir.

Önceki prototipte bilgiler Python kodunun içerisinde manuel olarak
tanımlanıyordu. Bu aşamada bilgiler gerçek dosyalardan okunmaya
başlanmıştır.

---

## 2. Teknik Doküman Koleksiyonu

Bilgi tabanı için toplam 12 teknik doküman hazırlanmıştır.

Dokümanlar:

- python_kurulumu.md
- sanal_ortam.md
- servis_kurulumu.md
- fastapi_kullanimi.md
- model_degerlendirme.md
- siniflandirma_metrikleri.md
- hata_cozumleri.md
- git_komutlari.md
- veri_temizleme.md
- loglama.md
- test_sureci.md
- proje_klasor_yapisi.md

Dokümanlar data klasörü içerisinde tutulmaktadır.

---

## 3. Metin Temizleme Modülü

src/text_cleaner.py modülü oluşturulmuştur.

clean_text() fonksiyonu ham doküman metnindeki gereksiz
biçimlendirme karakterlerini temizlemektedir.

Gerçekleştirilen işlemler:

1. Windows satır sonlarının standartlaştırılması
2. Tab karakterlerinin boşluğa dönüştürülmesi
3. Birden fazla boşluğun tek boşluğa indirilmesi
4. Art arda gelen fazla boş satırların azaltılması
5. Metnin başındaki ve sonundaki boşlukların temizlenmesi

Örnek:

Ham metin:

Python     kurulumu


çok      önemlidir.

Temizlenmiş metin:

Python kurulumu

çok önemlidir.

---

## 4. Doküman Yükleme Modülü

src/document_loader.py modülü geliştirilmiştir.

Bu modül data klasörünü tarayarak .md ve .txt uzantılı
dokümanları bulmaktadır.

Her dosya UTF-8 karakter kodlamasıyla okunmakta ve ardından
clean_text() fonksiyonuna gönderilmektedir.

Her doküman için aşağıdaki bilgiler tutulmaktadır:

- Kaynak dosya adı
- Dosya uzantısı
- Ham metin
- Temizlenmiş metin
- Ham karakter sayısı
- Temiz karakter sayısı
- Temizleme oranı

---

## 5. Desteklenen Dosya Türleri

Sistem şu anda aşağıdaki dosya türlerini desteklemektedir:

.md
.txt

Desteklenmeyen dosya türleri sisteme alınmamaktadır.

---

## 6. UTF-8 Kullanımı

Dosyalar UTF-8 karakter kodlaması kullanılarak okunmaktadır.

Bu sayede Türkçe karakterlerin doğru biçimde işlenmesi
amaçlanmıştır.

Örnek Türkçe karakterler:

ç, ğ, ı, İ, ö, ş, ü

---

## 7. Matematiksel Temel

Ham doküman uzunluğu:

L_raw

Temizlenmiş doküman uzunluğu:

L_clean

olarak tanımlanmıştır.

Temizleme sırasında çıkarılan karakter sayısı:

L_removed = L_raw - L_clean

formülüyle hesaplanmaktadır.

Temizleme oranı:

R = ((L_raw - L_clean) / L_raw) * 100

formülüyle hesaplanmaktadır.

Örneğin:

L_raw = 1000
L_clean = 950

ise:

L_removed = 1000 - 950 = 50

ve:

R = (50 / 1000) * 100 = %5

olmaktadır.

Ham dokümanın karakter sayısı sıfır olduğunda sıfıra bölme
hatasını önlemek amacıyla temizleme oranı 0 olarak
döndürülmektedir.

---

## 8. Ortalama Doküman Uzunluğu

N adet dokümanın temizlenmiş uzunlukları:

L1, L2, ..., LN

ile gösterildiğinde ortalama doküman uzunluğu:

L_ortalama = (L1 + L2 + ... + LN) / N

formülüyle hesaplanmaktadır.

Gerçek doküman koleksiyonunda toplam 12 doküman başarıyla
yüklenmiştir.

Son ölçümde ortalama temiz doküman uzunluğu yaklaşık:

1100.67 karakter

olarak hesaplanmıştır.

Bu değer sonraki aşamada chunk boyutu belirlenirken
kullanılabilecek yardımcı bir ölçümdür.

---

## 9. Hata Kontrolleri

Doküman yükleme modülünde aşağıdaki durumlar kontrol edilmiştir:

- Veri klasörünün bulunamaması
- Verilen yolun klasör olmaması
- Boş doküman
- Desteklenmeyen dosya uzantısı
- UTF-8 olarak okunamayan dosya

Bu durumlarda sistemin kontrolsüz biçimde çalışması yerine
uygun hata veya uyarı mekanizmaları kullanılmıştır.

---

## 10. Testler

Doküman yükleme ve metin temizleme modülleri için toplam
9 test uygulanmıştır.

Testler:

1. Metin temizleme testi
2. Temizleme oranı testi
3. Sıfıra bölme kontrolü
4. Markdown yükleme testi
5. TXT yükleme testi
6. Boş doküman testi
7. Desteklenmeyen uzantı testi
8. Olmayan klasör testi
9. Tüm dokümanları yükleme testi

Test sonuçları:

Toplam test = 9
Başarılı test = 9
Başarısız test = 0

Test başarı oranı:

Başarı Oranı = (Başarılı Test / Toplam Test) * 100

Başarı Oranı = (9 / 9) * 100

Başarı Oranı = %100

Bu oran yalnızca 5. gün kapsamında hazırlanan kontrollü
test senaryolarının başarı durumunu göstermektedir ve
sistemin genel doğruluk oranı olarak değerlendirilmemelidir.

---

## 11. Modüller Arası Bağlantı

Doküman işleme akışı:

data klasörü
    ↓
document_loader.py
    ↓
Dosya okuma
    ↓
text_cleaner.py
    ↓
Metin temizleme
    ↓
Karakter ve temizleme ölçümleri
    ↓
Document veri yapısı

Test akışı:

tests/test_document_loader.py
    ↓
src/document_loader.py
    ↓
src/text_cleaner.py

Python paket yapısının düzenli kullanılabilmesi için
src ve tests klasörlerine __init__.py dosyaları eklenmiştir.

Test modülü:

python -m tests.test_document_loader

komutuyla çalıştırılmıştır.

---

## 12. Gün Sonu Sonucu

5. gün sonunda AI Doküman Asistanının gerçek teknik
dokümanları okuyabilmesi için gerekli temel veri yükleme
altyapısı oluşturulmuştur.

Toplam 12 Markdown dokümanı başarıyla sisteme yüklenmiş,
metin temizleme işlemleri uygulanmış ve doküman uzunlukları
sayısal olarak ölçülmüştür.

Doküman yükleme ve metin temizleme modülleri 9 farklı
test senaryosuyla kontrol edilmiş ve tüm başlangıç
testleri başarılı sonuçlanmıştır.

Bir sonraki aşamada temizlenmiş dokümanların daha küçük
parçalara ayrılması için chunking ve her parçaya kaynak,
bölüm ve sıra bilgisi gibi metadata değerlerinin eklenmesi
planlanmaktadır.