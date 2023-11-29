import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36',
        # We can also add more agents if needed
    ]
    return random.choice(user_agents)

def scrape_real_estate_by_location(location_url):
    try:
        headers = {'User-Agent': get_random_user_agent()} # Sending HTTP request to the URL
        response = requests.get(location_url, headers=headers)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')  # Parsing the HTML content of the page

        listings = soup.find_all('div', class_='Box__BoxElement-sc-569ce14e-0 cGqbvd PropertyCard__PropertyCardContainer-sc-b3be8eee-4 eDPGkq')  # Locating HTML elements

        scraped_data = []

        for listing in listings:
            title = listing.find('div', class_='Text__TextBase-sc-53dad1a1-0-div Text__TextContainerBase-sc-53dad1a1-1 hivKgb dUGKZQ').text.strip()
            price = listing.find('div', class_='Text__TextBase-sc-53dad1a1-0-div Text__TextContainerBase-sc-53dad1a1-1 eNyLOr cyTrTF').text.strip()
            property_url = 'https://www.trulia.com' + listing.find('a', class_='Anchor__StyledAnchor-sc-3c3ff02e-1 doURDx')['href'].strip()

            scraped_data.append({'Title': title, 'Price': price, 'PropertyURL': property_url})

            time.sleep(random.uniform(1, 3))

        csv_filename = 'real_estate_data_Atlanta_GA.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Title', 'Price', 'PropertyURL']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(scraped_data)

        print(f"Scraped data saved to {csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


scrape_real_estate_by_location('https://www.trulia.com/GA/Atlanta/')
