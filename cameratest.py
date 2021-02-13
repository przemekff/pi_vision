import io
import random
import picamera
import time
from PIL import Image, ImageChops

prior_image = None
point_table = ([0] + ([255] * 255))
my_stream = io.BytesIO()

"""def detect_motion(camera):
    global prior_image
    camera.capture(my_stream, format='jpeg', use_video_port=True)
    my_stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(my_stream)
        return False
    else:
        current_image = Image.open(my_stream)
        diff = ImageChops.difference(prior_image, current_image)
        diff = diff.convert('L')
        diff = diff.point(point_table)
        new = diff.convert('RGB')
        new.paste(current_image, mask=diff)
        
        im3 = ImageChops.subtract(current_image, prior_image, scale = 1.0, offset = 2)
        
        im3.save(str(time.time())+'test.png')

        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        result = 0
        return result"""

"""def write_video(stream):
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    # Wipe the circular stream once we're done
    stream.seek(0)
    stream.truncate()"""

def dif_image(prior_image,current_image):
    diff = ImageChops.difference(prior_image, current_image)
    diff = diff.convert('L')
    diff = diff.point(point_table)
    new = diff.convert('RGB')
    new.paste(current_image, mask=diff)     
    im3 = ImageChops.subtract(current_image, prior_image, scale = 1.0, offset = 2)       
    im3.save(str(time.time())+'dif.png')


with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    time.sleep(0.5)
    camera.capture(my_stream, 'jpeg')
    my_stream.seek(0)
    while True:
        prev_image = Image.open(my_stream)
        prev_image.save(str(time.time())+'prev.png')
        time.sleep(0.5)
        my_stream.seek(0)
        my_stream.truncate()
        camera.capture(my_stream, 'jpeg')
        next_image = Image.open(my_stream)
        next_image.save(str(time.time())+'next.png')
        dif_image(prev_image,next_image)
        
    """stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(0.5)
            if detect_motion(camera):
                print('Motion detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                write_video(stream)
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
    """