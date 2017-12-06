#coding=utf-8
def break_words(stuff):
    """This function will break up words for us."""
    words = stuff.split(' ')
    return words

#sorted 排序
def sort_words(words):
    """Sorts the words."""
    return sorted(words)
#pop()用于移除列表中的一个元素，并且返回该元素的值    
def print_first_word(words):
    """prints the first word after poping it off."""
    word = words.pop(0)
    return word
def print_last_word(words):
    """prints the last word after popping it off."""
    word = words.pop(-1)
    return word
def sort_sentence(sentence):
    """Take in full sentence and returns the sorter words."""
    words = break_words(sentence)
    return sort_words(words)
def print_first_and_last(sentence):
    """Prints the first and last words of the sentence."""
    words = break_words(sentence)
    a = print_first_word(words)
    b = print_last_word(words)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"

    print a
    print b
    print words

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"
    return (print_first_word(words) , print_last_word(words))
    
def print_first_and_last_sorted(sentence):
    """Sorts the words then prints the first and last one."""
    words = sort_sentence(sentence)
    a = print_first_word(words)
    b = print_last_word(words)
    return a,b
