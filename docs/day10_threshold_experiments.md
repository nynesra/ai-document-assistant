# Day 10 - Similarity Threshold Experiments

## Amaç

10. gün çalışmasında TF-IDF ve Cosine Similarity tabanlı retrieval sistemine **Similarity Threshold** mekanizması eklenmiştir.

11. gün sonunda aday retrieval parametreleri:

* Chunk Size = 500
* Overlap = 100
* Top-K = 3

olarak belirlenmişti.

Top-3 retrieval sonuçları içerisinde düşük similarity skoruna sahip chunkların da bulunabilmesi nedeniyle, yalnızca yeterli benzerliğe sahip sonuçların kabul edilmesi amacıyla threshold mekanizması geliştirilmiştir.

---

## Similarity Threshold Mantığı

Her kullanıcı sorgusu ile doküman chunkı arasındaki benzerlik Cosine Similarity ile hesaplanmaktadır.

$$
\operatorname{cosine}(q,d_i)
============================

\frac{q\cdot d_i}
{|q||d_i|}
$$

Burada:

* (q): Kullanıcı sorgusunun TF-IDF vektörü
* (d_i): Doküman chunkının TF-IDF vektörü
* (s_i): Hesaplanan similarity skoru
* (T): Similarity Threshold

Bir chunkın kabul edilme koşulu:

$$
s_i\geq T
$$

Bir chunkın elenme koşulu:

$$
s_i<T
$$

olarak belirlenmiştir.

Bu nedenle Top-K = 3 olsa bile threshold sonrasında dönen chunk sayısı 0 ile 3 arasında değişebilmektedir.

---

## Kod Değişikliği

`search_with_index()` fonksiyonuna `threshold` parametresi eklenmiştir.

```python
def search_with_index(
    query: str,
    chunks,
    vectorizer,
    tfidf_matrix,
    top_k: int = 3,
    threshold: float = 0.0,
):
```

Geçersiz threshold değerleri kontrol edilmiştir.

```python
if threshold < 0 or threshold > 1:
    raise ValueError(
        "threshold 0 ile 1 arasında olmalıdır."
    )
```

Her retrieval sonucu için similarity skoru threshold ile karşılaştırılmıştır.

```python
if score < threshold:
    continue
```

Böylece düşük similarity skoruna sahip chunkların sonuç listesine eklenmesi engellenmiştir.

---

## Threshold Test Seti

Deneylerde 5 ilgili ve 5 ilgisiz olmak üzere toplam 10 sorgu kullanılmıştır.

### İlgili Sorgular

1. Sanal ortam nasıl oluşturulur?
2. Python nasıl kurulur?
3. FastAPI nedir?
4. Git deposu nasıl oluşturulur?
5. Loglama neden kullanılır?

Elde edilen Top-1 skorları:

| Sorgu           |   Skor |
| --------------- | -----: |
| Sanal ortam     | 0.6921 |
| Python kurulumu | 0.4813 |
| FastAPI         | 0.6062 |
| Git             | 0.6125 |
| Loglama         | 0.2576 |

İlgili sorgular içerisindeki minimum similarity skoru:

$$
S_{\text{ilgili,min}}=0.2576
$$

### İlgisiz Sorgular

1. Türkiye'nin başkenti neresidir?
2. 5 + 5 kaçtır?
3. En hızlı hayvan hangisidir?
4. Bugün hava nasıl?
5. Dünya'nın uydusu nedir?

Top-1 skorları:

| Sorgu                |   Skor |
| -------------------- | -----: |
| Türkiye'nin başkenti | 0.0000 |
| 5 + 5                | 0.0000 |
| En hızlı hayvan      | 0.0000 |
| Bugün hava           | 0.0000 |
| Dünya'nın uydusu     | 0.0855 |

İlgisiz sorgular içerisindeki maksimum similarity skoru:

$$
S_{\text{ilgisiz,max}}=0.0855
$$

İki grup arasındaki skor farkı:

$$
0.2576-0.0855=0.1721
$$

olarak elde edilmiştir.

---

## Threshold Deneyleri

Aşağıdaki threshold değerleri test edilmiştir:

$$
T\in
{0.00,0.05,0.10,0.15,0.20,0.25,0.30}
$$

Diğer parametreler sabit tutulmuştur:

$$
C=500
$$

$$
O=100
$$

$$
K=3
$$

Sonuçlar:

| Threshold | TP | TN | FP | FN | Accuracy | Ortalama Chunk |
| --------: | -: | -: | -: | -: | -------: | -------------: |
|      0.00 |  5 |  0 |  5 |  0 |      %50 |           3.00 |
|      0.05 |  5 |  4 |  1 |  0 |      %90 |           1.70 |
|      0.10 |  5 |  5 |  0 |  0 |     %100 |           1.30 |
|      0.15 |  5 |  5 |  0 |  0 |     %100 |           1.20 |
|      0.20 |  5 |  5 |  0 |  0 |     %100 |           1.20 |
|      0.25 |  5 |  5 |  0 |  0 |     %100 |           1.10 |
|      0.30 |  4 |  5 |  0 |  1 |      %90 |           0.90 |

Accuracy hesabında:

$$
Accuracy
========

\frac{TP+TN}
{TP+TN+FP+FN}
$$

formülü kullanılmıştır.

---

## False Positive Örneği

Threshold:

$$
T=0.05
$$

kullanıldığında “Dünya'nın uydusu nedir?” sorgusunun skoru:

$$
0.0855
$$

olarak elde edilmiştir.

Karşılaştırma:

$$
0.0855\geq0.05
$$

olduğu için ilgisiz sorgu yanlışlıkla kabul edilmiştir.

Bu durum **False Positive** olarak değerlendirilmiştir.

---

## False Negative Örneği

Threshold:

$$
T=0.30
$$

kullanıldığında “Loglama neden kullanılır?” sorgusunun skoru:

$$
0.2576
$$

olarak ölçülmüştür.

Karşılaştırma:

$$
0.2576<0.30
$$

olduğu için ilgili sorgu yanlışlıkla reddedilmiştir.

Bu durum **False Negative** olarak değerlendirilmiştir.

---

## Threshold Seçimi

Kontrollü test setinde:

$$
T\in{0.10,0.15,0.20,0.25}
$$

değerlerinin tamamında:

$$
Accuracy=100%
$$

elde edilmiştir.

Ancak Threshold = 0.25 değeri en düşük ilgili similarity skoruna oldukça yakın kalmıştır.

$$
0.2576-0.25=0.0076
$$

Threshold = 0.20 için ilgisiz sorgulara karşı marj:

$$
0.20-0.0855=0.1145
$$

İlgili sorgulara karşı marj:

$$
0.2576-0.20=0.0576
$$

olarak hesaplanmıştır.

Bu nedenle dengeli aday threshold değeri:

$$
T=0.20
$$

olarak seçilmiştir.

---

## Paraphrase Testi

Threshold = 0.20 değerinin aynı anlamın farklı ifadeleri üzerinde nasıl davrandığını incelemek amacıyla 5 paraphrase sorgu kullanılmıştır.

Sonuçlar:

| Sorgu                                            | Beklenen Kaynak      | Top-1 Skor | Sonuç        |
| ------------------------------------------------ | -------------------- | ---------: | ------------ |
| Python kurulumu için hangi adımları izlemeliyim? | python_kurulumu.md   |     0.3218 | Doğru        |
| FastAPI ne işe yarar?                            | fastapi_kullanimi.md |     0.4504 | Doğru        |
| Git projesi başlatmak için ne yapmalıyım?        | git_komutlari.md     |     0.3136 | Doğru        |
| Uygulamada neden log tutulur?                    | loglama.md           |     0.3098 | Doğru        |
| Python için sanal ortamı nasıl hazırlayabilirim? | sanal_ortam.md       |     0.3793 | Yanlış Top-1 |

