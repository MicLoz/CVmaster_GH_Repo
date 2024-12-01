import FreeSimpleGUI as Fsg
import json
import webbrowser
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup

FILE_PATH = 'job_sites.json'

# Function to load job sites from a JSON file
def load_job_sites():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)  # Return a list of job sites from the JSON file
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file doesn't exist or is empty

# Function to save job sites to a JSON file
def save_job_sites(job_sites_arg):
    with open(FILE_PATH, 'w') as file:
        json.dump(job_sites_arg, file, indent=4)  # Save the job sites as pretty-printed JSON

#Function to set the values in the Input Boxes to that of the Selected Job Site.
def set_input_box_values(selected_job_site_arg):
    # Populate the input fields with the selected job site's URL and location
    window["job_site_url_input"].update(value=selected_job_site_arg['url'])
    window["location_input_key"].update(value=selected_job_site_arg.get('location', ''))
    window["url_search_pref_key"].update(value=selected_job_site_arg.get('searchPrefix', ''))
    window["url_search_suff_key"].update(value=selected_job_site_arg.get('searchSuffix', ''))
    window["rep_srch_char"].update(value=selected_job_site_arg.get('replaceSpacesWith', ''))
    window["cap_dropD"].update(value=selected_job_site_arg.get('capitalisationRule', ''))

def get_input_box_values():
    get_input_url = values['job_site_url_input']  # Use the renamed key here
    get_input_location = values['location_input_key']
    get_input_search_pre = values['url_search_pref_key']
    get_input_search_suf = values['url_search_suff_key']
    get_input_space_rep = values['rep_srch_char']
    get_input_cap_rule = values['cap_dropD']
    return [get_input_url, get_input_location, get_input_search_pre, get_input_search_suf, get_input_space_rep,
            get_input_cap_rule]

def blank_out_input_box_values():
    window["job_site_url_input"].update(value='')
    window["location_input_key"].update(value='')
    window["url_search_pref_key"].update(value='')
    window["url_search_suff_key"].update(value='')
    window["rep_srch_char"].update(value='')
    window["cap_dropD"].update(value='')

def fetch_webpage(url ,headers_arg):
    #Fetch the webpage
    try:
        response = requests.get(url, headers=headers_arg)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage:", e)
        return None

def parse_webpage(response):
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


# UI Elements
#region Labels Region
label = Fsg.Text("Job Site Configuration")
url_label = Fsg.Text("Enter Job Site URL")
search_term_label = Fsg.Text("Enter Job Search Term:")
location_label = Fsg.Text("Enter Location (optional)")
job_sites_list_label = Fsg.Text("Current Job Sites:")
search_prefix_label = Fsg.Text("URL Search Prefix")
search_suffix_label = Fsg.Text("URL Search Suffix")
replace_space_label = Fsg.Text("Replace spaces in search term with:")
search_caps_rule_label = Fsg.Text("Search Caps Rule")
#endregion

#region Text Input Boxes
url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url_input')
location_input = Fsg.InputText(tooltip="Location for search", key='location_input_key')
search_term_input = Fsg.InputText(tooltip="Search term for job sites", key='search_term_input_key')
url_search_pref_input = Fsg.InputText(tooltip="Portion of URL that goes before search term",
                                      key='url_search_pref_key', size=(30,10))
url_search_suff_input = Fsg.InputText(tooltip="Portion of URL that goes after search term",
                                      key='url_search_suff_key', size=(30,10))
replace_search_char = Fsg.InputText(tooltip="The char. to replace spaces with in your search term",
                                    key="rep_srch_char", size=(1,10))
#endregion

#region InputCombo / Dropdowns
caps_rule_dropdwn = Fsg.InputCombo(values=['All Lowercase'], key="cap_dropD")
#endregion

#region Buttons
add_button = Fsg.Button("Add Job Site")
edit_button = Fsg.Button("Edit Job Site", key="edit_button_key")
search_button = Fsg.Button("Search", key="search_button_key")
delete_button = Fsg.Button("Delete Job Site", key='delete_button_key')
#endregion

#region List Boxes
job_sites_list_box = Fsg.Listbox(values=[site['url'] for site in load_job_sites()],
                                 key='job_sites_listbox_ky', size=(45, 10),
                                 enable_events=True)
#endregion

#Variables
selected_index = 0

