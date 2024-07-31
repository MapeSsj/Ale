import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from flask import Flask, render_template, request, jsonify
import threading

# Flask app
app = Flask(__name__)

no_click_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accept', methods=['POST'])
def accept():
    return jsonify({'message': '¡Qué alegría! 😊 ¡Gracias por aceptar!'})

@app.route('/deny', methods=['POST'])
def deny():
    global no_click_count
    no_click_count += 1
    if no_click_count > 5:
        return jsonify({'message': 'Ya cansate y sal a besarme'})
    return jsonify({'message': ''})

def run_flask():
    app.run(debug=False, port=5000, use_reloader=False)

# PyQt5 application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Una Pregunta Importante')
        self.setGeometry(100, 100, 800, 600)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
