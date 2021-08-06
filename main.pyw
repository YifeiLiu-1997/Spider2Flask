from flask import Flask
from flask import render_template
from spider2trans import get_translation
import webbrowser
import sys, os

if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")


app = Flask(__name__)


@app.route('/<wd>')
def index(wd):
    translation_list, uk_pron, uk_mp3, us_pron, us_mp3 = get_translation(str(wd))
    return render_template('query.html', trans_list=translation_list, keyword=wd, uk_pron=uk_pron, uk_mp3=uk_mp3,
                           us_pron=us_pron, us_mp3=us_mp3)


@app.route('/')
def trans():
    return render_template('base.html')


if __name__ == '__main__':
    webbrowser.open_new_tab("http://127.0.0.1:5000/")
    app.run(use_reloader=False)
