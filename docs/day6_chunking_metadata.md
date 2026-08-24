# 6. Gün - Chunking ve Metadata

## 1. Günün Amacı

Bu çalışmada bilgi tabanındaki teknik dokümanların daha küçük ve aranabilir
metin parçalarına ayrılması amaçlanmıştır.

RAG sistemlerinde bütün bir dokümanı tek parça olarak aramak yerine dokümanların
daha küçük parçalara ayrılması retrieval işleminin daha hassas yapılmasını sağlar.

Bu küçük metin parçalarına "chunk" adı verilir.

---

## 2. Chunk Nedir?

Chunk, bir dokümanın belirli uzunlukta oluşturulan daha küçük metin parçasıdır.

Örneğin 1100 karakterlik bir doküman, 500 karakterlik chunk boyutu ve
100 karakter overlap kullanılarak üç parçaya ayrılabilir.

Kullanılan temel parametreler:

- chunk_size = 500
- overlap = 100

Chunk boyutu C ile, overlap O ile gösterildiğinde ilerleme miktarı:

S = C - O

şeklinde hesaplanır.

Bu projede:

S = 500 - 100 = 400

olarak hesaplanmıştır.

Bu nedenle her yeni chunk bir önceki chunk başlangıcından 400 karakter sonra
başlamaktadır.

---

## 3. Overlap Nedir?

Overlap, ardışık iki chunk arasında tekrar edilen metin miktarıdır.

Örneğin:

Chunk 0:
0 - 500

Chunk 1:
400 - 900

olduğunda 400 ile 500 arasındaki 100 karakter iki chunk içerisinde de bulunur.

Overlap miktarı:

O = 500 - 400 = 100

olarak hesaplanır.

Overlap kullanılmasının amacı chunk sınırlarında önemli bağlamın kaybolmasını
azaltmaktır.

---

## 4. Chunk Sayısının Matematiksel Hesabı

Dokümanın uzunluğu L, chunk boyutu C ve overlap miktarı O olduğunda:

L <= C

ise doküman tek chunk olarak tutulur.

L > C olduğunda yaklaşık chunk sayısı:

N = 1 + ceil((L - C) / (C - O))

formülüyle hesaplanabilir.

Örnek:

L = 1100
C = 500
O = 100

S = 500 - 100 = 400

N = 1 + ceil((1100 - 500) / 400)

N = 1 + ceil(600 / 400)

N = 1 + ceil(1.5)

N = 3

Bu durumda chunklar:

Chunk 0:
0 - 500

Chunk 1:
400 - 900

Chunk 2:
800 - 1100

olarak oluşur.

---

## 5. Chunk Parametre Kontrolleri

Chunking işleminde aşağıdaki şartlar uygulanmıştır:

chunk_size > 0

overlap >= 0

overlap < chunk_size

Özellikle overlap değerinin chunk_size değerinden küçük olması gerekmektedir.

Eğer:

overlap = chunk_size

olursa:

step = chunk_size - overlap

step = 500 - 500

step = 0

olur.

Bu durumda algoritma doküman içerisinde ilerleyemez.

Bu nedenle geçersiz parametrelerde ValueError oluşturulmaktadır.

---

## 6. Chunk Metadata Yapısı

Her chunk yalnızca metni değil, chunkın hangi dokümandan ve hangi bölümden
geldiğini gösteren metadata bilgilerini de saklamaktadır.

Kullanılan metadata alanları:

- source
- section
- chunk_id
- chunk_index
- text
- start_char
- end_char

### source

Chunkın hangi dokümandan geldiğini gösterir.

Örnek:

servis_kurulumu.md

### section

Chunkın doküman içerisindeki hangi Markdown başlığına ait olduğunu gösterir.

Örnek:

Paketlerin Yüklenmesi

### chunk_id

Her chunk için kimlik oluşturur.

Örnek:

servis_kurulumu.md_0

### chunk_index

Chunkın doküman içerisindeki sırasını gösterir.

İlk chunk:

0

İkinci chunk:

1

şeklinde devam eder.

### start_char

Chunkın doküman içerisindeki başlangıç karakter konumunu gösterir.

### end_char

Chunkın doküman içerisindeki bitiş sınırını gösterir.

---

## 7. Section Metadata

