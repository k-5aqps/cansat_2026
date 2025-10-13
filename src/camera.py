import picamera
import io

def capture(cnt):
    camera = picamera.Picamera()
    stream=io.BytesIO()
    camera.resolution = (1024,768)

    camera.capture(stream,format='jpeg')
    camera.close()
    stream.seek(0)
    img_data = stream.getvalue()

    return img_data