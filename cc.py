
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

    img = np.zeros((1080, 1920, 4), np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = message
    
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    app.logger.debug('Text size : (%d, %d)' % (text_size[0], text_size[1]))

    margin = 10
    img_background_for_cc = np.zeros((text_size[1] + 2*margin, text_size[0] + 2*margin, 4), np.uint8)
    img_background_for_cc[:] = (0, 0, 0, 128)

    textX = int((img_background_for_cc.shape[1] - text_size[0]) / 2)
    textY = int((img_background_for_cc.shape[0] + text_size[1]) / 2)

    app.logger.debug('Text position : (%d, %d)' % (textX, textY))

    cv2.putText(img_background_for_cc, text, (textX, textY), font, 1, (255, 255, 255, 255), 2)
    cv2.imwrite('cc_debug.png', img_background_for_cc)

    offset_x = int((img.shape[1] - img_background_for_cc.shape[1]) / 2)
    # offset_y = int((img.shape[0] - img_background_for_cc.shape[0]) / 2)
    offset_y = 900
    img[offset_y:offset_y+img_background_for_cc.shape[0], offset_x:offset_x+img_background_for_cc.shape[1]] = img_background_for_cc[:]

    cv2.imwrite('hello_image.png', img)

    return send_from_directory(
        app.config['ROOT_DIR'], 'hello_image.png', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')