# Temel Git Komutları

## Git Nedir?

Git, yazılım projelerindeki dosya değişikliklerini takip etmek için kullanılan bir sürüm kontrol sistemidir.

Git sayesinde yapılan değişiklikler kayıt altına alınabilir ve projenin geçmiş sürümlerine erişilebilir.

## Repository Başlatma

Yeni bir Git repository oluşturmak için:

git init

komutu kullanılabilir.

## Durum Kontrolü

Dosyaların mevcut durumunu görmek için:

git status

komutu kullanılır.

## Dosyaları Stage Alanına Ekleme

Belirli bir dosyayı eklemek için:

git add dosya_adi

Tüm değişiklikleri eklemek için:

git add .

komutu kullanılabilir.

## Commit Oluşturma

Değişiklikleri açıklayıcı bir mesajla kaydetmek için:

git commit -m "Doküman yükleme modülü eklendi"

komutu kullanılabilir.

## Commit Geçmişi

Önceki commit kayıtlarını görüntülemek için:

git log

komutu kullanılabilir.

## Remote Repository

Uzak repository adresi aşağıdaki gibi eklenebilir:

git remote add origin repository_adresi

Yerel commitleri uzak repository'ye göndermek için:

git push

komutu kullanılabilir.