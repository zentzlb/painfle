

def findall(string: str, substring: str):
    """
    find index(s) of substring in string
    :param string: string to search
    :param substring: character to search for
    :return: indices of substring
    """
    find_list = [i for i in range(len(string)) if string[i] == substring]

    return find_list


def remove(g: str, ms: str, w: str):
    """
    removes redundant yellow letters from response
    :param g: guessed word
    :param ms: response
    :param w: actual word
    :return:
    """
    for i in range(len(ms)):
        if ms[i] == 'Y' and g.count(g[i]) > w.count(g[i]):  # letter appears more in the guess than the word
            num = w.count(g[i])  # number of times the letter appears in the word
            ind_list = findall(g, g[i])
            for j in ind_list:
                if ms[j] == 'G':
                    num -= 1
            for j in ind_list:
                if ms[j] == 'Y' and num == 0:
                    ms = ms[:j] + '-' + ms[j+1:]
                elif ms[j] == 'Y':
                    num -= 1
    return ms


def checker(guess: str, answer: str):
    """
    gives a response to a guess
    :param guess: guessed word
    :param answer: actual word
    :return: string of G, Y, and -
    """
    MyString = ''
    for i in range(len(guess)):
        if i < len(answer) and guess[i] == answer[i]:
            MyString += 'G'
        elif answer.find(guess[i]) != -1:  # add clause for multiple of same letter
            MyString += 'Y'
        else:
            MyString += '-'
    MyString = remove(guess, MyString, answer)
    return MyString


