# Yaygın Python Hataları ve Çözümleri

## ModuleNotFoundError

ModuleNotFoundError hatası, Python'un kullanılmak istenen modülü veya paketi bulamadığını gösterir.

Örnek hata:

ModuleNotFoundError: No module named 'pandas'

Bu durumda öncelikle ilgili paketin kurulu olup olmadığı kontrol edilmelidir.

Paket kurulumu için:

pip install pandas

komutu kullanılabilir.

## Sanal Ortam Kontrolü

Paket kurulu olmasına rağmen hata devam ediyorsa doğru sanal ortamın aktif olup olmadığı kontrol edilmelidir.

Windows üzerinde sanal ortam:

.venv\Scripts\activate

komutuyla etkinleştirilebilir.

## FileNotFoundError

FileNotFoundError, programın belirtilen dosya veya klasörü bulamadığını gösterir.

Dosya yolunun doğru yazıldığı ve programın doğru klasörden çalıştırıldığı kontrol edilmelidir.

## IndentationError

IndentationError, Python kodunda girintinin hatalı olduğunu gösterir.

if, for, while, try ve fonksiyon tanımlarından sonra gelen kod blokları uygun şekilde girintilenmelidir.

Python projelerinde genellikle dört boşluk kullanılması önerilir.

## UnicodeDecodeError

Bir metin dosyası yanlış karakter kodlamasıyla okunmaya çalışılırsa UnicodeDecodeError oluşabilir.

Türkçe karakterlerin doğru okunabilmesi için metin dosyalarında UTF-8 kodlaması kullanılabilir.