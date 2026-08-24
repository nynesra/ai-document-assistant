# 9. Gün - Chunk Size ve Top-K Deneyleri

## 1. Günün Amacı

Stajımın dokuzuncu gününde, önceki günlerde geliştirilen TF-IDF ve Cosine Similarity tabanlı retrieval sisteminin parametrelerinin deneysel olarak incelenmesine başlanmıştır.

Bu kapsamda özellikle iki temel parametre üzerinde çalışılmıştır:

* Chunk Size
* Top-K

Amaç, farklı chunk boyutlarının retrieval sisteminin oluşturduğu chunk sayısı, TF-IDF matris boyutu, vocabulary büyüklüğü ve retrieval sonuçları üzerindeki etkisini incelemek; ayrıca farklı Top-K değerlerinin sonuç listesinin kalitesine etkisini karşılaştırmaktır.

Deneylerde kontrollü bir yaklaşım kullanılmış ve her deneyde yalnızca incelenen parametre değiştirilmiştir.

---

# 2. `build_tfidf_index()` Fonksiyonunun Parametreli Hale Getirilmesi

Önceki yapıda `build_tfidf_index()` fonksiyonu içerisinde chunk size ve overlap değerleri sabit olarak tanımlanmıştı.

Bu nedenle farklı chunk boyutlarının karşılaştırılabilmesi amacıyla fonksiyon parametreli hale getirilmiştir.

Yeni fonksiyon yapısında:

```python
def build_tfidf_index(
    chunk_size: int = 500,
    overlap: int = 100,
):
```

kullanılmıştır.

Böylece varsayılan sistem davranışı korunurken farklı deneylerde:

```python
build_tfidf_index(
    chunk_size=300,
    overlap=100,
)
```

veya:

```python
build_tfidf_index(
    chunk_size=700,
    overlap=100,
)
```

şeklinde farklı parametreler kullanılabilir hale gelmiştir.

Bu değişikliğin önceki retrieval davranışını bozup bozmadığını kontrol etmek amacıyla mevcut otomatik testler yeniden çalıştırılmıştır.

Toplam test sayısı:

[
N=11
]

Başarılı test sayısı:

[
B=11
]

olarak elde edilmiştir.

Test başarı oranı:

[
\text{Başarı Oranı}
===================

\frac{11}{11}\times100
]

[
\boxed{\text{Başarı Oranı}=100%}
]

olarak bulunmuştur.

Böylece yapılan parametreleştirme işleminin mevcut retrieval sisteminde regression oluşturmadığı doğrulanmıştır.

---

# 3. Chunk Size Deneyinin Tasarlanması

Chunk size deneyinde üç farklı değer kullanılmıştır:

[
C\in{300,500,700}
]

Overlap bütün deneylerde sabit tutulmuştur:

[
O=100
]

Chunkların ilerleme miktarı aşağıdaki şekilde hesaplanmaktadır:

[
S=C-O
]

Burada:

* (C): Chunk Size
* (O): Overlap
* (S): Step

değerlerini ifade etmektedir.

---

# 4. Chunk Size = 300 Deneyi

İlk deneyde:

[
C=300
]

[
O=100
]

kullanılmıştır.

Step değeri:

[
S=300-100
]

[
\boxed{S=200}
]

olarak hesaplanmıştır.

Terminal çıktısında toplam chunk sayısı:

[
\boxed{N_{\text{chunk}}=67}
]

olarak elde edilmiştir.

TF-IDF matris boyutu:

[
\boxed{M_{300}\in\mathbb{R}^{67\times766}}
]

olarak ölçülmüştür.

Vocabulary boyutu:

[
\boxed{|V_{300}|=766}
]

olarak elde edilmiştir.

---

# 5. Chunk Size = 500 Deneyi

İkinci deneyde sistemin varsayılan değeri kullanılmıştır.

[
C=500
]

[
O=100
]

Step değeri:

[
S=500-100
]

[
\boxed{S=400}
]

olarak hesaplanmıştır.

Toplam chunk sayısı:

[
\boxed{N_{\text{chunk}}=37}
]

olarak elde edilmiştir.

TF-IDF matris boyutu:

[
\boxed{M_{500}\in\mathbb{R}^{37\times730}}
]

olarak ölçülmüştür.

Vocabulary boyutu:

[
\boxed{|V_{500}|=730}
]

olarak elde edilmiştir.

---

# 6. Chunk Size = 700 Deneyi

