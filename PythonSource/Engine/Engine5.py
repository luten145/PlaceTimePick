

class Engine5:

    placePattern = ["홀", "웨딩", "장례"]
    
    def extract_words(text, keyword):
        words = text.split()
        result = []
        for word in words:
            if keyword in word:
                result.append(word)
        return result