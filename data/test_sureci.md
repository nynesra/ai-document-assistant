# Yazılım Test Süreci

## Test Nedir?

Test, geliştirilen yazılımın beklenen davranışı gösterip göstermediğini kontrol etme işlemidir.

Test sırasında belirli bir girdi verilir ve elde edilen sonuç beklenen sonuçla karşılaştırılır.

## Test Senaryosu

Bir test senaryosu genel olarak şu bilgileri içerebilir:

- Test girdisi
- Beklenen sonuç
- Gerçek sonuç
- Başarılı veya başarısız durumu

## Pozitif Test

Sistemin normal ve geçerli girdiler karşısında doğru çalışıp çalışmadığını kontrol eder.

Örneğin geçerli bir Markdown dosyasının başarıyla yüklenmesi pozitif bir testtir.

## Negatif Test

Sistemin hatalı veya beklenmeyen girdiler karşısındaki davranışını kontrol eder.

Örneğin olmayan bir klasörün verilmesi veya boş bir dosyanın yüklenmeye çalışılması negatif test olabilir.

## Başarı Oranı

Toplam test sayısı N ve başarılı test sayısı B ise test başarı oranı:

Başarı Oranı = (B / N) * 100

formülüyle hesaplanabilir.

## AI Sistemlerinde Değerlendirme

Doküman asistanlarında yalnızca programın hata vermeden çalışması yeterli değildir.

Doğru kaynağın bulunması, kaynak gösterilmesi, doğru aracın seçilmesi ve yetersiz bilgi durumunda güvenli ret verilmesi de test edilmelidir.