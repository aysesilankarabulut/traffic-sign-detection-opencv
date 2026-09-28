import cv2
import numpy as np

img = cv2.imread('test_isare.jpg')

if img is None:
    print("Görsel bulunamadı! Dosya adını kontrol et.")
else:
    yukseklik, genislik = img.shape[:2]
    olcek = 600 / max(yukseklik, genislik)
    yeni_genislik = int(genislik * olcek)
    yeni_yukseklik = int(yukseklik * olcek)
    img_kucuk = cv2.resize(img, (yeni_genislik, yeni_yukseklik))

    # HSV renk uzayına çevir (kırmızıyı yakalamak RGB'den çok daha kolay)
    hsv = cv2.cvtColor(img_kucuk, cv2.COLOR_BGR2HSV)

    # Kırmızı renk aralığı (kırmızı HSV'de hem başta hem sonda olduğu için 2 aralık lazım)
    alt_kirmizi1 = np.array([0, 100, 100])
    ust_kirmizi1 = np.array([10, 255, 255])
    alt_kirmizi2 = np.array([160, 100, 100])
    ust_kirmizi2 = np.array([180, 255, 255])

    maske1 = cv2.inRange(hsv, alt_kirmizi1, ust_kirmizi1)
    maske2 = cv2.inRange(hsv, alt_kirmizi2, ust_kirmizi2)
    kirmizi_maske = cv2.bitwise_or(maske1, maske2)

    # Kırmızı bölgelerin konturlarını (dış hatlarını) bul
    konturlar, _ = cv2.findContours(kirmizi_maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # En büyük konturu bul (küçük gürültüleri elemek için)
    if konturlar:
        en_buyuk = max(konturlar, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(en_buyuk)

        # Tespit edilen bölgenin etrafına yeşil bir kutu çiz
        cv2.rectangle(img_kucuk, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(img_kucuk, 'Trafik Isareti Tespit Edildi', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        print(f"Kırmızı bölge bulundu! Konum: x={x}, y={y}, genişlik={w}, yükseklik={h}")
    else:
        print("Kırmızı bölge bulunamadı.")

    cv2.namedWindow('Tespit Sonucu', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Kirmizi Maske', cv2.WINDOW_NORMAL)
    cv2.imshow('Tespit Sonucu', img_kucuk)
    cv2.imshow('Kirmizi Maske', kirmizi_maske)

    cv2.waitKey(0)
    cv2.destroyAllWindows()