# 7. Gün - TF-IDF ve Cosine Similarity Tabanlı Retrieval

## 1. Günün Amacı

Bu çalışmada AI Doküman Asistanının kullanıcı sorgusuna göre bilgi tabanındaki
en ilgili metin parçalarını bulabilmesi için TF-IDF ve cosine similarity
tabanlı retrieval sistemi geliştirilmiştir.

Önceki aşamada bilgi tabanındaki 12 teknik doküman temizlenmiş ve toplam
37 chunk oluşturulmuştu.

7. gün çalışmasında bu 37 chunk TF-IDF kullanılarak sayısal vektörlere
dönüştürülmüş ve kullanıcı sorgusu ile chunklar arasındaki benzerlik
cosine similarity yöntemiyle hesaplanmıştır.

Sistem akışı:

12 teknik doküman
    ↓
37 chunk
    ↓
TF-IDF
    ↓
Sayısal vektörler
    ↓
Kullanıcı sorgusu
    ↓
Cosine Similarity
    ↓
Benzerlik skorları
    ↓
Top-K sonuçlar

---

## 2. TF-IDF Kavramı

TF-IDF, Term Frequency - Inverse Document Frequency ifadesinin
kısaltmasıdır.

TF-IDF'nin amacı bir kelimenin belirli bir doküman içerisindeki önemini
sayısal olarak ifade etmektir.

Bu aşamada kullanılan temel kavramlar:

- Term: Bir kelime veya token
- Document: Retrieval sisteminde bir chunk
- Corpus: 37 chunkın tamamı
- Vocabulary: Corpus içerisindeki benzersiz terimlerin tamamı

Bu projede her chunk bağımsız bir document gibi değerlendirilmiştir.

---

## 3. Term Frequency - TF

TF, bir kelimenin belirli bir doküman içerisinde ne kadar sık geçtiğini
göstermektedir.

Temel formül:

TF(t,d) =
t kelimesinin d dokümanındaki geçiş sayısı
/
d dokümanındaki toplam kelime sayısı

Örneğin:

python python sanal ortam

metninde toplam 4 kelime bulunmaktadır.

python kelimesi 2 defa geçtiği için:

TF(python,d) = 2 / 4 = 0.50

sanal kelimesi 1 defa geçtiği için:

TF(sanal,d) = 1 / 4 = 0.25

olarak hesaplanmaktadır.

---

## 4. Document Frequency - DF

DF, bir terimin kaç farklı dokümanda bulunduğunu göstermektedir.

Bir kelimenin aynı dokümanda birden fazla kez bulunması DF değerini
artırmamaktadır.

Örneğin:

D1 = python sanal ortam
D2 = python kurulum
D3 = git kurulum

olduğunda:

DF(python) = 2
DF(sanal) = 1
DF(ortam) = 1
DF(kurulum) = 2
DF(git) = 1

olarak elde edilmektedir.

---

## 5. Inverse Document Frequency - IDF

IDF, bir kelimenin bütün doküman koleksiyonu içerisinde ne kadar
ayırt edici olduğunu ifade etmektedir.

Temel IDF formülü:

IDF(t) = log(N / DF(t))

Burada:

N = toplam doküman sayısı
DF(t) = t kelimesinin bulunduğu doküman sayısı

Örneğin toplam 3 doküman bulunduğu ve python kelimesinin 2 dokümanda
geçtiği durumda:

IDF(python) = ln(3 / 2)

IDF(python) ≈ 0.405

sanal kelimesi yalnızca 1 dokümanda bulunduğu için:

IDF(sanal) = ln(3 / 1)

IDF(sanal) ≈ 1.099

olarak hesaplanmaktadır.

Bu sonuç daha nadir kelimelerin daha yüksek IDF ağırlığı alabildiğini
göstermektedir.

---

## 6. TF-IDF Hesabı

TF ve IDF değerleri:

TFIDF(t,d) = TF(t,d) × IDF(t)

formülüyle birleştirilmektedir.

Örneğin:

D1 = python sanal ortam

dokümanında her kelime bir kez geçtiği için:

TF = 1 / 3 ≈ 0.333

python için:

TFIDF(python,D1) ≈ 0.333 × 0.405

TFIDF(python,D1) ≈ 0.135

sanal için:

