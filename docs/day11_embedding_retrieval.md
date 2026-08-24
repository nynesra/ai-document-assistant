# Day 11 - Embedding Based Semantic Retrieval

## Amaç

11. gün çalışmasında mevcut TF-IDF tabanlı retrieval sistemine alternatif olarak **embedding tabanlı semantik retrieval sistemi** geliştirilmiştir.

Önceki çalışmalarda TF-IDF ve Cosine Similarity kullanılarak çalışan retrieval sistemi oluşturulmuş ve aşağıdaki aday parametreler belirlenmişti:

* Chunk Size = 500
* Overlap = 100
* Top-K = 3
* Similarity Threshold = 0.20

10. gün gerçekleştirilen paraphrase deneylerinde TF-IDF sisteminin doğru kaynağı çoğunlukla ilk sonuçlar içerisinde bulmasına rağmen bazı sorgu varyasyonlarında ranking problemi yaşayabildiği görülmüştü.

Bu nedenle 11. gün çalışmasında metinlerin yalnızca kelime ağırlıklarıyla değil, anlamsal özelliklerini temsil eden yoğun vektörlerle karşılaştırılması amacıyla embedding tabanlı retrieval yaklaşımı geliştirilmiştir.

---

## Embedding Modelinin Kurulması

Embedding işlemleri için `sentence-transformers` kütüphanesi projeye eklenmiştir.

Kullanılan model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

olarak belirlenmiştir.

Model Türkçe sorgularla çalışabilecek çok dilli bir sentence embedding modeli olarak kullanılmıştır.

---

## Embedding Kavramı

Embedding yaklaşımında bir metin sayısal bir vektöre dönüştürülmektedir.

Bir metin:

$$
x
$$

ile gösterildiğinde embedding işlemi:

$$
E(x)=\mathbf{v}
$$

şeklinde ifade edilmektedir.

Burada:

* (x): Metin
* (E): Embedding modeli
* (\mathbf{v}): Metnin sayısal vektör temsili

olarak tanımlanmaktadır.

Gerçekleştirilen ilk deneyde:

```text
Python için sanal ortam nasıl oluşturulur?
```

metni embedding modeline verilmiştir.

Embedding vektör boyutu:

$$
d=384
$$

olarak elde edilmiştir.

Dolayısıyla her metin:

$$
E(x)\in\mathbb{R}^{384}
$$

şeklinde temsil edilmektedir.

---

## İlk Semantik Benzerlik Deneyi

Embedding yaklaşımının anlamsal benzerliği temsil edip etmediğini gözlemlemek amacıyla üç cümle kullanılmıştır.

Birinci cümle:

```text
Python için sanal ortam nasıl oluşturulur?
```

İkinci cümle:

```text
Python için izole bir çalışma ortamı nasıl hazırlanır?
```

Üçüncü cümle:

```text
Bugün hava nasıl?
```

Birinci ve ikinci cümle anlamsal olarak yakın, üçüncü cümle ise ilgisiz olarak değerlendirilmiştir.

Embeddingler arasında Cosine Similarity hesaplanmıştır.

Cosine Similarity:

$$
\operatorname{cosine}(a,b)
==========================

\frac{a\cdot b}
{|a||b|}
$$

formülüyle hesaplanmaktadır.

Benzer iki cümlenin skoru:

$$
S_{\text{benzer}}=0.6454
$$

olarak elde edilmiştir.

İlgisiz cümle için:

$$
S_{\text{ilgisiz}}=-0.0329
$$

sonucu bulunmuştur.

Karşılaştırma:

$$
0.6454>-0.0329
$$

şeklinde gerçekleşmiştir.

Bu ilk deney, embedding modelinin anlamsal olarak yakın iki ifadeyi ilgisiz bir ifadeye göre daha yakın temsil edebildiğini göstermiştir.

---

## Embedding İndeksinin Oluşturulması

