# Day 14 - Kontrollü Tool Çağrıları ve Decision Trace

## Amaç

14. gün çalışmasında, 13. gün geliştirilen Query Routing ve Decision Flow yapısı kontrollü tool çağrıları ile genişletilmiştir.

Bir önceki aşamada sistem kullanıcı sorgusunu:

- INVALID
- CALCULATOR
- RETRIEVAL
- OUT_OF_SCOPE

sınıflarından birine yönlendirebiliyordu.

14. gün çalışmasında bu kararların ardından hangi tool'un çalıştırılabileceğinin kontrollü biçimde belirlenmesi amaçlanmıştır.

Ayrıca sistemin aldığı kararların izlenebilir olması amacıyla Decision Trace ve JSONL tabanlı loglama mekanizması geliştirilmiştir.

Genel yapı:

Kullanıcı Sorgusu

↓

Query Router

↓

Tool Selection

↓

Tool Authorization

↓

Controlled Tool Execution

↓

Decision Trace

↓

JSONL Log

şeklinde oluşturulmuştur.

---

## 1. Tool Registry Yapısının Oluşturulması

Tool seçimini merkezi ve kontrollü hale getirmek amacıyla:

    src/tool_registry.py

dosyası oluşturulmuştur.

Sistemde kullanılabilecek araçlar:

    NONE
    CALCULATOR
    RETRIEVER

olarak tanımlanmıştır.

Tool sınıfı:

    class ToolName(str, Enum):
        NONE = "none"
        CALCULATOR = "calculator"
        RETRIEVER = "retriever"

şeklinde oluşturulmuştur.

---

## 2. Route ve Tool Eşleşmesinin Belirlenmesi

Her Query Route için çalışmasına izin verilen tool belirlenmiştir.

Eşleşme aşağıdaki şekilde oluşturulmuştur:

| Route | İzin Verilen Tool |
|---|---|
| CALCULATOR | CALCULATOR |
| RETRIEVAL | RETRIEVER |
| INVALID | NONE |
| OUT_OF_SCOPE | NONE |

Bu yapı sayesinde matematik sorgularında Retriever Tool'un, doküman sorgularında ise Calculator Tool'un yanlışlıkla çalıştırılmasının önüne geçilmesi amaçlanmıştır.

---

## 3. Tool Selection Fonksiyonunun Geliştirilmesi

`select_tool()` fonksiyonu Query Router tarafından belirlenen route değerine göre kullanılacak tool'u seçmektedir.

Örneğin:

    Route = CALCULATOR

olduğunda:

    Tool = CALCULATOR

seçilmektedir.

Benzer şekilde:

    Route = RETRIEVAL

olduğunda:

    Tool = RETRIEVER

olarak belirlenmektedir.

INVALID ve OUT_OF_SCOPE durumlarında:

    Tool = NONE

seçilmektedir.

Bu sorgular için gerçek bir tool çağrısı yapılmamaktadır.

---

## 4. İlk Tool Registry Kontrolü

Tool Registry aşağıdaki route değerleriyle kontrol edilmiştir:

    CALCULATOR
    RETRIEVAL
    OUT_OF_SCOPE
    INVALID

Elde edilen sonuç:

    ToolName.CALCULATOR
    ToolName.RETRIEVER
    ToolName.NONE
    ToolName.NONE

olmuştur.

Bu sonuç route-tool eşleşmesinin doğru çalıştığını göstermiştir.

---

## 5. Tool Executor Yapısının Oluşturulması

Tool seçiminin ardından aracın gerçekten kontrollü şekilde çalıştırılmasını sağlamak amacıyla:

    src/tool_executor.py

dosyası oluşturulmuştur.

Tool Executor'ın temel amacı yalnızca route tarafından izin verilen aracın çalışmasına izin vermektir.

Akış:

Route

↓

Tool

↓

Authorization Check

↓

Allowed / Blocked

şeklinde oluşturulmuştur.

