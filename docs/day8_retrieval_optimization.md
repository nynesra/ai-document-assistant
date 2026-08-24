# 8. Gün - Retrieval Optimizasyonu ve Performans Analizi

## 1. Günün Amacı

Bu çalışmada, 7. günde geliştirilen TF-IDF ve cosine similarity tabanlı retrieval sisteminin daha verimli ve tekrar kullanılabilir hale getirilmesi amaçlanmıştır.

Önceki yapıda her kullanıcı sorgusu gönderildiğinde teknik dokümanlar yeniden yüklenmekte, yeniden chunklara ayrılmakta ve TF-IDF matrisi tekrar oluşturulmaktaydı.

Bilgi tabanı değişmediği sürece aynı TF-IDF indeksinin her sorguda yeniden oluşturulmasına ihtiyaç olmadığı değerlendirilmiştir.

Bu nedenle 8. gün çalışmasında TF-IDF indeksinin yalnızca bir kez oluşturulması ve birden fazla kullanıcı sorgusunda tekrar kullanılması sağlanmıştır.

Ayrıca:

* Top-K sınır durumları incelenmiştir.
* Top-3 retrieval sonuçları analiz edilmiştir.
* Eski ve yeni retrieval yapılarının çalışma süreleri ölçülmüştür.
* Performans ölçümü 10 kez tekrarlanarak ortalama değerler hesaplanmıştır.
* Optimizasyon sonrasında retrieval sonuçlarının değişmediği otomatik testlerle doğrulanmıştır.

---

## 2. Mevcut Retrieval Yapısındaki Verimsizliğin Belirlenmesi

7. günde geliştirilen `search()` fonksiyonu her sorgu gönderildiğinde kendi içerisinde:

```python
build_tfidf_index()
```

fonksiyonunu çalıştırmaktaydı.

Bu durumda her sorgu için işlem akışı:

```text
Kullanıcı sorgusu
      ↓
Dokümanları yükle
      ↓
37 chunk oluştur
      ↓
Vocabulary oluştur
      ↓
TF-IDF matrisini oluştur
      ↓
Sorguyu vektöre dönüştür
      ↓
Cosine similarity hesapla
      ↓
Top-K sonucu getir
```

şeklindeydi.

Beş sorgu kullanılması durumunda TF-IDF indeksinin oluşturulma sayısı:

[
N_{\text{index,eski}}=5
]

olmaktadır.

Bilgi tabanı bu sorgular arasında değişmediği için aynı işlemlerin tekrar gerçekleştirilmesinin gereksiz hesaplama maliyetine neden olduğu görülmüştür.

---

## 3. Hazır TF-IDF İndeksi Yaklaşımının Geliştirilmesi

Bu sorunu çözmek amacıyla TF-IDF indeksinin bir kez oluşturulması ve sonraki sorgular için aynı indeksin tekrar kullanılması yaklaşımı uygulanmıştır.

Yeni işlem akışı:

```text
12 teknik doküman
        ↓
37 chunk
        ↓
TF-IDF indeksini oluştur
        ↓
37 × 730 TF-IDF matrisi
        ↓
Hazır indeks
        ↓
 ├── Sorgu 1
 ├── Sorgu 2
 ├── Sorgu 3
 ├── Sorgu 4
 └── Sorgu 5
```

şeklinde düzenlenmiştir.

Bu durumda TF-IDF indeksinin oluşturulma sayısı:

[
N_{\text{index,yeni}}=1
]

olmaktadır.

Eski ve yeni yöntem arasındaki indeks oluşturma sayısı:

[
N_{\text{index,eski}}=5
]

[
N_{\text{index,yeni}}=1
]

şeklinde değişmiştir.

---

## 4. `search_with_index()` Fonksiyonunun Geliştirilmesi

Hazır TF-IDF indeksinde arama gerçekleştirmek amacıyla:

```python
search_with_index()
```

fonksiyonu geliştirilmiştir.

Fonksiyon aşağıdaki parametreleri almaktadır:

```text
query
chunks
vectorizer
tfidf_matrix
top_k
```

Burada:

* `query`: Kullanıcının sorgusunu,
* `chunks`: Bilgi tabanındaki 37 chunkı,
* `vectorizer`: Öğrenilmiş TF-IDF vocabulary yapısını,
* `tfidf_matrix`: Chunkların TF-IDF gösterimini,
* `top_k`: Döndürülecek en yüksek skorlu sonuç sayısını

ifade etmektedir.

Yeni fonksiyon içerisinde tekrar:

```python
build_tfidf_index()
```

çalıştırılmamaktadır.

Böylece indeks oluşturma ve sorgu çalıştırma işlemleri birbirinden ayrılmıştır.

