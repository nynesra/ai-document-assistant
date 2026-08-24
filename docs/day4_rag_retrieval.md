# 4. Gün – Retrieval ve RAG Akışı

## 1. Retrieval Nedir?

Retrieval, kullanıcının sorusuyla ilgili bilgilerin bir bilgi tabanından
veya doküman koleksiyonundan bulunması işlemidir.

AI Doküman Asistanı projesinde retrieval sistemi:

1. Kullanıcının sorusunu alır.
2. Doküman veya bilgi kayıtlarını inceler.
3. Soruyla en ilgili bilgileri belirler.
4. Bulunan bilgileri kaynaklarıyla birlikte döndürür.

Bu aşamada retrieval işlemi basit anahtar kelime eşleşmesi kullanılarak
gerçekleştirilecektir. Daha sonraki aşamalarda TF-IDF, cosine similarity
ve embedding yöntemleri kullanılacaktır.

## 2. Generation Nedir?

Generation, retrieval sonucunda bulunan bilgilerin kullanılarak kullanıcıya
anlaşılır bir cevap oluşturulmasıdır.

Bu projede generation aşaması, bulunan teknik bilgiye bağlı kısa bir cevap
hazırlanmasını ve kullanılan kaynağın gösterilmesini kapsar.

## 3. RAG Nedir?

RAG, Retrieval-Augmented Generation ifadesinin kısaltmasıdır.

RAG iki temel aşamayı birleştirir:

1. Retrieval: Kullanıcı sorusuyla ilgili bilgiyi dokümanlardan bulma
2. Generation: Bulunan bilgiyi kullanarak cevap oluşturma

Projedeki temel RAG akışı:

Kullanıcı sorusu
→ İlgili bilgiyi arama
→ En uygun kaydı bulma
→ Bulunan bilgiyi bağlam olarak kullanma
→ Kaynaklı cevap oluşturma

## 4. Güvenli Ret Davranışı

Sistem, kullanıcının sorusuyla ilgili yeterli bilgi bulamazsa cevap
uydurmamalıdır.

Bu durumda aşağıdaki gibi bir mesaj verilmelidir:

"Bu soruyu cevaplamak için bilgi tabanında yeterli kaynak bulunamadı."

Bu davranış, sistemin güvenilirliğini artırır ve yanlış bilgi üretmesini
azaltır.

## 5. Basit Prototipin Çalışma Mantığı

Dördüncü günde hazırlanacak prototip şu şekilde çalışacaktır:

1. Kullanıcı terminalden bir soru girer.
2. Soru küçük harflere dönüştürülür.
3. Noktalama işaretleri temizlenir.
4. Soru anlamlı kelimelere ayrılır.
5. Soru kelimeleri bilgi tabanındaki anahtar kelimelerle karşılaştırılır.
6. Her bilgi kaydı için bir eşleşme skoru hesaplanır.
7. En yüksek skora sahip kayıt seçilir.
8. Skor belirlenen eşikten yüksekse cevap ve kaynak gösterilir.
9. Skor düşükse güvenli ret mesajı verilir.

## 6. Prototipin Sınırlılıkları

Bu prototip tam bir RAG sistemi değildir.

Henüz:

- Gerçek doküman dosyaları okunmamaktadır.
- TF-IDF kullanılmamaktadır.
- Cosine similarity hesaplanmamaktadır.
- Embedding modeli kullanılmamaktadır.
- Bir LLM API'sine bağlanılmamaktadır.

Bu yapı, yalnızca kullanıcı sorusu, bilgi arama, kaynak gösterme ve güvenli
ret akışını göstermek için hazırlanan başlangıç prototipidir.

## 7. Prototip Test Sonuçları

| Test sorusu | Beklenen davranış | Gerçek sonuç | Durum |
|---|---|---|---|
| Model değerlendirme metrikleri nelerdir? | Model değerlendirme kaydını bulması | Doğru cevap ve model_degerlendirme.md kaynağı gösterildi | Başarılı |
| Uygulamayı yerelde nasıl çalıştırabilirim? | Servis kurulumu kaydını bulması | Doğru cevap ve servis_kurulumu.md kaynağı gösterildi | Başarılı |
| ModuleNotFoundError hatasının çözümü nedir? | Hata çözümü kaydını bulması | Doğru cevap ve hata_cozumleri.md kaynağı gösterildi | Başarılı |
| Şirket çalışanlarının maaşları ne kadar? | Güvenli ret vermesi | Bilgi tabanında yeterli kaynak bulunamadığı belirtildi | Başarılı |
| Boş soru | Hata mesajı göstermesi | Kullanıcı sorusunun boş bırakılamayacağı belirtildi | Başarılı |

Toplam test sayısı: 5  
Başarılı test sayısı: 5

Başarı oranı:

Başarı oranı = (Başarılı test sayısı / Toplam test sayısı) × 100

Başarı oranı = (5 / 5) × 100 = %100