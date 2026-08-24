# Python Kurulumu

## Python Nedir?

Python, genel amaçlı ve yüksek seviyeli bir programlama dilidir.
Yapay zeka, veri analizi, web geliştirme ve otomasyon gibi birçok alanda kullanılabilir.

## Python Kurulumu

Python kurulumu için resmi Python dağıtımı kullanılabilir.
Kurulum sırasında Python yorumlayıcısının sistem PATH değişkenine eklenmesi önerilir.

Windows sistemlerde kurulum ekranında "Add Python to PATH" seçeneği işaretlenmelidir.

## Kurulum Kontrolü

Kurulum tamamlandıktan sonra terminal açılarak aşağıdaki komut çalıştırılabilir:

python --version

Komut sonucunda kurulu Python sürümü görüntülenmelidir.

## Pip Kontrolü

Python paketlerinin kurulması için pip paket yöneticisi kullanılır.

pip --version

komutu ile pip kurulumunun çalışıp çalışmadığı kontrol edilebilir.

## Paket Kurulumu

Bir Python paketi aşağıdaki komutla kurulabilir:

pip install paket_adi

Bir projedeki tüm bağımlılıklar requirements.txt dosyasından aşağıdaki komutla yüklenebilir:

pip install -r requirements.txt