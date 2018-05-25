from functools import reduce
import string 
import sys

sys.setrecursionlimit(100000)
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
    def __init__(self, state):
        self.state = state

    def unwrap(self):
        return self.state

    # @property
    # def val0(self):
    #     # if isinstance(self.val[0], list):
    #     #     return flatten(self.val[0])
    #     # else:
    #     #     return [self.val[0]]
    #     return self.state.parsed

    def __str__(self):
        return "(Right %s)"% str(self.state)
    __repr__ = __str__

    def map(self, f):
        return Right(State(f(self.state.parsed), self.state.remaining))

class State:
    def __init__(self, parsed, remaining=""):
        self.parsed = parsed
        self.remaining = remaining
        self.val = (parsed, remaining)
        self.txt = ""
        self.idx = 0

    @property
    def line(self):
        return len(self.txt[:self.idx].splitlines())

    @property
    def col(self):
        txtuntilnow = self.txt[:self.idx]
        return len(txtuntilnow) - (txtuntilnow.rindex("\n") if "\n" in txtuntilnow else 0)

    def __getitem__(self, idx):
        return self.val[idx]        

    def __str__(self):
        return "@{}(line {}, column {})  ('{}', '{}')".format(self.idx, self.line, self.col, self.parsed, self.remaining)
    
    __repr__ = __str__

class Parser:
    def __init__(self, f):
        self.f = f
        self.name = ""
        self._suppressed = False
        self._originalf = self.f

    def parse(self, *args, **kwargs):
        # print("Calling parse with args: ", *args)
        return self.f(*args, **kwargs)

    __call__ = parse
    
    def __rshift__(self, rparser):
        return and_then(self, rparser)

    def __lshift__(self, rparser):
        return and_then(self, rparser)
    
    def __or__(self, rparser):
        return or_else(self, rparser)

    def map(self, transformer):
        p =  Parser(lambda *args, **kwargs: self.f(*args, **kwargs).map(transformer))
        p._originalf = self.f
        return p

    def __mul__(self, times):
       return n(self, times) 

    set_action = map

    def suppress(self):
        self._suppressed = True 
        return self

    def group(self):
        return group(self)

    def setname(self, name=""):
        self.name = name or self.__class__.__name__


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
    res = p(inp)
    return res

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
            state1 = res1.state
            res2 = p2(state1.remaining) # parse remaining chars.
            if isinstance(res2, Right):
                state2 = res2.state
                v1 = state1.parsed
                v2 = state2.parsed
                vs = []
                if not p1._suppressed and _isokval(v1):
                    vs += v1
                if not p2._suppressed and _isokval(v2):
                    vs += v2
                resstate = State(parsed=vs, remaining=state2.remaining)
                resstate.idx += state1.idx + state2.idx
                resstate.txt = state1.txt
                print("RES STATE: ", resstate, resstate.idx)

                return Right( resstate )
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
                parsed, remaining = res.state.val
                s = remaining
                fullparsed += parsed
        state = State(fullparsed, s)
        return Right(s)
    return Parser(curried)

def or_else(p1, p2):
    def curried(s):
        res = p1(s)
        # print("RES: ", res)
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
                state = State(c, s[1:])
                state.txt = s
                state.idx += 1
                return Right(state)
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
            state = State("", s)
            if seq == s[:len(seq)]:
                return Right(state)
            else:
                return Left("Expecting '%s' and found '%s'"%(seq, s[:len(seq)]))
    return Parser(curried)

def group(p):
    def curried(s):
        if not s:
            msg = "S is empty"
            return Left(msg)
        else:
            res = p.parse(s)
            if isinstance(res, Left):
                return res
            else:
                # print("RES: ", res)
                state = State([res.state.parsed], res.state.remaining)
                return Right(state)
    return Parser(curried)

def pushseq(seq):
    def curried(s):
        if not s:
            msg = "S is empty"
            return Left(msg)
        else:
            s = seq + s
            state = State("", s)
            return Right(state)

    return Parser(curried)

def until(p):
    def curried(s):
        res = p(s)
        if isinstance(res, Left):
            return res
        else:
            return Right(State("", s))
    return Parser(curried)

chars = parse_string

def parse_zero_or_more(parser, inp): #zero or more
    res = parser(inp)
    if isinstance(res, Left):
        return "", inp
    else:
        firstval, restinpafterfirst = res.state.val
        subseqvals, remaining = parse_zero_or_more(parser, restinpafterfirst)
        values = firstval
        # print("FIRST:", firstval, "SUBSEQ: ", subseqvals)
        if subseqvals:
            if isinstance(firstval, str):
                values = firstval+subseqvals
            elif isinstance(firstval, list):
                values = firstval+ ([subseqvals] if isinstance(subseqvals, str) else subseqvals)
        # print("RETURNING: ", values, remaining)
        return values, remaining

def many(parser):
    def curried(s):
        values, rem = parse_zero_or_more(parser, s)
        # print("VALUES: ", values)
        return Right(State(values, rem))
    return Parser(curried)


def many1(parser):
    def curried(s):
        res = parser._originalf(s)
        # print("APPLYING ORIGINALF ON ", s )
        if isinstance(res, Left):
            return res
        else:
            return run_parser(many(parser), s)
    return Parser(curried)


def optionally(parser):
    noneparser = Parser(lambda x: Right( State(Nothing(), "")))
    return or_else(parser, noneparser)

def sep_by1(sep, parser):
    sep_then_parser = sep >> parser
    return parser >> many(sep_then_parser)

def sep_by(sep, parser):
    return (sep_by1(sep, parser) | Parser(lambda x: Right( State([], ""))))

def forward(parsergeneratorfn):
    def curried(s):
        return parsergeneratorfn()(s)
    return curried

letter = any_of(string.ascii_letters)
lletter = any_of(string.ascii_lowercase)
uletter = any_of(string.ascii_uppercase)
digit = any_of(string.digits)
digits = many1(digit).map((lambda l: ["".join(l)]))
whitespace = any_of(string.whitespace)
ws = whitespace.suppress()
whites = many(ws)
letters = many1(letter).map((lambda l: ["".join(l)]))
word = letters
newline = char("\n")
alphanumword = (letter >> (letters|digits)).map((lambda l: ["".join(l)]))
num_as_int = digits.map(lambda l: int("".join(l)))
between = lambda p1, p2 , p3 : p1 >> p2 >> p3
surrounded_by = lambda surparser, contentparser: surparser >> contentparser >> surparser
quotedword = surrounded_by( (char('"')|char("'")).suppress() , word)
option = optionally

# commasepareted_p = sep_by(char(",").suppress(), many1(word) | many1(digit) | many1(quotedword))
commaseparated_of = lambda p: sep_by(char(",").suppress(), many(p))