Üçüncü deneyde:

[
C=700
]

[
O=100
]

kullanılmıştır.

Step değeri:

[
S=700-100
]

[
\boxed{S=600}
]

olarak hesaplanmıştır.

Toplam chunk sayısı:

[
\boxed{N_{\text{chunk}}=26}
]

olarak elde edilmiştir.

TF-IDF matris boyutu:

[
\boxed{M_{700}\in\mathbb{R}^{26\times722}}
]

olarak ölçülmüştür.

Vocabulary boyutu:

[
\boxed{|V_{700}|=722}
]

olarak elde edilmiştir.

---

# 7. Chunk Size Sonuçlarının Karşılaştırılması

Deney sonucunda aşağıdaki tablo elde edilmiştir:

| Chunk Size | Overlap | Step | Chunk Sayısı | TF-IDF Matris Boyutu | Vocabulary |
| ---------: | ------: | ---: | -----------: | -------------------- | ---------: |
|        300 |     100 |  200 |           67 | 67 × 766             |        766 |
|        500 |     100 |  400 |           37 | 37 × 730             |        730 |
|        700 |     100 |  600 |           26 | 26 × 722             |        722 |

Chunk size küçüldükçe chunk sayısının arttığı görülmüştür.

Genel ilişki:

[
C\downarrow
\Rightarrow
N_{\text{chunk}}\uparrow
]

şeklindedir.

Ters durumda:

[
C\uparrow
\Rightarrow
N_{\text{chunk}}\downarrow
]

ilişkisi gözlenmiştir.

300 karakterlik yapı ile 67 chunk elde edilirken, 700 karakterlik yapı ile yalnızca 26 chunk elde edilmiştir.

---

# 8. Chunk Size Retrieval Deneyi

Farklı chunk boyutlarının retrieval sonuçlarına etkisini değerlendirmek amacıyla beş sorgudan oluşan kontrollü bir test seti kullanılmıştır.

Kullanılan sorgular:

```text
Sanal ortam nasıl oluşturulur?
Python nasıl kurulur?
FastAPI nedir?
Git deposu nasıl oluşturulur?
Loglama neden kullanılır?
```

Her deneyde:

[
O=100
]

ve:

[
K=1
]

sabit tutulmuştur.

Değiştirilen tek parametre chunk size olmuştur.

---

# 9. Chunk Size = 300 Retrieval Sonuçları

Elde edilen Top-1 similarity skorları:

| Sorgu           |   Skor |
| --------------- | -----: |
| Sanal ortam     | 0.7015 |
| Python kurulumu | 0.5744 |
| FastAPI         | 0.4706 |
| Git             | 0.5803 |
| Loglama         | 0.3436 |

Beş sorgunun tamamında beklenen kaynak Top-1 sırada bulunmuştur.

[
\text{Top-1 Doğru}=5/5
]

[
\boxed{\text{Top-1 Başarı}=100%}
]

Ortalama Top-1 similarity skoru:

[
\overline{S}_{300}
==================

\frac{
0.7015+0.5744+0.4706+0.5803+0.3436
}{5}
]

[
\boxed{\overline{S}_{300}\approx0.5341}
]

olarak hesaplanmıştır.

---

# 10. Chunk Size = 500 Retrieval Sonuçları

Top-1 similarity skorları:

| Sorgu           |   Skor |
| --------------- | -----: |
| Sanal ortam     | 0.6921 |
| Python kurulumu | 0.4813 |
| FastAPI         | 0.6062 |
| Git             | 0.6125 |
| Loglama         | 0.2576 |

Beş sorgunun tamamı doğru kaynakla eşleşmiştir.

[
\text{Top-1 Doğru}=5/5
]

[
\boxed{\text{Top-1 Başarı}=100%}
]

Ortalama similarity skoru:

[
\overline{S}_{500}
==================

\frac{
0.6921+0.4813+0.6062+0.6125+0.2576
}{5}
]

[
\boxed{\overline{S}_{500}\approx0.5299}
]

olarak hesaplanmıştır.

---

# 11. Chunk Size = 700 Retrieval Sonuçları

Top-1 similarity skorları:

| Sorgu           |   Skor |
| --------------- | -----: |
| Sanal ortam     | 0.6813 |
| Python kurulumu | 0.5455 |
| FastAPI         | 0.5500 |
| Git             | 0.6688 |
| Loglama         | 0.2051 |

