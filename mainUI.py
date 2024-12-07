from file_system.file_manager import *
from ui.search_term_interact import *
from ui.initialise_ui import *
from ui.input_boxes import *
from web.scraper import *
from web.playwright_utils import *

#Variables that initialise using function calls or similar
search_terms = load_json(SEARCH_TERMS) # This has to be declared before it is used by the next line.
default_search_term = get_existing_default_search_term_if_exists(search_terms)

# Load the job sites initially
job_sites = load_json(FILE_PATH)

#Variables with "empty" initialisations, that aren't required to be BEFORE the UI Element creation.
selected_index = 0
selected_index_search_term = 0
selected_search_term = {}

window = create_ui(default_search_term, job_sites, search_terms)

# Event loop
while True:
    event, values = window.read()

    #current_search_term = get_default_search_term()
    print(1, event)
    print(2, values)  # Will show the whole values dictionary
    print(3, values["job_site_url_input"])  # Print the URL input field value
    print(f"window: {window}")
    print(f"Search Terms: {search_terms}")

    if event == "Add Job Site":
        url, location, search_pre, search_suf, space_rep, cap_rule = get_input_box_values(values)
        if url:
            # Create a new job site entry with URL and location (optional)
            new_job_site = {'url': url, 'location': location, 'searchPrefix': search_pre,
                            'searchSuffix': search_suf, 'replaceSpacesWith': space_rep,
                            'capitalisationRule': cap_rule}
            job_sites.append(new_job_site)  # Add to job sites list
            save_json(job_sites, FILE_PATH)  # Save updated job sites list to JSON file
            window["job_sites_listbox_ky"].update(values=[site['url'] for site in job_sites])  # Update the listbox

    elif event == "job_sites_listbox_ky":
        # Get the selected index from the listbox (indexes are 0-based)
        selected_tuple = window["job_sites_listbox_ky"].Widget.curselection()
        if len(selected_tuple) > 0:
            selected_index = selected_tuple[0]
            if selected_index is not None:
                # Convert the selected index to the actual job site in the list
                selected_job_site = job_sites[selected_index]
                set_input_box_values(selected_job_site, window)

    elif event == "edit_button_key":
        # Find the corresponding job site in the list
        (updated_url, updated_location, updated_search_pre,
         updated_search_suf, updated_space_rep, updated_cap_rule) = get_input_box_values(values)

        # Update the job site in the list
        job_sites[selected_index] = {'url': updated_url,
                                     'location': updated_location,
                                     'searchPrefix': updated_search_pre,
                                     'searchSuffix': updated_search_suf,
                                     'replaceSpacesWith': updated_space_rep,
                                     'capitalisationRule': updated_cap_rule}

        save_json(job_sites, FILE_PATH)  # Save updated job sites list to JSON file
        window["job_sites_listbox_ky"].update(values=[site['url'] for site in job_sites])  # Refresh the listbox

    elif event == 'delete_button_key':
        if selected_index is not None:
            job_sites.pop(selected_index)
            save_json(job_sites, FILE_PATH)  # Save updated job sites list to JSON file
            window["job_sites_listbox_ky"].update(values=[site['url'] for site in job_sites])

            if selected_index > 0:
                selected_index = selected_index - 1
                # Update the selection in the list box
                window["job_sites_listbox_ky"].update(set_to_index=selected_index)
                selected_job_site = job_sites[selected_index]
                set_input_box_values(selected_job_site, window)
            else:
                blank_out_input_box_values(window)

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
            job_details = parse_webpage(webpage_html)
            job_link_path = job_details["Job Link"]
            full_job_url = site_url + job_link_path
            encoded_full_job_url = quote(full_job_url, safe=":/?=&")
            print(3.5, encoded_full_job_url)
            print(4, get_jobdescrip_from_jobpage(encoded_full_job_url))

    elif event == "save_srch_term":
        search_val = values["search_term_input_key"].strip()
        if search_val != "":
            if save_search_term(search_val, search_terms) == False:
                Fsg.popup_error("This search term already exists.")
            else:
                # Update the listbox
                window["search_terms_listbox_ky"].update(values=[term['searchTerm'] for term in search_terms])
                save_json(search_terms, SEARCH_TERMS) # save_search_terms_to_JSON

    elif event == "search_terms_listbox_ky":
        selected_tuple_search = window["search_terms_listbox_ky"].Widget.curselection()
        print(9, selected_tuple_search)
        print("Just so I can commit")
        if len(selected_tuple_search) > 0:
            selected_index_search_term = selected_tuple_search[0]
            if selected_index_search_term is not None:
                # Convert the selected index to the actual job site in the list
                selected_search_term = search_terms[selected_index_search_term]
                print(10, selected_search_term)
                set_input_box_search_term_value(selected_search_term, window)

    elif event == "srch-def":
        # A Search term has been selected
        if len(selected_search_term) > 0:
            set_search_term_as_default(selected_search_term['searchTerm'], search_terms)
            save_json(search_terms, SEARCH_TERMS) # save_search_terms_to_JSON
        else:
            Fsg.popup("You must select a search term from the list, in order to set it as the default.")

    elif event == 'srch-del':
        if len(selected_search_term) > 0:
            deleted_index = delete_search_term(selected_search_term['searchTerm'], search_terms)
            save_json(search_terms, SEARCH_TERMS) # save_search_terms_to_JSON
            window["search_terms_listbox_ky"].update(values=[term['searchTerm'] for term in search_terms])  # Update the listbox

            if deleted_index is not None:
                if deleted_index > 0:
                    deleted_index = deleted_index - 1
                    # Update the selection in the list box
                    window["search_terms_listbox_ky"].update(set_to_index=deleted_index)
                    selected_index_search_term = search_terms[deleted_index]
                    set_input_box_search_term_value(search_terms[deleted_index], window)
        else:
            Fsg.popup("You must select a search term from the list, in order to delete it.")

    elif event == Fsg.WIN_CLOSED:
        break

window.close()