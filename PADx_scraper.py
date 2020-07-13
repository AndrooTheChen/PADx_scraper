import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import time
import os

# URL header to build
pdx_url = "http://puzzledragonx.com/en/img/monster/MONS_"
pdx_mon_url = "http://puzzledragonx.com/en/monster.asp?n="

# Black-list IDs
black_listed = ('94', '92', '90', '88', '96', '681')

# Black-listed 5* (disable this when parsing 6*)
black_listed_gods = ('1424', '1589', '2103', '1372', '1241')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def scrape(url, dfile):
    """
    Take in the formatted HTML, scrape for the desired elements,
    and write to a dfile generating all the desired URLS
    """
    # Open dfile to write output to
    # f_rem_urls = open("rem_urls.txt", "w")

    rem_src = requests.get(url)
    rem_plain_txt = rem_src.text
    rem_soup = BeautifulSoup(rem_plain_txt, features="html.parser")

    f_rem_urls = open(f"{dfile}", "w+")
    links = rem_soup.find_all(class_= "onload")
    numlinks = len(links)
    count=0
    print(f"{numlinks} monsters ready to be scraped")
    # Traverse HTML of all monsters queried
    for i, link in enumerate(links):
        printProgressBar(i, numlinks, prefix = 'Progress: ', suffix = 'Complete', length = 50)
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
        #print(f"{mon_img}@ {mon_name}@ {mon_att}@ {mon_rarity}@ {mon_types}@ {mon_series}\n" )
        f_rem_urls.write(f"{mon_img}@ {mon_name}@ {mon_att}@ {mon_rarity}@ {mon_types}@ {mon_series}\n") 
        count += 1
        time.sleep(0.1)
        printProgressBar(i + 1, numlinks, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    
    printProgressBar(numlinks, numlinks, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    f_rem_urls.close()
    print(f"Finished! {count} monsters successfully scraped.")

def imageScrape(ifile, dfoldr):
    """
    Take in the formatted HTML, scrape for the desired elements,
    and write to a dfile generating all the desired URLS
    """
    # Checks existence of input file and output destination
    # Creates output folder(s) if DNE
    dest = dfoldr
    if dest == "":
        dest = "img"

    if not os.path.exists(ifile):
        print(f"No such file or directory: '{ifile}'")
        return 1
    
    if not os.path.exists(dest):
        os.makedirs(dest)
        os.makedirs(dest+"/monster")
        os.makedirs(dest+"/thumbnail")
    else:
        if not os.path.exists(dest+"/monster"):
            os.makedirs(dest+"/monster")
        if not os.path.exists(dest+"/thumbnail"):
            os.makedirs(dest+"/thumbnail")

    #Reads in input file
    rfile= open(f"{ifile}", "r")
    lines = rfile.readlines()

    iCantCount = len("http://puzzledragonx.com/en/img/")
    numLines = len(lines)
    count=0
    print(f"{numLines} monsters ready to be scraped")
    # Traverse all monsters in ifile and save monster and thumbnail images in local directory
    for i, line in enumerate(lines):
        printProgressBar(i, numLines, prefix = 'Progress: ', suffix = 'Complete', length = 50)
        
        #path: img/monster/MONS_{number}.jpg
        #saved as: {dest}/monster/MONS_{number}.jpg
        link = line.split("@")[0]
        imgName = link[iCantCount:]
        imgData = requests.get(link).content
        with open(f"{dest}/{imgName}", 'wb') as handler:
            handler.write(imgData)
        
        #path: img/thumbnail/{number}.png
        #saved as: {dest}/thumbnail/{number}.png
        thumbLink = "thumbnail/".join(link.split("monster/MONS_"))[:-3] + "png"
        thumbImgName = thumbLink[iCantCount:]
        thumbImgData = requests.get(thumbLink).content
        with open(f"{dest}/{thumbImgName}", 'wb') as handler:
            handler.write(thumbImgData)
        
        count += 1
        time.sleep(0.1)
        printProgressBar(i + 1, numLines, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    
    printProgressBar(numLines, numLines, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    print(f"Finished! {count} monsters successfully scraped.")

    return 0


def main():
    """
    main
    """
    # Get URL to all fodder and 5* gods
    #url_rem = "http://puzzledragonx.com/en/monsterbook.asp?r=3,4,5&s=47,48,53,37,107,29,94,81,8,13,44,9,11,80,24,98,14,68,12,66,10,30,31,43,33,86,27,82,104&b1=1#view"

    # Get URL to GFE's (separated in two categories)
    #url_gfe1 = "http://puzzledragonx.com/en/monsterbook.asp?r=5&s=197&b1=1#view"

    # Get URL to more GFE's
    #url_gfe2 = "http://puzzledragonx.com/en/monsterbook.asp?r=6&s=54&b1=1#view"

    #Michael's scrape URL: http://puzzledragonx.com/en/monsterbook.asp?e1=3&r=5&s=47&b1=1#view
    # Select mode
    print("\nModes of operation:\n 1) Scrape info\n 2) Scrape images & download\n")
    mode = input("Select mode (1 or 2): ")
    operation = scrape
    url = ""
    dfile = ""

    if mode == "1":
        # Request URL to scrape from user
        url = input("Enter PADx URL to scrape: ")
        dfile = input("Destination file: ")
    elif mode == "2":
        # Request files from user
        url = input("Info-scraped file: ")
        dfile = input("Destination of images (leave empty for standard path): ")
        operation = imageScrape
    else:
        print("Invalid input. Please just use 1 or 2. Exiting.")
        return

    # Extract and format HTML from URL
    
    print("Scraping...")
    start = time.perf_counter()
    if (operation(url, dfile)):
        print("Exiting.")
        return
    end = time.perf_counter()
    print("Scraping completed in {:.2f} seconds.\n" .format(end - start))

if __name__ == "__main__":
    main()