# Day 12 - TF-IDF ve Embedding Retrieval Karşılaştırması

## Amaç

12. gün çalışmasında önceki gün geliştirilen **embedding tabanlı retrieval sistemi ile mevcut TF-IDF retrieval sisteminin daha kapsamlı ve ölçülebilir biçimde karşılaştırılması** amaçlanmıştır.

13. gün sonunda iki retrieval yaklaşımının aynı sorgularda farklı davranışlar gösterebildiği gözlemlenmişti.

Bu nedenle 12. gün çalışmasında yalnızca Top-1 sonucu incelemek yerine:

* Top-1 Accuracy
* Hit@3
* MRR@3
* İndeks oluşturma süresi
* Ortalama sorgu süresi

metrikleri birlikte değerlendirilmiştir.

Ayrıca sorgular üç farklı gruba ayrılmıştır:

* Basic
* Paraphrase
* Terminology

Böylece retrieval yöntemlerinin farklı sorgu türlerindeki davranışlarının ayrı ayrı incelenmesi sağlanmıştır.

---

## 1. Kullanılan Retrieval Yapıları

TF-IDF retrieval sisteminde önceki deneylerde belirlenen yapı korunmuştur.

Chunk Size:

$$
C=500
$$

Overlap:

$$
O=100
$$

Top-K:

$$
K=3
$$

olarak kullanılmıştır.

Embedding retrieval sisteminde de aynı Chunk Size, Overlap ve Top-K değerleri kullanılmıştır.

Böylece iki retrieval yaklaşımının mümkün olduğunca aynı veri yapısı üzerinde karşılaştırılması amaçlanmıştır.

TF-IDF karşılaştırma deneyinde Similarity Threshold uygulanmamıştır.

Bu nedenle:

$$
T=0
$$

kullanılmıştır.

Bu tercih, TF-IDF'nin ham retrieval sıralaması ile embedding retrieval sıralamasının doğrudan karşılaştırılabilmesi amacıyla yapılmıştır.

---

## 2. Test Setinin Genişletilmesi

12. gün karşılaştırmasında sorgular üç kategoriye ayrılmıştır.

### Basic Sorgular

Temel sorgular dokümanlarda kullanılan terminolojiye yakın ifadelerden oluşturulmuştur.

1. Sanal ortam nasıl oluşturulur?
2. Python nasıl kurulur?
3. FastAPI nedir?
4. Git deposu nasıl oluşturulur?
5. Loglama neden kullanılır?

Basic sorgu sayısı:

$$
N_{basic}=5
$$

olarak belirlenmiştir.

### Paraphrase Sorgular

Aynı bilgi farklı kelime ve cümle yapılarıyla ifade edilmiştir.

1. Python kurulumu için hangi adımları izlemeliyim?
2. FastAPI ne işe yarar?
3. Git projesi başlatmak için ne yapmalıyım?
4. Uygulamada neden log tutulur?
5. Python için sanal ortamı nasıl hazırlayabilirim?

Paraphrase sorgu sayısı:

$$
N_{paraphrase}=5
$$

olarak belirlenmiştir.

### Terminology Sorguları

Teknik terminolojinin farklı biçimlerde kullanıldığı sorgular oluşturulmuştur.

1. Git repository nasıl oluşturulur?
2. Yeni bir Git repository nasıl başlatılır?
3. Git projesi başlatmak için hangi komut kullanılır?
4. git init komutu ne işe yarar?

Terminology sorgu sayısı:

$$
N_{terminology}=4
$$

olarak belirlenmiştir.

Toplam sorgu sayısı:

$$
N
=

5+5+4
$$

Sonucunda:

$$
N=14
$$

olarak elde edilmiştir.

---

## 3. Çoklu Kabul Edilebilir Kaynak Yapısının Korunması

11. gün gerçekleştirilen hata analizlerinde bazı sorguların birden fazla doküman tarafından doğru şekilde cevaplanabildiği görülmüştür.

Özellikle:

```text
Python için sanal ortamı nasıl hazırlayabilirim?
```

sorgusu için:

```text
sanal_ortam.md
```

ve:

```text
servis_kurulumu.md
```

dosyalarının her ikisinin de ilgili bilgi içerdiği gözlemlenmiştir.

Bu nedenle değerlendirme yapısında:

```python
"expected_sources": [
    "sanal_ortam.md",
    "servis_kurulumu.md",
]
```