Beş sorgunun tamamı doğru kaynakla eşleşmiştir.

[
\text{Top-1 Doğru}=5/5
]

[
\boxed{\text{Top-1 Başarı}=100%}
]

Ortalama similarity skoru:

[
\overline{S}_{700}
==================

\frac{
0.6813+0.5455+0.5500+0.6688+0.2051
}{5}
]

[
\boxed{\overline{S}_{700}\approx0.5301}
]

olarak hesaplanmıştır.

---

# 12. Chunk Size Retrieval Sonuçlarının Genel Değerlendirilmesi

Üç farklı chunk size değerinde de kontrollü test setindeki beş sorgunun tamamında beklenen kaynak Top-1 sırada bulunmuştur.

[
A_{300}=100%
]

[
A_{500}=100%
]

[
A_{700}=100%
]

Ortalama similarity skorları:

[
\overline{S}_{300}=0.5341
]

[
\overline{S}_{500}=0.5299
]

[
\overline{S}_{700}=0.5301
]

olarak ölçülmüştür.

Sayısal olarak en yüksek ortalama skor:

[
\boxed{\overline{S}_{300}=0.5341}
]

ile 300 karakterlik chunk yapısında elde edilmiştir.

Ancak üç değer arasındaki fark oldukça küçüktür.

Ayrıca her sorgu için aynı chunk size en yüksek skoru vermemiştir.

300 karakter:

* Sanal ortam
* Python kurulumu
* Loglama

sorgularında en yüksek skoru üretmiştir.

500 karakter:

* FastAPI

sorgusunda en yüksek sonucu vermiştir.

700 karakter:

* Git

sorgusunda en yüksek skoru üretmiştir.

Bu nedenle yalnızca mevcut beş sorguya bakılarak 300 karakterlik yapının kesin olarak en iyi seçenek olduğu sonucuna varılmamıştır.

500 karakterlik yapı hem Top-1 başarısını korumuş hem de 37 chunk ile orta seviyede bir indeks büyüklüğü sağlamıştır.

Bu nedenle sonraki deneyler için:

[
\boxed{C=500}
]

değeri korunmuştur.

---

# 13. Top-K Deneyinin Tasarlanması

İkinci deneyde chunk parametreleri sabit tutulmuştur.

[
C=500
]

[
O=100
]

Değiştirilen parametre:

[
K\in{1,3,5}
]

olmuştur.

Top-K değerinin etkisini değerlendirmek amacıyla Precision@K metriği kullanılmıştır.

Precision@K:

[
P@K
===

\frac{
\text{İlk K sonuç içerisindeki ilgili sonuç sayısı}
}{
K
}
]

şeklinde tanımlanmıştır.

Bu kontrollü deneyde bir sonucun “ilgili” kabul edilmesi için retrieval sonucunun kaynak dosyası ile beklenen kaynak dosyasının aynı olması şartı kullanılmıştır.

---

# 14. Top-K = 1 Deneyi

Top-1 sonucunda beş sorgunun tamamında beklenen kaynak dosya elde edilmiştir.

Toplam ilgili sonuç:

[
5
]

Toplam döndürülen sonuç:

[
5
]

olmuştur.

Precision@1:

[
P@1
===

\frac{5}{5}
]

[
\boxed{P@1=1.0000}
]

Yüzde olarak:

[
\boxed{P@1=100%}
]

olarak elde edilmiştir.

---

# 15. Top-K = 3 Deneyi

Beş sorgu için üçer sonuç döndürüldüğünden toplam sonuç sayısı:

[
5\times3=15
]

olmuştur.

Beklenen kaynak dosyalardan gelen toplam sonuç sayısı:

[
11
]

olarak ölçülmüştür.

Precision@3:

[
P@3
===

\frac{11}{15}
]

[
P@3\approx0.7333
]

Yüzde olarak:

[
\boxed{P@3\approx73.33%}
]

olarak bulunmuştur.

---

# 16. Top-K = 5 Deneyi

Beş sorgu için beşer sonuç döndürüldüğünden toplam sonuç sayısı:

[
5\times5=25
]

olmuştur.

Beklenen kaynaklardan gelen sonuç sayısı:

[
11
]

olarak ölçülmüştür.

Precision@5:

[
P@5
===

\frac{11}{25}
]

[
P@5=0.44
]

Yüzde olarak:

[
\boxed{P@5=44%}
]

olarak hesaplanmıştır.

---