Dokümanlar önce mevcut chunking sistemi kullanılarak parçalara ayrılmıştır.

Kullanılan parametreler:

$$
C=500
$$

$$
O=100
$$

olarak korunmuştur.

Toplam chunk sayısı:

$$
N_{chunk}=37
$$

olarak elde edilmiştir.

Her chunk 384 boyutlu embedding vektörüne dönüştürüldüğünden embedding matrisi:

$$
E\in\mathbb{R}^{37\times384}
$$

boyutunda oluşturulmuştur.

Terminal çıktısında:

```text
Toplam chunk sayısı: 37
Embedding matris boyutu: (37, 384)
Tek chunk embedding boyutu: (384,)
```

sonuçları elde edilmiştir.

---

## Embedding Retrieval Fonksiyonunun Geliştirilmesi

Embedding tabanlı retrieval için:

```python
search_with_embedding_index()
```

fonksiyonu geliştirilmiştir.

Kullanıcı sorgusu önce embedding vektörüne dönüştürülmektedir.

$$
q=E(query)
$$

Sorgu embedding boyutu:

$$
q\in\mathbb{R}^{384}
$$

olmaktadır.

Ardından sorgu embeddingi ile 37 chunk embeddingi arasında Cosine Similarity hesaplanmaktadır.

Her chunk için:

$$
s_i
===

\frac{q\cdot d_i}
{|q||d_i|}
$$

hesaplanmaktadır.

Elde edilen skorlar büyükten küçüğe sıralanarak ilk K sonuç retrieval sonucu olarak döndürülmektedir.

Deneylerde:

$$
K=3
$$

kullanılmıştır.

---

## Temel Embedding Retrieval Deneyi

Embedding retrieval sistemi aşağıdaki beş temel sorgu üzerinde test edilmiştir:

1. Sanal ortam nasıl oluşturulur?
2. Python nasıl kurulur?
3. FastAPI nedir?
4. Git deposu nasıl oluşturulur?
5. Loglama neden kullanılır?

Top-1 sonuçları:

| Sorgu                          | Beklenen Kaynak      | Embedding Top-1      | Durum  |
| ------------------------------ | -------------------- | -------------------- | ------ |
| Sanal ortam nasıl oluşturulur? | sanal_ortam.md       | sanal_ortam.md       | Doğru  |
| Python nasıl kurulur?          | python_kurulumu.md   | python_kurulumu.md   | Doğru  |
| FastAPI nedir?                 | fastapi_kullanimi.md | fastapi_kullanimi.md | Doğru  |
| Git deposu nasıl oluşturulur?  | git_komutlari.md     | veri_temizleme.md    | Yanlış |
| Loglama neden kullanılır?      | loglama.md           | loglama.md           | Doğru  |

Doğru Top-1 sonuç sayısı:

$$
4/5
$$

olarak elde edilmiştir.

Top-1 başarı oranı:

$$
Top1
====

\frac{4}{5}\times100
$$

Sonucunda:

$$
Top1=80%
$$

olmuştur.

Doğru kaynağın Top-3 içerisinde bulunduğu sorgu sayısı:

$$
4/5
$$

olmuştur.

Hit@3:

$$
Hit@3
=====

\frac{4}{5}\times100
$$

Sonucunda:

$$
Hit@3=80%
$$

olarak elde edilmiştir.

---

## TF-IDF ve Embedding Temel Sorgu Karşılaştırması

Aynı beş sorgu TF-IDF ve embedding retrieval sistemleri üzerinde karşılaştırılmıştır.

| Yöntem    | Top-1 | Hit@3 |
| --------- | ----: | ----: |
| TF-IDF    |  %100 |  %100 |
| Embedding |   %80 |   %80 |

Top-1 başarı farkı:

$$
100%-80%=20
$$

yüzde puan olarak hesaplanmıştır.

Temel sorgu setinde TF-IDF retrieval yaklaşımının embedding yaklaşımından daha yüksek başarı sağladığı gözlemlenmiştir.

