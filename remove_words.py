import enchant
d = enchant.Dict("en_US")

file = open('words.txt', 'r')
text = file.read()
words = text.split('\n')

new_words = [word for word in words if d.check(word)]

new_text = '\n'
new_text = new_text.join(new_words)

new_file = open('curated.txt', 'w+')
new_file.write(new_text)
