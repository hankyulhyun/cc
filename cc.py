
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

import os

from PIL import Image, ImageFont, ImageDraw

app = Flask(__name__)
app.config['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/req_cc', methods=['POST'])
def req_cc():
    message = request.form['message']
    app.logger.debug('Message : ' + message)

    img = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))

    font = ImageFont.truetype("./Assets/Font/SeoulNamsanEB.ttf", 35)
    text_size = font.getsize(message)

    draw = ImageDraw.Draw(img)

    margin = 10

    text_draw_position_x = int((1920 - text_size[0]) / 2)
    # text_draw_position_y = int((1080 - text_size[1]) / 2)
    text_draw_position_y = 950

    rect_draw_position_start_x = text_draw_position_x - margin * 2
    rect_draw_position_start_y = text_draw_position_y - margin

    rect_draw_position_end_x = text_draw_position_x + text_size[0] + margin * 2
    rect_draw_position_end_y = text_draw_position_y + text_size[1] + margin

    draw.rectangle([rect_draw_position_start_x, rect_draw_position_start_y, rect_draw_position_end_x, rect_draw_position_end_y], fill=(0, 0, 0, 127))

    draw.text((text_draw_position_x, text_draw_position_y), message, font=font, fill=(255, 255, 255, 255))

    img.save("hello_image.png", "PNG")

    return send_from_directory(
            app.config['ROOT_DIR'], 'hello_image.png', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')