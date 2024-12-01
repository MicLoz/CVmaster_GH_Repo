import FreeSimpleGUI as Fsg
import json
import webbrowser

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

def blank_out_input_box_values():
    window["job_site_url_input"].update(value='')
    window["location_input_key"].update(value='')
    window["url_search_pref_key"].update(value='')
    window["url_search_suff_key"].update(value='')


# UI Elements
#region Labels Region
label = Fsg.Text("Job Site Configuration")
url_label = Fsg.Text("Enter Job Site URL")
search_term_label = Fsg.Text("Enter Job Search Term:")
location_label = Fsg.Text("Enter Location (optional)")
job_sites_list_label = Fsg.Text("Current Job Sites:")
search_prefix_label = Fsg.Text("URL Search Prefix")
search_suffix_label = Fsg.Text("URL Search Suffix")
#endregion

#region Text Input Boxes
url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url_input')
location_input = Fsg.InputText(tooltip="Location for search", key='location_input_key')
search_term_input = Fsg.InputText(tooltip="Search term for job sites", key='search_term_input_key')
url_search_pref_input = Fsg.InputText(tooltip="Portion of URL that goes before search term",
                                      key='url_search_pref_key', size=(30,10))
url_search_suff_input = Fsg.InputText(tooltip="Portion of URL that goes after search term",
                                      key='url_search_suff_key', size=(30,10))
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
        url = values['job_site_url_input']  # Use the renamed key here
        location = values['location_input_key']
        search_pre = values['url_search_pref_key']
        search_suf = values['url_search_suff_key']
        if url:
            # Create a new job site entry with URL and location (optional)
            new_job_site = {'url': url, 'location': location, 'searchPrefix': search_pre,
                            'searchSuffix': search_suf}
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
        updated_url = values['job_site_url_input']
        updated_location = values['location_input_key']
        updated_search_pre = values['url_search_pref_key']
        updated_search_suf = values['url_search_suff_key']

        job_sites[selected_index] = {'url': updated_url,
                                     'location': updated_location,
                                     'searchPrefix': updated_search_pre,
                                     'searchSuffix': updated_search_suf}  # Update the job site in the list
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
        search_term = values["search_term_input_key"].strip()

        # Validation
        if not search_term:
            Fsg.popup_error("Please enter a search term.")
            continue
        if len(job_sites) == 0:
            Fsg.popup_error("Please ensure the job site list has at least one entry.")
            continue

        # Construct and open URLs
        for site in job_sites:
            full_url = f"{site['url']}{site.get('searchPrefix', '')}{search_term}{site.get('searchSuffix', '')}"
            webbrowser.open(full_url)


    elif event == Fsg.WIN_CLOSED:
        break

window.close()