import requests
from bs4 import BeautifulSoup

#def fetch_webpage(url):
#    #Fetch the webpage
#    response = requests.get(url)
#    if response.status_code != 200:
#        print("Failed to fetch the page:", response.status_code)
#    else:

        ## Soup stuff, take out leading comments to use
        ## Step 3: Parse the HTML content
        #soup = BeautifulSoup(response.text, 'html.parser')
#
        ## Step 4: Extract job titles and links
        ## Find the <a> tag for the link
        #a_tag = soup.find('a', class_='res-1foik6i')
        #job_link = a_tag['href'] if a_tag else None
#
        ## Find the <div> for the title
        #job_title_div = soup.find('div', class_='res-nehv70')
        #job_title = job_title_div.get_text(strip=True) if job_title_div else None
#
        ## Output results
        #return {"Job Title:", job_title, "Job Link:", job_link}
#
