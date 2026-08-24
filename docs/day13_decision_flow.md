# Day 13 - Query Routing, Decision Flow ve Kontrollü Tool Kullanımı

## Amaç

13. gün çalışmasında AI Doküman Asistanına kontrollü bir karar katmanı eklenmiştir.

Önceki günlerde kullanıcı sorguları doğrudan retrieval sistemine gönderilirken, bu yaklaşımın her sorgu türü için uygun olmadığı değerlendirilmiştir.

Örneğin:

- Matematiksel bir sorgu retrieval sistemine gönderilmemelidir.
- Boş veya yalnızca noktalama işaretlerinden oluşan sorgular işleme alınmamalıdır.
- Bilgi tabanının kapsamı dışındaki genel bilgi soruları dokümanlarda aranarak yanlış kaynaklarla eşleştirilmemelidir.
- Teknik doküman soruları retrieval sistemine yönlendirilmelidir.

Bu nedenle kullanıcı sorgusunun önce sınıflandırıldığı bir Query Router geliştirilmiştir.

Genel karar akışı:

Kullanıcı Sorgusu

↓

Query Router

↓

INVALID / CALCULATOR / RETRIEVAL / OUT_OF_SCOPE

↓

Uygun işlem

---

## 1. Query Router Yapısının Oluşturulması

`src/query_router.py` dosyası oluşturulmuştur.

İlk aşamada üç temel route tanımlanmıştır:

    class QueryRoute(str, Enum):
        INVALID = "invalid"
        CALCULATOR = "calculator"
        RETRIEVAL = "retrieval"

Bu yapı sayesinde kullanıcı sorgusunun hangi işlem tarafından ele alınacağı merkezi olarak belirlenmiştir.

---

## 2. Geçersiz Sorgu Kontrolü

Kullanıcının yalnızca boşluk veya noktalama işaretlerinden oluşan bir değer göndermesi geçerli bir soru olarak kabul edilmemiştir.

Örnek geçersiz sorgular:

    ""
    "     "
    "!!!"
    "???"
    "...!!!"

Bir sorgunun geçerli kabul edilebilmesi için en az bir harf veya rakam içermesi şartı uygulanmıştır.

Geçersiz sorgular için:

    Route: invalid
    Status: rejected

sonucu üretilmiştir.

Bu sorgular herhangi bir retrieval veya tool işlemine gönderilmemiştir.

---

## 3. Matematik Sorgularının Belirlenmesi

Basit matematiksel sorguların doküman retrieval sistemine gönderilmemesi amacıyla `extract_math_expression()` fonksiyonu geliştirilmiştir.

Örneğin:

    5 + 5 kaç?

sorgusundan:

    5 + 5

ifadesi çıkarılmıştır.

Benzer şekilde:

    10 / 2 nedir?

sorgusu calculator route'una yönlendirilmiştir.

Desteklenen temel operatörler:

    +
    -
    *
    /
    ()

olarak belirlenmiştir.

---

## 4. Güvenli Calculator Tool Geliştirilmesi

`src/calculator_tool.py` dosyası oluşturulmuştur.

Kullanıcıdan gelen ifadelerin doğrudan Python tarafından çalıştırılması güvenlik riski oluşturabileceği için:

    eval()

kullanılmamıştır.

Bunun yerine Python AST yapısı kullanılmıştır.

Yalnızca izin verilen:

- Toplama
- Çıkarma
- Çarpma
- Bölme
- Pozitif ve negatif sayılar
- Parantezler

işlenmektedir.

Örneğin:

    5 + 5

işlemi için:

5 + 5 = 10

sonucu elde edilmiştir.

Benzer şekilde:

    (10 + 5) / 3

işleminde:

(10 + 5) / 3 = 5

sonucu elde edilmiştir.

Desteklenmeyen Python ifadeleri AST kontrolü tarafından reddedilmektedir.

---

## 5. Sıfıra Bölme Kontrolü

Calculator Tool içerisinde sıfıra bölme işlemi ayrıca kontrol edilmiştir.

Örneğin:

    10 / 0

işlemi için programın kontrolsüz şekilde hata vermesi yerine:

    Sıfıra bölme işlemi yapılamaz.

