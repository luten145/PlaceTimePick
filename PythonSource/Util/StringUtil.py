from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100

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
