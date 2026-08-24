# Uygulama Loglama

## Loglama Nedir?

Loglama, bir uygulama çalışırken gerçekleşen önemli olayların kayıt altına alınmasıdır.

Log kayıtları hata analizi, sistem davranışının izlenmesi ve değerlendirme amacıyla kullanılabilir.

## AI Doküman Asistanında Loglanabilecek Bilgiler

Sistemde aşağıdaki bilgiler kaydedilebilir:

- Kullanıcı sorusu
- Kullanılan araç
- Bulunan kaynak dokümanlar
- Benzerlik skorları
- Üretilen cevap
- Güvenli ret durumu
- İşlem zamanı

## Log Seviyeleri

Yaygın log seviyeleri arasında DEBUG, INFO, WARNING, ERROR ve CRITICAL bulunur.

INFO normal çalışma bilgilerini kaydetmek için kullanılabilir.

WARNING sistem çalışmaya devam etse bile dikkat edilmesi gereken durumları gösterebilir.

ERROR ise bir işlemin başarısız olduğunu belirtmek için kullanılabilir.

## Dosyaya Log Yazma

Log kayıtları metin, JSON veya JSONL biçimlerinde saklanabilir.

Yapılandırılmış log formatları daha sonra analiz yapılmasını kolaylaştırır.

## Gizlilik

Şifre, API anahtarı veya hassas kullanıcı bilgileri log dosyalarına doğrudan yazılmamalıdır.