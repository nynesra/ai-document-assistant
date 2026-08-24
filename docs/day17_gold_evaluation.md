# Day 17 - Gold Evaluation Set ile Uçtan Uca Sistem Değerlendirmesi

## Amaç

17. gün çalışmasında, 16. gün hazırlanan 20 soruluk Gold Evaluation Set gerçek AI Doküman Asistanı sistemi üzerinden çalıştırılmış ve sistemin uçtan uca performansı ölçülmüştür.

Önceki günlerde sistemin farklı bileşenleri ayrı deneylerle değerlendirilmişti.

Bu bileşenler:

- Input Guardrail
- Query Router
- Scope Control
- Tool Registry
- Tool Authorization
- Calculator Tool
- TF-IDF Retriever
- Similarity Threshold
- Decision Trace
- JSONL Logging

olarak geliştirilmiştir.

17. gün çalışmasında bu bileşenlerin tamamı ortak bir Gold Evaluation Set kullanılarak birlikte değerlendirilmiştir.

Genel değerlendirme akışı:

    Gold Evaluation Set
            |
            v
      Controlled Flow
            |
            v
        Prediction
            |
            v
       Gold Label
       Comparison
            |
            v
         Metrics

şeklinde uygulanmıştır.

---

## 1. Gold Evaluation Set'in Yüklenmesi

16. gün oluşturulan:

    evaluation/eval_set.json

dosyası değerlendirme için kullanılmıştır.

Evaluation Set toplam:

$$
N=20
$$

sorgudan oluşmaktadır.

Kategori dağılımı:

$$
N_{retrieval}=8
$$

$$
N_{calculator}=4
$$

$$
N_{out-of-scope}=3
$$

$$
N_{invalid}=2
$$

$$
N_{guardrail}=3
$$

olarak belirlenmiştir.

Toplam:

$$
8+4+3+2+3=20
$$

olarak doğrulanmıştır.

---

## 2. Gold Evaluation Scriptinin Oluşturulması

Gold Evaluation Set'i gerçek Controlled Flow üzerinden çalıştırmak amacıyla:

    evaluation/day17_gold_eval.py

dosyası oluşturulmuştur.

Her evaluation kaydı:

    run_controlled_flow()

fonksiyonuna gönderilmiştir.

Böylece kullanıcı sorguları gerçek sistemde olduğu gibi:

    Input Guardrail
            |
            v
       Query Router
            |
            v
      Scope Control
            |
            v
      Tool Selection
            |
            v
       Authorization
            |
            v
      Tool Execution
            |
            v
          Trace

akışından geçirilmiştir.

---

## 3. Gold ve Prediction Karşılaştırması

Her sorgu için sistem tarafından oluşturulan gerçek sonuçlar, Evaluation Set içerisinde tanımlanan Gold değerlerle karşılaştırılmıştır.

Temel yaklaşım:

$$
Prediction
\leftrightarrow
Gold
$$

şeklinde uygulanmıştır.

Karşılaştırılan ortak alanlar:

- Route
- Tool
- Status

olarak belirlenmiştir.

Ayrıca kategoriye özel doğruluk kontrolleri gerçekleştirilmiştir.

---

## 4. Route Accuracy Metriği

Sistemin kullanıcı sorgusunu doğru karar yoluna yönlendirip yönlendirmediğini ölçmek amacıyla Route Accuracy kullanılmıştır.

Formül:

$$
Accuracy_{route}
=
\frac{N_{doğru\ route}}
{N_{toplam}}
\times100
$$

olarak kullanılmıştır.

---

## 5. Tool Accuracy Metriği

Query Router tarafından verilen karar sonrasında doğru aracın seçilip seçilmediğini ölçmek amacıyla Tool Accuracy kullanılmıştır.

Formül:

$$
Accuracy_{tool}
=
\frac{N_{doğru\ tool}}
{N_{toplam}}
\times100
$$

olarak belirlenmiştir.

---

## 6. Status Accuracy Metriği

Tool veya karar akışı sonucunda doğru status değerinin üretilip üretilmediği ayrıca değerlendirilmiştir.

Örnek status değerleri:

    success
    not_executed
    guardrail_blocked

olarak bulunmaktadır.

Status Accuracy:

$$
Accuracy_{status}
=
\frac{N_{doğru\ status}}
{N_{toplam}}
\times100
$$

