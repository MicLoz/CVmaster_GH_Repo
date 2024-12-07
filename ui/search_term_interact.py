def set_search_term_default_if_only_one(search_terms):
    if len(search_terms) == 1:
        search_terms[0]['default'] = "True"
        default_search_term = search_terms[0]['searchTerm']

def set_search_term_as_default(search_term_arg, search_terms):
    remove_existing_search_term_as_default(search_terms)
    for term in search_terms:
        if term['searchTerm'] == search_term_arg:
            term['default'] = "True"
            default_search_term = term['searchTerm']

def remove_existing_search_term_as_default(search_terms):
    for term in search_terms:
        #Remove existing Search term
        if term['default'] == "True":
            term['default'] = "False"

def get_existing_default_search_term_if_exists(search_terms):
    if len(search_terms) > 0:
        for term in search_terms:
            if term['default'] == "True":
                return term['searchTerm']
    else:
        return None

def save_search_term(search_term_arg, search_terms):
    target_string = search_term_arg.upper()  # Convert the target string to uppercase
    if any(target_string in (value.upper() if isinstance(value, str) else value) for d in search_terms for value in
           d.values()):
        return False
    else:
        new_search_term_entry = {'searchTerm': search_term_arg, 'default': "False"}
        search_terms.append(new_search_term_entry)
        set_search_term_default_if_only_one(search_terms)
        return True

def delete_search_term(search_term_arg, search_terms):
    for index, term in enumerate(search_terms):
        if term['searchTerm'] == search_term_arg:
            search_terms.pop(index)
            return index