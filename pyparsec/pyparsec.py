from functools import reduce
import string 
flatten = lambda l: [item for sublist in l for item in sublist]

class Maybe:
    pass

class Just(Maybe):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "<Just %s>"%str(self.val)
    
class Nothing(Maybe):
    def __str__(self):
        return "<Nothing>"

class Either:
    pass

class Left:
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return "(Left %s)"%self.errmsg

    def map(self, f):
        return self 

class Right:
    def __init__(self, val):
        self.val = val

    @property
    def val0(self):
        try:
            return flatten(self.val[0])
        except:
            return [self.val[0]]
    def __str__(self):
        return "(Right %s)"% str(self.val)
    
    def map(self, f):
        # flatlist = [item for sublist in self.val0 for item in sublist]

        return Right( (f(self.val0), self.val[1])) 

class Parser:
    def __init__(self, f):
        self.f = f
        self._suppressed = False

    def parse(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    __call__ = parse
    
    def __rshift__(self, rparser):
        return andThen(self, rparser)
    
    def __or__(self, rparser):
        return orElse(self, rparser)

    def map(self, transformer):
        return Parser(lambda *args, **kwargs: self.f(*args, **kwargs).map(transformer))

    setAction = map

    def suppress(self):
        self._suppressed = True 
        return self

    # def apply(self, f, otherP):
    #     arg1 = lambda : self.f 
    #     arg2 = lambda : otherP.f
    #     return lambda inp: f(arg1(inp), arg2(inp))

def pureP(x):
    def curried(s):
        return Right((x, s))
    return Parser(curried)

def applyP(p1, p2):
    def curried(s):
        print("S: ", s, type(s))
        res = p2(s)
        print("RES: ", res)
        return p1(*res.val[0])

    return curried
    

def compose(p1, p2):
    def newf(*args, **kwargs):
        return p2(p1(*args, **kwargs))
    return newf

def runParser(p, inp):
    return p(inp)

def andThen(p1, p2):
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
                if not p1._suppressed:
                    vs += v1
                if not p2._suppressed:
                    vs += v2

                return Right( (vs, res2.val[1])) 
            return res2
    return Parser(curried)

def orElse(p1, p2):
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


def parseChar(c):
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
    return foldl(orElse, parsers)


def anyOf(chars):
    return choice(list(map(parseChar, chars)))


def parseString(s):
    return foldl(andThen, list(map(parseChar, list(s))))

def parseDigit():
    return anyOf(list(string.digits))

def parseZeroOrMore(parser, inp): #zero or more
    res = parser(inp)
    if isinstance(res, Left):
        return "", inp
    else:
        firstval, restinpafterfirst = res.val
        subseqvals, remaining = parseZeroOrMore(parser, restinpafterfirst)
        values = None
        # print("FIRST VAL: ", firstval, type(firstval))
        # print("SUBSEQ: ", subseqvals, type(subseqvals))
        if isinstance(firstval, str):
            values = firstval+subseqvals
        elif isinstance(firstval, list):
            values = firstval+ ([subseqvals] if isinstance(subseqvals, str) else subseqvals)
        # print("VALUES: ", values, "REM: ", remaining)
        return values, remaining

def many(parser):
    def curried(s):
        return Right(parseZeroOrMore(parser,s))
    return Parser(curried)


def many1(parser):
    def curried(s):
        res = runParser(parser, s)
        if isinstance(res, Left):
            return res
        else:
            return runParser(many(parser), s)
    return Parser(curried)


whitespaceParser = anyOf(string.whitespace)

def optionally(parser):
    noneparser = Parser(lambda x: Right( (Nothing(), "")))
    return orElse(parser, noneparser)

between = lambda p1, p2 , p3 : p1 >> p2 >> p3

def sepBy1(sep, parser):
    sep_then_parser = sep >> parser
    return parser >> many(sep_then_parser)

def sepBy(sep, parser):
    return (sepBy1(sep, parser) | Parser(lambda x: Right( ([], ""))))