formülüyle hesaplanmıştır.

---

## 7. Kategoriye Özel Değerlendirme

Route, Tool ve Status sonuçlarının doğru olması sistemin bütün görevlerde doğru sonucu verdiğini tek başına göstermemektedir.

Bu nedenle kategoriye özel ek kontroller yapılmıştır.

Retrieval için:

    Beklenen kaynak doğru mu?

Calculator için:

    Matematik sonucu doğru mu?

Guardrail için:

    Engelleme nedeni doğru mu?

kontrol edilmiştir.

---

## 8. Retrieval Top-1 Değerlendirmesi

Retrieval kategorisinde toplam:

$$
8
$$

Gold sorgu bulunmaktadır.

Bir retrieval sorgusunun Top-1 açısından doğru kabul edilmesi için:

$$
Top1\in R_q
$$

koşulu uygulanmıştır.

Burada:

$$
R_q
$$

ilgili sorgu için kabul edilebilir Gold kaynaklar kümesini ifade etmektedir.

---

## 9. Çoklu Kabul Edilebilir Kaynakların Korunması

Bazı sorguların birden fazla doğru kaynak tarafından cevaplanabileceği daha önce gözlemlenmişti.

Örneğin:

    Sanal ortam nasıl oluşturulur?

sorgusu için:

    sanal_ortam.md

ve:

    servis_kurulumu.md

kaynaklarının ikisi de kabul edilebilir kaynak olarak tanımlanmıştır.

Bu nedenle sistem bu kaynaklardan herhangi birini Top-1 sıraya getirirse sonuç doğru kabul edilmektedir.

---

## 10. Retrieval Hit@3 Değerlendirmesi

Doğru veya kabul edilebilir kaynağın ilk üç retrieval sonucu içerisinde bulunup bulunmadığını değerlendirmek amacıyla Hit@3 metriği kullanılmıştır.

Bir sorgu için:

$$
Hit@3=1
$$

olması için kabul edilebilir kaynaklardan en az birinin ilk üç sonuçta bulunması gerekmektedir.

Genel formül:

$$
Hit@3
=
\frac{N_{başarılı\ Hit@3}}
{N_{retrieval}}
\times100
$$

olarak kullanılmıştır.

---

## 11. Calculator Evaluation Mantığı

Calculator kategorisindeki sorgular için gerçek tool sonucu Evaluation Set içerisindeki:

    expected_result

değeriyle karşılaştırılmıştır.

Temel koşul:

$$
Result_{actual}
=
Result_{gold}
$$

olarak uygulanmıştır.

Floating-point sonuçlarda çok küçük sayısal farklılıkları tolere etmek amacıyla kontrollü tolerans karşılaştırması kullanılmıştır.

---

## 12. Guardrail Reason Evaluation Mantığı

Guardrail kategorisinde yalnızca sorgunun engellenmesi yeterli görülmemiştir.

Engelleme nedeninin de Gold değerle aynı olması beklenmiştir.

Koşul:

$$
Reason_{actual}
=
Reason_{gold}
$$

olarak uygulanmıştır.

Örnek Gold reason değerleri:

    prompt_injection
    control_character

olarak bulunmaktadır.

---

## 13. Out of Scope Değerlendirmesi

Out of Scope sorgularında beklenen:

    route = out_of_scope
    tool = none
    status = not_executed

davranışıdır.

Bu sayede bilgi tabanı dışında kalan sorguların Retriever Tool'a ulaşmadığı kontrol edilmiştir.

---

## 14. Invalid Sorgu Değerlendirmesi

Invalid sorgular için beklenen davranış:

    route = invalid
    tool = none
    status = not_executed

olarak belirlenmiştir.

Bu kategori yalnızca boşluk veya noktalama işaretlerinden oluşan geçersiz kullanıcı girdilerini kapsamaktadır.

---

## 15. End-to-End Doğruluk Tanımı

Bir Gold Evaluation kaydının tamamen doğru kabul edilmesi için birden fazla şartın aynı anda sağlanması gerekmektedir.

Koşullar:

$$
RouteCorrect=1
$$

$$
ToolCorrect=1
$$

$$
StatusCorrect=1
$$

$$
CategorySpecificCorrect=1
$$

olmalıdır.

Dolayısıyla tek sorgu için:

$$
E2E_i
=
Route_i
\land
Tool_i
\land
Status_i
\land
CategorySpecific_i
$$

