
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

import numpy as np
import cv2
import os

app = Flask(__name__)
app.config['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/req_cc', methods=['POST'])
def req_cc():
    message = request.form['message']
    app.logger.debug('Message : ' + message)

    img = np.zeros((1080, 1920, 3), np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = message
    
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    app.logger.debug('Text size : (%d, %d)' % (textsize[0], textsize[1]))

    textX = int((img.shape[1] - textsize[0]) / 2)
    textY = int((img.shape[0] - textsize[1]) / 2)
    app.logger.debug('Write position : (%d, %d)' % (textX, textY))

    cv2.putText(img, text, (textX, textY), font, 1, (255, 255, 255), 2)

    cv2.imwrite('hello_image.jpg', img)

    return send_from_directory(
        app.config['ROOT_DIR'], 'hello_image.jpg', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')