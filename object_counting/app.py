from importlib import import_module
from flask import Flask, render_template, Response
import os
from tensorflow.keras.models import load_model
from yolo4.model import Mish
import tensorflow as tf
import cv2
import time


app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera_stream, feed_type, device):
    """Video streaming generator function."""
    unique_name = (feed_type, device)

    num_frames = 0
    total_time = 0
    while True:
        time_start = time.time()

        cam_id, frame = camera_stream.get_frame(unique_name)
        if frame is None:
            break

        num_frames += 1

        time_now = time.time()
        total_time += time_now - time_start
        fps = num_frames / total_time

        # write camera name
        cv2.putText(frame, cam_id, (int(20), int(20 * 5e-3 * frame.shape[0])), 0, 2e-3 * frame.shape[0], (255, 255, 255), 2)

        if feed_type == 'yolo':
            cv2.putText(frame, "FPS: %.2f" % fps, (int(20), int(40 * 5e-3 * frame.shape[0])), 0, 2e-3 * frame.shape[0],
                        (255, 255, 255), 2)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()  # Remove this line for test camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/<feed_type>/<device>')
def video_feed(feed_type, device):
    """Video streaming route. Put this in the src attribute of an img tag."""
    port_list = (5555, 5566)
    if feed_type == 'camera':
        camera_stream = import_module('camera_server').Camera
        return Response(gen(camera_stream=camera_stream(feed_type, device, port_list), feed_type=feed_type, device=device),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    elif feed_type == 'yolo':
        camera_stream = import_module('camera_yolo').Camera
        yolo_model_copy = yolo_model
        return Response(gen(camera_stream=camera_stream(feed_type, device, port_list,yolo_model_copy), feed_type=feed_type, device=device),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    path = 'model_data/yolo4.h5'
    model_path = os.path.expanduser(path)
    assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

    yolo_model = load_model(model_path, custom_objects={'Mish': Mish}, compile=False)

    print('{} model, anchors, and classes loaded.'.format(model_path))

    app.run(host='0.0.0.0', threaded=True)