mesajı döndürülmektedir.

Bu yapı sayesinde tool hatalarının decision flow içerisinde kontrollü biçimde ele alınması sağlanmıştır.

---

## 6. Decision Flow Yapısının Oluşturulması

`src/decision_flow.py` dosyası oluşturulmuştur.

Bu dosyada Query Router tarafından belirlenen route değerine göre uygun işlem çalıştırılmaktadır.

İlk karar yapısı:

    INVALID
        ↓
    REJECTED

    CALCULATOR
        ↓
    CALCULATOR TOOL

    RETRIEVAL
        ↓
    TF-IDF RETRIEVER

şeklinde oluşturulmuştur.

Retrieval tarafında önceki deneylerde belirlenen aday yapılandırma kullanılmıştır.

Top-K:

$$
K=3
$$

Similarity Threshold:

$$
T=0.20
$$

olarak kullanılmıştır.

---

## 7. İlk Decision Flow Kontrolü

Decision Flow ilk olarak dört örnek sorgu üzerinde kontrol edilmiştir.

### Matematik Sorgusu

    5 + 5 kaç?

Sonuç:

    Route: calculator
    Status: success
    Sonuç: 10

### Doküman Sorgusu

    Python nasıl kurulur?

Sonuç:

    Route: retrieval
    Status: success
    Kaynak: python_kurulumu.md
    Skor: 0.4813

### İlgisiz Genel Bilgi Sorgusu

    Türkiye'nin başkenti nedir?

İlk sistem yapısında bu sorgu retrieval route'una yönlendirilmiştir ancak threshold sonrasında yeterli kaynak bulunmadığı için:

    Status: insufficient_source

sonucu üretilmiştir.

### Geçersiz Sorgu

    !!!

Sonuç:

    Route: invalid
    Status: rejected

olarak elde edilmiştir.

---

## 8. Decision Flow Otomatik Testleri

Decision Flow yapısının doğru çalışmasını kontrol etmek amacıyla otomatik testler hazırlanmıştır.

Kontrol edilen davranışlar:

- Geçersiz sorgunun reddedilmesi
- Matematik sorgusunun Calculator Tool'a gitmesi
- Doküman sorgusunun retrieval sistemine yönlendirilmesi
- Yetersiz kaynak durumunda kesin cevap verilmemesi
- Calculator hatalarının kontrollü ele alınması

Bu aşamada proje genelinde:

$$
43/43
$$

test başarılı olmuştur.

Test başarı oranı:

$$
\frac{43}{43}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

---

## 9. İlk Query Routing Deneyi

Query Router'ın kontrollü bir sorgu setindeki karar doğruluğunu ölçmek amacıyla 15 sorguluk ilk routing deneyi hazırlanmıştır.

Üç sınıf kullanılmıştır:

- INVALID
- CALCULATOR
- RETRIEVAL

Her sınıfta:

$$
5
$$

sorgu kullanılmıştır.

Toplam sorgu sayısı:

$$
N=5+5+5
$$

Sonucunda:

$$
N=15
$$

olmuştur.

Bütün sorgular doğru sınıflandırılmıştır.

Doğru karar:

$$
15
$$

Yanlış karar:

$$
0
$$

Routing Accuracy:

$$
Accuracy=
\frac{15}{15}\times100
$$

Sonucunda:

$$
Accuracy=100\%
$$

olarak elde edilmiştir.

---

## 10. Sınıf Bazlı İlk Routing Sonuçları

INVALID sınıfı:

$$
5/5
$$

Sonucunda:

$$
Accuracy_{INVALID}=100\%
$$

CALCULATOR sınıfı:

$$
5/5
$$

Sonucunda:

$$
Accuracy_{CALCULATOR}=100\%
$$

RETRIEVAL sınıfı:

$$
5/5
$$

Sonucunda:

$$
Accuracy_{RETRIEVAL}=100\%
$$

olarak ölçülmüştür.

Bu sonuç yalnızca hazırlanan kontrollü 15 sorguluk test seti kapsamında değerlendirilmiştir.

---

## 11. Routing Sınır Durumu Deneyi

