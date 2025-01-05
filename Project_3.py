"""
projekt_3.py: Third project to Engeto Online Python Akademie

author: Tereza Písecká
email: pisecka.tereza@seznam.cz
discord: TerkaP terka_41921
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
import re

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode(response.apparent_encoding, errors="replace")

def extract_municipality_data(soup, base_url):
    municipalities = []
    rows = soup.find_all("tr")[2:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        code = cols[0].text.strip()
        location = cols[1].text.strip()
        link = cols[0].find("a")

        if code and location and link:
            municipality_url = f"{base_url}/{link['href']}"
            municipality_data = get_municipality_details(municipality_url)
            municipality_data.update({
                "code": code,
                "location": location,
            })
            municipalities.append(municipality_data)
    
    return municipalities

def get_municipality_details(url):
    html = fetch_data(url)
    soup = BeautifulSoup(html, "html.parser")

    registered_voters, envelopes, valid = extract_table_1_data(soup)

    additional_attributes = get_additional_attributes(soup)

    return {
        "registered_voters": registered_voters,
        "envelopes": envelopes,
        "valid": valid,
        **additional_attributes,
    }

def extract_table_1_data(soup):
    table = soup.find("table")
    if not table:
        return "Not found", "Not found", "Not found"
    
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 7:
            try:
                registered_voters = cols[3].text.strip()
                envelopes = cols[4].text.strip()
                valid = cols[7].text.strip()
                return registered_voters, envelopes, valid
            except IndexError:
                print("IndexError: Table structure might have changed.")
                continue
    return "Not found", "Not found", "Not found"

def get_additional_attributes(soup):
    tables = soup.find_all("table")[1:3]
    additional_attributes = {}
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 2:
                attribute_name = cols[1].text.strip()
                attribute_value = cols[2].text.strip()
                if attribute_name:
                    additional_attributes[attribute_name] = attribute_value
    return additional_attributes

def save_to_csv(data, filename="municipality_data.csv"):
    fixed_fields = ["code", "location", "registered_voters", "envelopes", "valid"]

    additional_fields = []
    for row in data:
            for key in row.keys():
                if key not in fixed_fields and key not in additional_fields:
                    additional_fields.append(key)

    fieldnames = fixed_fields + additional_fields

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()

        for row in data:
            writer.writerow(row)

    print(f"Data successfully saved to {filename}")

def is_valid_url(url):
    regex = r'^(https?://)?(www\.)?[\w-]+\.[a-z]+(/[\w-]*)*'
    return re.match(regex, url) is not None

def main():
    if len(sys.argv) != 3:
        print("Url link or output filename is missing.")
        return

    url = sys.argv[1]
    output_filename = sys.argv[2]

    if not is_valid_url(url):
        print("Error: The URL provided is invalid.")
        return

    base_url = '/'.join(url.split('/')[:-1])
    print(f"Fetching main page: {url}")
    try:
        html = fetch_data(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")

    municipalities = extract_municipality_data(soup, base_url)

    save_to_csv(municipalities, output_filename)

if __name__ == "__main__":
    main()