yapısı kullanılmaya devam edilmiştir.

Bir sorgu için kabul edilebilir kaynaklar kümesi:

$$
R_q
$$

ile gösterilmiştir.

Top-1 sonucu:

$$
Top1\in R_q
$$

ise sonuç doğru kabul edilmiştir.

---

## 4. Top-1 Accuracy Metriği

Top-1 Accuracy, sistemin ilk sırada doğru veya kabul edilebilir bir kaynak getirip getirmediğini ölçmektedir.

Formül:

$$
Top1\ Accuracy
==============

\frac{N_{\text{doğru Top-1}}}
{N_{\text{toplam sorgu}}}
\times100
$$

şeklinde kullanılmıştır.

Bu metrik retrieval sisteminin kullanıcıya ilk sunduğu sonucun kalitesini değerlendirmek amacıyla kullanılmıştır.

---

## 5. Hit@3 Metriği

Hit@3 metriği, kabul edilebilir kaynaklardan en az birinin ilk üç retrieval sonucu içerisinde bulunup bulunmadığını ölçmektedir.

Bir sorgu için:

$$
Hit@3=
\begin{cases}
1, & Top3\cap R_q\neq\emptyset\
0, & Top3\cap R_q=\emptyset
\end{cases}
$$

olarak tanımlanmıştır.

Genel Hit@3 oranı:

$$
Hit@3
=====

\frac{N_{\text{Top-3 içinde doğru kaynak bulunan sorgu}}}
{N_{\text{toplam sorgu}}}
\times100
$$

formülü ile hesaplanmıştır.

---

## 6. Reciprocal Rank ve MRR@3 Metriğinin Eklenmesi

Top-1 ve Hit@3 metriklerine ek olarak doğru kaynağın Top-3 içerisinde hangi sırada bulunduğunu ölçmek amacıyla **Reciprocal Rank** kullanılmıştır.

Doğru kaynağın sırası:

$$
r
$$

ile gösterildiğinde:

$$
RR=\frac{1}{r}
$$

olarak hesaplanmaktadır.

Doğru kaynak birinci sıradaysa:

$$
RR=\frac{1}{1}
$$

Sonucunda:

$$
RR=1
$$

olmaktadır.

Doğru kaynak ikinci sıradaysa:

$$
RR=\frac{1}{2}
$$

Sonucunda:

$$
RR=0.5
$$

olmaktadır.

Doğru kaynak üçüncü sıradaysa:

$$
RR=\frac{1}{3}
$$

Sonucunda:

$$
RR\approx0.3333
$$

olmaktadır.

Doğru kaynak Top-3 içerisinde bulunmuyorsa:

$$
RR=0
$$

olarak kabul edilmiştir.

Bütün sorguların Reciprocal Rank değerlerinin ortalaması alınarak MRR@3 hesaplanmıştır.

$$
MRR@3
=====

\frac{1}{N}
\sum_{i=1}^{N}RR_i
$$

MRR@3 değeri 1'e yaklaştıkça doğru kaynakların daha üst sıralarda bulunduğu anlamına gelmektedir.

---

## 7. Basic Sorgu Sonuçları

Basic sorgu grubunda toplam:

$$
N=5
$$

sorgu kullanılmıştır.

### TF-IDF Sonuçları

Doğru Top-1 sonucu:

$$
5/5
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1_{\text{TF-IDF}}
====================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Top1_{\text{TF-IDF}}=100%
$$

olarak bulunmuştur.

Hit@3 sonucu:

$$
Hit@3_{\text{TF-IDF}}
=====================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Hit@3_{\text{TF-IDF}}=100%
$$

olarak elde edilmiştir.

Doğru kaynakların tamamı Top-1 sırada bulunduğundan:

$$
MRR@3_{\text{TF-IDF}}=1.0000
$$

olmuştur.

### Embedding Sonuçları

Doğru Top-1 sonucu:

$$
4/5
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1_{\text{Embedding}}
=======================

\frac{4}{5}\times100
$$

Sonucunda:

$$
Top1_{\text{Embedding}}=80%
$$

olarak bulunmuştur.

Hit@3 sonucu:

$$
Hit@3_{\text{Embedding}}
========================

\frac{4}{5}\times100
$$

Sonucunda:

$$
Hit@3_{\text{Embedding}}=80%
$$

olmuştur.

MRR@3:

$$
MRR@3_{\text{Embedding}}=0.8000
$$

olarak elde edilmiştir.

