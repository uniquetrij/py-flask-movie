import io

from flask import Flask, Response, Blueprint
from flask_cors import CORS
from threading import Thread

try:
    import cv2
    using_cv2 = True
except:
    using_cv2 = False
    try:
        from PIL import Image

    except:
        raise Exception("either CV2 or PIL packages must be available")

class FlaskMovie:

    def __init__(self, app=None, bp=None):
        if not app:
            app = Flask(__name__)
        if not bp:
            bp = Blueprint('flask_movie', __name__, template_folder='../templates')

        self.__bp = bp
        self.__app = app
        self.__routes_pipe = {}
        self.__routes_no_feed_img = {}
        self.__routes_timeout = {}
        self.__routes_allow_flush = {}
        CORS(app)

        @self.__bp.route('/<route>')
        def video_feed(route):
            return Response(self.__generate(self.__routes_pipe[route], self.__routes_no_feed_img[route],
                                            self.__routes_timeout[route], self.__routes_allow_flush[route]),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def __generate(self, pipe, no_feed_img, timeout, allow_flush):
        while True:
            try:
                pipe.pull_wait(timeout)
                ret, image = pipe.pull(allow_flush)
                if not ret:
                    image = no_feed_img

                if not using_cv2:
                    image = Image.fromarray(image)
                    byteIO = io.BytesIO()
                    image.save(byteIO, format='JPEG')
                    byteArr = byteIO.getvalue()
                else:
                    byteArr = cv2.imencode('.jpg', image)[1].tostring()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + byteArr + b'\r\n')

            except GeneratorExit as ex:
                print(ex)
                return
            except:
                print("no feed available yet...")
                pass

    def create(self, route, pipe, default_img=None, timeout=None, allow_flush=True):
        if timeout is None:
            timeout = 1
        self.__routes_pipe[route] = pipe
        self.__routes_no_feed_img[route] = default_img
        self.__routes_timeout[route] = timeout
        self.__routes_allow_flush[route] = allow_flush

    def start(self, bind_ip, bind_port, prefix=''):
        self.__app.register_blueprint(self.__bp, url_prefix=prefix)
        Thread(target=self.__app.run, args=(bind_ip, bind_port,)).start()
