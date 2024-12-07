print("Just so I can commit")
def get_input_box_values(values):
    get_input_url = values['job_site_url_input']
    get_input_location = values['location_input_key']
    get_input_search_pre = values['url_search_pref_key']
    get_input_search_suf = values['url_search_suff_key']
    get_input_space_rep = values['rep_srch_char']
    get_input_cap_rule = values['cap_dropD']
    return [get_input_url, get_input_location, get_input_search_pre, get_input_search_suf, get_input_space_rep,
            get_input_cap_rule]

#Function to set the values in the Input Boxes to that of the Selected Job Site.
def set_input_box_values(selected_job_site_arg, window):
    # Populate the input fields with the selected job site's URL and location
    window["job_site_url_input"].update(value=selected_job_site_arg['url'])
    window["location_input_key"].update(value=selected_job_site_arg.get('location', ''))
    window["url_search_pref_key"].update(value=selected_job_site_arg.get('searchPrefix', ''))
    window["url_search_suff_key"].update(value=selected_job_site_arg.get('searchSuffix', ''))
    window["rep_srch_char"].update(value=selected_job_site_arg.get('replaceSpacesWith', ''))
    window["cap_dropD"].update(value=selected_job_site_arg.get('capitalisationRule', ''))

def blank_out_input_box_values(window):
    window["job_site_url_input"].update(value='')
    window["location_input_key"].update(value='')
    window["url_search_pref_key"].update(value='')
    window["url_search_suff_key"].update(value='')
    window["rep_srch_char"].update(value='')
    window["cap_dropD"].update(value='')

def set_input_box_search_term_value(search_term_dict_arg, window):
    window["search_term_input_key"].update(value=search_term_dict_arg['searchTerm'])