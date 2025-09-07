import requests
import selectorlib
import smtplib
import os
from dotenv import load_dotenv
import time
import sqlite3
from email.message import EmailMessage

URL = "https://programmer100.pythonanywhere.com/tours/";
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'};

load_dotenv();

api_key = os.getenv("API_KEY");

connection = sqlite3.connect("data.db");

def scrape(url):
    response = requests.get(url, headers=HEADERS);
    source = response.text;
    return source;

def extraxt(source):
    extraxtor = selectorlib.Extractor.from_yaml_file("extraxt.yaml");
    value = extraxtor.extract(source)["tours"];
    return value;

def send_email(extracted):
    email_message = EmailMessage()
    email_message["subject"] = "New tour event detected!"
    email_message["From"] = "tihomirtx88@gmail.com"
    email_message["To"] = "tihomirtx88@gmail.com"

    if extracted == "No upcoming tours":
        email_message.set_content("No upcoming tours found.")
    else:
        # You can include the band, city, date in the email
        email_message.set_content(f"New tour event found:\n{extracted}")

    # Use starttls() for port 587
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login("tihomirtx88@gmail.com", api_key)  # app password
        server.send_message(email_message)
        print("✅ Email sent successfully!")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row];

    cursor = connection.cursor();
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row);
    connection.commit();

def read(extracted):
    if extracted == "No upcoming tours":
        return []

    row = extracted.split(",")
    row = [item.strip() for item in row]

    if len(row) != 3:
        return []

    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date,))
    rows = cursor.fetchall()
    return rows

while True:
    if __name__ == "__main__":
        scraped = scrape(URL);
        extracted = extraxt(scraped);

        if extracted != "No upcoming tours":
            row = read(extracted);
            if not row:
                store(extracted);
                send_email(extracted)

        time.sleep(2);
