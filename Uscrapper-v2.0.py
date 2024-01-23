import requests
from bs4 import BeautifulSoup
import random
import argparse
import re
from termcolor import colored
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import signal
from datetime import datetime

print("\n")
print(colored("   █░█","blue"),colored("█▀ █▀▀ █▀█ ▄▀█ █▀█ █▀█ █▀▀ █▀█  ","white",attrs=['bold']))
print(colored("   █▄█","blue"),colored("▄█ █▄▄ █▀▄ █▀█ █▀▀ █▀▀ ██▄ █▀▄ ","white", attrs=['bold']),colored("(v2.0)","blue",))

print(colored("\n   A Powerfull OSINT WebScrapper","yellow"))
print(colored("          ~By: Pranjal Goel (z0m31en7)\n", "red"))

extracted_usernames0 = []
extracted_phone_numbers0 = []
extracted_emails0 = []
geolocations0 = []
author_names0 = []
social_links0 = []
email_addresses0 = []
counter = 0
driver = 0
email_addresses1 = []
social_links1 = []
extracted_emails1 = []
author_names1 = []
geolocations1 = []
extracted_phone_numbers1 = []
extracted_usernames1 = []
report_content = ""
link_list = ""

def handler(signum, frame):
    res = input(colored("\n[x] Ctrl-c was pressed. Do you really want to exit? y/n: ","red"))
    if res == 'y':
        print(colored("[exiting..]","red"))
        exit(1)

def selenium_wd(url):

    global counter
    global driver
    options = Options()
    options.add_argument('-headless')
    if counter == 0:
        driver = webdriver.Firefox(options=options)
        counter = 1
    driver.get(url)
    source = driver.page_source
    return source

def get_links_from_page(url):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        domain = urlparse(url).netloc


        links = set()
        for anchor in soup.find_all("a", href=True):
            link = anchor["href"]
            absolute_link = urljoin(url, link)
            parsed_link = urlparse(absolute_link)


            if parsed_link.netloc == domain and parsed_link.scheme in {"http", "https"}:
                links.add(absolute_link)

        return links

    if response.status_code != 200 and response.status_code != 404:
        soup = BeautifulSoup(selenium_wd(url),"html.parser")
        domain = urlparse(url).netloc


        links = set()
        for anchor in soup.find_all("a", href=True):
            link = anchor["href"]
            absolute_link = urljoin(url, link)
            parsed_link = urlparse(absolute_link)


            if parsed_link.netloc == domain and parsed_link.scheme in {"http", "https"}:
                links.add(absolute_link)

        return links

    else:
        print(f"Error: Unable to fetch {url}. Status code: {response.status_code}")
        return set()

def web_crawler(start_url, max_pages=10, num_threads=4):

    if num_threads == None:
       num_threads = 4
    visited_links = set()
    queue = [start_url]

    def crawl_page(url):
        global link_list
        if url in visited_links:
            return set()

        print(f"Crawling: {url}")
        link_list += url
        link_list += "\n"
        extract_details(url, args.generate_report, args.nonstrict)
        links_on_page = get_links_from_page(url)
        visited_links.add(url)
        return links_on_page

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while queue and len(visited_links) < max_pages:
            current_url = queue.pop(0)

            future = executor.submit(crawl_page, current_url)
            links_on_page = future.result()

            for link in links_on_page:
                if link not in visited_links:
                    queue.append(link)

    print("Crawling finished.")