# 17. Top-K Sonuçlarının Karşılaştırılması

Genel sonuçlar:

| Top-K | İlgili Sonuç | Toplam Sonuç | Precision |
| ----: | -----------: | -----------: | --------: |
|     1 |            5 |            5 |    1.0000 |
|     3 |           11 |           15 |    0.7333 |
|     5 |           11 |           25 |    0.4400 |

Sonuçlar:

[
P@1=1.0000
]

[
P@3=0.7333
]

[
P@5=0.4400
]

olarak elde edilmiştir.

Top-1 ile Top-3 arasındaki precision düşüşü:

[
1.0000-0.7333=0.2667
]

[
\boxed{26.67\text{ yüzde puan}}
]

olmuştur.

Top-3 ile Top-5 arasındaki düşüş:

[
0.7333-0.4400=0.2933
]

[
\boxed{29.33\text{ yüzde puan}}
]

olarak hesaplanmıştır.

---

# 18. Top-5 Sonuçlarının Ek Katkısının İncelenmesi

Top-3 deneyinde ilgili sonuç sayısı:

[
R_3=11
]

olarak elde edilmiştir.

Top-5 deneyinde de ilgili sonuç sayısı:

[
R_5=11
]

olarak kalmıştır.

Dolayısıyla ilgili sonuç sayısındaki artış:

[
R_5-R_3
]

[
11-11=0
]

[
\boxed{\Delta R=0}
]

olmuştur.

Buna karşılık toplam sonuç sayısı:

[
15\longrightarrow25
]

olarak artmıştır.

Eklenen sonuç sayısı:

[
25-15=10
]

olmasına rağmen yeni ilgili sonuç sayısı:

[
0
]

olmuştur.

Bu deney kapsamında `K=5` değerinin ek fayda sağlamadığı ve sonuç listesini daha fazla düşük ilgili sonuçla genişlettiği görülmüştür.

---

# 19. Sorgu Bazında Precision@K Sonuçları

| Sorgu           |    P@1 |    P@3 |    P@5 |
| --------------- | -----: | -----: | -----: |
| Sanal ortam     | 1.0000 | 0.6667 | 0.4000 |
| Python kurulumu | 1.0000 | 0.6667 | 0.4000 |
| FastAPI         | 1.0000 | 1.0000 | 0.6000 |
| Git             | 1.0000 | 1.0000 | 0.6000 |
| Loglama         | 1.0000 | 0.3333 | 0.2000 |

Özellikle “Loglama neden kullanılır?” sorgusunda Top-K arttıkça precision değerinin hızlı biçimde azaldığı görülmüştür.

[
P@1=1.0000
]

[
P@3\approx0.3333
]

[
P@5=0.2000
]

Bu sorguda yalnızca ilk sonucun `loglama.md` dokümanından gelmesi, K değeri artırıldıkça daha az ilgili sonuçların listeye eklendiğini göstermektedir.

---

# 20. Parametre Seçiminin Değerlendirilmesi

Chunk size deneylerinde üç değer de kontrollü test setinde %100 Top-1 kaynak başarısı sağlamıştır.

300 karakterlik yapı en yüksek ortalama similarity skorunu üretmesine rağmen 67 chunk oluşturmaktadır.

500 karakterlik yapı:

[
N_{\text{chunk}}=37
]

ile daha kompakt bir indeks oluştururken %100 Top-1 başarısını korumuştur.

700 karakterlik yapı ise yalnızca 26 chunk üretmiştir ancak bütün sorgularda en yüksek similarity skorunu sağlayamamıştır.

Bu nedenle mevcut deneyler sonucunda chunk size için:

[
\boxed{C=500}
]

değerinin korunmasına karar verilmiştir.

Top-K deneyinde sadece Precision dikkate alındığında:

[
K=1
]

en yüksek değeri üretmiştir.

Ancak RAG sisteminde cevap üretimi sırasında tek bir chunk yerine birden fazla ilgili chunkın modele ek bağlam sağlayabileceği dikkate alınmıştır.

Bu nedenle:

[
\boxed{K=3}
]

sonraki deneyler için daha dengeli bir aday olarak değerlendirilmiştir.

---

# 21. Deneyin Sınırlılıkları

Bu çalışmada kullanılan kontrollü sorgu seti yalnızca 5 sorudan oluşmaktadır.

Bu nedenle elde edilen %100 Top-1 başarısı bütün olası kullanıcı sorguları için genel retrieval doğruluğu olarak değerlendirilmemelidir.

