#Handles general web functions
def generate_search_url(site, search_term):
    search_term = search_term.lower() if site.get("capitalisationRule") == "All Lowercase" else search_term
    search_term = search_term.replace(" ", site.get("replaceSpacesWith", ""))
    return f"{site['url']}{site.get('searchPrefix', '')}{search_term}{site.get('searchSuffix', '')}"

def generate_single_job_url(site, job_link_path):
    single_job_url = f"{site['url']}{job_link_path}"
    return single_job_url

def get_cookie_popup_selector(site, web_details):
    for details in web_details:
        if details['url'] == site:
            return f"{details.get('cookiePopUpSelector', '')}"
        else:
            return ""

def get_job_description_selector(site, web_details):
    for details in web_details:
        if details['url'] == site:
            return f"{details.get('jobDescriptionSelector', '')}"
        else:
            return ""

