# Sınıflandırma Metrikleri

## Confusion Matrix

Bir sınıflandırma modelinin sonuçları True Positive, True Negative, False Positive ve False Negative değerleriyle incelenebilir.

True Positive, pozitif bir örneğin doğru şekilde pozitif tahmin edilmesidir.

True Negative, negatif bir örneğin doğru şekilde negatif tahmin edilmesidir.

False Positive, negatif bir örneğin yanlış şekilde pozitif tahmin edilmesidir.

False Negative, pozitif bir örneğin yanlış şekilde negatif tahmin edilmesidir.

## Accuracy

Accuracy, doğru tahminlerin toplam tahminlere oranıdır.

Accuracy = (TP + TN) / (TP + TN + FP + FN)

## Precision

Precision, pozitif olarak tahmin edilen örneklerin ne kadarının gerçekten pozitif olduğunu gösterir.

Precision = TP / (TP + FP)

## Recall

Recall, gerçek pozitif örneklerin ne kadarının model tarafından bulunduğunu gösterir.

Recall = TP / (TP + FN)

## F1-score

F1-score, precision ve recall değerlerinin harmonik ortalamasıdır.

F1 = 2 * (Precision * Recall) / (Precision + Recall)

## Metrik Seçimi

Uygun metrik probleme göre seçilmelidir.

Sınıfların dengesiz olduğu veri kümelerinde yalnızca accuracy değerine bakmak yanıltıcı olabilir.