---

## 6. Tool Yetkilendirme Kontrolü

`is_tool_allowed()` fonksiyonu ile seçilen tool'un mevcut route için izin verilen tool olup olmadığı kontrol edilmiştir.

Eğer:

    seçilen tool = izin verilen tool

ise işlem devam etmektedir.

Ancak eşleşme yoksa:

    status = blocked

sonucu üretilmektedir.

Bu yapı, kontrollü tool çağrılarının temel güvenlik katmanı olarak kullanılmıştır.

---

## 7. Yetkisiz Retriever Çağrısının Engellenmesi

İlk güvenlik testinde matematik sorgusu için Retriever Tool zorla çağrılmaya çalışılmıştır.

Route:

    calculator

Zorlanan Tool:

    retriever

olarak belirlenmiştir.

Sonuç:

    status: blocked

olarak elde edilmiştir.

Bu test sonucunda Calculator route'u altında Retriever Tool'un çalıştırılmasının engellendiği doğrulanmıştır.

---

## 8. Doğru Calculator Tool Çağrısının Kontrolü

Calculator route'u ve Calculator Tool birlikte kullanılmıştır.

Sorgu:

    5 + 5 kaç?

olarak verilmiştir.

Sistem:

    Route: calculator
    Tool: calculator
    Status: success

sonucunu üretmiştir.

Hesaplama sonucu:

$$
5+5
$$

Sonucunda:

$$
10
$$

olarak elde edilmiştir.

---

## 9. Doğru Retriever Tool Çağrısının Kontrolü

Teknik doküman sorgusunda Retriever Tool kontrollü şekilde çalıştırılmıştır.

Sorgu:

    Python nasıl kurulur?

olarak verilmiştir.

Sonuç:

    Route: retrieval
    Tool: retriever
    Status: success

olarak elde edilmiştir.

Top-1 kaynak:

    python_kurulumu.md

olmuştur.

Top-1 similarity skoru yaklaşık:

$$
s=0.4813
$$

olarak ölçülmüştür.

Böylece doğru route-tool eşleşmesinde retrieval işleminin başarıyla çalıştığı doğrulanmıştır.

---

## 10. Controlled Flow Yapısının Oluşturulması

Routing, Tool Selection ve Tool Execution işlemlerini tek bir kontrollü akış içerisinde birleştirmek amacıyla:

    src/controlled_flow.py

dosyası oluşturulmuştur.

Genel akış:

Query

↓

Route

↓

Tool Selection

↓

Tool Execution

↓

Trace

şeklinde oluşturulmuştur.

Bu yapı sayesinde kullanıcı sorgusunun hangi karar adımlarından geçtiği merkezi olarak yönetilmeye başlanmıştır.

---

## 11. Decision Trace Yapısının Eklenmesi

Sistemin aldığı kararların sonradan incelenebilmesi amacıyla Decision Trace yapısı oluşturulmuştur.

Her sorgu için aşağıdaki bilgiler trace içerisinde tutulmaktadır:

- timestamp
- query
- route
- selected_tool
- tool_status
- message
- result
- result_count
- top_source
- top_score

Bu yapı sayesinde yalnızca sistem çıktısı değil, sistemin hangi route ve tool kararlarını verdiği de kayıt altına alınmıştır.

---

## 12. Calculator Decision Trace Kontrolü

Calculator sorgusu:

    5 + 5 kaç?

kontrollü akıştan geçirilmiştir.

Trace içerisinde:

    query: 5 + 5 kaç?
    route: calculator
    selected_tool: calculator
    tool_status: success
    result: 10
    result_count: 0
    top_source: None
    top_score: None

bilgilerinin bulunduğu görülmüştür.

Bu sonuç Calculator Tool çağrısının izlenebilir hale geldiğini göstermiştir.

---

## 13. Retrieval Trace Kontrolü

Sorgu:

    Python nasıl kurulur?

