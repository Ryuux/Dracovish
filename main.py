import requests
from bs4 import BeautifulSoup
import csv
import logging
from datetime import datetime
from colorama import Fore, Style, init

init()

logging.basicConfig(filename='scraping.log', level=logging.ERROR)

def scrape_links(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')

        links = soup.find_all('a')
        urls = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('http') and '.' in link.get('href')]

        return urls
    except requests.exceptions.RequestException as e:
        logging.error(Fore.RED + f'Error scraping {url}: {e}' + Style.RESET_ALL)

def write_csv_file(filename, data):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([Fore.BLUE + 'URL' + Style.RESET_ALL])
            for url in data:
                writer.writerow([url])
            print(Fore.GREEN + f'[{len(data)}] URLs scraped successfully.' + Style.RESET_ALL)
    except Exception as e:
        logging.error(Fore.RED + f'Error writing to {filename}: {e}' + Style.RESET_ALL)

def scrape_and_write(url):
    try:
        urls = scrape_links(url)
        if urls:
            now = datetime.now()
            filename = now.strftime('%Y-%m-%d-%H-%M-%S') + '.csv'
            write_csv_file(filename, urls)
    except Exception as e:
        logging.error(Fore.RED + f'Error scraping {url}: {e}' + Style.RESET_ALL)

if __name__ == '__main__':
    url = input(Fore.YELLOW + 'Web: ' + Style.RESET_ALL)
    scrape_and_write(url)