İlk routing deneyinde bütün sorgular doğru sınıflandırıldığı için sistem daha zor ve farklı biçimde yazılmış sorgularla test edilmiştir.

Toplam:

$$
N=12
$$

sınır durumu kullanılmıştır.

Özellikle matematiksel ifadelerin farklı yazım biçimleri denenmiştir.

Örnekler:

    3 x 7 kaç?
    20 bölü 4 kaç?

İlk deney sonucunda:

Doğru karar:

$$
10
$$

Yanlış karar:

$$
2
$$

olmuştur.

Accuracy:

$$
Accuracy=
\frac{10}{12}\times100
$$

Sonucunda:

$$
Accuracy=83.33\%
$$

olarak elde edilmiştir.

---

## 12. Sınır Durumu Hata Analizi

İki hatalı sorgu:

    3 x 7 kaç?

ve:

    20 bölü 4 kaç?

olarak belirlenmiştir.

Her iki sorgu için beklenen route:

    calculator

iken sistem:

    retrieval

sonucu üretmiştir.

Hatanın nedeni Query Router'ın yalnızca:

    +
    -
    *
    /

sembollerini matematik operatörü olarak tanımasıdır.

Türkçe doğal dil veya alternatif çarpma gösterimi henüz desteklenmemekteydi.

---

## 13. Matematik Normalizasyonunun Geliştirilmesi

Gözlemlenen hatalar sonucunda Query Router geliştirilmiştir.

Çarpma için:

    x

ifadesi:

    *

operatörüne dönüştürülmüştür.

Bölme için:

    bölü

kelimesi:

    /

operatörüne dönüştürülmüştür.

Böylece:

    3 x 7 kaç?

sorgusu:

    3 * 7

şeklinde normalize edilmiştir.

Aynı şekilde:

    20 bölü 4 kaç?

sorgusu:

    20 / 4

şeklinde normalize edilmiştir.

---

## 14. Sınır Durumu Deneyinin Tekrarlanması

Router iyileştirildikten sonra aynı 12 sorguluk sınır durumu deneyi tekrar çalıştırılmıştır.

Doğru karar:

$$
12
$$

Yanlış karar:

$$
0
$$

olmuştur.

Yeni Accuracy:

$$
Accuracy=
\frac{12}{12}\times100
$$

Sonucunda:

$$
Accuracy=100\%
$$

olarak elde edilmiştir.

İyileştirme öncesinde:

$$
83.33\%
$$

olan accuracy değeri iyileştirme sonrasında:

$$
100\%
$$

olmuştur.

---

## 15. Yeni Davranışların Regression Testlerine Eklenmesi

Yeni desteklenen:

    3 x 7 kaç?

ve:

    20 bölü 4 kaç?

sorguları otomatik testlere eklenmiştir.

Birinci sorgunun beklenen sonucu:

$$
3\times7=21
$$

İkinci sorgunun beklenen sonucu:

$$
\frac{20}{4}=5
$$

olarak belirlenmiştir.

Yeni testler sonrasında proje genelinde:

$$
45/45
$$

test başarılı olmuştur.

Test başarı oranı:

$$
100\%
$$

olarak elde edilmiştir.

---

## 16. İlk Uçtan Uca Decision Flow Deneyi

Router'ın yalnızca sınıflandırma doğruluğunu değil, bütün karar zincirini değerlendirmek amacıyla uçtan uca deney hazırlanmıştır.

İlk deneyde toplam:

$$
N=16
$$

sorgu kullanılmıştır.

Beklenen davranış grupları:

- Calculator Success
- Retrieval Success
- Insufficient Source
- Invalid Rejected

olarak belirlenmiştir.

İlk deney sonucunda:

Doğru route:

$$
16/16
$$

Doğru status:

$$
15/16
$$

Tam doğru karar:

$$
15/16
$$

olmuştur.

Route Accuracy:

$$
\frac{16}{16}\times100=100\%
$$

Status Accuracy:

$$
\frac{15}{16}\times100=93.75\%
$$

End-to-End Accuracy:

$$
\frac{15}{16}\times100=93.75\%
$$