için oluşturulan trace içerisinde:

    route: retrieval
    selected_tool: retriever
    tool_status: success

bilgileri bulunmuştur.

Ayrıca:

    top_source: python_kurulumu.md

ve yaklaşık:

$$
top\_score=0.4813
$$

bilgileri kayıt altına alınmıştır.

Bu sayede retrieval işleminin hangi kaynağı hangi skorla getirdiğinin izlenebilir olması sağlanmıştır.

---

## 14. OUT_OF_SCOPE Trace Kontrolü

Sorgu:

    Türkiye nin başkenti nedir?

için:

    route: out_of_scope
    selected_tool: none
    tool_status: not_executed

sonucu elde edilmiştir.

Bu sorguda gerçek bir tool çağrısı yapılmamıştır.

Ancak verilen karar Decision Trace içerisinde kayıt altına alınmıştır.

Bu davranış sayesinde tool çalıştırılmayan kararların da izlenebilir olması sağlanmıştır.

---

## 15. INVALID Trace Kontrolü

Geçersiz sorgu:

    !!!

için:

    route: invalid
    selected_tool: none
    tool_status: not_executed

sonucu elde edilmiştir.

Bu sorgu da herhangi bir araca gönderilmemiş, ancak sistem kararı trace içerisinde tutulmuştur.

---

## 16. JSONL Trace Logger Yapısının Oluşturulması

Decision Trace kayıtlarının kalıcı olarak saklanması amacıyla:

    src/trace_logger.py

dosyası oluşturulmuştur.

Varsayılan log dosyası:

    logs/decision_trace.jsonl

olarak belirlenmiştir.

Trace kayıtları JSONL formatında saklanmaktadır.

---

## 17. JSONL Formatının Kullanılması

JSONL formatında her satır bağımsız bir JSON kaydıdır.

Örnek:

    {"query":"5 + 5 kaç?","route":"calculator",...}
    {"query":"Python nasıl kurulur?","route":"retrieval",...}
    {"query":"!!!","route":"invalid",...}

Bu yapı sayesinde her yeni kayıt dosyanın sonuna eklenebilmektedir.

Birinci trace:

$$
Trace_1\rightarrow Satır_1
$$

İkinci trace:

$$
Trace_2\rightarrow Satır_2
$$

Üçüncü trace:

$$
Trace_3\rightarrow Satır_3
$$

şeklinde saklanmaktadır.

Bu nedenle bütün log dosyasının her işlemde yeniden yazılması gerekmemektedir.

---

## 18. Trace Kayıtlarının Kalıcı Hale Getirilmesi

`run_controlled_flow()` fonksiyonuna `save_trace()` işlemi eklenmiştir.

Böylece her kontrollü flow çağrısından sonra oluşan Decision Trace otomatik olarak:

    logs/decision_trace.jsonl

dosyasına eklenmektedir.

Bu yapı sistem kararlarının çalışma sonrasında incelenebilmesini sağlamaktadır.

---

## 19. UTF-8 Loglama Kontrolü

Trace kayıtlarında Türkçe karakterler bulunduğu için dosya UTF-8 formatında açılmaktadır.

Loglama sırasında:

    encoding="utf-8"

kullanılmıştır.

PowerShell üzerinde dosya içeriği kontrol edilirken:

    Get-Content .\logs\decision_trace.jsonl -Encoding utf8

komutu kullanılmıştır.

Bu şekilde Türkçe karakterlerin doğru görüntülendiği doğrulanmıştır.

---

## 20. Otomatik Tool Control Testlerinin Eklenmesi

Tool Registry, Tool Executor, Controlled Flow ve Trace Logger davranışlarını kontrol etmek amacıyla:

    tests/test_tool_control.py

dosyası oluşturulmuştur.

Toplam:

$$
8
$$

yeni test eklenmiştir.

Kontrol edilen başlıca davranışlar:

