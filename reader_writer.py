import re
def stripNonLetterChars(anyText):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', anyText)

def letterToRank(letter):
    return(ord(letter.lower()) - ord('a'))

def rankToLetter(rank):
    return(chr(rank + ord('a')))

def key_read(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def num_to_text(numtext):
    numtext = str(numtext)
    to_be_letters = [numtext[i:i+2] for i in range(0, len(numtext), 2)]
    letters = []
    for to_be_letter in to_be_letters:
        letters.append(rankToLetter(int(to_be_letter)))
    return ''.join(letters)

def text_to_num(text):
    text = stripNonLetterChars(text)
    nums = []
    for letter in text:
        num = letterToRank(letter)
        if num < 10: num = '0' + str(num)
        else: num = str(num)
        nums.append(num) 
    return ''.join(nums)

def key_write(text, filename):
    with open(filename, 'x') as f:
        f.write(text)