---

## 5. Aynı TF-IDF İndeksi ile Çoklu Sorgu Çalıştırılması

Hazır indeks yapısının doğru çalışıp çalışmadığını kontrol etmek amacıyla aşağıdaki 5 sorgu aynı TF-IDF indeksi üzerinde çalıştırılmıştır:

```text
Sanal ortam nasıl oluşturulur?
Python nasıl kurulur?
FastAPI nedir?
Git deposu nasıl oluşturulur?
Loglama neden kullanılır?
```

TF-IDF indeks bilgileri:

Nchunk=37
∣V∣=730

olarak elde edilmiştir.

M∈R37×730

şeklindedir.

Elde edilen Top-1 sonuçlar:

```text
Sanal ortam nasıl oluşturulur?
→ sanal_ortam.md
→ 0.6921

Python nasıl kurulur?
→ python_kurulumu.md
→ 0.4813

FastAPI nedir?
→ fastapi_kullanimi.md
→ 0.6062

Git deposu nasıl oluşturulur?
→ git_komutlari.md
→ 0.6125

Loglama neden kullanılır?
→ loglama.md
→ 0.2576
```

Beş sorgunun tamamında beklenen kaynak dosyanın Top-1 sırada bulunduğu görülmüştür.

---

## 6. Top-K Sınır Kontrolünün Geliştirilmesi

Retrieval fonksiyonunda `top_k` parametresinin bilgi tabanındaki toplam chunk sayısından büyük verilmesi durumu incelenmiştir.

Bilgi tabanında:

Nchunk=37
chunk bulunmaktadır.

Örneğin:

Kistenen​=100
verildiğinde sistemde 100 sonuç bulunmadığı için etkin Top-K değeri:

[
K_{\text{etkin}}
================

\min
\left(
K_{\text{istenen}},
N_{\text{chunk}}
\right)
]

formülüyle sınırlandırılmıştır.

Değerler yerine yazıldığında:

[
K_{\text{etkin}}
================

\min(100,37)
]

[
K_{\text{etkin}}=37
]

olarak elde edilmiştir.

Terminal üzerinde yapılan kontrolde:

```text
İstenen top_k: 100
Dönen sonuç: 37
```

sonucu alınmıştır.

Ayrıca:

[
K\leq0
]

olması geçersiz kabul edilmekte ve bu durumda `ValueError` oluşturulmaktadır.

---

## 7. Top-3 Retrieval Analizi

Retrieval sisteminin yalnızca Top-1 sonucunun değil, ilk üç sonucunun da incelenmesi amacıyla:

```text
evaluation/day8_topk_analysis.py
```

dosyası oluşturulmuştur.

Sanal ortam sorgusunda:

[
S_1=0.6921
]

[
S_2=0.4811
]

[
S_3=0.3264
]

olarak elde edilmiştir.

İlk iki sonuç `sanal_ortam.md`, üçüncü sonuç ise sanal ortam oluşturma bilgisi içeren `servis_kurulumu.md` dokümanından gelmiştir.

Git sorgusunda:

[
S_1=0.6125
]

[
S_2=0.4069
]

[
S_3=0.3886
]

olarak elde edilmiş ve ilk üç sonucun tamamı `git_komutlari.md` dokümanından gelmiştir.

FastAPI sorgusunda da ilk üç sonuç `fastapi_kullanimi.md` dokümanından elde edilmiştir.

---

## 8. Retrieval Sonuçlarının Nitel Değerlendirilmesi

Top-3 analizinde bazı sorgularda ilk üç sonucun tamamının ilgili olduğu, bazı sorgularda ise yalnızca ilk sonucun güçlü olduğu görülmüştür.

Örneğin:

```text
Sorgu: Loglama neden kullanılır?
```

için:

[
S_1=0.2576
]

[
S_2=0.1454
]

[
S_3=0.0470
]

sonuçları elde edilmiştir.

Top-1 sonuç:

```text
loglama.md
```

olmasına rağmen ikinci ve üçüncü sonuçların farklı teknik konulardaki dokümanlardan geldiği görülmüştür.

Birinci ve üçüncü sonuç arasındaki skor farkı:

[
\Delta S
========

S_1-S_3
]

[
\Delta S
========

0.2576-0.0470
]

[
\Delta S
========

0.2106
]

olarak hesaplanmıştır.

Bu durum yalnızca `top_k=3` kullanılmasının döndürülen üç sonucun tamamının mutlaka ilgili olduğu anlamına gelmediğini göstermiştir.

Bu gözlem, ilerleyen aşamalarda similarity threshold değerinin incelenmesi gerektiğini göstermektedir.

---

