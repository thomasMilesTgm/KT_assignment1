lowerCase = "abcdefghijklmnopqrstuvwxyz"
upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

chars = lowerCase

def neighbors(pattern, d):
    r = []
    if d <= 0:
        return None

    for i in range(0, len(pattern)+1):
        # insertion
        for letter in chars:
            insertion = pattern[:i] + letter + pattern[i:]
            r.append(insertion)

            recursion = neighbors(insertion, d - 1)
            if recursion:
                r += recursion

    for i in range(0, len(pattern)):
        # deletion
        deletion = pattern[:i] + pattern[i+1:]
        r.append(deletion)

        recursion = neighbors(deletion, d - 1)
        if recursion:
            r += recursion

        # replacement
        for letter in chars:
            replacement = pattern[:i] + letter + pattern[i+1:]
            if letter != pattern[i]:
                r.append(replacement)

                recursion = neighbors(replacement, d - 1)
                if recursion:
                    r += recursion

    return r