# pyparsec
python parser combinators (parsec) library

## Example
```python
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
```


> It's not production ready, please use pyparsing instead or send me PRs to make it better :)