- Calculator route'unun Calculator Tool seçmesi
- Retrieval route'unun Retriever Tool seçmesi
- INVALID route'unun NONE seçmesi
- OUT_OF_SCOPE route'unun NONE seçmesi
- Yetkisiz tool çağrısının engellenmesi
- Calculator Tool'un doğru çalışması
- Retriever Tool'un doğru çalışması
- Trace Logger'ın JSONL yazma ve okuma işlemi
- Controlled Flow içerisinde trace bilgilerinin doğru oluşturulması

olmuştur.

---

## 21. Regression Test Sonuçları

13. gün sonunda proje genelinde:

$$
47
$$

otomatik test bulunmaktaydı.

14. gün:

$$
8
$$

yeni test eklenmiştir.

Toplam test sayısı:

$$
47+8
$$

Sonucunda:

$$
55
$$

olmuştur.

Bütün testlerin başarılı olduğu görülmüştür.

Test başarı oranı:

$$
\frac{55}{55}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

---

## 22. Kontrollü Tool-Call Deneyinin Tasarlanması

14. günün final deneyinde Controlled Flow yapısının uçtan uca davranışı değerlendirilmiştir.

Toplam:

$$
N=16
$$

normal kullanıcı sorgusu kullanılmıştır.

Sorgular dört gruba ayrılmıştır:

- Calculator
- Retrieval
- Out of Scope
- Invalid

Her grupta:

$$
4
$$

sorgu bulunmaktadır.

Toplam:

$$
N=4+4+4+4
$$

Sonucunda:

$$
N=16
$$

olmuştur.

---

## 23. Kontrollü Flow İçin Ölçülen Metrikler

Deneyde aşağıdaki metrikler ölçülmüştür:

- Route Accuracy
- Tool Selection Accuracy
- Tool Status Accuracy
- Trace Completeness
- End-to-End Controlled Flow Accuracy

Route Accuracy:

$$
Accuracy_{route}
=
\frac{N_{\text{doğru route}}}
{N_{\text{toplam sorgu}}}
\times100
$$

Tool Selection Accuracy:

$$
Accuracy_{tool}
=
\frac{N_{\text{doğru tool}}}
{N_{\text{toplam sorgu}}}
\times100
$$

Trace Completeness:

$$
Trace\ Completeness
=
\frac{N_{\text{eksiksiz trace}}}
{N_{\text{toplam sorgu}}}
\times100
$$

olarak değerlendirilmiştir.

---

## 24. Controlled Flow Genel Sonuçları

Toplam sorgu:

$$
16
$$

olarak belirlenmiştir.

Doğru route:

$$
16/16
$$

Doğru tool seçimi:

$$
16/16
$$

Doğru tool status:

$$
16/16
$$

Eksiksiz trace:

$$
16/16
$$

Tam doğru akış:

$$
16/16
$$

olarak elde edilmiştir.

---

## 25. Route Accuracy Sonucu

Route Accuracy:

$$
Accuracy_{route}
=
\frac{16}{16}\times100
$$

Sonucunda:

$$
Accuracy_{route}=100\%
$$

olarak elde edilmiştir.

---

## 26. Tool Selection Accuracy Sonucu

Tool Selection Accuracy:

$$
Accuracy_{tool}
=
\frac{16}{16}\times100
$$

Sonucunda:

$$
Accuracy_{tool}=100\%
$$

olarak bulunmuştur.

Bu sonuç kontrollü test setinde bütün sorgular için doğru tool'un seçildiğini göstermiştir.

---

## 27. Tool Status Accuracy Sonucu

Doğru tool status sayısı:

$$
16/16
$$

olarak elde edilmiştir.

Tool Status Accuracy:

$$
Accuracy_{status}
=
\frac{16}{16}\times100
$$

Sonucunda:

$$
Accuracy_{status}=100\%
$$

olarak bulunmuştur.

---

## 28. Trace Completeness Sonucu

Bütün sorgular için gerekli Decision Trace alanlarının oluşturulduğu görülmüştür.

