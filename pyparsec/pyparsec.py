from functools import reduce
import string 
flatten = lambda l: [item for sublist in l for item in (sublist if isinstance(sublist, list) else [sublist] )]

class Maybe:
    pass

class Just(Maybe):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "<Just %s>"%str(self.val)
    
class Nothing(Maybe):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __str__(self):
        return "<Nothing>"

class Either:
    pass

class Left:
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return "(Left %s)"%self.errmsg

    __repr__ = __str__
    def map(self, f):
        return self 

class Right:
    def __init__(self, val):
        self.val = val

    def unwrap(self):
        return self.val

    @property
    def val0(self):
        if isinstance(self.val[0], list):
            return flatten(self.val[0])
        else:
            return [self.val[0]]

    def __str__(self):
        return "(Right %s)"% str(self.val)
    __repr__ = __str__

    def map(self, f):
        return Right( (f(self.val0), self.val[1])) 


class Parser:
    def __init__(self, f):
        self.f = f
        self._suppressed = False

    def parse(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    __call__ = parse
    
    def __rshift__(self, rparser):
        return and_then(self, rparser)

    def __lshift__(self, rparser):
        return and_then(self, rparser)
    
    def __or__(self, rparser):
        return or_else(self, rparser)

    def map(self, transformer):
        return Parser(lambda *args, **kwargs: self.f(*args, **kwargs).map(transformer))

    def __mul__(self, times):
       return n(self, times) 

    set_action = map

    def suppress(self):
        self._suppressed = True 
        return self

def pure(x):
    def curried(s):
        return Right((x, s))
    return Parser(curried)

def ap(p1, p2):
    def curried(s):
        res = p2(s)
        return p1(*res.val[0])
    return curried

def compose(p1, p2):
    def newf(*args, **kwargs):
        return p2(p1(*args, **kwargs))
    return newf

def run_parser(p, inp):
    return p(inp)

def _isokval(v):
    if isinstance(v, str) and not v.strip():
        return False
    if isinstance(v, list) and v and v[0] == "":
        return False
    return True

def and_then(p1, p2):
    def curried(s):
        res1 = p1(s)
        if isinstance(res1, Left):
            return res1
        else:
            res2 = p2(res1.val[1]) # parse remaining chars.
            if isinstance(res2, Right):
                v1 = res1.val0
                v2 = res2.val0
                vs = []
                if not p1._suppressed and _isokval(v1):
                    vs += v1 
                if not p2._suppressed and _isokval(v2):
                    vs += v2

                return Right( (vs, res2.val[1])) 
            return res2
    return Parser(curried)

def n(parser, count):
    def curried(s):
        fullparsed = ""
        for i in range(count):
            res = parser(s)
            if isinstance(res, Left):
                return res
            else:
                parsed, remaining = res.unwrap()
                s = remaining
                fullparsed += parsed
        return Right((fullparsed, s))
    return Parser(curried)

def or_else(p1, p2):
    def curried(s):
        res = p1(s)
        if isinstance(res, Right):
            return res
        else:
            res = p2(s)
            if isinstance(res, Right):
                return res
            else:
                return Left("Failed at both") 
    return Parser(curried)

def char(c):
    def curried(s):
        if not s:
            msg = "S is empty"
            return Left(msg)
        else:
            if s[0] == c:
                return Right((c, s[1:]) )
            else:
                return Left("Expecting '%s' and found '%s'"%(c, s[0]))
    return Parser(curried)

foldl = reduce
def choice(parsers):
    return foldl(or_else, parsers)

def any_of(chars):
    return choice(list(map(char, chars)))

def parse_string(s):
    return foldl(and_then, list(map(char, list(s)))).map(lambda l: "".join(l))

def until_seq(seq):
    def curried(s):
        if not s:
            msg = "S is empty"
            return Left(msg)
        else:
            if seq == s[:len(seq)]:
                return Right(("", s))
            else:
                return Left("Expecting '%s' and found '%s'"%(seq, s[:len(seq)]))
    return Parser(curried)

def until(p):
    def curried(s):
        res = p(s)
        if isinstance(res, Left):
            return res
        else:
            return Right(("", s))
    return Parser(curried)

chars = parse_string

def parse_zero_or_more(parser, inp): #zero or more
    res = parser(inp)
    if isinstance(res, Left):
        return "", inp
    else:
        firstval, restinpafterfirst = res.val
        subseqvals, remaining = parse_zero_or_more(parser, restinpafterfirst)
        values = firstval
        if subseqvals:
            if isinstance(firstval, str):
                values = firstval+subseqvals
            elif isinstance(firstval, list):
                values = firstval+ ([subseqvals] if isinstance(subseqvals, str) else subseqvals)
        return values, remaining

def many(parser):
    def curried(s):
        return Right(parse_zero_or_more(parser,s))
    return Parser(curried)


def many1(parser):
    def curried(s):
        res = run_parser(parser, s)
        if isinstance(res, Left):
            return res
        else:
            return run_parser(many(parser), s)
    return Parser(curried)


def optionally(parser):
    noneparser = Parser(lambda x: Right( (Nothing(), "")))
    return or_else(parser, noneparser)

def sep_by1(sep, parser):
    sep_then_parser = sep >> parser
    return parser >> many(sep_then_parser)

def sep_by(sep, parser):
    return (sep_by1(sep, parser) | Parser(lambda x: Right( ([], ""))))

def forward(parsergeneratorfn):
    def curried(s):
        return parsergeneratorfn()(s)
    return curried

letter = any_of(string.ascii_letters)
lletter = any_of(string.ascii_lowercase)
uletter = any_of(string.ascii_uppercase)
digit = any_of(string.digits)
digits = many1(digit)
whitespace = any_of(string.whitespace)
ws = whitespace.suppress()
letters = many1(letter)
word = letters
alphanumword = many(letter >> (letters|digits))
num_as_int = digits.map(lambda l: int("".join(l)))
between = lambda p1, p2 , p3 : p1 >> p2 >> p3
surrounded_by = lambda surparser, contentparser: surparser >> contentparser >> surparser
quotedword = surrounded_by( (char('"')|char("'")).suppress() , word)
option = optionally

# commasepareted_p = sep_by(char(",").suppress(), many1(word) | many1(digit) | many1(quotedword))
commaseparated_of = lambda p: sep_by(char(",").suppress(), many(p))

