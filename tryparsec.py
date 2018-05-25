from pyparsec import *
aparser = char("a")
bparser = char("b")
print(aparser("a"))

print(aparser("abc"))
print(bparser("b"))
print(bparser("bca"))

abparser = aparser >> bparser
print(abparser("abc"))

abcdeparser = any_of(list("abcde"))
print(abcdeparser("abcde"))

abcparser = parse_string("abc")
print(abcparser("abc"))

lowerparser = many1(lletter).map(lambda l:"".join(l))
print(lowerparser("abcA"))

print(digits("12abc"))

twodigitparser = group(digit >> digit).map(lambda l: "".join(l[0]))
print(twodigitparser("12abcd"))

manyAparser = group(many(char("a")))
print(manyAparser("aaab"))

manyAparser = many(char("a"))
print(manyAparser("aaab"))

# print(lowerparser("helloworld"))
# whitespaceGreeting = whitespace >> lowerparser.group()
# print(whitespaceGreeting("\thello"))

# aquestionparser = char("a") >> optionally(char("?"))
# print(aquestionparser("a?"))

# qparser = many(lletter).group() >> char("?")
# print(qparser("hello?"))

# aorbparser = aparser | bparser
# print(aorbparser("acd"))
# print(aorbparser("bcd"))


# valp = forward(lambda:  digits | listp) 
# listp = char("{").suppress() >> sep_by(char(",").suppress(),many(valp).group()) >> char("}").suppress()

# print(run_parser(valp, "4"))
# print(valp("{8,6,7}"))
# print(valp("{1,2,{1,2}}"))

# surp = char("'")
# qword = surrounded_by(surp, many(any_of(string.ascii_letters)))
# print(qword("'hello'"))