Eksiksiz trace:

$$
16/16
$$

olarak elde edilmiştir.

Trace Completeness:

$$
\frac{16}{16}\times100
$$

Sonucunda:

$$
Trace\ Completeness=100\%
$$

olarak ölçülmüştür.

---

## 29. End-to-End Controlled Flow Sonucu

Bir sorgunun tam doğru kabul edilmesi için:

- Route doğru olmalı
- Tool doğru seçilmeli
- Tool Status doğru olmalı
- Trace eksiksiz olmalı

şartları birlikte aranmıştır.

Tam doğru akış:

$$
16/16
$$

olarak elde edilmiştir.

End-to-End Controlled Flow Accuracy:

$$
Accuracy_{E2E}
=
\frac{16}{16}\times100
$$

Sonucunda:

$$
Accuracy_{E2E}=100\%
$$

olarak elde edilmiştir.

---

## 30. Yetkisiz Tool Çağrısı Deneyinin Tasarlanması

Sistemin yalnızca doğru tool çağrılarını gerçekleştirmesi yeterli görülmemiştir.

Yanlış veya yetkisiz tool çağrılarının da engellenmesi test edilmiştir.

Toplam:

$$
4
$$

yetkisiz tool çağrısı hazırlanmıştır.

Test senaryoları:

1. CALCULATOR route altında RETRIEVER çağrısı
2. RETRIEVAL route altında CALCULATOR çağrısı
3. OUT_OF_SCOPE route altında RETRIEVER çağrısı
4. INVALID route altında CALCULATOR çağrısı

olarak belirlenmiştir.

---

## 31. Yetkisiz Calculator-Route Retriever Çağrısı

Route:

    calculator

iken zorlanan tool:

    retriever

olmuştur.

Sonuç:

    status: blocked

olarak elde edilmiştir.

Bu çağrının çalıştırılması engellenmiştir.

---

## 32. Yetkisiz Retrieval-Route Calculator Çağrısı

Route:

    retrieval

iken zorlanan tool:

    calculator

olmuştur.

Sonuç:

    status: blocked

olarak elde edilmiştir.

Bu çağrı da başarıyla engellenmiştir.

---

## 33. OUT_OF_SCOPE Route Üzerinde Tool Çağrısının Engellenmesi

Route:

    out_of_scope

iken Retriever Tool zorla çağrılmaya çalışılmıştır.

Sonuç:

    status: blocked

olarak elde edilmiştir.

Bu sonuç kapsam dışı sorguların retrieval sistemine zorla gönderilemediğini göstermiştir.

---

## 34. INVALID Route Üzerinde Tool Çağrısının Engellenmesi

Route:

    invalid

iken Calculator Tool çalıştırılmaya çalışılmıştır.

Sonuç:

    status: blocked

olarak elde edilmiştir.

Geçersiz sorgularda tool çağrısının yapılamadığı doğrulanmıştır.

---

## 35. Tool Block Rate Sonucu

Toplam yetkisiz çağrı:

$$
N_{\text{yetkisiz}}=4
$$

olarak belirlenmiştir.

Engellenen çağrı:

$$
N_{\text{engellenen}}=4
$$

olmuştur.

Tool Block Rate:

$$
Block\ Rate
=
\frac{N_{\text{engellenen}}}
{N_{\text{yetkisiz}}}
\times100
$$

Gerçek değerler kullanıldığında:

$$
Block\ Rate
=
\frac{4}{4}\times100
$$

Sonucunda:

$$
Block\ Rate=100\%
$$

olarak elde edilmiştir.

---

## 36. Gün Sonunda Oluşan Kontrollü Akış

14. gün sonunda sistemin genel karar yapısı:

    Kullanıcı Sorgusu
            |
            v
       Query Router
            |
            v
       Route Kararı
            |
            v
       Tool Registry
            |
            v
       Tool Selection
            |
            v
       Authorization
         /       \
    Allowed      Blocked
       |            |
       v            v
    Tool          İşlem
   Execution     Engellenir
       |
       v
   Tool Status
       |
       v
 Decision Trace
       |
       v
 JSONL Logger

