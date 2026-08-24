# 3. Gün – Temel Yapay Zekâ Kavramları

## 1. LLM Nedir?

LLM, Large Language Model yani Büyük Dil Modeli anlamına gelir.
Çok miktarda metin üzerinde eğitilmiş ve verilen metne göre uygun
devamı üretebilen yapay zekâ modelidir.

LLM, metni doğrudan kelimeler hâlinde değil, token adı verilen küçük
birimler hâlinde işler. Model, kendisine verilen bağlama göre sıradaki
uygun tokenı tahmin ederek cevap oluşturur.

### Projedeki karşılığı

AI Doküman Asistanı projesinde LLM, kullanıcının sorusu ile
dokümanlardan getirilen ilgili bilgileri kullanarak kısa ve anlaşılır
bir cevap oluşturmak için kullanılacaktır.

Modelin kendi bilgisinden kesin cevap üretmesi yerine yalnızca verilen
doküman bağlamına bağlı kalması sağlanacaktır.

---

## 2. Prompt Nedir?

Prompt, yapay zekâ modeline verilen talimat, soru ve bağlamın tamamıdır.

İyi hazırlanmış bir prompt:

- Modelin görevini açıklar.
- Kullanması gereken bağlamı belirtir.
- Cevabın biçimini tanımlar.
- Kaynakta olmayan bilgilerin üretilmesini engeller.
- Cevabın kısa ve anlaşılır olmasını sağlar.

### Projedeki karşılığı

Kullanıcı sorusu ve retrieval sonucunda bulunan doküman parçaları
bir prompt içerisinde modele gönderilecektir.

Örnek:

Görev:
Yalnızca verilen teknik doküman bağlamını kullanarak cevap ver.

Bağlam:
Uygulamayı çalıştırmak için gerekli paketler requirements.txt
dosyasından yüklenmelidir.

Soru:
Uygulamayı çalıştırmadan önce ne yapılmalıdır?

Kurallar:
- Bağlamda bulunmayan bilgi üretme.
- Kısa cevap ver.
- Kullanılan kaynağı belirt.
- Yeterli bilgi yoksa bunu açıkça söyle.

---

## 3. Token Nedir?

Token, yapay zekâ modelinin metni işlerken kullandığı küçük metin
birimidir.

Bir token:

- Tam bir kelime,
- Kelimenin bir bölümü,
- Noktalama işareti,
- Sayı veya karakter grubu

olabilir.

Token sayısı her zaman kelime sayısına eşit değildir.

### Projedeki karşılığı

Sistem talimatı, kullanıcı sorusu, bulunan doküman parçaları ve
oluşturulacak cevap modelin bağlam alanını kullanır.

Doküman parçalarının çok uzun olması gereksiz token kullanımına,
çok kısa olması ise bilgi ve bağlam kaybına neden olabilir.

---

## 4. Context Nedir?

Context, modelin cevap oluştururken görebildiği bütün bilgidir.

Projede context şu bölümlerden oluşacaktır:

- Sistem talimatı
- Kullanıcı sorusu
- Retrieval sonucunda bulunan doküman parçaları
- Kaynak bilgileri
- Gerekli cevap biçimi

Modelin üreteceği cevabın güvenilir olması için doğru ve yeterli
doküman parçalarının context içerisine eklenmesi gerekir.

---

## 5. Embedding Nedir?

Embedding, metinleri bilgisayar tarafından karşılaştırılabilir sayısal
vektörlere dönüştüren bir temsil yöntemidir.

Anlam bakımından birbirine yakın metinlerin embedding vektörlerinin de
birbirine yakın olması beklenir.

Örneğin:

- "Servis nasıl çalıştırılır?"
- "Uygulama nasıl başlatılır?"

ifadeleri farklı kelimeler kullansa da anlamsal olarak benzerdir.
Embedding yöntemi bu benzerliği yakalamaya yardımcı olabilir.

### Projedeki karşılığı

Kullanıcının sorusu ve doküman parçaları embedding vektörlerine
dönüştürülecektir. Vektörler arasındaki benzerlik hesaplanarak soruya
en yakın doküman parçaları bulunacaktır.

---

## 6. Kavramların Proje Akışındaki Yeri

1. Kullanıcı bir soru girer.
2. Soru tokenlara ayrılarak işlenir.
3. Soru ve dokümanlar sayısal olarak temsil edilir.
4. En ilgili doküman parçaları retrieval ile bulunur.
5. Bulunan parçalar context olarak prompt içerisine eklenir.
6. LLM yalnızca bu bağlama göre cevap oluşturur.
7. Cevapla birlikte kaynak bilgileri gösterilir.

## 7. Token Kullanımının Matematiksel Temeli

Modele gönderilen toplam token miktarı aşağıdaki şekilde gösterilebilir:

T_toplam = T_sistem + T_soru + T_bağlam + T_cevap

Burada:

- T_sistem: Modelin görev ve kurallarını içeren sistem talimatı
- T_soru: Kullanıcının sorusundaki token sayısı
- T_bağlam: Getirilen doküman parçalarının token sayısı
- T_cevap: Modelin oluşturacağı cevap için ayrılan token sayısı

Örnek:

- Sistem talimatı: 100 token
- Kullanıcı sorusu: 20 token
- Üç doküman parçası: 600 token
- Cevap için ayrılan alan: 200 token

T_toplam = 100 + 20 + 600 + 200

T_toplam = 920 token

Bu nedenle retrieval sonucunda gereğinden fazla veya çok uzun doküman
parçalarının modele gönderilmesi verimsiz olabilir.

## 8. Embedding Vektörlerinin Matematiksel Gösterimi

Bir metnin embedding işlemi sonucunda d boyutlu bir vektör elde edilir:

E(metin) = [x1, x2, x3, ..., xd]

Burada:

- E: Embedding fonksiyonu
- d: Vektör boyutu
- x1, x2, ..., xd: Metnin sayısal özellikleri

Örnek olarak kullanıcı sorusunun vektörü:

q = [0.20, 0.40, -0.10]

Bir doküman parçasının vektörü:

d1 = [0.18, 0.38, -0.12]

şeklinde olabilir.

Bu iki vektör birbirine yakınsa soru ile doküman parçasının anlamsal
olarak ilişkili olduğu kabul edilir.

Vektörlerin benzerliği ilerleyen günlerde cosine similarity yöntemiyle
hesaplanacaktır.