import cv2
import numpy as np

def renk_maskesi_olustur(hsv, renk_adi):
    if renk_adi == 'kirmizi':
        alt1 = np.array([0, 100, 100])
        ust1 = np.array([10, 255, 255])
        alt2 = np.array([160, 100, 100])
        ust2 = np.array([180, 255, 255])
        maske1 = cv2.inRange(hsv, alt1, ust1)
        maske2 = cv2.inRange(hsv, alt2, ust2)
        maske = cv2.bitwise_or(maske1, maske2)
    elif renk_adi == 'mavi':
        alt = np.array([100, 100, 100])
        ust = np.array([130, 255, 255])
        maske = cv2.inRange(hsv, alt, ust)
    elif renk_adi == 'sari':
        alt = np.array([20, 150, 150])
        ust = np.array([32, 255, 255])
        maske = cv2.inRange(hsv, alt, ust)

    cekirdek = np.ones((15, 15), np.uint8)
    maske = cv2.morphologyEx(maske, cv2.MORPH_CLOSE, cekirdek)
    return maske

def sekli_tanimla(kose_sayisi, renk_adi):
    if renk_adi == 'kirmizi':
        if 7 <= kose_sayisi <= 9:
            return 'STOP Tabelasi'
        elif kose_sayisi == 3:
            return 'Yasak/Uyari Tabelasi'
        else:
            return f'Kirmizi Nesne ({kose_sayisi} kose)'
    elif renk_adi == 'mavi':
        if kose_sayisi >= 8:
            return 'Zorunlu Yon Tabelasi'
        else:
            return f'Mavi Nesne ({kose_sayisi} kose)'
    elif renk_adi == 'sari':
        if kose_sayisi in [3, 4]:
            return 'Dikkat/Uyari Tabelasi'
        else:
            return f'Sari Nesne ({kose_sayisi} kose)'

kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Kamera açılamadı!")
else:
    print("Kamera açıldı. Çıkmak için 'q' tuşuna bas.")

    renkler = {
        'kirmizi': (0, 0, 255),
        'mavi': (255, 0, 0),
        'sari': (0, 255, 255)
    }

    while True:
        basarili, kare = kamera.read()
        if not basarili:
            break

        hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)

        for renk_adi, kutu_rengi in renkler.items():
            maske = renk_maskesi_olustur(hsv, renk_adi)
            konturlar, _ = cv2.findContours(maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for kontur in konturlar:
                alan = cv2.contourArea(kontur)
                if alan > 800:
                    x, y, w, h = cv2.boundingRect(kontur)

                    kutu_alani = w * h
                    doluluk = alan / kutu_alani if kutu_alani > 0 else 0

                    if doluluk < 0.35:
                        continue

                    cevre = cv2.arcLength(kontur, True)
                    yaklasik_sekil = cv2.approxPolyDP(kontur, 0.02 * cevre, True)
                    kose_sayisi = len(yaklasik_sekil)

                    etiket = sekli_tanimla(kose_sayisi, renk_adi)

                    cv2.rectangle(kare, (x, y), (x + w, y + h), kutu_rengi, 2)
                    cv2.putText(kare, etiket, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, kutu_rengi, 2)

        cv2.imshow('Cok Renkli Tabela Tespiti', kare)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    kamera.release()
    cv2.destroyAllWindows()