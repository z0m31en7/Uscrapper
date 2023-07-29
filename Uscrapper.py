import requests
from bs4 import BeautifulSoup
import argparse
import re
from termcolor import colored
from urllib.parse import urlparse

print("\n")
print("   █░█ █▀ █▀▀ █▀█ ▄▀█ █▀█ █▀█ █▀▀ █▀█")
print("   █▄█ ▄█ █▄▄ █▀▄ █▀█ █▀▀ █▀▀ ██▄ █▀▄  (v1)")

print(colored("\n   A Webpage scrapper for OSINT.","yellow"))
print(colored("          ~By: Pranjal Goel (z0m31en7)\n", "red"))

def extract_details(url, generate_report, non_strict):
    
    user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.3'
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Mobile/15E148 Safari/604.'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
]
    response = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    soup = BeautifulSoup(response.text, 'html.parser')

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
        print(colored("\n[+] Email Addresses:", "cyan"))
        for email in email_addresses:
            print(email)

    if social_links:
        print(colored("\n[+] Social Media Links:", "cyan"))
        social_media_platforms = ['instagram', 'facebook', 'whatsapp', 'snapchat', 'github', 'reddit', 'youtube', 'linkedin', 'twitter', 'telegram', 'imo', 'discord']
        for link in social_links:
            for platform in social_media_platforms:
                if platform in link:
                    print(link)

    if author_names:
        print(colored("\n[+] Author Names:", "cyan"))
        for author in author_names:
            print(author)

    if geolocations:
        print(colored("\n[+] Geolocations:", "cyan"))
        for location in geolocations:
            print(location)

    if generate_report:
        with open('report.txt', 'w') as report_file:
            if usernames:
                report_file.write("[+] Usernames:\n")
                for username in usernames:
                    report_file.write(username + '\n')

            if email_addresses:
                report_file.write("\n[+] Email Addresses:\n")
                for email in email_addresses:
                    report_file.write(email + '\n')

            if extracted_phone_numbers:
                report_file.write("\n[+] Phone Numbers:\n")
                for phone in extracted_phone_numbers:
                    report_file.write(phone + '\n')

            if social_links:
                report_file.write("\n[+] Social Media Links:\n")
                for link in social_links:
                    report_file.write(link + '\n')

            if author_names:
                report_file.write("\n[+] Author Names:\n")
                for author in author_names:
                    report_file.write(author + '\n')

            if geolocations:
                report_file.write("\n[+] Geolocations:\n")
                for location in geolocations:
                    report_file.write(location + '\n')

    if extracted_emails or extracted_phone_numbers or extracted_usernames:
        print(colored("\n----------Non-Hyperlinked Details----------", "yellow"))

    if extracted_emails:
        print(colored("\n[+] Email Addresses:", "cyan"))
        for email in extracted_emails:
            if email.lower().startswith("email"):
                email = email[5:]
            print(email)

    if extracted_phone_numbers:
        print(colored("\n[+] Phone Numbers:", "cyan"))
        for phone in extracted_phone_numbers:
            print(phone)

    if extracted_usernames and non_strict:
        print(colored("\n[+] Usernames:", "cyan"))
        for username in extracted_usernames:
            print(username)
    print("\n")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OSINT Tool for Webpage scraping')
    parser.add_argument('-u', '--url', help='URL of the website')
    parser.add_argument('-O', '--generate-report', action='store_true', help='Generate a report')
    parser.add_argument('-ns', '--nonstrict', action='store_true', help='Display non-strict usernames (may show inaccurate results)')
    args = parser.parse_args()

    if args.url:
        url = args.url
        print(colored("TARGET:","magenta"), colored(url,"green"))
        if not url.startswith('http://') and not url.startswith('https://'):
             url = 'https://' + url
        try:
             response = requests.get(url)
             if response.status_code == 200: 
                 extract_details(url, args.generate_report, args.nonstrict)
             else:
                 print(f"URL is down: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
             print("Error occurred while checking the link:", e)
    else:
        print("Please provide the URL using the -u/--url option.")
