import cv2

kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Kamera açılamadı!")
else:
    print("Kamera açıldı, bir kare okunuyor...")
    basarili, kare = kamera.read()
    if basarili:
        cv2.imwrite('anlik_goruntu.jpg', kare)
        print("Başarılı! anlik_goruntu.jpg dosyasına kaydedildi.")
        cv2.imshow('Test', kare)
        cv2.waitKey(3000)
    else:
        print("Kare okunamadı, kamera veri vermiyor.")

kamera.release()
cv2.destroyAllWindows()