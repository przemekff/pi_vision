from tflite_runtime.interpreter import Interpreter 
from PIL  import Image
import numpy as np
import time
import picamera
import picamera.array
import io
#from picamera import PiCamera
from time import sleep


def load_labels(path): # Read the labels from the text file as a Python list.
  with open(path, 'r') as f:
    return [line.strip() for i, line in enumerate(f.readlines())]

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  # print(interpreter.get_input_details())
  input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
  set_input_tensor(interpreter, image)

  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  print(output_details['index'])
  output = interpreter.get_tensor(output_details['index'])
  print(output)
  output = np.squeeze(interpreter.get_tensor(output_details['index']))
  print(output)
  #scores = interpreter.get_tensor(output_details[2]['index'])
  #print(interpreter.get_tensor(output_details['index']))
  threshold = 0.7
  if output > threshold:
    return 1
  elif output < -threshold:
    return -1
  else:
      return 0
    
def capture_img(camera):
 #    camera.start_preview()
# Camera warm-up time
    sleep(2)
    camera.capture(str(time.time())+'test.jpg',resize=(640, 480))
    
data_folder = "/home/pi/Camera_Interpreter/"

model_path = data_folder + "vwmodelv1.tflite"
# label_path = data_folder + "labels_test.txt"

interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height, ")")

# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32


# capture_img(camera)
# Load an image to be classified.
image = Image.open(data_folder + "tesla.jpg").convert('RGB').resize((width, height))

# Classify the image.
time1 = time.time()
score = classify_image(interpreter, image)
time2 = time.time()
classification_time = np.round(time2-time1, 3)
print("Classificaiton Time =", classification_time, "seconds.")

"""with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (1280, 720)
        camera.capture(output, 'rgb')
        print('Captured %dx%d image' % (
                output.array.shape[1], output.array.shape[0]))
        output.truncate(0)
        camera.resolution = (1280, 720)
        camera.capture(output, 'rgb')
        print('Captured %dx%d image' % (
                output.array.shape[1], output.array.shape[0]))"""
with picamera.PiCamera() as camera:
    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    camera.resolution = (1920, 1080)
    camera.framerate = 15
    camera.rotation = 180
    time.sleep(2)
    # Set up 40 in-memory streams
    outputs = [io.BytesIO() for i in range(40)]
    start = time.time()
    camera.capture_sequence(outputs, 'jpeg', use_video_port=True)

    finish = time.time()
    # How fast were we?
    print('Captured 40 images at %.2ffps' % (40 / (finish - start)))

    count = 0
    for frameData in outputs:
        rawIO = frameData
        rawIO.seek(0)
        byteImg = Image.open(rawIO)

        count += 1
        filename = "image" + str(count) + ".jpg"
        byteImg.save(filename, 'JPEG')


if score == 1:
    print("Arteon is detected")
elif score == -1:
    print("Arteon is not detected")
else:
    print("Arteon is not detected()")
#print("Image Label is :", classification_label, ", with Accuracy :", np.round(prob*100, 2), "%.")