def extract_details(url, generate_report, non_strict):

    user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.3'
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Mobile/15E148 Safari/604.'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' ]

    response = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200 and response.status_code != 404:
       soup = BeautifulSoup(selenium_wd(url), 'html.parser')

    usernames = []
    if non_strict:
        usernames = set(username.string for username in soup.find_all('a', href=True, string=re.compile(r'^[^\s]+$')))

    email_addresses = set(email['href'].replace('mailto:', '') for email in soup.find_all('a', href=lambda href: href and 'mailto:' in href))
    social_links = set(link['href'] for link in soup.find_all('a', href=True))
    author_names = set(author['content'] for author in soup.find_all('meta', attrs={'name': 'author'}))
    geolocations = set(location['content'] for location in soup.find_all('meta', attrs={'name': 'geo.position'}))

    webpage_text = soup.get_text()

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    extracted_emails = set(re.findall(email_regex, webpage_text))
    phone_regex3 = r'\(\d{3}\)\s\d{3}\s\d{5}'
    phone_regex = r'\b\+?\d{10,12}\b'
    phone_regex2 = r'(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}\)?[- ]?\d{4}\b'
    phone_regex_combined = '|'.join('(?:{0})'.format(x) for x in (phone_regex, phone_regex2, phone_regex3))
    extracted_phone_numbers = set(re.findall(phone_regex_combined, webpage_text))
    username_regex = r'@[A-Za-z0-9_]+'
    extracted_usernames = set(re.findall(username_regex, webpage_text))

    if email_addresses:
        for email in email_addresses:
            email_addresses0.append(email)

    if social_links:
        social_media_platforms = ['instagram', 'facebook', 'whatsapp', 'snapchat', 'github', 'reddit', 'youtube', 'linkedin', 'twitter', 'telegram', 'discord','pinterest']
        for link in social_links:
            for platform in social_media_platforms:
                if platform in link:
                    social_links0.append(link)

    if author_names:
        for author in author_names:
            author_names0.append(author)

    if geolocations:
        for location in geolocations:
            geolocations0.append(location)

    if extracted_emails:
       for email in extracted_emails:
            if email.lower().startswith("email"):
                email = email[5:]
            extracted_emails0.append(email)

    if extracted_phone_numbers:
        for phone in extracted_phone_numbers:
            extracted_phone_numbers0.append(phone)

    if extracted_usernames and non_strict:
        for username in extracted_usernames:
            extracted_usernames0.append(username)

def printlist():

    global email_addresses1
    global social_links1
    global extracted_emails1
    global author_names1
    global geolocations1
    global extracted_phone_numbers1
    global extracted_usernames1

    if email_addresses0:
        print(colored("\n[+] Email Addresses:", "cyan"))
        email_addresses1 = list(OrderedDict.fromkeys(email_addresses0))
        for email in email_addresses1:
            print(email)

    if social_links0:
        print(colored("\n[+] Social Media Links:", "cyan"))
        social_links1 = list(OrderedDict.fromkeys(social_links0))
        for links in social_links1:
            print(links)

    if author_names0:
        print(colored("\n[+] Author Names:", "cyan"))
        author_names1 = list(OrderedDict.fromkeys(author_names0))
        for author in author_names1:
            print(author)

    if geolocations0:
        print(colored("\n[+] Geolocations:", "cyan"))
        geolocations1 = list(OrderedDict.fromkeys(geolocations0))
        for location in geolocations1:
            print(location)

    if extracted_emails0 or extracted_phone_numbers0 or extracted_usernames0:
        print(colored("\n----------Non-Hyperlinked Details----------", "yellow"))

    if extracted_emails0:
        print(colored("\n[+] Email Addresses:", "cyan"))
        extracted_emails1 = list(OrderedDict.fromkeys(extracted_emails0))
        for email in extracted_emails1:
            print(email)

    if extracted_phone_numbers0:
        print(colored("\n[+] Phone Numbers:", "cyan"))
        extracted_phone_numbers1 = list(OrderedDict.fromkeys(extracted_phone_numbers0))
        for phone in extracted_phone_numbers1:
            print(phone)

    if extracted_usernames0 and non_strict:
        print(colored("\n[+] Usernames:", "cyan"))
        extracted_usernames1 = list(OrderedDict.fromkeys(extracted_usernames0))
        for username in extracted_usernames1:
            print(username)
 
    concl = "Email Addresses:"+str(len(email_addresses1)+len(extracted_emails1)),"Social Links:"+str(len(social_links1)),"Phone Numbers:"+str(len(extracted_phone_numbers1)), "Geolocations:"+str(len(geolocations1))
    print("\n")
    print(colored(concl, "green", attrs=['blink']))
    print("\n")
    if args.generate_report:
       generate_report()
    if counter != 0:
       driver.quit()
    exit(1)