# Create the window layout
window = Fsg.Window('Job Sites Configuration',
                    layout=[[label],
                            [url_label, url_input],
                            [search_prefix_label, url_search_pref_input, search_suffix_label, url_search_suff_input],
                            [location_label, location_input],
                            [search_term_label, search_term_input, search_button],
                            [replace_space_label, replace_search_char, search_caps_rule_label, caps_rule_dropdwn],
                            [add_button, edit_button, delete_button],
                            [job_sites_list_label],
                            [job_sites_list_box]],
                    font=('Helvetica', 14))

# Load the job sites initially
job_sites = load_job_sites()

# Event loop
while True:
    event, values = window.read()
    print(1, event)
    print(2, values)  # Will show the whole values dictionary
    print(3, values["job_site_url_input"])  # Print the URL input field value

    if event == "Add Job Site":
        url, location, search_pre, search_suf, space_rep, cap_rule = get_input_box_values()
        if url:
            # Create a new job site entry with URL and location (optional)
            new_job_site = {'url': url, 'location': location, 'searchPrefix': search_pre,
                            'searchSuffix': search_suf, 'replaceSpacesWith': space_rep,
                            'capitalisationRule': cap_rule}
            job_sites.append(new_job_site)  # Add to job sites list
            save_job_sites(job_sites)  # Save updated list to JSON file
            job_sites_list_box.update(values=[site['url'] for site in job_sites])  # Update the listbox

    elif event == "job_sites_listbox_ky":
        # Get the selected index from the listbox (indexes are 0-based)
        selected_tuple = window["job_sites_listbox_ky"].Widget.curselection()
        if len(selected_tuple) > 0:
            selected_index = selected_tuple[0]
            if selected_index is not None:
                # Convert the selected index to the actual job site in the list
                selected_job_site = job_sites[selected_index]
                set_input_box_values(selected_job_site)

    elif event == "edit_button_key":
        # Find the corresponding job site in the list
        (updated_url, updated_location, updated_search_pre,
         updated_search_suf, updated_space_rep, updated_cap_rule) = get_input_box_values()

        # Update the job site in the list
        job_sites[selected_index] = {'url': updated_url,
                                     'location': updated_location,
                                     'searchPrefix': updated_search_pre,
                                     'searchSuffix': updated_search_suf,
                                     'replaceSpacesWith': updated_space_rep,
                                     'capitalisationRule': updated_cap_rule}

        save_job_sites(job_sites)  # Save the updated list back to the JSON file
        job_sites_list_box.update(values=[site['url'] for site in job_sites])  # Refresh the listbox

    elif event == 'delete_button_key':
        if selected_index is not None:
            job_sites.pop(selected_index)
            save_job_sites(job_sites)
            job_sites_list_box.update(values=[site['url'] for site in job_sites])

            if selected_index > 0:
                selected_index = selected_index - 1
                # Update the selection in the list box
                job_sites_list_box.update(set_to_index=selected_index)
                selected_job_site = job_sites[selected_index]
                set_input_box_values(selected_job_site)
            else:
                blank_out_input_box_values()

    elif event == "search_button_key":
        search_term = values["search_term_input_key"]

        # Validation
        if not search_term:
            Fsg.popup_error("Please enter a search term.")
            continue
        if len(job_sites) == 0:
            Fsg.popup_error("Please ensure the job site list has at least one entry.")
            continue

        # Construct and open URLs
        for site in job_sites:
            site_cap_rule = f"{site.get('capitalisationRule', '')}"
            space_rep_char = f"{site.get('replaceSpacesWith', '')}"
            if site_cap_rule == "All Lowercase":
                search_term = search_term.lower()
                print(2.1, search_term)
            if space_rep_char != "":
                search_term = search_term.replace(" ",space_rep_char)
                print(2.2, search_term)

            #Populate vars with Portions of full URL.
            site_url = f"{site['url']}"
            srch_pre = f"{site.get('searchPrefix', '')}"
            srch_suf = f"{site.get('searchSuffix', '')}"
            print(2.3, site_url)

            search_path = srch_pre + search_term + srch_suf
            full_url = site_url + search_path

            print(3.1, search_path)
            print(3.2, full_url)
            webbrowser.open(full_url)

            encoded_full_url = quote(full_url, safe=":/?=&")
            print(3.3, encoded_full_url)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }

            webpage_html = fetch_webpage(full_url, headers)
            print(3.4, parse_webpage(webpage_html))

    elif event == Fsg.WIN_CLOSED:
        break

window.close()