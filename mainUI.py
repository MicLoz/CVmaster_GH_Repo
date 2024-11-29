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
url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url_input')  # Renamed for clarity
location_label = Fsg.Text("Enter Location (optional)")
location_input = Fsg.InputText(tooltip="Location for search", key='location_input')
add_button = Fsg.Button("Add Job Site")
edit_button = Fsg.Button("Edit Job Site", key="edit_button")
job_sites_list_label = Fsg.Text("Current Job Sites:")
job_sites_list_box = Fsg.Listbox(values=[site['url'] for site in load_job_sites()],
                                 key='job_sites_listbox', size=[45, 10],
                                 enable_events=True)  # Renamed for clarity
save_button = Fsg.Button("Save Edit", key="save_button_key")

# Create the window layout
window = Fsg.Window('Job Sites Configuration',
                    layout=[[label],
                            [url_label, url_input],
                            [location_label, location_input],
                            [add_button, edit_button, save_button],
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
    print(3, values.get("job_site_url_input", "No URL"))  # Print the URL input field value

    if event == "Add Job Site":
        url = values['job_site_url_input']  # Use the renamed key here
        location = values['location_input']
        if url:
            # Create a new job site entry with URL and location (optional)
            new_job_site = {'url': url, 'location': location}
            job_sites.append(new_job_site)  # Add to job sites list
            save_job_sites(job_sites)  # Save updated list to JSON file
            job_sites_list_box.update(values=[site['url'] for site in job_sites])  # Update the listbox

    elif event == "job_sites_listbox":
        print(4, event)
        print(5, values)
        print(6, values.get("job_sites_listbox", "No selection"))
        window["job_site_url_input"].update(value=values['job_sites_listbox'][0])  # Update the input with the selected job site URL
        print('TextBoxUpdated')

    elif event == "Edit Job Site":
        try:
            selected_index_to_edit = window['job_sites_listbox'].Widget.curselection()
            if selected_index_to_edit:
                index = selected_index_to_edit[0]
                selected_job_site = job_sites[index]
                url_input.update(value=selected_job_site['url'])  # Populate the input field with selected URL
                location_input.update(value=selected_job_site.get('location', ''))  # Populate location if available
                window["save_button_key"].update(visible=True)  # Show the "Save Edit" button
            else:
                Fsg.popup("Select an item from the list before you Edit.")
        except IndexError:
            Fsg.popup("Select an item from the list before you Edit.")

    elif event == "Save Edit":
        selected_index_to_edit = window['job_sites_listbox'].Widget.curselection()
        if selected_index_to_edit:
            index = selected_index_to_edit[0]
            updated_url = values['job_site_url_input']  # Use the renamed key here
            updated_location = values['location_input']
            job_sites[index] = {'url': updated_url, 'location': updated_location}  # Update the job site in the list
            save_job_sites(job_sites)  # Save the updated list back to the JSON file
            job_sites_list_box.update(values=[site['url'] for site in job_sites])  # Refresh the listbox
            window["save_button_key"].update(visible=False)  # Hide the "Save Edit" button after saving
        else:
            Fsg.Popup("Select an item from the list to save the edit.")

    elif event == Fsg.WIN_CLOSED:
        break

window.close()