---

## 8. Paraphrase Sorgu Sonuçları

Paraphrase grubunda:

$$
N=5
$$

sorgu kullanılmıştır.

### TF-IDF Sonuçları

Top-1 doğru sonuç:

$$
5/5
$$

olmuştur.

Top-1 başarı oranı:

$$
Top1_{\text{TF-IDF}}
====================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Top1_{\text{TF-IDF}}=100%
$$

olarak elde edilmiştir.

Hit@3:

$$
Hit@3_{\text{TF-IDF}}
=====================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Hit@3_{\text{TF-IDF}}=100%
$$

olarak bulunmuştur.

MRR@3:

$$
MRR@3_{\text{TF-IDF}}=1.0000
$$

olarak elde edilmiştir.

### Embedding Sonuçları

Top-1 doğru sonuç:

$$
4/5
$$

olmuştur.

Top-1 başarı oranı:

$$
Top1_{\text{Embedding}}
=======================

\frac{4}{5}\times100
$$

Sonucunda:

$$
Top1_{\text{Embedding}}=80%
$$

olarak elde edilmiştir.

Doğru kaynakların tamamı ilk üç retrieval sonucu içerisinde bulunmuştur.

Hit@3:

$$
Hit@3_{\text{Embedding}}
========================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Hit@3_{\text{Embedding}}=100%
$$

olarak bulunmuştur.

MRR@3:

$$
MRR@3_{\text{Embedding}}=0.8667
$$

olarak ölçülmüştür.

Top-1 başarısının %80 olmasına rağmen Hit@3 değerinin %100 olması, embedding sisteminin doğru kaynakları çoğunlukla bulduğunu ancak bazı sorgularda doğru kaynağı ilk sıraya yerleştiremediğini göstermiştir.

---

## 9. Terminology Sorgu Sonuçları

Terminology grubunda:

$$
N=4
$$

sorgu kullanılmıştır.

### TF-IDF Sonuçları

Doğru Top-1 sonucu:

$$
4/4
$$

olmuştur.

Top-1 başarı oranı:

$$
Top1_{\text{TF-IDF}}
====================

\frac{4}{4}\times100
$$

Sonucunda:

$$
Top1_{\text{TF-IDF}}=100%
$$

olarak bulunmuştur.

Hit@3:

$$
Hit@3_{\text{TF-IDF}}
=====================

\frac{4}{4}\times100
$$

Sonucunda:

$$
Hit@3_{\text{TF-IDF}}=100%
$$

olmuştur.

MRR@3:

$$
MRR@3_{\text{TF-IDF}}=1.0000
$$

olarak elde edilmiştir.

### Embedding Sonuçları

Doğru Top-1 sonucu:

$$
3/4
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1_{\text{Embedding}}
=======================

\frac{3}{4}\times100
$$

Sonucunda:

$$
Top1_{\text{Embedding}}=75%
$$

olarak bulunmuştur.

Doğru kaynak bütün sorgularda ilk üç sonuç içerisinde bulunmuştur.

Hit@3:

$$
Hit@3_{\text{Embedding}}
========================

\frac{4}{4}\times100
$$

Sonucunda:

$$
Hit@3_{\text{Embedding}}=100%
$$

olarak elde edilmiştir.

MRR@3:

$$
MRR@3_{\text{Embedding}}=0.8750
$$

olarak ölçülmüştür.

---

## 10. Sorgu Türü Bazlı Genel Karşılaştırma

Deney sonuçları aşağıdaki şekilde elde edilmiştir:

| Sorgu Türü  | Yöntem    | Top-1 | Hit@3 |  MRR@3 |
| ----------- | --------- | ----: | ----: | -----: |
| Basic       | TF-IDF    |  %100 |  %100 | 1.0000 |
| Basic       | Embedding |   %80 |   %80 | 0.8000 |
| Paraphrase  | TF-IDF    |  %100 |  %100 | 1.0000 |
| Paraphrase  | Embedding |   %80 |  %100 | 0.8667 |
| Terminology | TF-IDF    |  %100 |  %100 | 1.0000 |
| Terminology | Embedding |   %75 |  %100 | 0.8750 |

Mevcut kontrollü sorgu setinde TF-IDF yaklaşımı üç sorgu türünde de Top-1 ve MRR@3 açısından embedding yaklaşımından daha yüksek değer üretmiştir.