olarak elde edilmiştir.

---

## 17. Uçtan Uca Deneyde False Positive Tespiti

Uçtan uca deneyde başarısız olan tek sorgu:

    5G hangi ülkede geliştirildi?

olmuştur.

Beklenen:

    retrieval / insufficient_source

iken sistem:

    retrieval / success

sonucu üretmiştir.

Bu nedenle sorgunun ham TF-IDF retrieval sonuçları ayrıca analiz edilmiştir.

Top-1 sonuç:

    Kaynak: model_degerlendirme.md
    Bölüm: Hata Analizi
    Skor: 0.2928

olarak elde edilmiştir.

Ancak ilgili chunk içerisinde 5G hakkında bilgi bulunmamaktadır.

Bu nedenle sonuç gerçek bir False Positive olarak değerlendirilmiştir.

---

## 18. Threshold Sınırlılığının Ortaya Çıkması

Mevcut aday threshold değeri:

$$
T=0.20
$$

idi.

5G sorgusunun ilgisiz Top-1 skoru:

$$
S_{ilgisiz}=0.2928
$$

olarak ölçülmüştür.

Bu durumda:

$$
0.2928\geq0.20
$$

olduğu için ilgisiz chunk kabul edilmiştir.

Önceki threshold deneylerinde ilgili sorguların minimum skoru:

$$
S_{ilgili,min}=0.2576
$$

olarak ölçülmüştü.

Yeni ilgisiz skor:

$$
0.2928
$$

olduğundan:

$$
0.2928>0.2576
$$

sonucu ortaya çıkmıştır.

Bu nedenle yalnızca threshold kullanılarak bütün ilgili ve ilgisiz sorguların tamamen ayrılması mümkün değildir.

5G sorgusunun reddedilebilmesi için:

$$
T>0.2928
$$

gerekir.

Ancak bu durumda:

$$
0.2576<T
$$

olacağından daha önce doğru olan düşük skorlu ilgili bir sorgu False Negative olabilir.

Bu deney sonucunda:

**Tek başına similarity threshold yeterli değildir.**

sonucuna ulaşılmıştır.

---

## 19. OUT_OF_SCOPE Route'unun Eklenmesi

False Positive analizinden sonra Query Router geliştirilmiştir.

Yeni karar sınıfı:

    OUT_OF_SCOPE

eklenmiştir.

Güncellenmiş route yapısı:

    class QueryRoute(str, Enum):
        INVALID = "invalid"
        CALCULATOR = "calculator"
        RETRIEVAL = "retrieval"
        OUT_OF_SCOPE = "out_of_scope"

şeklinde oluşturulmuştur.

---

## 20. Bilgi Tabanı Kapsam Kontrolü

Teknik doküman koleksiyonunun temel kapsamını belirlemek amacıyla kontrollü konu anahtar kelimeleri tanımlanmıştır.

Örnek konu ifadeleri:

    python
    fastapi
    git
    repository
    repo
    sanal ortam
    venv
    log
    loglama
    servis
    api
    veri temizleme
    model

Bir sorgunun mevcut teknik bilgi tabanıyla ilişkili olup olmadığı retrieval işleminden önce kontrol edilmeye başlanmıştır.

Yeni karar sırası:

INVALID

↓

CALCULATOR

↓

KB Scope Control

↓

RETRIEVAL veya OUT_OF_SCOPE

şeklinde oluşturulmuştur.

---

## 21. OUT_OF_SCOPE Güvenli Ret Davranışı

Kapsam dışı sorgular için:

    Route: out_of_scope
    Status: rejected

sonucu üretilmektedir.

Örneğin:

    Türkiye'nin başkenti nedir?

sorgusu:

    out_of_scope / rejected

olarak sonuçlanmıştır.

Benzer şekilde daha önce False Positive oluşturan:

    5G hangi ülkede geliştirildi?

sorgusu da:

    out_of_scope / rejected

olarak sonuçlanmıştır.

Bu sorgu artık TF-IDF retrieval sistemine gönderilmemektedir.

---

## 22. Threshold ve Scope Control Katmanlarının Ayrılması

