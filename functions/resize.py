from PIL import Image

img = Image.open("icons/sigadisindo.png")
resized_img = img.resize((480, 480))
resized_img.save("icons/sigadisindo_resized.png")
