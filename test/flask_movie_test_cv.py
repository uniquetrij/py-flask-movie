from threading import Thread

import cv2
from py_pipe.pipe import Pipe

from py_flask_movie.flask_movie import FlaskMovie


def read_camera(cap, pipe):
    while True:
        ret, image = cap.read()
        if not ret:
            continue
        # image[:,:,0],image[:,:,1],image[:,:,2] = image[:,:,2],image[:,:,1],image[:,:,0]
        pipe.push(image)


if __name__ == '__main__':
    fs = FlaskMovie()
    fs.start("0.0.0.0", 5000)

    cap0 = cv2.VideoCapture(0)
    pipe0 = Pipe()
    fs.create('feed_0', pipe0)
    Thread(target=read_camera, args=(cap0, pipe0,)).start()

    # cap1 = cv2.VideoCapture(1)
    # pipe1 = Pipe()
    # fs.create('feed_1', pipe1)
    # Thread(target=read_camera, args=(cap1, pipe1,)).start()