def generate_report():

    global report_content
    report_content = "\nTARGET: "+url+"\n\n"

    if args.crawl:
       report_content += "[!] URLs Scrapped:\n"
       report_content += link_list

    report_content += "\n{Email Addresses:"+str(len(email_addresses1)+len(extracted_emails1))+", Social Links:"+str(len(social_links1))+", Phone Numbers:"+str(len(extracted_phone_numbers1))+", Geolocations:"+str(len(geolocations1))+"}\n"

    if email_addresses1:
        report_content += "\n[+] Email Addresses:\n"
        for email in email_addresses1:
            report_content += email
            report_content += '\n'

    if social_links1:
        report_content += "\n[+] Social Media Links:\n"
        for links in social_links1:
            report_content += links
            report_content += '\n'

    if author_names1:
        report_content += "\n[+] Author Names:\n"
        for author in author_names1:
            report_content += author
            report_content += '\n'

    if geolocations1:
        report_content += "\n[+] Geolocations:\n"
        for location in geolocations1:
            report_content += location
            report_content += '\n'

    if extracted_emails1 or extracted_phone_numbers1 or extracted_usernames1:
        report_content += "\n----------Non-Hyperlinked Details----------\n"

    if extracted_emails1:
        report_content += "\n[+] Email Addresses:\n"
        for email in extracted_emails1:
            report_content += email
            report_content += '\n'

    if extracted_phone_numbers1:
        report_content += "\n[+] Phone Numbers:\n"
        for phone in extracted_phone_numbers1:
            report_content += phone
            report_content += '\n'

    if extracted_usernames1 and non_strict:
        report_content += "\n[+] Usernames:\n"
        for username in extracted_usernames1:
            report_content += phone
            report_content += '\n'

    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{formatted_date_time}.txt"
    
    try:

        with open(file_name, 'w') as file:
            # Write the report content to the file
            file.write(report_content)
        print(f"Report saved to {file_name} successfully.")
    except Exception as e:
        print(f"Error while saving the report: {e}")
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OSINT Tool for Webpage scraping')
    parser.add_argument('-u', '--url', help='URL of the website')
    parser.add_argument('-O', '--generate-report', action='store_true', help='Generate a report')
    parser.add_argument('-ns', '--nonstrict', action='store_true', help='Display non-strict usernames (may show inaccurate results)')
    parser.add_argument('-c', '--crawl', type=int, help= 'specify max number of links to  Crawl and scrape within the same scope')
    parser.add_argument('-t', '--threads', type=int, help= 'Number of threads to utilize while crawling (default=4)')
    args = parser.parse_args()
    signal.signal(signal.SIGINT, handler)
    counter = 0

    if args.url:
        url = args.url
        print(colored("TARGET:","magenta"), colored(url,"green"))
        if not url.startswith('http://') and not url.startswith('https://'):
             url = 'https://' + url
        try:
             response = requests.get(url)
             if response.status_code == 200:
                 if args.crawl:
                     web_crawler(url, args.crawl, args.threads)
                     printlist()
                 extract_details(url, args.generate_report, args.nonstrict)
                 printlist()
                 generate_report()

             if response.status_code != 200 and response.status_code != 404:
                print(colored("\n[!] Status code:","red"),colored(response.status_code,"red"),colored("Website might be using anti webscrapping methods.", "red"))
                print(colored("[+] Trying to bypass...","green"))
                if args.crawl:
                    web_crawler(url, args.crawl, args.threads)
                extract_details(url, args.generate_report, args.nonstrict)
                printlist()

             else:
                 print(f"URL is down: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
             print("Error occurred while checking the link:", e)
    else:
        print("Please provide the URL using the -u/--url option.")