TFIDF(sanal,D1) ≈ 0.333 × 1.099

TFIDF(sanal,D1) ≈ 0.366

olarak hesaplanmaktadır.

Böylece aynı dokümanda aynı sıklıkta bulunan kelimeler, corpus genelindeki
yaygınlıklarına göre farklı ağırlıklar alabilmektedir.

---

## 7. Vektör Gösterimi

TF-IDF işleminden sonra metinler sayısal vektörlerle temsil edilmektedir.

Örneğin vocabulary:

python
sanal
ortam
git
kurulum

şeklindeyse bir metnin TF-IDF gösterimi:

[0.135, 0.366, 0.366, 0, 0]

gibi bir vektör olabilir.

Her vektör elemanı vocabulary içerisindeki belirli bir terime karşılık
gelmektedir.

Bu sayısal gösterim sayesinde kullanıcı sorgusu ile chunklar matematiksel
olarak karşılaştırılabilmektedir.

---

## 8. Cosine Similarity

Kullanıcı sorgusu ile chunk vektörleri arasındaki benzerlik cosine similarity
yöntemiyle hesaplanmıştır.

Temel formül:

cos(A,B) = (A · B) / (||A|| × ||B||)

Burada:

A · B = iki vektörün dot product değeri
||A|| = A vektörünün normu
||B|| = B vektörünün normu

Örneğin:

A = [1,1]
B = [1,0]

olduğunda:

A · B = (1 × 1) + (1 × 0) = 1

A vektörünün normu:

||A|| = sqrt(1² + 1²) = sqrt(2)

B vektörünün normu:

||B|| = sqrt(1² + 0²) = 1

Cosine similarity:

cos(A,B) = 1 / sqrt(2)

cos(A,B) ≈ 0.707

olarak hesaplanmaktadır.

Skorun 1 değerine yaklaşması vektörlerin yönlerinin daha benzer olduğunu,
0 değerine yaklaşması ise ortak özelliklerinin daha az olduğunu göstermektedir.

---

## 9. Scikit-learn Kurulumu

TF-IDF ve cosine similarity işlemleri için scikit-learn kütüphanesi
kullanılmıştır.

Kütüphane:

pip install scikit-learn

komutuyla sanal ortama kurulmuştur.

Kurulum kontrolü sonucunda:

scikit-learn sürümü = 1.9.0

olarak görülmüştür.

Ayrıca proje bağımlılıklarının kaydedilmesi amacıyla requirements.txt
dosyasına:

scikit-learn

satırı eklenmiştir.

---

## 10. Retriever Modülünün Geliştirilmesi

Retrieval işlemlerini gerçekleştirmek amacıyla:

src/retriever.py

modülü oluşturulmuştur.

Bu modül içerisinde temel olarak:

- build_tfidf_index()
- search()

fonksiyonları geliştirilmiştir.

build_tfidf_index() fonksiyonu bilgi tabanındaki dokümanları yüklemekte,
chunklara ayırmakta ve bütün chunklar için TF-IDF matrisini oluşturmaktadır.

---

## 11. TF-IDF Matrisinin Oluşturulması

Chunk metinleri TfidfVectorizer kullanılarak sayısal özelliklere
dönüştürülmüştür.

Gerçek veri üzerinde yapılan çalıştırmada:

Toplam chunk sayısı: 37

TF-IDF matris boyutu:

(37, 730)

olarak elde edilmiştir.

Vocabulary boyutu:

730

olarak ölçülmüştür.

Burada:

37 = TF-IDF matrisindeki satır sayısı, yani chunk sayısı

730 = vocabulary içerisindeki TF-IDF özellik sayısı

anlamına gelmektedir.

Bu nedenle oluşturulan TF-IDF matrisi:

37 × 730

boyutundadır.

---

## 12. fit_transform() İşlemi

TF-IDF matrisini oluşturmak için:

vectorizer.fit_transform(chunk_texts)

işlemi kullanılmıştır.

fit işlemi corpus içerisindeki vocabulary ve IDF bilgilerini öğrenmektedir.

transform işlemi ise her chunkı öğrenilen aynı vocabulary kullanılarak
sayısal TF-IDF vektörüne dönüştürmektedir.

Kullanıcı sorgusunda yeniden fit işlemi yapılmamış, yalnızca:

vectorizer.transform([query])

