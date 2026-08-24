# Python Sanal Ortam Kullanımı

## Sanal Ortam Nedir?

Sanal ortam, bir Python projesinin paketlerini diğer projelerden bağımsız olarak yönetmeyi sağlar.

Bu sayede farklı projelerde farklı paket sürümleri kullanılabilir.

## Sanal Ortam Oluşturma

Python ile sanal ortam oluşturmak için aşağıdaki komut kullanılabilir:

python -m venv .venv

Bu komut proje klasörü içerisinde .venv isimli bir sanal ortam oluşturur.

## Windows Üzerinde Etkinleştirme

Windows sistemlerde sanal ortam aşağıdaki komutla etkinleştirilir:

.venv\Scripts\activate

Etkinleştirildikten sonra terminal satırının başında genellikle (.venv) ifadesi görünür.

## Sanal Ortamı Kapatma

Aktif sanal ortamdan çıkmak için:

deactivate

komutu kullanılabilir.

## Neden Kullanılır?

Sanal ortam kullanımı:

- Paket çakışmalarını azaltır.
- Projelerin bağımlılıklarını birbirinden ayırır.
- Projenin başka bilgisayarlarda tekrar kurulmasını kolaylaştırır.