---

## Paraphrase Karşılaştırma Deneyi

Embedding yaklaşımının anlamsal sorgu varyasyonlarında davranışını değerlendirmek amacıyla aşağıdaki paraphrase sorgular kullanılmıştır:

1. Python kurulumu için hangi adımları izlemeliyim?
2. FastAPI ne işe yarar?
3. Git projesi başlatmak için ne yapmalıyım?
4. Uygulamada neden log tutulur?
5. Python için sanal ortamı nasıl hazırlayabilirim?

İlk değerlendirmede her sorgu için yalnızca tek bir beklenen kaynak kullanılmıştır.

Ancak yapılan hata analizinde bazı sorguların birden fazla doküman tarafından doğru şekilde cevaplanabildiği görülmüştür.

Özellikle:

```text
Python için sanal ortamı nasıl hazırlayabilirim?
```

sorgusunda hem:

```text
sanal_ortam.md
```

hem de:

```text
servis_kurulumu.md
```

dosyalarının ilgili içerik taşıdığı görülmüştür.

Bu nedenle değerlendirme yapısı tek `expected_source` yerine birden fazla kabul edilebilir kaynak destekleyecek şekilde geliştirilmiştir.

Örnek:

```python
"expected_sources": [
    "sanal_ortam.md",
    "servis_kurulumu.md",
]
```

şeklinde tanımlanmıştır.

---

## Çoklu İlgili Kaynak Değerlendirmesi

Top-1 sonucu aşağıdaki koşul ile değerlendirilmiştir:

$$
Top1\in R_q
$$

Burada:

$$
R_q
$$

bir sorgu için kabul edilebilir kaynaklar kümesini ifade etmektedir.

Hit@3 için ise kabul edilebilir kaynaklardan en az birinin Top-3 içerisinde bulunması yeterli kabul edilmiştir.

$$
Hit@3=
\begin{cases}
1,& Top3\cap R_q\neq\emptyset\
0,& Top3\cap R_q=\emptyset
\end{cases}
$$

Bu değişiklik sonrasında paraphrase sonuçları yeniden hesaplanmıştır.

---

## Paraphrase Karşılaştırma Sonuçları

Güncellenmiş değerlendirme sonucunda:

| Yöntem    |      Top-1 |      Hit@3 |
| --------- | ---------: | ---------: |
| TF-IDF    | 5/5 = %100 | 5/5 = %100 |
| Embedding |  4/5 = %80 | 5/5 = %100 |

TF-IDF Top-1 başarısı:

$$
Top1_{\text{TF-IDF}}
====================

\frac{5}{5}\times100
$$

Sonucunda:

$$
Top1_{\text{TF-IDF}}=100%
$$

olarak hesaplanmıştır.

Embedding Top-1 başarısı:

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

Her iki yöntemde de:

$$
Hit@3=100%
$$

sonucu elde edilmiştir.

---

## Embedding Ranking Hatasının İncelenmesi

Paraphrase deneyinde:

```text
Uygulamada neden log tutulur?
```

sorgusunda beklenen kaynak:

```text
loglama.md
```

olmasına rağmen embedding sistemi:

```text
sanal_ortam.md
```

kaynağını Top-1 olarak getirmiştir.

Embedding sıralaması:

| Sıra | Kaynak            |   Skor |
| ---: | ----------------- | -----: |
|    1 | sanal_ortam.md    | 0.4434 |
|    2 | veri_temizleme.md | 0.4342 |
|    3 | loglama.md        | 0.4196 |

olarak elde edilmiştir.

Yanlış Top-1 ile doğru kaynak arasındaki similarity farkı:

$$
0.4434-0.4196
$$

Sonucunda:

$$
\Delta s=0.0238
$$

olarak hesaplanmıştır.

Doğru kaynak Top-3 içerisinde bulunduğundan:

$$
Hit@3=1
$$

olmuştur.

