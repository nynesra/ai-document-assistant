# Proje Klasör Yapısı

## Genel Yapı

AI Doküman Asistanı projesi farklı görevleri birbirinden ayıran modüler bir klasör yapısıyla geliştirilebilir.

## data Klasörü

data klasörü bilgi tabanında kullanılacak Markdown ve TXT dokümanlarını içerir.

Retrieval sistemi bu dokümanları okuyarak aranabilir bilgi parçaları oluşturur.

## src Klasörü

src klasörü projenin temel Python modüllerini içerir.

Doküman yükleme, metin temizleme, chunking, retrieval ve agent işlemleri bu klasörde bulunabilir.

## docs Klasörü

docs klasörü tasarım notları ve teknik açıklamalar için kullanılabilir.

## evaluation Klasörü

evaluation klasörü sistem performansını ölçmek için hazırlanan soru ve beklenen sonuçları içerebilir.

## logs Klasörü

logs klasörü kullanıcı sorguları, sistem kararları ve retrieval sonuçlarının kayıtlarını saklamak için kullanılabilir.

## tests Klasörü

tests klasörü otomatik veya manuel test senaryolarına ait dosyalar için kullanılabilir.

## app.py

app.py uygulamanın kullanıcı arayüzünü veya ana çalışma akışını başlatan dosya olarak kullanılabilir.

## requirements.txt

requirements.txt projenin ihtiyaç duyduğu Python paketlerini ve bağımlılıklarını tanımlar.

## .env

.env dosyası API anahtarları gibi ortam değişkenlerini tutabilir.

Gerçek gizli değerlerin Git repository içerisine eklenmemesi gerekir.