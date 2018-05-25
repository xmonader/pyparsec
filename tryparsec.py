from pyparsec import *
# aparser = char("a")
# bparser = char("b")
# print(aparser("a"))

# print(aparser("abc"))
# print(bparser("b"))
# print(bparser("bca"))

# abparser = aparser >> bparser
# print(abparser("abc"))

# abcdeparser = any_of(list("abcde"))
# print(abcdeparser("abcde"))

# abcparser = parse_string("abc")
# print(abcparser("abc"))

lowerparser = many1(lletter)
# print(lowerparser("abcA"))

# print(digits("12abc"))

# twodigitparser = group((digit >> digit))
# print(twodigitparser("12abcd"))

# manyAparser = group(many(char("a")))
# print(manyAparser("aaab"))

print(lowerparser("helloworld"))
whitespaceGreeting = whitespace >> lowerparser
print(whitespaceGreeting("\thello"))

aquestionparser = char("a") >> optionally(char("?"))
print(aquestionparser("a?"))

qparser = many(lletter) >> char("?")
print(qparser("hello?"))