Dokümanlarda bulunan Markdown başlıkları kullanılarak chunklara bölüm bilgisi
eklenmiştir.

Örneğin servis_kurulumu.md dokümanında yapılan test sonucunda:

Chunk 0:
Bölüm = Servis Kurulumu
Konum = 0 - 500

Chunk 1:
Bölüm = Paketlerin Yüklenmesi
Konum = 400 - 773

sonuçları elde edilmiştir.

Böylece ilerleyen retrieval aşamasında yalnızca kaynak dosya değil, bilginin
dokümanın hangi bölümünden geldiği de kullanıcıya gösterilebilecektir.

---

## 8. Birden Fazla Dokümanın Chunklanması

Tek bir doküman için chunk_document() fonksiyonu geliştirilmiştir.

Birden fazla dokümanı işlemek için chunk_documents() fonksiyonu oluşturulmuştur.

Sistem akışı:

data klasörü
    ↓
load_documents()
    ↓
temizlenmiş dokümanlar
    ↓
chunk_documents()
    ↓
chunk_document()
    ↓
tüm chunkların listesi

chunk_documents() fonksiyonunda her doküman sırayla işlenmiş ve oluşturulan
chunklar extend() kullanılarak tek bir liste içerisinde birleştirilmiştir.

---

## 9. Gerçek Veri Sonuçları

Bilgi tabanında toplam 12 teknik doküman kullanılmıştır.

Kullanılan parametreler:

chunk_size = 500
overlap = 100
step = 400

Chunking işlemi sonucunda:

Doküman sayısı = 12

Toplam chunk sayısı = 37

elde edilmiştir.

Dokümanlara göre oluşan chunk sayıları:

fastapi_kullanimi.md -> 3 chunk

git_komutlari.md -> 3 chunk

hata_cozumleri.md -> 3 chunk

loglama.md -> 3 chunk

model_degerlendirme.md -> 3 chunk

proje_klasor_yapisi.md -> 4 chunk

python_kurulumu.md -> 3 chunk

sanal_ortam.md -> 3 chunk

servis_kurulumu.md -> 2 chunk

siniflandirma_metrikleri.md -> 3 chunk

test_sureci.md -> 3 chunk

veri_temizleme.md -> 4 chunk

Toplam:

3 + 3 + 3 + 3 + 3 + 4 + 3 + 3 + 2 + 3 + 3 + 4 = 37

---

## 10. Testler

Chunking modülü için toplam 10 test hazırlanmıştır.

Test edilen durumlar:

1. Step hesaplama
2. Standart chunking
3. Overlap miktarı
4. Kısa doküman
5. Boş metin
6. Geçersiz chunk_size
7. Negatif overlap
8. overlap = chunk_size durumu
9. Chunk metadata
10. Gerçek dokümanların chunklanması

Test sonucu:

Toplam test = 10

Başarılı test = 10

Başarısız test = 0

Başarı oranı:

Başarı Oranı = (10 / 10) x 100

Başarı Oranı = %100

Bu sonuç yalnızca chunking modülü için hazırlanan kontrollü testlerin tamamının
başarılı olduğunu göstermektedir. Sistemin genel RAG doğruluğunu ifade etmez.

---

## 11. Oluşturulan ve Güncellenen Dosyalar

src/chunker.py

tests/test_chunker.py

docs/day6_chunking_metadata.md

---

## 12. 6. Gün Sonucu

6. gün sonunda dokümanların retrieval sisteminde kullanılabilecek küçük metin
parçalarına ayrılması sağlanmıştır.

Chunking işlemi overlap yöntemiyle uygulanmış, parametre kontrolleri eklenmiş ve
her chunk için kaynak, bölüm, kimlik ve karakter konumu metadata bilgileri
oluşturulmuştur.

Gerçek 12 dokümandan toplam 37 chunk elde edilmiştir.

Oluşturulan chunking modülü 10 farklı test ile kontrol edilmiş ve testlerin
tamamı başarılı olmuştur.

Bir sonraki aşamada oluşturulan 37 chunk üzerinde TF-IDF tabanlı metin
temsilleri oluşturulacak ve cosine similarity kullanılarak kullanıcı sorgusuna
en benzer chunkların bulunması sağlanacaktır.