olarak değerlendirilmiştir.

Genel End-to-End Accuracy:

$$
Accuracy_{E2E}
=
\frac{N_{tam\ doğru}}
{N_{toplam}}
\times100
$$

formülüyle hesaplanmıştır.

---

## 16. Gold Evaluation Deneyinin Çalıştırılması

Evaluation scripti:

    python -m evaluation.day17_gold_eval

komutuyla çalıştırılmıştır.

Toplam:

$$
20
$$

Gold sorgu gerçek Controlled Flow üzerinden değerlendirilmiştir.

---

## 17. Genel Gold Evaluation Sonucu

Toplam sorgu:

$$
N=20
$$

olarak bulunmuştur.

Doğru route:

$$
20/20
$$

Doğru tool:

$$
20/20
$$

Doğru status:

$$
20/20
$$

Doğru kategoriye özel sonuç:

$$
20/20
$$

Tam doğru End-to-End sonuç:

$$
20/20
$$

olarak elde edilmiştir.

---

## 18. Route Accuracy Sonucu

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

olarak elde edilmiştir.

---

## 19. Tool Accuracy Sonucu

Tool Accuracy:

$$
Accuracy_{tool}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{tool}=100\%
$$

olarak bulunmuştur.

---

## 20. Status Accuracy Sonucu

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

olarak elde edilmiştir.

---

## 21. Category-Specific Accuracy Sonucu

Kategoriye özel kontrol sonucu:

$$
20/20
$$

olarak elde edilmiştir.

Category-Specific Accuracy:

$$
Accuracy_{category}
=
\frac{20}{20}\times100
$$

Sonucunda:

$$
Accuracy_{category}=100\%
$$

olarak bulunmuştur.

---

## 22. End-to-End Accuracy Sonucu

Tam doğru akış:

$$
20/20
$$

olarak ölçülmüştür.

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

## 23. Retrieval Sonuçları

Gold Evaluation Set içerisinde:

$$
N_{retrieval}=8
$$

retrieval sorgusu bulunmaktadır.

Doğru Top-1 kaynak sayısı:

$$
8
$$

olarak elde edilmiştir.

Retrieval Top-1 Accuracy:

$$
Accuracy_{Top1}
=
\frac{8}{8}\times100
$$

Sonucunda:

$$
Accuracy_{Top1}=100\%
$$

olarak bulunmuştur.

---

## 24. Retrieval Hit@3 Sonucu

Doğru kaynağın Top-3 içerisinde bulunduğu retrieval sorgu sayısı:

$$
8
$$

olarak elde edilmiştir.

Hit@3:

$$
Hit@3
=
\frac{8}{8}\times100
$$

Sonucunda:

$$
Hit@3=100\%
$$

olarak ölçülmüştür.

---

## 25. Calculator Sonuçları

Calculator kategorisinde:

$$
N_{calculator}=4
$$

sorgu bulunmaktadır.

Doğru matematik sonucu:

$$
4/4
$$

olarak elde edilmiştir.

Calculator Accuracy:

$$
Accuracy_{calculator}
=
\frac{4}{4}\times100
$$

Sonucunda:

$$
Accuracy_{calculator}=100\%
$$

olarak bulunmuştur.

---

## 26. Guardrail Sonuçları

Guardrail kategorisinde:

$$
N_{guardrail}=3
$$

sorgu bulunmaktadır.

Doğru Guardrail Reason:

$$
3/3
$$

olarak elde edilmiştir.

Guardrail Reason Accuracy:

$$
Accuracy_{guardrail-reason}
=
\frac{3}{3}\times100
$$

Sonucunda:

$$
Accuracy_{guardrail-reason}=100\%
$$

olarak bulunmuştur.

---

## 27. Kategori Bazlı End-to-End Sonuçları

Retrieval kategorisi:

$$
8/8
$$

Sonucunda:

$$
Accuracy_{retrieval}=100\%
$$

Calculator kategorisi:

$$
4/4
$$

Sonucunda:

$$
Accuracy_{calculator}=100\%
$$

Out of Scope kategorisi:

$$
3/3
$$

Sonucunda:

$$
Accuracy_{out-of-scope}=100\%
$$

Invalid kategorisi:

$$
2/2
$$

Sonucunda:

$$
Accuracy_{invalid}=100\%
$$

Guardrail kategorisi:

$$
3/3
$$

Sonucunda:

$$
Accuracy_{guardrail}=100\%
$$

olarak elde edilmiştir.

---

## 28. Genel Sonuç Tablosu

| Metrik | Sonuç |
|---|---:|
| Route Accuracy | %100 |
| Tool Accuracy | %100 |
| Status Accuracy | %100 |
| Category-Specific Accuracy | %100 |
| End-to-End Accuracy | %100 |
| Retrieval Top-1 Accuracy | %100 |
| Retrieval Hit@3 | %100 |
| Calculator Accuracy | %100 |
| Guardrail Reason Accuracy | %100 |

---

## 29. Kategori Bazlı Sonuç Tablosu

| Kategori | Doğru | Toplam | Accuracy |
|---|---:|---:|---:|
| Retrieval | 8 | 8 | %100 |
| Calculator | 4 | 4 | %100 |
| Out of Scope | 3 | 3 | %100 |
| Invalid | 2 | 2 | %100 |
| Guardrail | 3 | 3 | %100 |
| **Genel** | **20** | **20** | **%100** |

---

## 30. Hatalı Gold Evaluation Sonuçlarının Kontrolü

Evaluation scripti tam doğru olmayan sorguları ayrıca hata listesine ekleyecek şekilde geliştirilmiştir.

Bu deneyde:

$$
N_{error}=0
$$

olarak elde edilmiştir.

Dolayısıyla:

    HATALI GOLD EVALUATION SONUÇLARI

bölümünde herhangi bir kayıt oluşmamıştır.

---

## 31. Evaluation Sonuçlarının Kalıcı Hale Getirilmesi

Gold Evaluation sonuçlarının yalnızca terminal çıktısında kalmaması amacıyla:

    evaluation/day17_eval_summary.py

dosyası oluşturulmuştur.

Sonuçlar:

    evaluation/day17_eval_results.json

dosyasına JSON formatında kaydedilmiştir.

---

## 32. Evaluation Result JSON İçeriği

JSON sonuç dosyasında:

- Toplam sorgu sayısı
- Genel metrikler
- Retrieval metrikleri
- Calculator metrikleri
- Out of Scope sonuçları
- Invalid sonuçları
- Guardrail sonuçları
- Kategori bazlı End-to-End sonuçlar
- Hata listesi

saklanmaktadır.

Bu yapı daha sonra raporlama veya karşılaştırma işlemlerinde tekrar kullanılabilir hale getirilmiştir.

---

## 33. Sonuç Dosyasının Kontrolü

Evaluation summary scripti:

    python -m evaluation.day17_eval_summary

komutuyla çalıştırılmıştır.

Sonuç:

    Toplam sorgu: 20
    End-to-End Accuracy: %100.00
    Hata sayısı: 0

olarak elde edilmiştir.

Sonuç dosyası:

    evaluation/day17_eval_results.json

olarak oluşturulmuştur.

---

## 34. Gold Evaluation Regression Testlerinin Eklenmesi

Gold Evaluation sonuçlarının ilerleyen geliştirmelerde bozulmasını otomatik olarak tespit etmek amacıyla:

    tests/test_gold_evaluation.py

dosyası oluşturulmuştur.

Toplam:

$$
5
$$

yeni regression testi eklenmiştir.

---

## 35. Route, Tool ve Status Regression Testi

İlk regression testinde 20 Gold kaydın tamamı gerçek Controlled Flow üzerinden çalıştırılmıştır.

Her kayıt için:

$$
Route_{actual}
=
Route_{gold}
$$

$$
Tool_{actual}
=
Tool_{gold}
$$

$$
Status_{actual}
=
Status_{gold}
$$

koşulları kontrol edilmiştir.

---

## 36. Retrieval Gold Regression Testi

Evaluation Set içerisindeki:

$$
8
$$

retrieval sorgusunun tamamı test edilmiştir.

Her sorguda:

$$
Top1\in R_q
$$

koşulu aranmıştır.

Bütün retrieval testleri başarıyla geçmiştir.

---

## 37. Calculator Gold Regression Testi

Evaluation Set içerisindeki:

$$
4
$$

Calculator kaydının tamamında gerçek sonuç Gold sonuç ile karşılaştırılmıştır.

Koşul:

$$
Result_{actual}
=
Result_{gold}
$$

olarak uygulanmıştır.

