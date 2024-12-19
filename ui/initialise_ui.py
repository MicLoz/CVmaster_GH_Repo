import FreeSimpleGUI as Fsg

def create_ui_elements(default_search_term, job_sites, search_terms, last_search_path, last_cv_paths, last_cv_path,
                       last_dir_paths, last_dir_path):
    # Create the UI elements dynamically
    #region Labels
    label = Fsg.Text("Job Site Configuration", justification="left")
    blank_Label = Fsg.Text("")
    url_label = Fsg.Text("Enter Job Site URL", justification="left")
    search_prefix_label = Fsg.Text("URL Search Prefix", justification="left")
    search_suffix_label = Fsg.Text("URL Search Suffix", justification="left")
    location_label = Fsg.Text("Enter Location (optional)", justification="left")
    search_term_label = Fsg.Text("Enter Job Search Term:", justification="left")
    job_sites_list_label = Fsg.Text("Current Job Sites:")
    replace_space_label = Fsg.Text("Replace spaces in search term with:")
    search_caps_rule_label = Fsg.Text("Search Caps Rule")
    search_term_space = " " * 70
    search_terms_list_label = Fsg.Text(f"{search_term_space}Current Search Terms:", key="search_terms_label")
    CV_browser_label = Fsg.Text("Choose existing CV to use as basis for Rewrite:")
    CV_destination_label = Fsg.Text("Choose a folder for you rewritten CV:")
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
    CV_dropdown = Fsg.Combo(values=[path['cvPath'] for path in last_cv_paths], default_value=last_cv_path,
                            key="CV_dropD", enable_events=True)
    CV_folder_dropdown = Fsg.Combo(values=[path['dirPath'] for path in last_dir_paths],
                                   default_value=last_dir_path
                                   ,key="CV_dest_dropD", size=(35,1), enable_events=True)
    #endregion

    #region Buttons
    add_button = Fsg.Button("Add Job Site")
    edit_button = Fsg.Button("Edit Job Site", key="edit_button_key")
    search_button = Fsg.Button("Search", key="search_button_key")
    save_search_button = Fsg.Button("Save Search Term", key="save_srch_term")
    search_default_button = Fsg.Button("Set as Default", key="srch-def")
    search_delete_button = Fsg.Button("Delete Search Term", key="srch-del")
    delete_button = Fsg.Button("Delete Job Site", key='delete_button_key')
    preview_CV_button = Fsg.Button("Preview CV", key="preview_cv_button_clicked")
    #endregion

    #region File Browsers
    CV_browse_button = Fsg.FileBrowse("Browse", key='clicked_cv_browse_button'
                                      ,file_types=(("Word Documents", "*.docx"),)
                                      )
    #endregion

    #region Folder Browsers
    CV_destination_folder_browse_button = Fsg.FolderBrowse("Browse", key="clicked_cv_destination_button")
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

    #region MultiLines
    CV_preview = Fsg.Multiline(size=(80, 20), key="-CV_PREVIEW-", disabled=True, autoscroll=False)
    #endregion

    #region Column Organisation
    column1 = [
        [label],
        [url_label],
        [search_prefix_label],
        [search_suffix_label],
        [location_label],
        [search_term_label]
    ]

    column2 = [
        [blank_Label],
        [url_input],
        [url_search_pref_input],
        [url_search_suff_input],
        [location_input],
        [search_term_input]
    ]
    #endregion

    return [
        [Fsg.Column(column1), Fsg.Column(column2)],
        [search_button, save_search_button],
        [replace_space_label, replace_search_char, search_caps_rule_label, caps_rule_dropdwn],
        [add_button, edit_button, delete_button],
        [job_sites_list_label, search_terms_list_label],
        [job_sites_list_box, search_terms_list_box, search_default_button, search_delete_button],
        [CV_browser_label, CV_dropdown, CV_browse_button],
        [CV_destination_label, CV_folder_dropdown, CV_destination_folder_browse_button],
        [preview_CV_button]
    ]

def create_ui(default_search_term, job_sites, search_terms, last_search_path, theme_name, last_cv_paths, last_cv_path, last_dir_paths,last_dir_path):
    set_theme(theme_name)
    layout = create_ui_elements(default_search_term, job_sites, search_terms, last_search_path, last_cv_paths, last_cv_path, last_dir_paths,last_dir_path)
    window = Fsg.Window('Job Sites Configuration', layout, font=('Helvetica', 14))
    return window

def set_theme(theme_name):
    Fsg.theme(theme_name)
