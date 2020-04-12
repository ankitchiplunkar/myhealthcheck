from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)

video_stream = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    assert video_stream.isOpened()
    while True:
        ret, frame = video_stream.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_stream),
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port="8080", threaded=True)