import FreeSimpleGUI as Fsg

def create_ui_elements(default_search_term, job_sites, search_terms):
    # Create the UI elements dynamically
    #region Labels
    label = Fsg.Text("Job Site Configuration")
    url_label = Fsg.Text("Enter Job Site URL")
    search_term_label = Fsg.Text("Enter Job Search Term:")
    location_label = Fsg.Text("Enter Location (optional)")
    job_sites_list_label = Fsg.Text("Current Job Sites:")
    search_prefix_label = Fsg.Text("URL Search Prefix")
    search_suffix_label = Fsg.Text("URL Search Suffix")
    replace_space_label = Fsg.Text("Replace spaces in search term with:")
    search_caps_rule_label = Fsg.Text("Search Caps Rule")
    search_term_space = " " * 70
    search_terms_list_label = Fsg.Text(f"{search_term_space}Current Search Terms:", key="search_terms_label")
    #endregion

    #region Text Input Boxes
    url_input = Fsg.InputText(tooltip="Job site URL", key='job_site_url_input')
    location_input = Fsg.InputText(tooltip="Location for search", key='location_input_key')
    search_term_input = Fsg.InputText(
        tooltip="Search term for job sites", key='search_term_input_key',
        default_text=f"{default_search_term}" if default_search_term else ""
    )
    url_search_pref_input = Fsg.InputText(tooltip="Portion of URL that goes before search term",
                                          key='url_search_pref_key', size=(30, 10))
    url_search_suff_input = Fsg.InputText(tooltip="Portion of URL that goes after search term",
                                          key='url_search_suff_key', size=(30, 10))
    replace_search_char = Fsg.InputText(tooltip="The char. to replace spaces with in your search term",
                                        key="rep_srch_char", size=(1, 10))
    #endregion

    #region Drop Downs
    caps_rule_dropdwn = Fsg.InputCombo(values=['All Lowercase'], key="cap_dropD")
    #endregion

    #region Buttons
    add_button = Fsg.Button("Add Job Site")
    edit_button = Fsg.Button("Edit Job Site", key="edit_button_key")
    search_button = Fsg.Button("Search", key="search_button_key")
    save_search_button = Fsg.Button("Save Search Term", key="save_srch_term")
    search_default_button = Fsg.Button("Set as Default", key="srch-def")
    search_delete_button = Fsg.Button("Delete Search Term", key="srch-del")
    delete_button = Fsg.Button("Delete Job Site", key='delete_button_key')
    #endregion

    #region List Boxes
    job_sites_list_box = Fsg.Listbox(
        values=[site['url'] for site in job_sites],
        key='job_sites_listbox_ky', size=(45, 10), enable_events=True
    )
    search_terms_list_box = Fsg.Listbox(
        values=[term['searchTerm'] for term in search_terms],
        key='search_terms_listbox_ky', size=(45, 10), enable_events=True
    )
    #endregion

    return [
        [label],
        [url_label, url_input],
        [search_prefix_label, url_search_pref_input, search_suffix_label, url_search_suff_input],
        [location_label, location_input],
        [search_term_label, search_term_input, search_button, save_search_button],
        [replace_space_label, replace_search_char, search_caps_rule_label, caps_rule_dropdwn],
        [add_button, edit_button, delete_button],
        [job_sites_list_label, search_terms_list_label],
        [job_sites_list_box, search_terms_list_box, search_default_button, search_delete_button]
    ]

def create_ui(default_search_term, job_sites, search_terms):
    layout = create_ui_elements(default_search_term, job_sites, search_terms)
    window = Fsg.Window('Job Sites Configuration', layout, font=('Helvetica', 14))
    return window