Yeni decision flow içerisinde iki farklı güvenlik katmanı bulunmaktadır.

Birinci katman:

    Scope Control

Sorgunun bilgi tabanıyla ilişkili olup olmadığını kontrol etmektedir.

İkinci katman:

    Similarity Threshold

Bilgi tabanı kapsamındaki sorgular için yeterince güçlü retrieval sonucu bulunup bulunmadığını kontrol etmektedir.

Bu nedenle:

$$
Scope\ Control\neq Similarity\ Threshold
$$

olarak değerlendirilmiştir.

Scope Control, doküman alanı dışındaki soruları retrieval öncesinde engellemektedir.

Threshold ise retrieval sonrasında bulunan chunk skorlarını filtrelemektedir.

---

## 23. Insufficient Source Davranışının Korunması

OUT_OF_SCOPE route'u eklendikten sonra `insufficient_source` davranışı kaldırılmamıştır.

Bir sorgu teknik bilgi tabanı kapsamında olabilir ancak yeterince güçlü retrieval sonucu bulunmayabilir.

Bu davranış otomatik testte yüksek threshold kullanılarak kontrol edilmiştir.

Örneğin:

    Python nasıl kurulur?

sorgusu için normal skor yaklaşık:

$$
s=0.4813
$$

olarak ölçülmüştür.

Test sırasında:

$$
T=0.99
$$

kullanılmıştır.

Bu durumda:

$$
0.4813<0.99
$$

olduğundan chunk elenmiştir.

Sonuç:

    Route: retrieval
    Status: insufficient_source

olarak elde edilmiştir.

Buradaki:

$$
T=0.99
$$

değeri üretim threshold'u değildir.

Yalnızca `insufficient_source` karar yolunu deterministik biçimde test etmek için kullanılmıştır.

Normal aday threshold:

$$
T=0.20
$$

olarak korunmuştur.

---

## 24. Güncellenmiş Regression Testleri

OUT_OF_SCOPE davranışı için yeni testler eklenmiştir.

Özellikle daha önce False Positive oluşturan:

    5G hangi ülkede geliştirildi?

sorgusunun artık:

    out_of_scope / rejected

olarak sonuçlanması test edilmiştir.

Ayrıca teknik bir sorgunun yüksek threshold altında:

    retrieval / insufficient_source

sonucu üretebildiği doğrulanmıştır.

Son regression test sonucu:

$$
47/47
$$

olarak elde edilmiştir.

Test başarı oranı:

$$
\frac{47}{47}\times100
$$

Sonucunda:

$$
100\%
$$

olmuştur.

---

## 25. Dört Sınıflı Final Routing Deneyi

Query Router güncellendikten sonra routing değerlendirme setine OUT_OF_SCOPE sınıfı da eklenmiştir.

Dört sınıf kullanılmıştır:

- INVALID
- CALCULATOR
- RETRIEVAL
- OUT_OF_SCOPE

Her sınıfta:

$$
5
$$

sorgu bulunmaktadır.

Toplam sorgu sayısı:

$$
N=5+5+5+5
$$

Sonucunda:

$$
N=20
$$

olmuştur.

---

## 26. Final Routing Sonuçları

Bütün 20 sorgu doğru sınıflandırılmıştır.

Doğru karar:

$$
20
$$

Yanlış karar:

$$
0
$$

Routing Accuracy:

$$
Accuracy_{routing}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{routing}=100\%
$$

olarak elde edilmiştir.

Sınıf bazında:

INVALID:

$$
5/5=100\%
$$

CALCULATOR:

$$
5/5=100\%
$$

RETRIEVAL:

$$
5/5=100\%
$$

OUT_OF_SCOPE:

$$
5/5=100\%
$$

sonuçları elde edilmiştir.

Bu sonuç yalnızca hazırlanan kontrollü 20 sorguluk routing test seti kapsamında değerlendirilmiştir.

---

## 27. Final Uçtan Uca Decision Flow Deneyi

Son aşamada bütün decision flow yeni yapı ile tekrar değerlendirilmiştir.

Beş farklı davranış grubu kullanılmıştır:

