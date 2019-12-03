from setuptools import setup
import pip

setup(
    name='py_flask_movie',
    version='0.0.1',
    description="A video streaming library over http using flask",
    url='https://github.com/uniquetrij/py-flask-movie',
    author='Trijeet Modak',
    author_email='uniquetrij@gmail.com',
    install_requires=[
        'opencv-python',
        'Flask',
        'Flask-Cors',
        'imageio',
        'pillow',
        'py_pipe' if pip.__version__ < '19.0' else '',
    ],
    dependency_links=[
        'https://github.com/uniquetrij/py-pipe/tarball/release#egg=py-pipe-v0.0.1'
    ],
    packages=['py_flask_movie'],
    zip_safe=False
)
