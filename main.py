import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv
import time

URL = "https://programmer100.pythonanywhere.com/tours/";
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'};

load_dotenv();

api_key = os.getenv("API_KEY");

def scrape(url):
    response = requests.get(url, headers=HEADERS);
    source = response.text;
    return source;

def extraxt(source):
    extraxtor = selectorlib.Extractor.from_yaml_file("extraxt.yaml");
    value = extraxtor.extract(source)["tours"];
    return value;

def send_email(message):
    host = "smtp.gmail.com";
    port = 465;

    username = "tihpmirtx88@gmail.com";
    password = api_key;

    receiver = "tihpmirtx88@gmail.com"
    context = ssl.create_default_context();

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n");

def read(extracted):
    try:
        with open("data.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""

while True:
    if __name__ == "__main__":
        scraped = scrape(URL);
        extracted = extraxt(scraped);
        content = read(extracted);

        if extracted not in content:
            store(extracted)
            send_email(message="New event found boy")
        time.sleep(2);
