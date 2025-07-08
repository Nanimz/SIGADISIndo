from PIL import Image

img = Image.open("icons/splash.png")
resized_img = img.resize((480, 480))
resized_img.save("icons/splash_resized.png")
