# Metin ve Veri Temizleme

## Veri Temizleme Nedir?

Veri temizleme, ham veride bulunan gereksiz veya hatalı yapıların düzenlenmesi işlemidir.

Doküman tabanlı yapay zeka sistemlerinde metnin tutarlı biçimde hazırlanması retrieval kalitesini etkileyebilir.

## Gereksiz Boşlukların Temizlenmesi

Metinde art arda bulunan gereksiz boşluklar tek boşluğa dönüştürülebilir.

Örneğin:

Python     kurulumu

ifadesi:

Python kurulumu

şeklinde düzenlenebilir.

## Satır Sonlarının Normalleştirilmesi

Farklı işletim sistemleri satır sonlarını farklı karakterlerle gösterebilir.

Metin işleme sırasında satır sonlarının ortak bir biçime dönüştürülmesi sonraki işlemleri kolaylaştırır.

## Tab Karakterleri

Tab karakterleri gerektiğinde normal boşluk karakterlerine dönüştürülebilir.

## Boş Satırlar

Art arda gelen çok sayıda boş satır azaltılarak dokümanın yapısı daha düzenli hale getirilebilir.

## Aşırı Temizlemeden Kaçınma

Başlıklar, paragraf ayrımları ve teknik ifadeler retrieval açısından önemli bilgiler taşıyabilir.

Bu nedenle temizleme sırasında dokümanın anlamsal yapısı korunmalıdır.

## Temizleme Ölçümü

Ham metnin karakter sayısı L_raw ve temizlenmiş metnin karakter sayısı L_clean ile gösterilebilir.

Çıkarılan karakter miktarı:

L_removed = L_raw - L_clean

Temizleme oranı:

R = ((L_raw - L_clean) / L_raw) * 100

formülüyle hesaplanabilir.