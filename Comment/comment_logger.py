import comment_filter 
import os

def load(filename):
    # Get the directory that this script (comment_filter.py) is in
    script_dir = os.path.dirname(__file__)

    # Go up one level (to project/), then into data/
    data_dir = os.path.join(script_dir, '..', 'data')
    file_path = os.path.join(data_dir, filename)

    # Normalize to an absolute path
    file_path = os.path.abspath(file_path)

    with open(file_path, 'r') as f:
        text = f.read()
        banned_words = text.split()
    return banned_words


def replace_text_in_file(filepath, old_text, new_text):
    """Replaces all occurrences of old_text with new_text in a file."""
    with open(filepath, 'r') as file:
        content = file.read()
    
    modified_content = content.replace(old_text, new_text)
    
    with open(filepath, 'w') as file:
        file.write(modified_content)

def is_text_in_file(filepath, search_text):
    """
    Checks if a given text is present in a specified text file.

    Args:
        filepath (str): The path to the text file.
        search_text (str): The text to search for.

    Returns:
        bool: True if the text is found in the file, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return search_text in content
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def append_to_file(filepath, content_to_add):
    """Appends content to the end of a file."""
    with open(filepath, 'a') as file:
        file.write(content_to_add)

# Example usage:
# append_to_file("my_document.txt", "\nThis line was added at the end.")

def log_comment(text, location, rating, month, day, year, hour, minute):
    '''
    format:
    __location__: __location_name__
    __start__
    __when__: date and time
    __rating__: (int from 0 to 5)
    __text__: comment text here
    __end__

    we will replace __location__ with the full comment format, including __location__ at
    the head so it remains at the top of the list of comments under it, staying as a label
    over the most recent comment

    we will track the name of the location with a __ before and after the locations name,
    this way, if a person includes the name of another location in the comment, searching
    for it in the log will not cause it to find another comment rather than the label
    (we will hope that people do not include this formatting inside of their comment with
    any of the key words that are a part of our formatting
    we could also make this a part of the comment filter to make sure it is not)
    '''
    banned_words = load('banned_words.txt')

    location_label = "__location__: " + "__" + location + "__"
    label_with_comment = location_label + "\n__start__\n"
    label_with_comment += "__when__: " + str(month) + '.' + str(day) + '.' + str(year) + " " + str(hour) + ":" + str(minute) +'\n'
    label_with_comment += "__rating__: " + str(rating) + "\n"
    label_with_comment += "__text__: " + text + '\n' + "__end__\n"

    if (comment_filter.filter(banned_words, text)):
        if (is_text_in_file("comment_log.txt", location_label)):
            replace_text_in_file("comment_log.txt", location_label, label_with_comment)
        else:
            append_to_file("comment_log.txt", label_with_comment)
    else:
        replace_text_in_file("comment_log.txt", "__location__: __FILTERED__", label_with_comment)

def average_rating(location):
    file_path = "comment_log.txt" 

    try:
        with open(file_path, 'r') as file:
            this_location = False
            total = 0
            num = 0
            # add up the total ratings and then divide by the number of ratings found
            for line_number, line in enumerate(file, 1):
                if (line.strip() == "__location__: " + "__" + location + "__"):
                    this_location = True
                elif ("__location__" in line and this_location):
                    this_location = False
                    break
                elif (this_location):
                    if ("__rating__" in line):
                        pieces = line.split()
                        # -1 implies there was no rating
                        if (int(pieces[1]) != -1):
                            total += int(pieces[1])
                            num += 1
            if (num == 0):
                return -1
            else:
                return total / num

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