1. Calculator → Success
2. Retrieval → Success
3. Retrieval → Insufficient Source
4. Out of Scope → Rejected
5. Invalid → Rejected

Her grupta:

$$
4
$$

test bulunmaktadır.

Toplam sorgu sayısı:

$$
N=4+4+4+4+4
$$

Sonucunda:

$$
N=20
$$

olmuştur.

---

## 28. Final Decision Flow Sonuçları

Final deneyde bütün route ve status sonuçları beklenen şekilde elde edilmiştir.

Doğru route:

$$
20/20
$$

Doğru status:

$$
20/20
$$

Tam doğru karar:

$$
20/20
$$

Route Accuracy:

$$
Accuracy_{route}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{route}=100\%
$$

Status Accuracy:

$$
Accuracy_{status}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{status}=100\%
$$

End-to-End Accuracy:

$$
Accuracy_{E2E}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{E2E}=100\%
$$

olarak elde edilmiştir.

---

## 29. Final Decision Flow Dağılımı

Final deneyde sonuç dağılımı:

    Calculator Success: 4
    Retrieval Success: 4
    Insufficient Source: 4
    Out of Scope Rejected: 4
    Invalid Rejected: 4

olarak elde edilmiştir.

Her karar yolu kontrollü olarak test edilmiş ve beklenen davranışı göstermiştir.

---

## 30. Gün Sonunda Oluşan Decision Flow

13. gün sonunda sistemin karar yapısı:

    Kullanıcı Sorgusu
            |
            v
       Geçerli mi?
         /      \
       Hayır    Evet
        |         |
     INVALID      v
     REJECTED  Matematik mi?
                 /      \
               Evet     Hayır
                |         |
           CALCULATOR     v
              TOOL     KB kapsamı mı?
                         /      \
                       Hayır    Evet
                        |         |
                  OUT_OF_SCOPE    v
                    REJECTED   RETRIEVAL
                                   |
                                   v
                             Similarity
                             Threshold
                              /       \
                        Yetersiz     Yeterli
                           |             |
                    INSUFFICIENT       SUCCESS
                       SOURCE

Bu yapı sayesinde her kullanıcı sorgusunun doğrudan retrieval sistemine gönderilmesinin önüne geçilmiştir.

---

## 31. Deneyin Sınırlılıkları

Routing sisteminde kullanılan bilgi tabanı kapsam kontrolü şu anda basit ve kontrollü anahtar kelimelere dayanmaktadır.

Bu nedenle gerçek kullanıcı sorgularının bütün dilsel varyasyonlarını kapsadığı kabul edilmemelidir.

Örneğin teknik bir konu kullanıcı tarafından mevcut anahtar kelimeler kullanılmadan ifade edilirse yanlışlıkla `OUT_OF_SCOPE` olarak sınıflandırılabilir.

Ayrıca kontrollü routing test setinde:

$$
20
$$

sorgu kullanılmıştır.

Bu nedenle:

$$
100\%
$$

routing doğruluğu bütün gerçek kullanıcı sorgularında aynı performansın elde edileceğini garanti etmemektedir.

Benzer şekilde final Decision Flow deneyinde elde edilen:

$$
100\%
$$

End-to-End Accuracy yalnızca hazırlanan kontrollü 20 sorguluk deney seti kapsamında değerlendirilmiştir.

Bilgi tabanı kapsam kontrolünün ilerleyen çalışmalarda anahtar kelime tabanlı yapı yerine daha esnek semantik veya sınıflandırıcı tabanlı yöntemlerle geliştirilebileceği değerlendirilmiştir.

---

## 32. Gün Sonunda Elde Edilen Çıktılar

13. gün sonunda:

- `src/query_router.py` oluşturulmuştur.
- INVALID sorgu kontrolü eklenmiştir.
- CALCULATOR route'u oluşturulmuştur.
- RETRIEVAL route'u oluşturulmuştur.
- OUT_OF_SCOPE route'u eklenmiştir.
- `src/calculator_tool.py` geliştirilmiştir.
- Calculator işlemlerinde güvenli AST yaklaşımı kullanılmıştır.
- `eval()` kullanımından kaçınılmıştır.
- Sıfıra bölme kontrolü eklenmiştir.
- `src/decision_flow.py` oluşturulmuştur.
- Query Router ile Calculator Tool birbirine bağlanmıştır.
- Query Router ile TF-IDF Retriever birbirine bağlanmıştır.
- Similarity Threshold karar akışına dahil edilmiştir.
- `insufficient_source` güvenli ret davranışı korunmuştur.
- `x` ile çarpma işlemi desteklenmiştir.
- `bölü` kelimesi ile bölme işlemi desteklenmiştir.
- Routing sınır durumları analiz edilmiştir.
- 5G sorgusunda gerçek bir False Positive tespit edilmiştir.
- Tek başına threshold kullanımının sınırlılığı gösterilmiştir.
- Bilgi tabanı Scope Control katmanı eklenmiştir.
- Dört sınıflı final routing deneyi gerçekleştirilmiştir.
- Final uçtan uca Decision Flow deneyi gerçekleştirilmiştir.
- Proje genelinde 47 otomatik test başarıyla tamamlanmıştır.

---

## 33. Sonuç

13. gün çalışmasında AI Doküman Asistanına Query Routing ve kontrollü Decision Flow katmanı eklenmiştir.

Sistem ilk olarak:

- INVALID
- CALCULATOR
- RETRIEVAL

olmak üzere üç karar sınıfıyla geliştirilmiştir.

Calculator Tool güvenli AST yaklaşımı kullanılarak oluşturulmuş ve doğrudan `eval()` kullanımı engellenmiştir.

İlk kontrollü routing deneyinde:

$$
15/15
$$

doğru karar elde edilmiştir.

Routing Accuracy:

$$
100\%
$$

olarak bulunmuştur.

Daha zor sınır durumlarında ilk sonuç:

$$
10/12
$$

olmuştur.

Accuracy:

$$
83.33\%
$$

olarak ölçülmüştür.

`x` ve `bölü` ifadelerinin desteklenmesi sonrasında aynı deney:

$$
12/12
$$

doğru karar ile tamamlanmıştır.

Accuracy:

$$
100\%
$$

olmuştur.

İlk uçtan uca Decision Flow deneyinde ise:

$$
15/16
$$

tam doğru karar elde edilmiştir.

End-to-End Accuracy:

$$
93.75\%
$$

olarak ölçülmüştür.

Hata analizinde:

    5G hangi ülkede geliştirildi?

sorgusunun ilgisiz bir chunk için:

$$
0.2928
$$

similarity skoru aldığı görülmüştür.

Bu değer önceki ilgili minimum skor:

$$
0.2576
$$

değerinden daha yüksek olduğu için tek başına similarity threshold kullanmanın yeterli olmadığı sonucuna ulaşılmıştır.

Bunun üzerine sisteme:

    OUT_OF_SCOPE

route'u ve bilgi tabanı kapsam kontrolü eklenmiştir.

Güncellenmiş dört sınıflı routing deneyinde:

$$
20/20
$$

doğru karar alınmıştır.

Routing Accuracy:

$$
100\%
$$

olarak elde edilmiştir.

Final uçtan uca Decision Flow deneyinde:

$$
20/20
$$

route doğru,

$$
20/20
$$

status doğru,

$$
20/20
$$

tam karar doğru

olarak bulunmuştur.

End-to-End Accuracy:

$$
100\%
$$

olarak ölçülmüştür.

Son regression testlerinde:

$$
47/47
$$

otomatik test başarıyla tamamlanmıştır.

Test başarı oranı:

$$
\frac{47}{47}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

13. gün sonunda sistem artık kullanıcı sorgularını kontrollü biçimde sınıflandırabilmekte, yalnızca gerekli durumda retrieval veya Calculator Tool çalıştırmakta, kapsam dışı sorguları retrieval öncesinde reddetmekte ve yeterli kaynak bulunmadığında kesin cevap üretmemektedir.

Böylece AI Doküman Asistanının yalnızca doküman araması yapan bir yapıdan, kullanıcı sorgusuna göre hangi işlemin uygulanacağına karar verebilen kontrollü bir karar akışına geçişi gerçekleştirilmiştir.