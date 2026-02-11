# run.py
from wsgiref.simple_server import make_server
from app import app

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000... Press Ctrl+C to stop.')
        httpd.serve_forever()