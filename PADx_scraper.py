import requests
from bs4 import BeautifulSoup
import urllib.request


def remove_non_ascii_1(text):
    """
    Remove extended ASCII characters resulting from trying to
    translate JP names to ENG
    """
    return ''.join(i for i in text if ord(i)<128)

# Get URL to all fodder and 5* gods
url_rem = "http://puzzledragonx.com/en/monsterbook.asp?r=3,4,5&s=47,48,53,37,107,29,94,81,8,13,44,9,11,80,24,98,14,68,12,66,10,30,31,43,33,86,27,82,104&b1=1#view"

# Get URL to GFE's (separated in two categories)
url_gfe1 = "http://puzzledragonx.com/en/monsterbook.asp?r=5&s=197&b1=1#view"

# Get URL to more GFE's
url_gfe2 = "http://puzzledragonx.com/en/monsterbook.asp?r=6&s=54&b1=1#view"

# Extract and format HTML from URL
rem_src = requests.get(url_rem)
rem_plain_txt = rem_src.text
rem_soup = BeautifulSoup(rem_plain_txt)

# Open file to write output to
f_rem_urls = open("rem_urls.txt", "w")

pdx_url = "http://puzzledragonx.com/en/img/monster/MONS_"

# Traverse HTML of all monsters queried
for link in rem_soup.find_all("img", {"class": "onload"}):
    mon_id = link.get('data-original')
    if mon_id is None:
        continue

    mon_name_struct = link.get('title').split()

    # Gets Monster name : URL but cuts some out due to .index()
    if ('Active:' not in mon_name_struct):
        # Edge case for monster Manekimewdra which doesn't have an Active skill
        mon_name = mon_name_struct[1]
    else:
        # Filter out name of monster
        last_idx = mon_name_struct.index('Active:')
        mon_name_str = mon_name_struct[1:last_idx-1]
        mon_name_unfiltered = ' '.join(mon_name_str)
        mon_name = remove_non_ascii_1(mon_name_unfiltered).rstrip()

    # Build URL
    mon_nbr = mon_id[14:].strip('.png')
    mon_url = f"{pdx_url}{mon_nbr}.jpg"
        
    f_rem_urls.write(f"{mon_name}: {mon_url}\n") 

f_rem_urls.close()