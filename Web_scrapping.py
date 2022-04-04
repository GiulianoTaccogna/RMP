from pydoc import pager
import requests
from bs4 import BeautifulSoup
#The url of the rate my professor website
root = 'https://www.ratemyprofessors.com'
links = ['/ShowRatings.jsp?tid=2581891']
it = 0
while it < 1000:
    print(links)
    if len(links) >= (it+1):
        url = f'{root}{links[it]}'
    else:
        print(f'Only {it} Professors found.')
        break

    #Making a request to the website
    page = requests.get(url)
    print(page)

    #Read the raw html data from the website
    soup = BeautifulSoup(page.text, "lxml")

    #Find all information, intressted in: rating, tags and new Professors
    rating = soup.find('div', class_="RatingValue__Numerator-qw8sqy-2 liyUjw")
    proftags = soup.findAll("span", class_="Tag-bs9vf4-0 hHOVKF")
    new_links = soup.findAll('a', class_="SimilarProfessorListItem__StyledSimilarProfessorLink-x7cr0c-2 jSKXed", href=True)
    
    #Converting into a plain textformat
    if it==0:
        mode = 'w'
    else:
        mode = 'a'

    tags = []
    with open(f'RMP.csv', mode) as file:
        file.write(rating.get_text())
        for mytag in proftags:
            if mytag.get_text() not in tags:
                tags.append(mytag.get_text())
                file.write(' ,'+mytag.get_text())
        file.write('\n')

    for link in new_links:
        if link['href'] not in links:
            links.append(link['href'])
    print(it)
    it = it+1
