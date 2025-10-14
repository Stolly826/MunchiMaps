import re

'''
Run the comment through various checks to make sure it is A-Ok
If issues are found it will print a message with the explanation
'''
def filter(banned_words, comment):
    comment_words = comment.split()
    check_banned_words(banned_words, comment)
    check_multiple_links(comment, comment_words)
    check_repeats(comment, comment_words)
    check_length(comment, comment_words)

# Detects comments with bad words. 
def check_banned_words(banned_words, comment):
    for word in banned_words:
        if re.search(word, comment, re.IGNORECASE):
            print("BAD COMMENT (USED BANNED WORDS): " + comment)

# Detects multiple links inside of a comment
def check_multiple_links(comment, comment_words):
    link_count = 0
    for word in comment_words:
        if (re.search("www.", word, re.IGNORECASE) ):
            link_count += 1
        if (link_count == 2):
            print("BAD COMMENT (MULTIPLE LINKS): " + comment)  

# Detects excessively repeated words (comment is > 10 words and more than 40% of them are the same)  
def check_repeats(comment, comment_words):
    if comment_words.len > 10:
        cur_repeats = 0
        for a in range(0, comment_words.len):
            cur_repeats = 0
            for b in range(a, comment_words.len):
                if comment_words[a] == comment_words[b]:
                    cur_repeats += 1
            if cur_repeats > comment_words.len * .4:
                print("BAD COMMENT (EXCESSIVELY REPEATED WORDS): " + comment)
                return

# Detects if a comment is > 1000 words or empty
def check_length(comment, comment_words):
    if comment_words.len > 1000:
        print("BAD COMMENT (AIN'T NO WAY YOU GOT THAT MUCH TO SAY ABOUT A VENDING MACHINE): " + comment)
    if comment_words.len == 0:
        print("BAD COMMENT (EMPTY): " + comment)

def load(filename):
    with open(filename, 'r') as f:
        text = f.read()
        banned_words = text.split()
    return banned_words

#TODO: Place banned_words in database when deployed, change it to fetch from db and add spam comment filter. 
def main():
    comment = input("Comment: ").strip()
    banned_words = load('banned_words.txt')
    filter(banned_words, comment)

if __name__ == "__main__":
    main()