Embedding yaklaşımında özellikle paraphrase ve terminology sorgularında Hit@3 değerinin yüksek kalması, doğru kaynağın çoğunlukla bulunabildiğini ancak her zaman ilk sıraya getirilemediğini göstermiştir.

---

## 11. Genel TF-IDF Sonuçları

Toplam sorgu sayısı:

$$
N=14
$$

olmuştur.

TF-IDF doğru Top-1 sonucu:

$$
14/14
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1_{\text{TF-IDF}}
====================

\frac{14}{14}\times100
$$

Sonucunda:

$$
Top1_{\text{TF-IDF}}=100%
$$

olarak bulunmuştur.

Hit@3:

$$
Hit@3_{\text{TF-IDF}}
=====================

\frac{14}{14}\times100
$$

Sonucunda:

$$
Hit@3_{\text{TF-IDF}}=100%
$$

olarak elde edilmiştir.

Doğru kaynakların tamamı Top-1 sırada bulunduğundan:

$$
MRR@3_{\text{TF-IDF}}=1.0000
$$

olmuştur.

---

## 12. Genel Embedding Sonuçları

Toplam:

$$
N=14
$$

sorgunun 11 tanesinde embedding sistemi kabul edilebilir kaynağı Top-1 sırada getirmiştir.

Doğru Top-1 sonucu:

$$
11/14
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1_{\text{Embedding}}
=======================

\frac{11}{14}\times100
$$

Sonucunda:

$$
Top1_{\text{Embedding}}\approx78.57%
$$

olarak bulunmuştur.

Doğru kaynağın Top-3 içerisinde bulunduğu sorgu sayısı:

$$
13/14
$$

olmuştur.

Hit@3:

$$
Hit@3_{\text{Embedding}}
========================

\frac{13}{14}\times100
$$

Sonucunda:

$$
Hit@3_{\text{Embedding}}\approx92.86%
$$

olarak elde edilmiştir.

Embedding sisteminin genel MRR@3 değeri:

$$
MRR@3_{\text{Embedding}}=0.8452
$$

olarak ölçülmüştür.

---

## 13. MRR@3 Sonuçlarının Karşılaştırılması

TF-IDF için:

$$
MRR@3_{\text{TF-IDF}}=1.0000
$$

Embedding için:

$$
MRR@3_{\text{Embedding}}=0.8452
$$

olarak elde edilmiştir.

MRR farkı:

$$
\Delta MRR
==========

1.0000-0.8452
$$

Sonucunda:

$$
\Delta MRR=0.1548
$$

olarak hesaplanmıştır.

Bu sonuç, mevcut kontrollü test setinde TF-IDF sisteminin doğru kaynakları embedding sistemine göre daha üst sıralarda getirdiğini göstermiştir.

---

## 14. Retrieval Performans Deneyinin Tasarlanması

Retrieval kalitesinin yanında iki yaklaşımın hesaplama maliyetini karşılaştırmak amacıyla performans deneyi gerçekleştirilmiştir.

İki farklı süre ölçülmüştür:

### İndeks Oluşturma Süresi

TF-IDF ve embedding indekslerinin oluşturulması için gereken süre ölçülmüştür.

### Ortalama Query Süresi

Beş temel sorgunun retrieval süreleri ölçülmüş ve ortalamaları alınmıştır.

Süre ölçümünde Python `time.perf_counter()` fonksiyonu kullanılmıştır.

---

## 15. İndeks Oluşturma Süreleri

TF-IDF indeks oluşturma süresi:

$$
T_{\text{TF-IDF,index}}=0.0208\text{ saniye}
$$

olarak ölçülmüştür.

Embedding indeks oluşturma süresi:

$$
T_{\text{Embedding,index}}=8.4682\text{ saniye}
$$

olarak elde edilmiştir.

Embedding indeks süresinin TF-IDF indeks süresine oranı:

$$
R_{\text{index}}
================

\frac{8.4682}{0.0208}
$$

Sonucunda:

$$
R_{\text{index}}\approx407.13
$$

olarak hesaplanmıştır.

Bu çalıştırmada embedding indeksinin oluşturulması TF-IDF indeksine göre yaklaşık 407 kat daha uzun sürmüştür.

Bu oran yalnızca mevcut deney ortamı için gözlemlenen bir değerdir.

---

## 16. Ortalama Query Süreleri

TF-IDF ortalama sorgu süresi:

$$
T_{\text{TF-IDF,query}}
=======================