Bu örnek embedding sisteminde bir **ranking hatası** olarak değerlendirilmiştir.

---

## Git Retrieval Hatasının İncelenmesi

Temel sorgu deneyinde:

```text
Git deposu nasıl oluşturulur?
```

sorgusunda embedding sistemi doğru `git_komutlari.md` kaynağını Top-3 içerisinde bulamamıştır.

Tüm 37 chunk sıralandığında `git_komutlari.md` dosyasının en iyi chunkı:

$$
r=22
$$

sırada bulunmuştur.

Similarity skoru:

$$
s=0.0904
$$

olarak ölçülmüştür.

İlgili chunk içerisinde doğrudan:

```text
## Repository Başlatma

Yeni bir Git repository oluşturmak için:

git init
```

bilgisinin bulunduğu görülmüştür.

Bu nedenle söz konusu durum gerçek bir embedding retrieval/ranking başarısızlığı olarak değerlendirilmiştir.

---

## Git Sorgu Varyasyonu Deneyi

Embedding modelinin Git sorgularındaki terminoloji değişikliklerine duyarlılığını incelemek amacıyla beş farklı sorgu kullanılmıştır.

| Sorgu                                              | git_komutlari.md Sırası |   Skor | Hit@3 |
| -------------------------------------------------- | ----------------------: | -----: | ----- |
| Git deposu nasıl oluşturulur?                      |                      22 | 0.0904 | Hayır |
| Git repository nasıl oluşturulur?                  |                       1 | 0.7252 | Evet  |
| Yeni bir Git repository nasıl başlatılır?          |                       1 | 0.7051 | Evet  |
| Git projesi başlatmak için hangi komut kullanılır? |                       1 | 0.6303 | Evet  |
| git init komutu ne işe yarar?                      |                       2 | 0.2647 | Evet  |

Top-1 doğru sorgu sayısı:

$$
3/5
$$

olmuştur.

Top-1 başarı:

$$
\frac{3}{5}\times100
$$

Sonucunda:

$$
Top1=60%
$$

olarak hesaplanmıştır.

Hit@3 doğru sorgu sayısı:

$$
4/5
$$

olmuştur.

Hit@3 başarı oranı:

$$
\frac{4}{5}\times100
$$

Sonucunda:

$$
Hit@3=80%
$$

olarak elde edilmiştir.

---

## Terminoloji Duyarlılığının İncelenmesi

“Git deposu nasıl oluşturulur?” sorgusunda doğru kaynak skoru:

$$
0.0904
$$

olarak ölçülmüştür.

“Git repository nasıl oluşturulur?” sorgusunda ise:

$$
0.7252
$$

skoru elde edilmiştir.

Similarity skorundaki değişim:

$$
\Delta s
========

0.7252-0.0904
$$

Sonucunda:

$$
\Delta s=0.6348
$$

olarak hesaplanmıştır.

Doğru kaynağın sırası da:

$$
22\rightarrow1
$$

şeklinde değişmiştir.

Bu deney kullanılan embedding modelinin belirli terminoloji varyasyonlarına duyarlılık gösterebildiğini ortaya koymuştur.

Özellikle `depo` ve `repository` ifadeleri arasında beklenen güçlü anlamsal eşleşmenin bu sorguda oluşmadığı görülmüştür.

Ancak tamamen Türkçe olan:

```text
Git projesi başlatmak için hangi komut kullanılır?
```

sorgusunda doğru kaynak Top-1 olarak bulunduğu için sorun yalnızca Türkçe kullanımına bağlanmamıştır.

---

## Genel TF-IDF ve Embedding Değerlendirmesi

Gerçekleştirilen deneylerde TF-IDF ve embedding yaklaşımlarının farklı güçlü ve zayıf yönleri gözlemlenmiştir.

TF-IDF yaklaşımı mevcut küçük teknik doküman koleksiyonunda, özellikle sorgu ve doküman terminolojisinin örtüştüğü durumlarda yüksek retrieval başarısı sağlamıştır.

