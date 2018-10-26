from pyparsec import *

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
if isinstance(res, Right):
    parsed, remaining = res.unwrap()
    for secinfo in parsed:
        secname = secinfo[0]
        kvs = secinfo[1:]
        print("SEC: ", secname)
        for (k,v) in kvs:
            print("\t", k, v)