0.001056\text{ saniye}
$$

olarak ölçülmüştür.

Embedding ortalama sorgu süresi:

$$
T_{\text{Embedding,query}}
==========================

0.077931\text{ saniye}
$$

olarak elde edilmiştir.

İki süre arasındaki oran:

$$
R_{\text{query}}
================

\frac{0.077931}{0.001056}
$$

Sonucunda:

$$
R_{\text{query}}\approx73.80
$$

olarak hesaplanmıştır.

Bu çalıştırmada embedding sorgularının ortalama retrieval süresi TF-IDF sorgularına göre yaklaşık 74 kat daha uzun ölçülmüştür.

---

## 17. Retrieval Kalitesi ve Performansın Birlikte Değerlendirilmesi

Genel sonuçlar:

| Ölçüt                   |      TF-IDF |   Embedding |
| ----------------------- | ----------: | ----------: |
| Top-1                   |        %100 |      %78.57 |
| Hit@3                   |        %100 |      %92.86 |
| MRR@3                   |      1.0000 |      0.8452 |
| İndeks oluşturma süresi |   0.0208 sn |   8.4682 sn |
| Ortalama sorgu süresi   | 0.001056 sn | 0.077931 sn |

Mevcut kontrollü deney setinde TF-IDF yaklaşımı hem retrieval kalitesi hem de hesaplama süresi açısından daha yüksek sonuç üretmiştir.

Ancak bu sonuç yalnızca mevcut küçük teknik doküman koleksiyonu, kullanılan sorgu seti ve seçilen embedding modeli kapsamında değerlendirilmiştir.

---

## 18. Performans Ölçümünün Sınırlılıkları

Süre ölçümleri kullanılan bilgisayarın donanım özelliklerinden etkilenmektedir.

Embedding indeks oluşturma süresi içerisinde embedding modelinin yüklenme maliyeti de bulunmaktadır.

Ayrıca model dosyalarının önbellekte bulunup bulunmaması toplam çalışma süresini etkileyebilir.

Bu nedenle:

$$
407.13
$$

ve:

$$
73.80
$$

gibi oranlar genel veya donanımdan bağımsız performans değerleri olarak değerlendirilmemiştir.

Bu değerler yalnızca mevcut deney ortamında TF-IDF ve embedding yaklaşımları arasındaki göreli maliyeti göstermek amacıyla kullanılmıştır.

---

## 19. 12. Gün Metrik Testlerinin Hazırlanması

12. gün geliştirilen değerlendirme fonksiyonlarının doğru çalışmasını kontrol etmek amacıyla dört yeni otomatik test hazırlanmıştır.

Testlerde:

* Doğru kaynağın birinci sırada olması
* Doğru kaynağın ikinci sırada olması
* Doğru kaynağın Top-3 dışında kalması
* Birden fazla kabul edilebilir kaynağın desteklenmesi

durumları kontrol edilmiştir.

Birinci sıradaki doğru kaynak için:

$$
RR@3=1
$$

beklenmiştir.

İkinci sıradaki doğru kaynak için:

$$
RR@3=0.5
$$

beklenmiştir.

Doğru kaynak Top-3 dışında ise:

$$
RR@3=0
$$

olması test edilmiştir.

---

## 20. Regression Testlerinin Gerçekleştirilmesi

11. gün sonunda toplam otomatik test sayısı:

$$
34
$$

idi.

12. gün dört yeni değerlendirme testi eklenmiştir.

Toplam test sayısı:

$$
34+4
$$

Sonucunda:

$$
N=38
$$

olmuştur.

Bütün testlerin başarılı olduğu görülmüştür.

Başarılı test sayısı:

$$
B=38
$$

olarak elde edilmiştir.

Test başarı oranı:

$$
Başarı\ Oranı
=============

\frac{38}{38}\times100
$$

Sonucunda:

$$
Başarı\ Oranı=100%
$$

olarak bulunmuştur.

Bu sonuç yeni MRR@3 ve çoklu kaynak değerlendirme mantığının mevcut sistem davranışlarında regression oluşturmadığını göstermiştir.

---

## 21. Deneyin Sınırlılıkları

12. gün değerlendirmesinde toplam:

$$
14
$$

kontrollü sorgu kullanılmıştır.

Bu nedenle elde edilen sonuçların gerçek kullanıcıların bütün olası sorgularını temsil ettiği kabul edilmemelidir.

Test setinde:

* 5 Basic
* 5 Paraphrase
* 4 Terminology

sorgusu bulunmaktadır.

Ayrıca yalnızca bir embedding modeli kullanılmıştır.

Farklı embedding modelleri aynı veri setinde farklı retrieval performansı gösterebilir.

TF-IDF'nin mevcut test setinde %100 başarı sağlaması da bütün gerçek sorgularda aynı başarı oranının elde edileceği anlamına gelmemektedir.

Sonuçlar yalnızca mevcut kontrollü değerlendirme seti kapsamında yorumlanmıştır.

---

## 22. Gün Sonunda Elde Edilen Çıktılar

12. gün sonunda retrieval karşılaştırma test seti 14 sorguya genişletilmiştir.

Sorgular:

* Basic
* Paraphrase
* Terminology

olmak üzere üç gruba ayrılmıştır.

Değerlendirmeye yeni olarak:

$$
MRR@3
$$

metriği eklenmiştir.

TF-IDF genel Top-1 başarısı:

$$
100%
$$

olarak elde edilmiştir.

Embedding genel Top-1 başarısı:

$$
78.57%
$$

olarak ölçülmüştür.

TF-IDF Hit@3:

$$
100%
$$

Embedding Hit@3:

$$
92.86%
$$

olarak bulunmuştur.

TF-IDF MRR@3:

$$
1.0000
$$

Embedding MRR@3:

$$
0.8452
$$

olarak elde edilmiştir.

Performans deneyinde TF-IDF indeks oluşturma süresi:

$$
0.0208\text{ saniye}
$$

Embedding indeks oluşturma süresi:

$$
8.4682\text{ saniye}
$$

olarak ölçülmüştür.

TF-IDF ortalama sorgu süresi:

$$
0.001056\text{ saniye}
$$

Embedding ortalama sorgu süresi:

$$
0.077931\text{ saniye}
$$

olarak elde edilmiştir.

Son olarak proje genelinde:

$$
38/38
$$

otomatik test başarılı olmuştur.

Test başarı oranı:

$$
100%
$$

olarak elde edilmiştir.

---

## Sonuç

12. gün çalışmasında TF-IDF ve embedding tabanlı retrieval yaklaşımları daha kapsamlı bir değerlendirme seti üzerinde karşılaştırılmıştır.

Toplam:

$$
14
$$

sorgu kullanılmıştır.

TF-IDF sistemi:

$$
Top1=100%
$$

$$
Hit@3=100%
$$

$$
MRR@3=1.0000
$$

sonuçlarını elde etmiştir.

Embedding sistemi:

$$
Top1=78.57%
$$

$$
Hit@3=92.86%
$$

$$
MRR@3=0.8452
$$

sonuçlarını üretmiştir.

Embedding sisteminde Hit@3 değerinin Top-1 değerinden daha yüksek olması, doğru kaynakların çoğunlukla ilk üç sonuç içerisinde bulunmasına rağmen bazı sorgularda doğru sıralamanın yapılamadığını göstermiştir.

Performans ölçümlerinde TF-IDF indeks oluşturma süresi:

$$
0.0208\text{ saniye}
$$

Embedding indeks oluşturma süresi:

$$
8.4682\text{ saniye}
$$

olarak ölçülmüştür.

Ortalama query süreleri ise:

$$
0.001056\text{ saniye}
$$

ve:

$$
0.077931\text{ saniye}
$$

olarak elde edilmiştir.

Mevcut küçük teknik doküman koleksiyonunda ve hazırlanan kontrollü test setinde **TF-IDF yaklaşımı Top-1, Hit@3, MRR@3 ve hesaplama süresi açısından kullanılan embedding modelinden daha yüksek sonuç üretmiştir.**

Bununla birlikte bu sonuç, TF-IDF'nin genel olarak bütün semantik retrieval sistemlerinden daha iyi olduğu şeklinde yorumlanmamıştır.

Retrieval performansının:

* Veri setinin yapısı
* Sorgu tipi
* Teknik terminoloji
* Kullanılan embedding modeli
* Değerlendirme kriterleri

gibi birçok faktörden etkilendiği gözlemlenmiştir.

12. gün sonunda TF-IDF ve embedding retrieval yaklaşımlarının kontrollü karşılaştırması tamamlanmıştır.

Sonraki çalışma gününde case planına uygun olarak **karar akışı ve araç çağrıları** üzerinde çalışılması planlanmıştır.
