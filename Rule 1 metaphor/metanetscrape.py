#---------------------------------------------------------
# Michelle Carney
# michelle.carney@berkeley.edu
# metanet scrape: https://metaphor.icsi.berkeley.edu/pub/en/index.php/Category:Metaphor
# Goal: get metanet metaphors to print into one file, look at synsets? tbd.
#---------------------------------------------------------

import sys
import urllib.request as req
from bs4 import BeautifulSoup
import operator

url = 'https://metaphor.icsi.berkeley.edu/pub/en/index.php/Category:Metaphor'


response = req.urlopen(url)
page_source = response.read()

soup = BeautifulSoup(page_source, 'html.parser')
from pprint import pprint 
#pprint(soup)

# ##First get all of the lists
# div_metaphors = soup.find_all('div', {'class': 'smw-columnlist-container'}) 
# print(div_metaphors)
# #print(names)

# All links from metanet main page of metaphors:

links_list = []
links = soup.find_all('a')
for item in links:
    links_list += item
#print(links_list)

#get metaphors from page, put into metaphor bucket and junk bucket
metaphor_list = []
junk_list = []
for item in links_list:
    if type(item) is not None:
        if item.isupper() == True:
            # print('Upper')
            metaphor_list.append(item)
        elif item.startswith('Metaphor:'):
            # print('meta')
            item = item.replace('Metaphor:', '')
            metaphor_list.append(item)
        else:
            # print('junk')
            junk_list.append(item)
    elif type(item) is None:
        metaphor_list = [x.lower() for x in metaphor_list]
        print(metaphor_list)
        break

#sanity check that you are getting the right stuff:
if (len(metaphor_list)+len(junk_list)) == len(links_list):
    print('good')

#get your metaphors to stop yelling at you
metaphor_list = [x.lower() for x in metaphor_list]
print(metaphor_list)

metaphors_final = open('metanet.txt', 'w')
for item in metaphor_list:
    metaphors_final.write(item + '\n')
metaphors_final.close()
