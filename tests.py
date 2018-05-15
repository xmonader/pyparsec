from pyparsec import *

aparser = parseChar("a")
bparser = parseChar("b")

print(runParser(aparser, "abc"))
print(runParser(bparser, "bcd"))

abparser = andThen(aparser, bparser)
print(runParser(abparser, "abc"))

aorbparser = orElse(aparser, bparser)
print(runParser(aorbparser, "akcd"))
print(runParser(aorbparser, "bkcd"))

abparser = aparser >> bparser
print(runParser(abparser, "abc"))

aorbparser = aparser| bparser
print(runParser(aorbparser, "akcd"))
print(runParser(aorbparser, "bkcd"))

abcdeparser = anyOf(list("abcde"))
print(runParser(abcdeparser, "abcde"))
print(runParser(abcdeparser, "ello"))

abcparser = parseString("abc")
print(runParser(abcparser, "abcd"))

lowerparser = anyOf(string.ascii_lowercase)
print(runParser(lowerparser, "abcd"))


digitparser = anyOf(string.digits)
print(runParser(digitparser, "12abc"))
twodigitparser = digitparser >> digitparser

print(runParser(twodigitparser, "12abcd"))

converToInt = lambda l: int("".join(l))
twodigitparserAsInt = twodigitparser.map(converToInt)
print(runParser(twodigitparserAsInt, "12abcd"))
manyAparser = many(parseChar("a"))
print(runParser(manyAparser, "aaab"))
print(runParser(manyAparser, "bbc")) # zero or more

print(runParser(whitespaceParser, "\thello"))
whitespaceGreeting = whitespaceParser >> many(lowerparser)
print(runParser(whitespaceGreeting, "\thello"))

many1aParser = many1(parseChar("a"))
print(runParser(many1aParser, "aaab"))
print(runParser(many1aParser, "bbc")) # zero or more

manyDigits = many1(digitparser)
manyDigitsAsInt = manyDigits.map(converToInt)
print(runParser(manyDigitsAsInt, "12345bcd"))


aquestionparser = parseChar("a") >> optionally(parseChar("?"))
print(runParser(aquestionparser, "a?"))
print(runParser(aquestionparser, "a"))


pint = optionally(parseChar("-")) >> manyDigits
def convertToNum(args):
    sign = args[0]
    num = "".join(args[1:])
    num = int(num)
    if sign == "-":
        return num*-1
    return num
parsesignedint = pint.map(convertToNum)
print(runParser(parsesignedint, "-10"))


singlequote = parseChar('"')
wordinquotes = None
def oninnerword(x):
    global wordinquotes
    wordinquotes = x
    return x



ab_space_cd_parser = parseString("ab") >> many1(whitespaceParser) >> parseString("cd")
print(ab_space_cd_parser("ab cd"))

ab_space_cd_ef_parser = parseString("ab") >> many1(whitespaceParser) >> parseString("cd") >> parseString("ef")
print(ab_space_cd_ef_parser("ab cdef"))

quotedword = between(singlequote, many1(lowerparser).map(oninnerword), singlequote)
print(quotedword('"abc"'))
print(wordinquotes)


def onitem(l):
    return l 


adigitlist = sepBy1(whitespaceParser.suppress(), digitparser).map(onitem)

print(runParser(adigitlist, '1 2 3 4 5'))

