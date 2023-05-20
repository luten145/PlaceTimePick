def countPattern(string, pattern):
    if string == '\0':
        return 0
    count = string.count(pattern)

    return count