## 9. Eski ve Yeni Retrieval Yöntemlerinin Süre Karşılaştırması

Hazır indeks yaklaşımının performansa etkisini ölçmek amacıyla:

```text
evaluation/day8_index_performance.py
```

dosyası oluşturulmuştur.

İlk performans ölçümünde 5 sorgu kullanılmıştır.

Eski yöntemin çalışma süresi:

[
T_{\text{eski}}
===============

0.025763\text{ s}
]

Hazır indeks yönteminin çalışma süresi:

[
T_{\text{hazır}}
================

0.007020\text{ s}
]

olarak ölçülmüştür.

Hızlanma katsayısı:

[
H=
\frac{T_{\text{eski}}}
{T_{\text{hazır}}}
]

formülüyle hesaplanmıştır.

Değerler yerine yazıldığında:

[
H=
\frac{0.025763}
{0.007020}
]

[
H\approx3.67
]

olarak elde edilmiştir.

İlk tek ölçümde hazır indeks yönteminin yaklaşık:

[
H\approx3.67\times
]

daha hızlı olduğu görülmüştür.

---

## 10. Tekrarlı Performans Analizi

Tek bir süre ölçümünün sistem yükünden etkilenebileceği göz önünde bulundurularak performans deneyi 10 kez tekrarlanmıştır.

Bu amaçla:

```text
evaluation/day8_repeated_performance.py
```

dosyası geliştirilmiştir.

Tekrar sayısı:

[
R=10
]

Sorgu sayısı:

[
N_q=5
]

olarak belirlenmiştir.

Bir yöntemin ortalama çalışma süresi:

[
\overline{T}
============

\frac{
T_1+T_2+\cdots+T_R
}
{R}
]

formülüyle hesaplanmıştır.

10 tekrar sonucunda eski yöntemin ortalama süresi:

[
\overline{T}_{\text{eski}}
==========================

0.045166\text{ s}
]

olarak ölçülmüştür.

Hazır indeks yönteminin ortalama süresi:

[
\overline{T}_{\text{hazır}}
===========================

0.011543\text{ s}
]

olarak ölçülmüştür.

---

## 11. Ortalama Hızlanma Katsayısının Hesaplanması

Tekrarlı deney sonucundaki ortalama hızlanma katsayısı:

[
H_{\text{ortalama}}
===================

\frac{
\overline{T}*{\text{eski}}
}{
\overline{T}*{\text{hazır}}
}
]

formülüyle hesaplanmıştır.

Değerler yerine yazıldığında:

[
H_{\text{ortalama}}
===================

\frac{
0.045166
}{
0.011543
}
]

[
H_{\text{ortalama}}
\approx
3.91
]

olarak elde edilmiştir.

Buna göre hazır indeks yöntemi mevcut test ortamında ortalama:

[
\boxed{
H_{\text{ortalama}}
\approx
3.91\times
}
]

daha hızlı çalışmıştır.

Bu sonuç tek bir çalışma yerine 10 tekrarın ortalamasına dayandığı için performans değerlendirmesinde temel sonuç olarak kullanılmıştır.

---

## 12. Eski ve Yeni Retrieval Sonuçlarının Karşılaştırılması

Performans optimizasyonunun retrieval sonuçlarını değiştirmediğini kontrol etmek amacıyla eski `search()` fonksiyonu ile yeni `search_with_index()` fonksiyonunun sonuçları karşılaştırılmıştır.

Her iki yöntem için aşağıdaki alanlar kontrol edilmiştir:

```text
source
section
chunk_id
score
```

Float türündeki similarity skorlarının karşılaştırılmasında:

```python
isclose()
```

fonksiyonu kullanılmıştır.

Aynı sorgu için eski ve yeni yöntemlerin aynı Top-3 kaynakları, aynı bölümleri, aynı chunk kimliklerini ve aynı similarity skorlarını ürettiği doğrulanmıştır.

Böylece performans optimizasyonunun retrieval sıralamasını değiştirmediği görülmüştür.

---

## 13. Test Sonuçları

7. gün sonunda retrieval modülü için 8 test bulunmaktaydı.

8. günde aşağıdaki yeni testler eklenmiştir:

```text
Hazır TF-IDF indeksi tekrar kullanım testi
Büyük top_k sınır testi
Eski ve hazır indeks sonuç eşitliği testi
```

Toplam test sayısı:

[
N=11
]

Başarılı test sayısı:

[
B=11
]

Başarısız test sayısı:

[
H=0
]

olarak elde edilmiştir.

Test başarı oranı:

[
\text{Başarı Oranı}
===================

\frac{B}{N}\times100
]

[
\text{Başarı Oranı}
===================

\frac{11}{11}\times100
]

