from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests


app = Flask(_name_)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        link = request.form.get('link')
        result = link_checker(link)
    return render_template('index.html', result=result)
//

def link_checker(link):
    try:
        # GET request
        req = requests.get(link)

        # check status-code
        if req.status_code in [400, 404, 403, 408, 409, 501, 502, 503]:
            print(f"{link} => Broken status-code: {req.status_code}")
        else:
            print(f"{link} => Good")

    # Exception
    except requests.exceptions.RequestException as e:
        # print link with Errs
        print(f"{link}: Something wrong \nErr: {e}")

'''
link = input("Enter link:")
print("Link is: " + link)

link_checker(link)

url = link
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    print(link.get('href'))
'''
if _name_ == '_main_':
    app.run(debug=True)