Ayrıca Precision@K hesabında bir sonucun ilgili kabul edilmesi için:

```python
result["source"] == expected_source
```

koşulu kullanılmıştır.

Bu yaklaşım deneyin otomatik olarak ölçülebilmesini sağlamaktadır ancak farklı bir kaynak dosyasında bulunan ve sorguyla semantik olarak ilgili olabilecek chunkları “ilgili değil” olarak değerlendirebilir.

Bu nedenle hesaplanan Precision@K değerleri **kaynak-eşitliği tabanlı kontrollü deney metrikleri** olarak yorumlanmalıdır.

---

# 22. Gün Sonunda Elde Edilen Çıktılar

9. gün sonunda:

* `build_tfidf_index()` fonksiyonu chunk size ve overlap parametrelerini alabilecek hale getirilmiştir.
* Yapılan değişiklik sonrasında mevcut 11 retrieval testi yeniden çalıştırılmıştır.
* 11 testin tamamından beklenen sonuç alınmıştır.
* 300, 500 ve 700 karakterlik chunk size değerleri karşılaştırılmıştır.
* Chunk size 300 için 67 chunk ve 766 vocabulary elde edilmiştir.
* Chunk size 500 için 37 chunk ve 730 vocabulary elde edilmiştir.
* Chunk size 700 için 26 chunk ve 722 vocabulary elde edilmiştir.
* Üç chunk size değerinde de 5/5 Top-1 doğru kaynak sonucu elde edilmiştir.
* Ortalama Top-1 similarity skorları hesaplanmıştır.
* 300 karakter için ortalama skor 0.5341 olarak elde edilmiştir.
* 500 karakter için ortalama skor 0.5299 olarak elde edilmiştir.
* 700 karakter için ortalama skor 0.5301 olarak elde edilmiştir.
* Top-K için 1, 3 ve 5 değerleri karşılaştırılmıştır.
* Precision@1 değeri %100 olarak hesaplanmıştır.
* Precision@3 değeri %73.33 olarak hesaplanmıştır.
* Precision@5 değeri %44 olarak hesaplanmıştır.
* K=3'ten K=5'e geçildiğinde ilgili sonuç sayısının artmadığı belirlenmiştir.
* Sonraki deneyler için `chunk_size=500` ve `top_k=3` değerlerinin korunmasına karar verilmiştir.
* Düşük skorlu retrieval sonuçlarını filtrelemek amacıyla similarity threshold deneylerinin gerekli olduğu belirlenmiştir.

---

# 23. Gün Sonucu

Stajımın dokuzuncu gününde TF-IDF tabanlı retrieval sisteminin **Chunk Size ve Top-K parametreleri deneysel olarak incelenmiştir.**

Chunk size değerinin değiştirilmesinin bilgi tabanında oluşturulan chunk sayısını, TF-IDF matris boyutunu, vocabulary büyüklüğünü ve similarity skorlarını etkilediği görülmüştür.

Bununla birlikte mevcut beş sorguluk kontrollü test setinde:

[
C=300
]

[
C=500
]

ve:

[
C=700
]

değerlerinin tamamında:

[
\boxed{\text{Top-1 Başarı}=100%}
]

elde edilmiştir.

Top-K deneyinde:

[
P@1=100%
]

[
P@3\approx73.33%
]

[
P@5=44%
]

sonuçları elde edilmiştir.

K değeri arttıkça daha fazla retrieval sonucu döndürülmesine rağmen sonuç listesindeki kaynak-eşitliği tabanlı precision değerinin azaldığı görülmüştür.

Özellikle Top-3 ile Top-5 karşılaştırıldığında ilgili sonuç sayısının:

[
11\longrightarrow11
]

olarak değişmediği halde toplam sonuç sayısının:

[
15\longrightarrow25
]

seviyesine yükseldiği belirlenmiştir.

Bu nedenle mevcut deney sonuçlarında `K=5` kullanımının ek fayda sağlamadığı görülmüştür.

Sonraki deneyler için:

[
\boxed{C=500}
]

[
\boxed{O=100}
]

[
\boxed{K=3}
]

değerleri aday yapı olarak korunmuştur.

Bir sonraki aşamada düşük benzerlik skoruna sahip sonuçların filtrelenmesi amacıyla **similarity threshold deneylerinin gerçekleştirilmesi** planlanmıştır.