Bütün Calculator Gold testleri başarılı olmuştur.

---

## 38. Guardrail Gold Regression Testi

Evaluation Set içerisindeki:

$$
3
$$

Guardrail kaydı test edilmiştir.

Kontrol edilen koşullar:

    route = blocked

    selected_tool = none

ve:

$$
Reason_{actual}
=
Reason_{gold}
$$

olarak belirlenmiştir.

Bütün Guardrail Gold testleri başarıyla geçmiştir.

---

## 39. Gold End-to-End Regression Testi

Son regression testinde bütün:

$$
20
$$

Gold Evaluation kaydı tek tek Controlled Flow üzerinden geçirilmiştir.

Bir sorgunun doğru kabul edilmesi için:

$$
RouteCorrect
\land
ToolCorrect
\land
StatusCorrect
\land
CategorySpecificCorrect
$$

koşulu uygulanmıştır.

Tam doğru sorgu:

$$
20
$$

olarak elde edilmiştir.

---

## 40. Genel Regression Test Sonucu

16. gün sonunda:

$$
71
$$

otomatik test bulunmaktaydı.

17. gün:

$$
5
$$

yeni test eklenmiştir.

Toplam:

$$
71+5
$$

Sonucunda:

$$
76
$$

otomatik test olmuştur.

Bütün testler başarılı olmuştur.

Test başarı oranı:

$$
\frac{76}{76}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

---

## 41. Gold Evaluation Set ile Önceki Deneylerin İlişkisi

17. gün Gold Evaluation sonucu, önceki günlerde yapılan deneylerin yerine geçmemektedir.

Örneğin:

- Threshold sınırları
- Embedding hataları
- Routing edge case'leri
- Prompt Injection edge case'leri
- Tool authorization deneyleri

daha geniş hata analizi sağlamaktadır.

Gold Evaluation Set ise sistemin mevcut final konfigürasyonunun kontrollü 20 sorgu üzerindeki uçtan uca davranışını ölçmektedir.

---

## 42. %100 Sonucun Yorumlanması

Gold Evaluation Set üzerinde:

$$
100\%
$$

End-to-End Accuracy elde edilmiştir.

Ancak bu sonuç:

    Sistem bütün gerçek kullanıcı
    sorgularında %100 doğrudur.

anlamına gelmemektedir.

Doğru yorum:

    Hazırlanan 20 soruluk kontrollü
    Gold Evaluation Set üzerinde sistem
    %100 End-to-End Accuracy sağlamıştır.

şeklindedir.

---

## 43. Değerlendirmenin Sınırlılıkları

Gold Evaluation Set yalnızca:

$$
20
$$

sorgudan oluşmaktadır.

Bu nedenle gerçek kullanıcı sorgularının bütün dilsel ve anlamsal çeşitliliğini temsil etmemektedir.

Retrieval değerlendirmesinde yalnızca:

$$
8
$$

sorgu bulunmaktadır.

Guardrail değerlendirmesinde ise:

$$
3
$$

Gold sorgu bulunmaktadır.

Önceki edge-case deneylerinde Guardrail'in başlangıçta bazı Prompt Injection varyasyonlarını kaçırdığı zaten gözlemlenmiştir.

Dolayısıyla kontrollü Gold Set sonucu, daha geniş adversarial veya gerçek kullanıcı testlerinin yerine geçmemektedir.

---

## 44. Evaluation Set Overfitting Riski

Evaluation Set geliştirme sırasında bilinen sorgulardan oluştuğu için sisteme veya kurallara dolaylı biçimde uyum sağlama riski bulunmaktadır.

Bu nedenle ilerleyen gerçek kullanım testlerinde daha önce görülmemiş sorgular kullanılması daha güçlü bir değerlendirme sağlayacaktır.

Gold Evaluation Set'in yeni geliştirmelerde regression kontrolü amacıyla kullanılması uygun görülmüştür.

---

## 45. Sistem Kalitesi Açısından Elde Edilen Sonuç

17. gün değerlendirmesi sonucunda mevcut sistem:

- Doğru route seçebilmiştir.
- Doğru tool seçebilmiştir.
- Doğru status üretebilmiştir.
- Retrieval sorgularında doğru kaynakları getirebilmiştir.
- Calculator sorgularında doğru hesaplama yapabilmiştir.
- Out of Scope sorguları tool çalıştırmadan durdurabilmiştir.
- Invalid sorguları tool çalıştırmadan reddedebilmiştir.
- Guardrail sorgularını doğru nedenle engelleyebilmiştir.

