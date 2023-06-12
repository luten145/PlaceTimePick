import re
from difflib import SequenceMatcher


def getSimilarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def countPattern(string, pattern):
    if string == '' or pattern == '':
        return 0
    count = string.count(pattern)
    return count


def split_string(text):
    words = text.split()
    return words


def generateCombinations(text):
    words = text.split()
    result = []
    for i in range(1, len(words)+1):
        for j in range(len(words)-i+1):
            combination = words[j:j+i]
            if all(len(word) >= 2 for word in combination):
                result.append(' '.join(combination))
    return result


def removeSubstring(text, substring):
    words = text.split()
    result = []
    for word in words:
        if word != substring:
            result.append(word)
    return ' '.join(result)


def containsSubstring(text, substring):
    return substring in text


# Find words in a line of text that contain the keyword word
def extractWords(text, keyword):  # text : TextLine , keyword : word to find
    result = []
    for word in text.split():
        if keyword in word:
            result.append(word)
    return result


def extractNumbers(text):
    return re.findall(r'\d+(?:-\d+)?', text)


def getTextList(raw):  # Json text to textlist
    return str(["".join(raw["task_result"]["text"])]).split('\\n')