kullanılmıştır.

Böylece kullanıcı sorusunun chunklarla aynı 730 boyutlu özellik uzayında
temsil edilmesi sağlanmıştır.

---

## 13. search() Fonksiyonunun Geliştirilmesi

Kullanıcının sorgusuna en benzer chunkları bulmak amacıyla search()
fonksiyonu geliştirilmiştir.

Fonksiyonun temel işlem sırası:

Kullanıcı sorgusu
    ↓
Boş sorgu kontrolü
    ↓
TF-IDF indeksini oluştur
    ↓
Sorguyu TF-IDF vektörüne dönüştür
    ↓
37 chunk ile cosine similarity hesapla
    ↓
Skorları büyükten küçüğe sırala
    ↓
Top-K sonucu seç
    ↓
Metadata ile sonucu döndür

şeklindedir.

---

## 14. Top-K Retrieval

Retrieval sonucunda bütün 37 chunkı kullanıcıya göstermek yerine en yüksek
benzerlik skoruna sahip belirli sayıda sonuç seçilmektedir.

Bu işlem Top-K olarak adlandırılmaktadır.

Başlangıç değeri:

top_k = 3

olarak belirlenmiştir.

Böylece sistem en yüksek cosine similarity değerine sahip üç chunkı
döndürmektedir.

top_k değerinin sıfır veya negatif olması geçersiz kabul edilmiş ve bu
durum için ValueError kontrolü eklenmiştir.

---

## 15. Retrieval Metadata Yapısı

Arama sonuçlarında yalnızca chunk metni değil aşağıdaki bilgiler de
korunmuştur:

- source
- section
- chunk_id
- text
- score

Bu yapı sayesinde bulunan bilginin hangi dokümandan ve hangi bölümden
geldiği görülebilmektedir.

Metadata yapısı 6. günde geliştirilen chunking sistemiyle retrieval
katmanının bağlantısını sağlamaktadır.

---

## 16. İlk Gerçek Retrieval Sonucu

İlk manuel retrieval sorgusu:

Sanal ortam nasıl oluşturulur?

olarak belirlenmiştir.

Elde edilen ilk üç sonuç:

1. Sonuç

Kaynak: sanal_ortam.md
Bölüm: Python Sanal Ortam Kullanımı
Chunk ID: sanal_ortam.md_0
Benzerlik skoru: 0.6921

2. Sonuç

Kaynak: sanal_ortam.md
Bölüm: Sanal Ortam Oluşturma
Chunk ID: sanal_ortam.md_1
Benzerlik skoru: 0.4811

3. Sonuç

Kaynak: servis_kurulumu.md
Bölüm: Servis Kurulumu
Chunk ID: servis_kurulumu.md_0
Benzerlik skoru: 0.3264

olarak elde edilmiştir.

İlk sonuçta sanal ortam oluşturma komutunu içeren ilgili teknik doküman
başarıyla ilk sırada bulunmuştur.

---

## 17. Retrieval Testlerinin Hazırlanması

Retrieval modülünün kontrollü şekilde test edilmesi amacıyla:

tests/test_retriever.py

dosyası oluşturulmuştur.

Toplam 8 test uygulanmıştır:

1. TF-IDF chunk sayısı testi
2. TF-IDF vocabulary testi
3. Top-K sonuç sayısı testi
4. Doğru kaynak retrieval testi
5. Benzerlik skorlarının sıralanması testi
6. Retrieval metadata testi
7. Boş sorgu testi
8. Geçersiz top_k testi

Testlerin tamamı başarılı olarak sonuçlanmıştır.

Toplam test sayısı:

N = 8

Başarılı test sayısı:

B = 8

Başarı oranı:

Başarı Oranı = (8 / 8) × 100

Başarı Oranı = %100

Bu değer yalnızca retrieval modülü için hazırlanan kontrollü testlerin
tamamının geçtiğini göstermektedir.

---

## 18. Retrieval Ön Değerlendirmesi

Sistemin yalnızca tek bir sorguda değil farklı teknik konularda da doğru
kaynağı bulup bulamadığını gözlemlemek amacıyla küçük bir değerlendirme
seti hazırlanmıştır.

evaluation/day7_retrieval_check.py

dosyası oluşturulmuştur.

Toplam 5 sorgu kullanılmıştır.

