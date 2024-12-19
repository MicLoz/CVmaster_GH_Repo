# Check if any value in the dictionaries matches input_arg
def check_unique(input_arg, list_arg):
    for dictionary in list_arg:
        for value in dictionary.values():
            # Check if the value matches the input_arg
            if input_arg == value:
                return False
    return True

def return_last_used_path(paths, valueTerm):
    #valueTerm = 'cvPath', 'dirPath'
    return_path = ""
    if len(paths) > 1:
        return_path = paths[len(paths) - 1][valueTerm]
        return return_path
    elif len(paths) == 1:
        return_path = paths[0]
        return return_path
    else:
        return return_path