[
\text{Başarı Oranı}
===================

100%
]

olarak hesaplanmıştır.

Başarısızlık oranı:

[
\text{Başarısızlık Oranı}
=========================

\frac{H}{N}\times100
]

[
\text{Başarısızlık Oranı}
=========================

\frac{0}{11}\times100
]

[
\text{Başarısızlık Oranı}
=========================

0%
]

olarak elde edilmiştir.

Bu değerler yalnızca mevcut retrieval modülü için hazırlanan kontrollü testlerin sonuçlarını ifade etmektedir.

---

## 14. 7. Gün ile 8. Gün Arasındaki Teknik Gelişim

7. gün sonunda retrieval akışı:

```text
Kullanıcı sorgusu
      ↓
TF-IDF indeksini oluştur
      ↓
Cosine Similarity
      ↓
Top-K Retrieval
```

şeklindeydi.

8. gün sonunda sistem:

```text
12 teknik doküman
        ↓
37 chunk
        ↓
TF-IDF indeksini 1 kez oluştur
        ↓
37 × 730 matris
        ↓
Hazır indeks
        ↓
Birden fazla kullanıcı sorgusu
        ↓
Cosine Similarity
        ↓
Top-K Retrieval
```

seviyesine getirilmiştir.

Böylece doküman yükleme, chunking ve TF-IDF oluşturma işlemlerinin her sorguda tekrarlanması engellenmiştir.

---

## 15. Gün Sonunda Elde Edilen Çıktılar

8. gün sonunda:

* TF-IDF indeksinin her sorguda yeniden oluşturulduğu mevcut yapı analiz edilmiştir.
* `search_with_index()` fonksiyonu geliştirilmiştir.
* TF-IDF indeksinin bir kez oluşturulup tekrar kullanılması sağlanmıştır.
* Aynı hazır indeks üzerinde 5 farklı sorgu başarıyla çalıştırılmıştır.
* 5 sorgunun tamamında beklenen kaynak Top-1 sırada bulunmuştur.
* `top_k` değerinin toplam chunk sayısından büyük olması durumu kontrol altına alınmıştır.
* `top_k=100` için mevcut 37 chunkın döndürülmesi sağlanmıştır.
* Top-3 retrieval sonuçları analiz edilmiştir.
* Bazı sorgularda Top-2 ve Top-3 sonuçların ilgisinin azaldığı belirlenmiştir.
* Eski ve hazır indeks yöntemlerinin çalışma süreleri ölçülmüştür.
* İlk performans ölçümünde yaklaşık `3.67x` hızlanma görülmüştür.
* Performans deneyi 10 kez tekrarlanmıştır.
* Eski yöntemin ortalama çalışma süresi `0.045166 saniye` olarak ölçülmüştür.
* Hazır indeks yönteminin ortalama çalışma süresi `0.011543 saniye` olarak ölçülmüştür.
* Ortalama hızlanma katsayısı `3.91x` olarak hesaplanmıştır.
* Eski ve yeni yöntemin aynı retrieval sonuçlarını ürettiği doğrulanmıştır.
* Retrieval test sayısı 11'e çıkarılmıştır.
* 11 testin tamamından beklenen sonuç alınmıştır.

---

## 16. Gün Sonucu

8. gün sonunda TF-IDF ve cosine similarity tabanlı retrieval sisteminin çalışma yapısı optimize edilmiştir.

Önceki yapıda TF-IDF indeksi her kullanıcı sorgusunda yeniden oluşturulurken, geliştirilen hazır indeks yaklaşımı sayesinde dokümanların yüklenmesi, chunklara ayrılması ve TF-IDF matrisinin oluşturulması işlemleri yalnızca bir kez gerçekleştirilmiştir.

Hazır indeksin birden fazla kullanıcı sorgusunda tekrar kullanılabildiği doğrulanmış ve mevcut test ortamında 10 tekrarlı performans analizi sonucunda yaklaşık:

[
3.91\times
]

ortalama hızlanma elde edilmiştir.

Ayrıca yapılan optimizasyonun retrieval sonuçlarının sırasını veya benzerlik skorlarını değiştirmediği otomatik testlerle doğrulanmıştır.

Top-3 retrieval analizi sonucunda bazı sorgularda ikinci ve üçüncü sonuçların ilgisinin düşebildiği gözlemlenmiştir. Bu sonuç ilerleyen aşamalarda Top-K, similarity threshold ve chunk parametrelerinin deneysel olarak karşılaştırılması gerektiğini göstermektedir.

8. gün sonunda retrieval sistemi hem işlevsel hem de performans açısından daha verimli bir yapıya getirilmiştir.
