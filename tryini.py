from pyparsec import *

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
        else:
            return []
    wrapper.has_run = False
    return wrapper

action = run_once


kv = (word >> option(whites) >> char("=").suppress() >> option(whites) >> word >> newline.suppress()).group()
section = (char("[").suppress() >> many(word | whitespace)>> char("]").suppress() >> newline.suppress() >> many1(kv)).group()
inifile = many1(section)


txt = """[login]
user=ahmed
email=theredotcom
[publisher]
host=github
"""

res = inifile(txt)
print(res)
if isinstance(res, Right):
    state = res.state
    print(state.parsed)
    for secinfo in state.parsed:
        secname = secinfo[0]
        kvs = secinfo[1:]
        print("SEC: ", secname)
        for (k,v) in kvs:
            print("\t", k, v)

# p = (word.map(lambda l: ["".join(l)]) >> whitespace >> word)
# print(p("hello world"))