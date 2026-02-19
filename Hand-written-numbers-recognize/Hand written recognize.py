import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('my_mnist_model_conv.keras')

def prepare_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28,28))
    img_array = np.array(img) / 255.0
    img_array=img_array.reshape(28,28)
    
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

def smart_process_image(image_path):
    img = Image.open(image_path).convert('L')
    pixel_sample = img.getpixel((0, 0))
    if pixel_sample > 128: 
        img = ImageOps.invert(img)

    bbox = img.getbbox()
    if bbox:
        img_cropped = img.crop(bbox)
    else:
        return None

    new_img = Image.new("L", (28, 28), 0) 
    width, height = img_cropped.size
    max_side = max(width, height)
    ratio = 20.0 / max_side

    new_width = int(width * ratio)
    new_height = int(height * ratio)

    img_resized = img_cropped.resize((new_width, new_height))
    

    x_offset = (28 - new_width) // 2
    y_offset = (28 - new_height) // 2
    

    new_img.paste(img_resized, (x_offset, y_offset))
    

    img_array = np.array(new_img) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    plt.imshow(img_array.reshape(28, 28), cmap='gray')
    plt.title("Smart Processed Image")
    plt.show()
    return img_array



prediction = model.predict(smart_process_image('test_digit.png'))
predicted_digit = np.argmax(prediction)
confidence = np.max(prediction)
print(f"predict number: {predicted_digit}, confidence: {confidence:.4f}")





