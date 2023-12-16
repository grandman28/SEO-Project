from flask import Flask, render_template, request
import requests  # Add this line
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlparse
 
 
app = Flask(__name__)
 
 
def link_checker(link):
    try:
        if link != None:
            if link[:8] != 'https://':
                if link[:7] != 'http://':
                    s = 'https://'
                    link = s + link
                    print(link)
 
            req = requests.get(link)
 
            status = f"Broken status-code: {req.status_code}" if req.status_code in [400, 404, 403, 408, 409, 501, 502, 503] else "Good"

            return link, status
 
    except requests.exceptions.RequestException as e:
        return link, "Bad"
 



def get_urls_from_website(url):
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f'https://{url}'

        response = requests.get(url)
        response.raise_for_status()  # Ridică o excepție dacă cererea HTTP a eșuat

        soup = BeautifulSoup(response.text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a')]

        return urls
    except Exception as e:
        print(f"Error: {e}")
        return None

    
def check_link_on_page(urls):
    result_list = []
    url_list = []
    
    for i_url in urls:
        url, status = link_checker(i_url)
        result_list.append(status)
        url_list.append(url)
    
    return url_list, result_list

 
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html") 
 
@app.route("/result", methods=['GET', 'POST'])
def result():
    result_url = None
    result_status = None
    urls = None
    if request.method == 'POST':
        link = request.form.get('link')
        link_result = link_checker(link)
        urls = get_urls_from_website(link)
        
        if urls is not None:
            result_url, result_status = check_link_on_page(urls)
        else:
            result_url, result_status = [], []  # Provide empty lists if no URLs are found
        result = {'link_result': link_result, 'urls': list(zip(result_url, result_status))}
    return render_template("index.html", result=result)
 
if __name__ == '__main__':
    app.run(debug=True, port=5001)