Embedding yaklaşımı anlamsal vektör temsili kullanmasına rağmen her sorguda TF-IDF yaklaşımından daha iyi sıralama üretmemiştir.

Bazı sorgularda doğru kaynak Top-3 içerisinde bulunmuş ancak Top-1 sıraya yerleşememiştir.

Bazı terminoloji varyasyonlarında ise doğru kaynak sıralamada önemli ölçüde geriye düşmüştür.

Bu nedenle:

```text
Embedding her durumda TF-IDF'den daha başarılıdır.
```

şeklinde bir sonuca ulaşılmamıştır.

Retrieval performansının kullanılan model, veri seti, teknik terminoloji ve sorgu biçiminden etkilendiği deneysel olarak gözlemlenmiştir.

---

## Otomatik Testler

Embedding retrieval sistemi için dört yeni otomatik test hazırlanmıştır.

Testlerde:

* Embedding vektör boyutunun 384 olması,
* Boş metin için hata oluşturulması,
* Bilinen sorguda doğru kaynağın Top-1 gelmesi,
* Geçersiz Top-K değerinde hata oluşturulması

kontrol edilmiştir.

Embedding boyutu için:

$$
d=384
$$

koşulu doğrulanmıştır.

Projede bulunan bütün otomatik testler tekrar çalıştırılmıştır.

Önceki test sayısı:

$$
30
$$

Yeni embedding test sayısı:

$$
4
$$

Toplam test sayısı:

$$
30+4=34
$$

olmuştur.

Başarılı test sayısı:

$$
B=34
$$

olarak elde edilmiştir.

Test başarı oranı:

$$
Test\ Başarı\ Oranı
===================

\frac{34}{34}\times100
$$

Sonucunda:

$$
Test\ Başarı\ Oranı=100%
$$

olarak bulunmuştur.

---

## Sonuç

11. gün sonunda embedding tabanlı semantik retrieval sistemi çalışır hale getirilmiştir.

Dokümanlardan oluşturulan 37 chunkın her biri 384 boyutlu embedding vektörüne dönüştürülmüştür.

Embedding matrisi:

$$
37\times384
$$

boyutunda oluşturulmuştur.

TF-IDF ve embedding yaklaşımları temel ve paraphrase sorgular üzerinde karşılaştırılmıştır.

Temel sorgularda:

$$
Top1_{\text{TF-IDF}}=100%
$$

$$
Top1_{\text{Embedding}}=80%
$$

sonuçları elde edilmiştir.

Güncellenmiş çoklu kaynak değerlendirmesi kullanılan paraphrase deneyinde:

$$
Top1_{\text{TF-IDF}}=100%
$$

$$
Top1_{\text{Embedding}}=80%
$$

olmuştur.

Her iki yaklaşımda da paraphrase sorgular için:

$$
Hit@3=100%
$$

sonucu elde edilmiştir.

Embedding sisteminde gözlemlenen hatalar incelendiğinde bazı problemlerin gerçek ranking hatalarından, bazı problemlerin ise tek doğru kaynak kabul eden değerlendirme yapısından kaynaklanabildiği görülmüştür.

Bu nedenle değerlendirme sistemi birden fazla kabul edilebilir kaynağı destekleyecek şekilde geliştirilmiştir.

Son olarak Git sorgu varyasyonlarında embedding modelinin terminolojiye duyarlı davranabildiği gözlemlenmiştir.

Tüm geliştirmeler sonrasında:

$$
34/34
$$

otomatik test başarılı olmuştur.

Test başarı oranı:

$$
100%
$$

olarak elde edilmiştir.

Bir sonraki çalışma gününde embedding retrieval yaklaşımının deneysel analizinin genişletilmesi ve TF-IDF ile embedding yöntemlerinin daha ayrıntılı karşılaştırılmasına devam edilmesi planlanmıştır.
