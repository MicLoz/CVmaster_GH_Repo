import FreeSimpleGUI as Fsg

# UI Elements
label = Fsg.Text("Job Site Configuration")
url_label = Fsg.Text("Enter Job Site URL")
url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url')
add_button = Fsg.Button("Add Job Site")
job_sites_list_label = Fsg.Text("Current Job Sites:")
job_sites_list_box = Fsg.Listbox(values=[], key='job_sites_list', size=[45, 10])

# Create the window layout
window = Fsg.Window('Job Sites Configuration',
                    layout=[[label],
                            [url_label, url_input],
                            [add_button],
                            [job_sites_list_label],
                            [job_sites_list_box]],
                    font=('Helvetica', 14))

# Store job sites temporarily in a list
job_sites = []

# Event loop
while True:
    event, values = window.read()

    if event == "Add Job Site":
        url = values['job_site_url']
        if url:
            job_sites.append(url)  # Add URL to job_sites list
            job_sites_list_box.update(values=job_sites)  # Update the listbox with new site

    elif event == Fsg.WIN_CLOSED:
        break

window.close()