Değerlendirmede her sorgu için doğru kabul edilen kaynak dosyanın
retrieval sonuçlarında birinci sıraya gelip gelmediği kontrol edilmiştir.

Kullanılan konular:

- Sanal ortam
- Python kurulumu
- FastAPI
- Git
- Loglama

Değerlendirme sonucunda:

Toplam sorgu: 5

Doğru Top-1 kaynak: 5

Top-1 kaynak başarı oranı: %100.00

olarak elde edilmiştir.

Örneğin:

Sorgu:
Loglama neden kullanılır?

Beklenen kaynak:
loglama.md

Bulunan kaynak:
loglama.md

Benzerlik skoru:
0.2576

Sonuç:
BAŞARILI

olarak elde edilmiştir.

Buradaki %100 değeri AI Doküman Asistanının genel retrieval doğruluğunu
ifade etmemektedir. Yalnızca 7. gün için hazırlanmış 5 kontrollü sorguda
beklenen kaynak dosyasının birinci sırada bulunma oranını göstermektedir.

---

## 19. Modüller Arasındaki Güncel Akış

7. gün sonunda proje veri ve retrieval akışı:

data/
    ↓
document_loader.py
    ↓
text_cleaner.py
    ↓
chunker.py
    ↓
37 chunk
    ↓
retriever.py
    ↓
TF-IDF matrisi
    ↓
Cosine Similarity
    ↓
Top-K retrieval
    ↓
Kaynak + Bölüm + Metin + Skor

şeklinde oluşturulmuştur.

---

## 20. Gün Sonunda Elde Edilen Çıktılar

7. gün sonunda:

- scikit-learn kütüphanesi kurulmuştur.
- requirements.txt dosyası düzenlenmiştir.
- src/retriever.py oluşturulmuştur.
- TF-IDF kavramı ve matematiksel temeli incelenmiştir.
- DF ve IDF hesapları incelenmiştir.
- Vektör kavramı incelenmiştir.
- Cosine similarity matematiği incelenmiştir.
- 37 chunk TF-IDF vektörlerine dönüştürülmüştür.
- 37 × 730 boyutlu TF-IDF matrisi oluşturulmuştur.
- Vocabulary boyutu 730 olarak ölçülmüştür.
- Kullanıcı sorgusunun aynı TF-IDF uzayına dönüştürülmesi sağlanmıştır.
- Cosine similarity ile 37 chunk karşılaştırılmıştır.
- Top-K retrieval sistemi geliştirilmiştir.
- Kaynak, bölüm, metin ve skor bilgileri korunmuştur.
- İlk gerçek retrieval sorgusu başarıyla çalıştırılmıştır.
- tests/test_retriever.py içerisinde 8 test hazırlanmıştır.
- 8 testin tamamı başarılı olmuştur.
- 5 sorguluk retrieval ön değerlendirmesi gerçekleştirilmiştir.
- 5 sorgunun tamamında beklenen kaynak Top-1 sırada bulunmuştur.

---

## 21. 7. Gün Sonucu

7. gün sonunda AI Doküman Asistanının temel retrieval sistemi çalışır hale
getirilmiştir.

Önceki gün oluşturulan 37 chunk TF-IDF kullanılarak sayısal vektörlere
dönüştürülmüş ve kullanıcı sorgusu ile her chunk arasındaki benzerlik
cosine similarity yöntemi kullanılarak hesaplanmıştır.

En yüksek benzerlik skoruna sahip sonuçların Top-K yöntemiyle seçilmesi ve
kaynak metadata bilgileriyle birlikte döndürülmesi sağlanmıştır.

Gerçek dokümanlarla yapılan ilk retrieval denemesinde ilgili kaynakların
üst sıralarda bulunduğu görülmüş, geliştirilen modül 8 otomatik test ile
kontrol edilmiş ve testlerin tamamı başarılı olmuştur.

Ayrıca 5 farklı teknik sorgudan oluşan ön değerlendirmede beklenen kaynak
dosyalarının tamamı Top-1 sırada bulunmuştur.

Bir sonraki aşamada TF-IDF ve cosine similarity tabanlı retrieval yapısı
geliştirilecek, farklı sorgular ve retrieval sonuçları üzerinde daha kapsamlı
kontroller gerçekleştirilecektir.