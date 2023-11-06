from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

def link_checker(link):
    try:
        if link[:8] != 'https://':
            if link[:7] != 'http://':
                s = 'http://'
                link = s + link
                print(link)
            # GET request
        req = requests.get(link)

        # check status-code
        if req.status_code in [400, 404, 403, 408, 409, 501, 502, 503]:
            return f"{link} => Broken status-code: {req.status_code}"
        else:
            return f"{link} => Good"
    
    # Exception
    except requests.exceptions.RequestException as e:
        return f"{link}: Something wrong \nErr: {e}"
    
@app.route("/result", methods=['POST', 'GET'])
def result():
    result = "No result"  
    if request.method == 'POST':
        link = request.form.get('link')
        link_result = link_checker(link)
        if link_result is not None:
            result = link_result
    return render_template("index.html", result=result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