şeklinde oluşturulmuştur.

---

## 37. Traceability Açısından Kazanımlar

Yeni yapı sayesinde bir sorgu sonrasında aşağıdaki sorular cevaplanabilir hale gelmiştir:

- Kullanıcı hangi sorguyu gönderdi?
- Hangi route seçildi?
- Hangi tool seçildi?
- Tool gerçekten çalıştırıldı mı?
- Tool sonucu başarılı mıydı?
- Retrieval yapıldıysa kaç sonuç bulundu?
- Top-1 kaynak hangisiydi?
- Top-1 similarity skoru neydi?
- Karar hangi zamanda verildi?

Bu yapı sistem davranışlarının daha sonra analiz edilmesini kolaylaştırmaktadır.

---

## 38. Kontrollü Tool Çağrılarının Önemi

Query Router'ın doğru tool'u seçmesi tek başına yeterli değildir.

Tool execution katmanında ayrıca izin kontrolü yapılmadığında başka bir kod parçası veya yanlış bir karar sonucu farklı bir tool çalıştırılabilir.

Bu nedenle:

$$
Routing\ Decision
\neq
Tool\ Authorization
$$

olarak değerlendirilmiştir.

Routing hangi tool'un kullanılması gerektiğine karar vermektedir.

Tool Authorization ise seçilen tool'un gerçekten çalıştırılmasına izin verilip verilmediğini kontrol etmektedir.

Bu iki katmanın ayrılması sistemin kontrollü çalışmasını güçlendirmiştir.

---

## 39. Deneyin Sınırlılıkları

14. gün Controlled Flow deneyinde:

$$
16
$$

normal sorgu kullanılmıştır.

Yetkisiz tool çağrısı deneyinde:

$$
4
$$

senaryo test edilmiştir.

Bu nedenle elde edilen:

$$
100\%
$$

başarı oranları bütün gerçek kullanıcı sorguları ve bütün olası saldırı veya yanlış kullanım biçimleri için garanti olarak değerlendirilmemelidir.

Tool Registry şu anda yalnızca:

- Calculator
- Retriever

olmak üzere iki gerçek tool içermektedir.

Sistem büyüdükçe yeni araçların:

- izin kuralları
- giriş parametreleri
- hata davranışları
- loglama alanları

ayrıca tasarlanmalıdır.

JSONL log dosyasının büyümesi durumunda log rotasyonu veya merkezi loglama gibi mekanizmalar gerekebilir.

---

## 40. Gün Sonunda Elde Edilen Çıktılar

14. gün sonunda:

- `src/tool_registry.py` oluşturulmuştur.
- Tool isimleri merkezi olarak tanımlanmıştır.
- Route-tool eşleşmesi oluşturulmuştur.
- INVALID için `NONE` tool kullanılmıştır.
- OUT_OF_SCOPE için `NONE` tool kullanılmıştır.
- `src/tool_executor.py` oluşturulmuştur.
- Tool authorization kontrolü eklenmiştir.
- Yetkisiz tool çağrılarında `blocked` davranışı eklenmiştir.
- Calculator Tool kontrollü executor üzerinden çalıştırılmıştır.
- Retriever Tool kontrollü executor üzerinden çalıştırılmıştır.
- `src/controlled_flow.py` oluşturulmuştur.
- Query Router, Tool Registry ve Tool Executor tek akışta birleştirilmiştir.
- Decision Trace yapısı oluşturulmuştur.
- Timestamp kaydı eklenmiştir.
- Route bilgisi trace'e eklenmiştir.
- Tool bilgisi trace'e eklenmiştir.
- Tool status bilgisi trace'e eklenmiştir.
- Retrieval Top-1 kaynak ve skor bilgisi trace'e eklenmiştir.
- `src/trace_logger.py` oluşturulmuştur.
- JSONL tabanlı kalıcı loglama eklenmiştir.
- UTF-8 loglama kontrol edilmiştir.
- 8 yeni otomatik test eklenmiştir.
- Proje genelinde 55/55 test başarılı olmuştur.
- 16 sorguluk Controlled Flow deneyi gerçekleştirilmiştir.
- Route Accuracy %100 elde edilmiştir.
- Tool Selection Accuracy %100 elde edilmiştir.
- Tool Status Accuracy %100 elde edilmiştir.
- Trace Completeness %100 elde edilmiştir.
- End-to-End Controlled Flow Accuracy %100 elde edilmiştir.
- 4 yetkisiz tool çağrısı test edilmiştir.
- 4 çağrının tamamı engellenmiştir.
- Tool Block Rate %100 olarak elde edilmiştir.

