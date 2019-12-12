import cv2

sizes = [16,24,32,48,64]
for i, x in enumerate(sizes, start=1):
    image = r"C:\Users\John.IOCA\Desktop\icon.png"
    image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    dim = (x,x)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'C:\\Users\\John.IOCA\\Desktop\\{x}.png', resized)
