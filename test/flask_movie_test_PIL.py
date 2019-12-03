from threading import Thread

import numpy as np
from py_pipe.pipe import Pipe

from py_flask_movie.flask_movie import FlaskMovie


def read_camera(cap, pipe):
    while True:
        image = cap.get_next_data()
        image[:, :, 0], \
        image[:, :, 1], \
        image[:, :, 2] = image[:, :, 2].copy(), \
                         image[:, :, 1].copy(), \
                         image[:, :, 0].copy()
        pipe.push(image)


if __name__ == '__main__':
    import imageio

    fs = FlaskMovie()
    fs.start("0.0.0.0", 5000)

    cap0 = imageio.get_reader('<video0>')
    pipe0 = Pipe()
    fs.create('feed_0', pipe0)
    Thread(target=read_camera, args=(cap0, pipe0,)).start()

    # cap1 = imageio.get_reader('<video1>')
    # pipe1 = Pipe()
    # fs.create('feed_1', pipe1)
    # Thread(target=read_camera, args=(cap1, pipe1,)).start()
