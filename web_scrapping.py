import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import csv

#DON'T FORGET TO CHANGE THE CSV FILE NAME DOWN IN DRIVER CODE

def get_all_links(url_list):
    links = []
    for url in url_list:
        #Get HTML content
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        #Get all links from each url
        for link in soup.find_all("a"):
            href = link.get("href")
            if href is not None:
                links.append(href)

    return links

def get_emails(url_list):
    emails = []
    for each_url in url_list:
        #text = "contact me at alijodat16@gmail.com for further information."
        response = requests.get(each_url)
        html_content = response.text
        # Pattern for email matching
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        curr_url_emails = re.findall(email_pattern, html_content)
        #print(curr_url_emails)
        if curr_url_emails not in emails:
            emails = emails + curr_url_emails

        #print(emails)
    return emails

def write_emails_in_file(email_list, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # each email in separate row
        for row in email_list:
            writer.writerow([row])
    
    print('Successfully written in file : ', filename)

urls = pd.read_csv('urls.csv')  #CHANGE THE CSV FILE NAME
#print(urls)
url_list = urls.to_numpy().flatten()
#all_links = get_all_links(url_list)
#cleaned_links = [url for url in all_links if url.startswith('https://')]
#print(cleaned_links)
emails = get_emails(url_list)
# Print the found email addresses
emails = np.unique(emails)
#print(emails)

output_file = "extracted_emails.csv"
write_emails_in_file(emails,output_file)

