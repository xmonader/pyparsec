from pyparsec import *

aparser = char("a")
bparser = char("b")

assert "a", "" == aparser("a").unwrap()
assert "b", "" == bparser("b").unwrap()

parsed, rem = aparser("abc").unwrap()
assert parsed, rem == ("a", "bc")

parsed, rem = bparser("bcd").unwrap()
assert parsed, rem == ("b", "cd")

abparser = aparser >> bparser
parsed, rem = abparser("abc").unwrap()
assert parsed, rem ==  ("ab", "c")

aorbparser = aparser | bparser
parsed, rem = aorbparser("acd").unwrap()
assert parsed, rem == ("a", "cd")

parsed, rem = aorbparser("bcd").unwrap()
assert parsed, rem == ("b", "cd")

abcdeparser = any_of(list("abcde"))
res = abcdeparser("abcde")
assert isinstance(res, Right) is True

assert "a", "bcde" ==  res.unwrap()
res = abcdeparser("ello")
assert "e", "llo" == res.unwrap()
assert isinstance(res, Right) is True


abcparser = parse_string("abc")
res = abcparser("abcd")
assert isinstance(res, Right)
assert "abc", "d" == res.unwrap()

lowerparser = many1(lletter)
res = lowerparser("abcA")
assert isinstance(res, Right)
assert "abc", "A" == res.unwrap()

res = digits("12abc")
assert isinstance(res, Right)
assert "12", "abc" == res.unwrap()

twodigitparser = digit >> digit
res = twodigitparser("12abcd")
assert isinstance(res, Right)
assert "12", "abc" == res.unwrap()

manyAparser = many(char("a"))
res = manyAparser("aaab")
assert "aaa", "b" == res.unwrap()


res = manyAparser("bbc") # zero or more
print("RES :", res)
assert ("", "bbc") == res.unwrap()

whitespaceGreeting = whitespace >> many(lowerparser)
res = whitespaceGreeting("\thello")
assert "\t", "hello" == res.unwrap()


many1aParser = many1(char("a"))
res = many1aParser("aaab")
assert "aaa", "b" == res.unwrap()
res = many1aParser("bbc") # one or more
assert isinstance(res, Left) is True



res = digits("12345bcd")
assert res.unwrap() == ("12345", "bcd")


aquestionparser = char("a") >> optionally(char("?"))
res = aquestionparser("a?")
assert res.unwrap() == (["a", "?"], "")

res = aquestionparser("a")
assert res.unwrap() == (["a", Nothing()], "")



ab_space_cd_parser = parse_string("ab") >> many1(whitespace).suppress() >> parse_string("cd")
res = ab_space_cd_parser("ab cd")
assert res.unwrap() == (["ab","cd"], "")

ab_space_cd_ef_parser = parse_string("ab") >> many1(whitespace).suppress() >> parse_string("cd") >> parse_string("ef")
res = ab_space_cd_ef_parser("ab cdef")
assert res.unwrap() == (["ab", "cd", "ef"], "")


adigitlist = sep_by(whitespace.suppress(), digit)
res = adigitlist('1 2 3 4 5')
assert res.unwrap() == (["1", "2", "3", "4", "5"], "")

# from functools import partial
# def add2(x, y):
#     print("X:",x  )
#     print("Y: ", y)
#     return x+y

# def add3(x, y, z):
#     return x+y+z
# def addargs(*args):
#     print("Args: ", args)
#     return sum(args)

# numparser = num_as_int 
# addparser2 = Parser(add2)
# p = ap(addparser2, numparser >> numparser )
# print(run_parser(p, "123"))

# addparser3 = Parser(addargs)

# p = ap(addparser3, (numparser >> numparser >> numparser) )
# print(run_parser(p, "123"))
# p = numparser >> numparser >> numparser
# print(run_parser(p, "123"))


valp = forward(lambda:  digits | listp) 
listp = char("[") >> sep_by(char(",").suppress(),many(valp)) >> char("]")

print(run_parser(valp, "4"))
print(valp("[8,6,7]"))
print(valp("[1,2,[1,2]]"))

surp = char("'")
qword = surrounded_by(surp, many(any_of(string.ascii_letters)))
print(qword("'hello'"))