---

## 41. Sonuç

14. gün çalışmasında AI Doküman Asistanının kontrollü tool çağrı altyapısı geliştirilmiştir.

Öncelikle Query Route değerlerini kullanılabilecek tool'larla eşleştirmek amacıyla Tool Registry oluşturulmuştur.

Calculator sorguları:

    Calculator Tool

ile eşleştirilmiştir.

Doküman sorguları:

    Retriever Tool

ile eşleştirilmiştir.

INVALID ve OUT_OF_SCOPE sorgularında:

    Tool = NONE

kullanılmıştır.

Tool Executor katmanı ile seçilen aracın mevcut route için çalıştırılmasına izin verilip verilmediği ayrıca kontrol edilmiştir.

Yanlış tool çağrılarında:

    status = blocked

davranışı uygulanmıştır.

Sistemin aldığı kararların izlenebilmesi amacıyla Decision Trace yapısı oluşturulmuştur.

Trace içerisinde:

- query
- timestamp
- route
- selected_tool
- tool_status
- result
- result_count
- top_source
- top_score

alanları tutulmuştur.

Trace kayıtları:

    logs/decision_trace.jsonl

dosyasına JSONL formatında kalıcı olarak kaydedilmeye başlanmıştır.

14. gün sonunda 8 yeni otomatik test eklenmiş ve proje genelinde:

$$
55/55
$$

test başarılı olmuştur.

Test başarı oranı:

$$
\frac{55}{55}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

Final Controlled Flow deneyinde toplam:

$$
16
$$

sorgu değerlendirilmiştir.

Doğru route:

$$
16/16
$$

Doğru tool:

$$
16/16
$$

Doğru tool status:

$$
16/16
$$

Eksiksiz trace:

$$
16/16
$$

Tam doğru controlled flow:

$$
16/16
$$

olarak elde edilmiştir.

Buna göre:

$$
Route\ Accuracy=100\%
$$

$$
Tool\ Selection\ Accuracy=100\%
$$

$$
Tool\ Status\ Accuracy=100\%
$$

$$
Trace\ Completeness=100\%
$$

$$
End-to-End\ Controlled\ Flow\ Accuracy=100\%
$$

sonuçları elde edilmiştir.

Yetkisiz tool çağrısı deneyinde toplam:

$$
4
$$

çağrı gerçekleştirilmiştir.

Bu çağrıların:

$$
4/4
$$

tanesi engellenmiştir.

Tool Block Rate:

$$
\frac{4}{4}\times100
$$

Sonucunda:

$$
100\%
$$

olarak elde edilmiştir.

14. gün sonunda sistem yalnızca kullanıcı sorgusu için uygun aracı seçmekle kalmamakta, seçilen aracın gerçekten o route için yetkili olup olmadığını kontrol etmekte ve bütün karar sürecini izlenebilir şekilde loglamaktadır.

Böylece 13–14. günler için planlanan Query Routing, Decision Flow ve kontrollü tool çağrıları aşaması tamamlanmıştır.