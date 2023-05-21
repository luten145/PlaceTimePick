from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100

def countPattern(string, pattern):
    if string == '' or pattern == '':
        return 0
    count = string.count(pattern)

    return count
