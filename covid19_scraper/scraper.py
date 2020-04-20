"""
Very simple script for scraping some local news sites for corona virus news.
"""


import bcolors
import requests
from bs4 import BeautifulSoup


# URLs to scrape
RESOURCES = {
    "nezavisne": "https://www.nezavisne.com/index/najnovije_vijesti",
    "srpskainfo": "https://srpskainfo.com/sve-vijesti/",
    "n1info": "http://ba.n1info.com/Najnovije",
    "klix": "https://www.klix.ba/najnovije",
    "avaz": "https://avaz.ba/najnovije"
}

# selectors for targeting news links
CSS_SELECTORS = {
    "nezavisne": "div.media.clearfix > div.media-body > h5.media-heading > a",
    "srpskainfo": "div.article-content > div.entry-header > h3.entry-title > a",
    "n1info": "article.news-wrapper > div.text-wrapper > h2.title > a",
    "klix": "article.kartica > a",
    "avaz": "div.top-article-four > div.article-info > div.article-title > h4 > a"
}

# keywords to filter URLs by
KEYWORDS = [
    "korona",
    "kovid",
    "covid",
    "sars",
    "virus",
    "zaražen"
]


print("\nScraping news sites for corona virus news...\n\n")

for site in RESOURCES:
    # if no selector is specified for scraping
    if site not in CSS_SELECTORS:
        print("\n\n{}{}:{}".format(bcolors.HEADER, site.upper(), bcolors.ENDC))
        print("\nPlease define a CSS selector!\n".format(site))
        continue

    page = requests.get(RESOURCES[site])
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.select(CSS_SELECTORS[site])

    output = {}

    for article in articles:
        link = article['href']

        # relative links fixes
        if link.startswith("//"):
            link = link[2:]
        if site+"." not in link:
            link = RESOURCES[site][:RESOURCES[site].rfind('/')] + link

        # klix stores title in a different element
        title = article.text if site != 'klix' else article.findChildren('h1', recursive=False)[0].text

        for keyword in KEYWORDS:
            if keyword.lower() in title.lower():
                output[title] = link

    print("\n\n{}{} ({}):{}".format(bcolors.HEADER, site.upper(), len(output), bcolors.ENDC))
    for key in output:
        print("{}\n  -> {}{}{}".format(key, bcolors.BLUEIC, output[key], bcolors.ENDC))
