from bs4 import BeautifulSoup
from multiprocessing import Process
import numpy as np
import requests
import pickle


def fetchURLs():
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
    source = requests.get(url).content
    soup = BeautifulSoup(source, 'lxml')

    # Get generations
    gens = soup.find('li', class_=['toclevel-1',
                                   'tocsection-1']).find_all('li')
    generations = [gen.text.split(' ', 1)[1] for gen in gens]

    tables = soup.find_all('table')
    links = {}

    # Get the pokemon page link from the table
    for _ in range(len(generations)):
        rows = tables[_+1].find_all('tr')
        links[generations[_]] = list(set([
            f"https://bulbapedia.bulbagarden.net{rows[i].find_all('a')[1]['href']}" for i in range(1, len(rows))]))
    return links


def getDownloadLink(link):
    source = requests.get(link).content
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('table', class_='roundy').find(
        'table', class_='roundy').find('table', class_='roundy')
    links = table.find_all('a')
    pageLinks = [f"https://bulbapedia.bulbagarden.net{link['href']}"
                 for link in links if link['href'].startswith('/wiki/File:')]
    return pageLinks


def getImageLink(link):
    source = requests.get(link).content
    soup = BeautifulSoup(source, 'lxml')
    return (soup.find(id='firstHeading').text, f"https:{soup.find('div', class_='fullMedia').find('a')['href']}")


def downloadGeneration(gen, arr):
    links = []
    count = 0
    for a in arr:
        for pageLink in getDownloadLink(a):
            links.append(getImageLink(pageLink))
            count += 1
            print(count)
    file = open(gen, 'wb')
    pickle.dump(links, file)
    file.close()


def main():
    links = fetchURLs()
    for link in links:
        p = Process(target=downloadGeneration, args=[link, links[link]])
        p.start()


if __name__ == '__main__':
    main()
