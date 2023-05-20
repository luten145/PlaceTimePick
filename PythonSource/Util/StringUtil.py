def countPattern(string, pattern):
    if string == '' or pattern == '':
        return 0
    count = string.count(pattern)

    return count
