from pyparsec import *

aparser = char("a")
bparser = char("b")

lowerparser = many1(lletter)

def test_char_parser():
    aparser = char("a")
    bparser = char("b")

    assert "a", "" == aparser("a").unwrap()
    assert "b", "" == bparser("b").unwrap()

def test_parser_and_remains():
    parsed, rem = aparser("abc").unwrap()
    assert parsed, rem == ("a", "bc")

    parsed, rem = bparser("bcd").unwrap()
    assert parsed, rem == ("b", "cd")

def test_parser_followed_by_parser():
    abparser = aparser >> bparser
    parsed, rem = abparser("abc").unwrap()
    assert parsed, rem ==  ("ab", "c")

def test_alternate_parser():
    aorbparser = aparser | bparser
    parsed, rem = aorbparser("acd").unwrap()
    assert parsed, rem == ("a", "cd")

    parsed, rem = aorbparser("bcd").unwrap()
    assert parsed, rem == ("b", "cd")

def test_anyof_parser():

    abcdeparser = any_of(list("abcde"))
    res = abcdeparser("abcde")
    assert isinstance(res, Right) is True
    assert "a", "bcde" ==  res.unwrap()
    res = abcdeparser("ello")
    assert "e", "llo" == res.unwrap()
    assert isinstance(res, Right) is True

def test_parse_string():
    abcparser = parse_string("abc")
    res = abcparser("abcd")
    assert isinstance(res, Right)
    assert "abc", "d" == res.unwrap()

def test_lower_parser():
    res = lowerparser("abcA")
    assert isinstance(res, Right)
    assert "abc", "A" == res.unwrap()

def test_digits_parser():
    res = digits("12abc")
    assert isinstance(res, Right)
    assert "12", "abc" == res.unwrap()

    twodigitparser = digit >> digit
    res = twodigitparser("12abcd")
    assert isinstance(res, Right)
    assert "12", "abc" == res.unwrap()

def test_many_parser():
    manyAparser = many(char("a"))
    res = manyAparser("aaab")
    print(res)
    assert ("aaa", "b") == res.unwrap()
    res = manyAparser("bbc") # zero or more
    assert res.unwrap() == ("", "bbc")


def test_parse_greeting():
    whitespaceGreeting = whitespace >> many(lowerparser)
    res = whitespaceGreeting("\thello")
    assert "\t", "hello" == res.unwrap()


def test_parse_many1():
    many1aParser = many1(char("a"))
    res = many1aParser("aaab")
    assert "aaa", "b" == res.unwrap()
    res = many1aParser("bbc") # one or more
    assert isinstance(res, Left) is True

def test_parse_digits():
    res = digits("12345bcd")
    assert "12345", "bcd" == res.unwrap()

def test_parse_question():
    aquestionparser = char("a") >> optionally(char("?"))
    res = aquestionparser("a?")
    assert  ["a", "?"], "" == res.unwrap()
    res = aquestionparser("a")
    assert ["a", nothing], "" == res.unwrap()  


def test_abspace_cd_parsed():
    ab_space_cd_parser = parse_string("ab") >> many1(whitespace).suppress() >> parse_string("cd")
    res = ab_space_cd_parser("ab cd")
    assert res.unwrap() == (["ab","cd"], "")
    ab_space_cd_ef_parser = parse_string("ab") >> many1(whitespace).suppress() >> parse_string("cd") >> parse_string("ef")
    res = ab_space_cd_ef_parser("ab cdef")
    assert res.unwrap() == (["ab", "cd", "ef"], "")


def test_digitlist_parser():
    adigitlist = sep_by(whitespace.suppress(), digit)
    res = adigitlist('1 2 3 4 5')
    assert res.unwrap() == (["1", "2", "3", "4", "5"], "")


# # from functools import partial
# # def add2(x, y):
# #     print("X:",x  )
# #     print("Y: ", y)
# #     return x+y

# # def add3(x, y, z):
# #     return x+y+z
# # def addargs(*args):
# #     print("Args: ", args)
# #     return sum(args)

# # numparser = num_as_int 
# # addparser2 = Parser(add2)
# # p = ap(addparser2, numparser >> numparser )
# # print(run_parser(p, "123"))

# # addparser3 = Parser(addargs)

# # p = ap(addparser3, (numparser >> numparser >> numparser) )
# # print(run_parser(p, "123"))
# # p = numparser >> numparser >> numparser
# # print(run_parser(p, "123"))

def test_parse_forward_decl():
    valp = forward(lambda:  digits | listp) 
    listp = char("[") >> sep_by(char(",").suppress(),many(valp)) >> char("]")
    res = valp("4")
    assert res.unwrap() == ("4", "")
    res = valp("[8,6,7]")
    assert res.unwrap() == (["[", "8", "6", "7", "]"], "")
    # print(valp("[1,2,[1,2]]"))
    # assert True

def test_quoted_word_parser():
    surp = char("'")
    qword = surrounded_by(surp, many(any_of(string.ascii_letters))).map(lambda l: "".join(l))
    
    res = qword("'hello'")
    assert res.unwrap() == ("'hello'", "")