Bu davranışların tamamı hazırlanan Gold Evaluation Set üzerinde birlikte doğrulanmıştır.

---

## 46. Gün Sonunda Elde Edilen Çıktılar

17. gün sonunda:

- `evaluation/day17_gold_eval.py` oluşturulmuştur.
- 20 soruluk Gold Evaluation Set gerçek Controlled Flow üzerinde çalıştırılmıştır.
- Route Accuracy ölçülmüştür.
- Tool Accuracy ölçülmüştür.
- Status Accuracy ölçülmüştür.
- Category-Specific Accuracy ölçülmüştür.
- End-to-End Accuracy ölçülmüştür.
- Retrieval Top-1 Accuracy ölçülmüştür.
- Retrieval Hit@3 ölçülmüştür.
- Calculator Accuracy ölçülmüştür.
- Guardrail Reason Accuracy ölçülmüştür.
- Kategori bazlı End-to-End sonuçlar çıkarılmıştır.
- 20 sorgunun tamamı doğru çalışmıştır.
- Evaluation hata sayısı 0 olarak elde edilmiştir.
- `evaluation/day17_eval_summary.py` oluşturulmuştur.
- `evaluation/day17_eval_results.json` oluşturulmuştur.
- 5 yeni Gold Evaluation regression testi eklenmiştir.
- Proje genelinde 76/76 otomatik test başarılı olmuştur.

---

## 47. Sonuç

17. gün çalışmasında 16. gün hazırlanan 20 soruluk Gold Evaluation Set kullanılarak AI Doküman Asistanının uçtan uca performansı ölçülmüştür.

Toplam Gold sorgu:

$$
N=20
$$

olarak belirlenmiştir.

Doğru route:

$$
20/20
$$

Doğru tool:

$$
20/20
$$

Doğru status:

$$
20/20
$$

Doğru kategoriye özel sonuç:

$$
20/20
$$

Tam doğru End-to-End sonuç:

$$
20/20
$$

olarak elde edilmiştir.

Route Accuracy:

$$
100\%
$$

Tool Accuracy:

$$
100\%
$$

Status Accuracy:

$$
100\%
$$

Category-Specific Accuracy:

$$
100\%
$$

End-to-End Accuracy:

$$
100\%
$$

olarak ölçülmüştür.

Retrieval sorgularında:

$$
8/8
$$

Top-1 sonucu doğru bulunmuştur.

Retrieval Top-1 Accuracy:

$$
100\%
$$

olarak elde edilmiştir.

Doğru kaynak bütün retrieval sorgularında Top-3 içerisinde bulunmuştur.

Retrieval Hit@3:

$$
100\%
$$

olarak ölçülmüştür.

Calculator sorgularında:

$$
4/4
$$

doğru sonuç üretilmiştir.

Calculator Accuracy:

$$
100\%
$$

olarak bulunmuştur.

Guardrail sorgularında:

$$
3/3
$$

doğru reason üretilmiştir.

Guardrail Reason Accuracy:

$$
100\%
$$

olarak elde edilmiştir.

Kategori bazında Retrieval, Calculator, Out of Scope, Invalid ve Guardrail gruplarının tamamında:

$$
100\%
$$

End-to-End Accuracy elde edilmiştir.

Evaluation sırasında:

$$
0
$$

hatalı Gold sonucu gözlemlenmiştir.

Sonuçlar:

    evaluation/day17_eval_results.json

dosyasına kaydedilmiştir.

Gold Evaluation davranışlarını korumak amacıyla beş yeni regression testi eklenmiştir.

Proje genelinde:

$$
76/76
$$

otomatik test başarılı olmuştur.

Test başarı oranı:

$$
\frac{76}{76}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

17. gün sonunda AI Doküman Asistanının mevcut kontrollü sistem konfigürasyonu 20 soruluk Gold Evaluation Set üzerinde uçtan uca doğrulanmıştır.

Elde edilen %100 başarı oranlarının yalnızca mevcut doküman koleksiyonu ve kontrollü Evaluation Set kapsamında geçerli olduğu, gerçek kullanıcı sorgularının tamamı için %100 başarı garantisi anlamına gelmediği değerlendirilmiştir.