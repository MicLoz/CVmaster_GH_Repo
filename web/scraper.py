import webbrowser
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup

def fetch_webpage(url ,headers_arg):
    try:
        response = requests.get(url, headers=headers_arg)
        if response.status_code == 200:
            return response.text  # Returning the raw text content of the response
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def parse_webpage(response):
    if response is None:
        return {"Job Title": None, "Job Link": None}  # Safe handling of None response

    soup = BeautifulSoup(response, 'html.parser')

    # Step 4: Extract job titles and links
    # Find the <a> tag for the link
    a_tag = soup.find('a', class_='res-1foik6i')
    job_link = a_tag['href'] if a_tag else None

    # Find the <div> for the title
    job_title_div = soup.find('div', class_='res-nehv70')
    job_title = job_title_div.get_text(strip=True) if job_title_div else None

    # Output results as a dictionary
    return {"Job Title": job_title, "Job Link": job_link}