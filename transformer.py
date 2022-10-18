import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
output = './output'
if not os.path.exists(output):
    os.makedirs(output)
files = './files'
if os.path.exists(files):
    for i in os.listdir(files):
        print('file = ' , i)
        img = cv2.imread(files + '/' + i)

        while 1:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
            ret, thresh1 = cv2.threshold(
                gaussian_blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
            dilation = cv2.dilate(thresh1, rect_kernel, iterations=3)

            contours, _ = cv2.findContours(
                dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            im2 = img.copy()

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 735 and w < 750:
                    y = y - 20
                    h = h + 30
                    cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    ROI = img[y:y+h, x:x+w]
                    #cv2.imwrite('0.png', ROI)

            ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(ROI)
            text = text.split(':')[1].strip()[4:]
            
            #text = text[-7:-2]
            #print(text)
            cv2.putText(im2, text, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)
            cv2.imshow('pic', im2)
            
            key = cv2.waitKey(1)
            if key == ord('y'):
                cv2.imwrite(os.path.join(output, f'{text}.png'), img)
                break
            if key == ord('n'):
                break
        cv2.destroyAllWindows()
else : 
    print('folder named "files" was not found in directory')