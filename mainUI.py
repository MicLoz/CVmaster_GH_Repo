import FreeSimpleGUI as Fsg
import json

FILE_PATH = 'job_sites.json'


# Function to load job sites from a JSON file
def load_job_sites():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)  # Return a list of job sites from the JSON file
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file doesn't exist or is empty


# Function to save job sites to a JSON file
def save_job_sites(job_sites):
    with open(FILE_PATH, 'w') as file:
        json.dump(job_sites, file, indent=4)  # Save the job sites as pretty-printed JSON


# UI Elements
label = Fsg.Text("Job Site Configuration")
url_label = Fsg.Text("Enter Job Site URL")
url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url')
location_label = Fsg.Text("Enter Location (optional)")
location_input = Fsg.InputText(tooltip="Location for search", key='location_input')
add_button = Fsg.Button("Add Job Site")
edit_button = Fsg.Button("Edit Job Site")
job_sites_list_label = Fsg.Text("Current Job Sites:")
job_sites_list_box = Fsg.Listbox(values=[site['url'] for site in load_job_sites()], key='job_sites_list', size=[45, 10])

# Create the window layout
window = Fsg.Window('Job Sites Configuration',
                    layout=[[label],
                            [url_label, url_input],
                            [location_label, location_input],
                            [add_button, edit_button],
                            [job_sites_list_label],
                            [job_sites_list_box]],
                    font=('Helvetica', 14))

# Load the job sites initially
job_sites = load_job_sites()

# Event loop
while True:
    event, values = window.read()

    if event == "Add Job Site":
        url = values['job_site_url']
        location = values['location_input']
        if url:
            # Create a new job site entry with URL and location (optional)
            new_job_site = {'url': url, 'location': location}
            job_sites.append(new_job_site)  # Add to job sites list
            save_job_sites(job_sites)  # Save updated list to JSON file
            job_sites_list_box.update(values=[site['url'] for site in job_sites])  # Update the listbox

    elif event == "Edit Job Site":
        try:
            selected_index_to_edit = window['job_sites_list'].Widget.curselection()
            if selected_index_to_edit:
                index = selected_index_to_edit[0]
                selected_job_site = job_sites[index]
                url_input.update(value=selected_job_site['url'])  # Populate the input field with selected URL
                location_input.update(value=selected_job_site.get('location', ''))  # Populate location if available

                # Once user edits, update the list
                window["job_sites_list"].Widget.selection_clear(0, 'end')  # Clear selection
                window["job_sites_list"].update(values=[site['url'] for site in job_sites])  # Refresh the listbox
            else:
                Fsg.Popup("Select Item from list before you Edit.")
        except IndexError:
            Fsg.Popup("Select Item from list before you Edit.")

    elif event == Fsg.WIN_CLOSED:
        break

window.close()
