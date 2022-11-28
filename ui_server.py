from flask import Flask, render_template

app = Flask(__name__, static_url_path='',
                  static_folder='react',
                  template_folder='react')

@app.route("/")
def hello():
    return render_template("index.html")

if __name__=="__main__":
    app.run(port=3000,host="0.0.0.0")