Doğru Top-1 sonucu:

$$
\frac{4}{5}
$$

olmuştur.

Dolayısıyla:

$$
Top1\ Başarı=80%
$$

elde edilmiştir.

Threshold nedeniyle reddedilen ilgili sorgu sayısı:

$$
0
$$

olarak bulunmuştur.

---

## Ranking Problemi

“Python için sanal ortamı nasıl hazırlayabilirim?” sorgusunda Top-3 sonuçları:

| Sıra | Kaynak             |   Skor |
| ---: | ------------------ | -----: |
|    1 | servis_kurulumu.md | 0.3793 |
|    2 | sanal_ortam.md     | 0.3624 |
|    3 | sanal_ortam.md     | 0.3230 |

olarak elde edilmiştir.

Yanlış Top-1 sonuç ile ilk doğru kaynak arasındaki skor farkı:

$$
0.3793-0.3624=0.0169
$$

olarak hesaplanmıştır.

Doğru kaynak retrieval sonuçlarında bulunduğu ancak ilk sıraya yerleşemediği için bu durum **retrieval ranking problemi** olarak değerlendirilmiştir.

---

## Hit@3 Sonucu

Beş paraphrase sorgusunun tamamında doğru kaynak ilk üç retrieval sonucu içerisinde bulunmuştur.

$$
Hit@3
=====

\frac{5}{5}
$$

Sonucunda:

$$
Hit@3=100%
$$

elde edilmiştir.

Sonuç olarak:

$$
Top1\ Başarı=80%
$$

$$
Hit@3=100%
$$

olmuştur.

Bu durum TF-IDF retrieval sisteminin doğru kaynağı ilk sonuçlar içerisinde bulabildiğini ancak bazı sorgu varyasyonlarında doğru sıralamayı yapamadığını göstermiştir.

---

## Otomatik Testler

Threshold mekanizması için aşağıdaki davranışlar otomatik olarak test edilmiştir:

* Threshold altındaki sonuçların filtrelenmesi
* İlgisiz sorguların reddedilmesi
* Yüksek threshold nedeniyle ilgili sorgunun reddedilebilmesi
* Geçersiz threshold değerlerinin hata üretmesi

Bütün proje testleri:

```bash
python -m pytest
```

komutu ile çalıştırılmıştır.

Toplam test sayısı:

$$
N=30
$$

Başarılı test sayısı:

$$
B=30
$$

Test başarı oranı:

$$
\frac{30}{30}\times100
$$

Sonucunda:

$$
Test\ Başarı\ Oranı=100%
$$

elde edilmiştir.

Terminal sonucu:

```text
30 passed in 1.57s
```

olarak görülmüştür.

---

## Son Konfigürasyon

10. gün sonunda retrieval sistemi için aday konfigürasyon:

$$
C=500
$$

$$
O=100
$$

$$
K=3
$$

$$
T=0.20
$$

olarak belirlenmiştir.

Yani:

```text
Chunk Size = 500
Overlap    = 100
Top-K      = 3
Threshold  = 0.20
```

kullanılmasına karar verilmiştir.

## Sonuç

Similarity Threshold mekanizmasının eklenmesiyle düşük similarity skoruna sahip retrieval sonuçları filtrelenebilir hale getirilmiştir.

Kontrollü deneylerde Threshold = 0.20 değeri ilgili sorguların tamamını kabul etmiş, ilgisiz sorguların tamamını reddetmiş ve gereksiz dönen chunk sayısını azaltmıştır.

Paraphrase deneyleri ise TF-IDF sisteminin doğru kaynağı Top-3 içerisinde bulmasına rağmen bazı anlamsal sorgu varyasyonlarında Top-1 sıralamasında hata yapabildiğini göstermiştir.

Bu bulgu, sonraki aşamada gerçekleştirilecek **embedding tabanlı semantik retrieval** çalışmaları için deneysel bir gerekçe oluşturmuştur.
