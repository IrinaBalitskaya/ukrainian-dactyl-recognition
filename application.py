from ukrainian_dactyl_recognition.dactyl_detection import detect_dactyl

from flask import Flask, render_template, Response, request, jsonify
import ukrainian_dactyl_recognition.cfg as cfg

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/stream')
def stream():
    return Response(detect_dactyl(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@application.route('/translation')
def translation():
    return jsonify('', render_template('translation_textarea.html',
                                       translation=''.join(cfg.sentence)))


@application.route('/clear_textarea', methods=['DELETE'])
def clear_textarea():
    cfg.sentence = []
    return jsonify('', render_template('translation_textarea.html', translation=''))


@application.route('/start_pause_webcam', methods=['PUT'])
def start_pause_webcam():
    cfg.is_feed_on = not cfg.is_feed_on
    btn_text = request.get_json()['btn_text']
    btn_text = "Зупинити" if btn_text == "Почати" else "Почати"
    return jsonify({'btn_text': btn_text})


if __name__ == "__main__":
    application.run(debug=True)
