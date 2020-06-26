import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import time

# URL header to build
pdx_url = "http://puzzledragonx.com/en/img/monster/MONS_"
pdx_mon_url = "http://puzzledragonx.com/en/monster.asp?n="

# Black-list IDs
black_listed = ('94', '92', '90', '88', '96', '681')

# Black-listed 5* (disable this when parsing 6*)
black_listed_gods = ('1424', '1589', '2103', '1372', '1241')

def remove_non_ascii_1(text):
    """
    Remove extended ASCII characters resulting from trying to
    translate JP names to ENG
    """
    return ''.join(i for i in text if ord(i)<128)

def scrape(url, file):
    """
    Take in the formatted HTML, scrape for the desired elements,
    and write to a file generating all the desired URLS
    """
    # Open file to write output to
    # f_rem_urls = open("rem_urls.txt", "w")

    rem_src = requests.get(url)
    rem_plain_txt = rem_src.text
    rem_soup = BeautifulSoup(rem_plain_txt, features="html.parser")

    f_rem_urls = open(f"{file}", "w+")
    links = rem_soup.find_all(class_= "onload")
    numlinks = len(links)
    print(f"{numlinks} monsters ready to be scraped")
    # Traverse HTML of all monsters queried
    printProgressBar(0, numlinks, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    for i, link in enumerate(links):
        mon_id = link.get('data-original')
        if mon_id is None:
            continue
        # Build URL for non-blacklisted monsters
        mon_nbr = mon_id[14:].strip('.png')
        if mon_nbr in black_listed or mon_nbr in black_listed_gods or int(mon_nbr) >= 1946:
            continue
        mon_img = f"{pdx_url}{mon_nbr}.jpg"
        mon_url = f"{pdx_mon_url}{mon_nbr}"
        mon_src = requests.get(mon_url)
        mon_txt = mon_src.text
        mon_soup = BeautifulSoup(mon_txt, features="html.parser")
        #series
        mon_s = mon_soup.find_all("span", string = re.compile("Series"))
        mon_series = ""
        for s in mon_s:
            mon_series += s.string + "/"
        mon_series = mon_series[:-1]
        mon_m = mon_soup.find_all("meta", {"name":"description"})
        mon_meta = mon_m[0].get('content').split(" monster")
        #name and attributes/elements
        [mon_name, mon_att] = mon_meta[0].split(" is a ")
        #rarity and types
        [mon_rarity, mon_types] = mon_meta[1].split(" stars ")
        mon_att = mon_att.replace(" and ", "/")
        mon_rarity = f"{mon_rarity[-1:]} stars"

        f_rem_urls.write(f"{mon_img}@ {mon_name}@ {mon_att}@ {mon_rarity}@ {mon_types}@ {mon_series}\n") 

        time.sleep(0.1)
        printProgressBar(i + 1, numlinks, prefix = 'Progress: ', suffix = 'Complete', length = 50)
        
    f_rem_urls.close()
    print("Finished!")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def main():
    """
    main
    """
    # Get URL to all fodder and 5* gods
    url_rem = "http://puzzledragonx.com/en/monsterbook.asp?r=3,4,5&s=47,48,53,37,107,29,94,81,8,13,44,9,11,80,24,98,14,68,12,66,10,30,31,43,33,86,27,82,104&b1=1#view"

    # Get URL to GFE's (separated in two categories)
    url_gfe1 = "http://puzzledragonx.com/en/monsterbook.asp?r=5&s=197&b1=1#view"

    # Get URL to more GFE's
    url_gfe2 = "http://puzzledragonx.com/en/monsterbook.asp?r=6&s=54&b1=1#view"

    # Request URL to scrape from user
    url = input("Enter PADx URL to scrape: ")
    file = input("Destination file: ")

    # Extract and format HTML from URL
    
    print("Scraping...")
    start = time.perf_counter()
    scrape(url, file)
    end = time.perf_counter()
    print(f"Scraping completed in {end - start} seconds.")

if __name__ == "__main__":
    main()