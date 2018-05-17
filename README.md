# pyparsec
python parser combinators (parsec) library (under development)

## Examples

```ipython

In [2]: from pyparsec import *

In [3]: aparser = char("a")

In [4]: bparser = char("b")

In [5]: aparser("abc")
Out[5]: (Right ('a', 'bc'))

In [6]: bparser("abc")
Out[6]: <pyparsec.pyparsec.Left at 0x7f5fdd6746a0>

In [7]: bparser("bca")
Out[7]: (Right ('b', 'ca'))
```
so to create a parser for 1 character you use `char`
and to run parser you call it with input string 

```ipython
In [8]: aparser.parse("abc")
Out[8]: (Right ('a', 'bc'))

In [9]: aparser("abc")
Out[9]: (Right ('a', 'bc'))

In [10]: run_parser(aparser, "abc")
Out[10]: (Right ('a', 'bc'))
```
using `__call__` is the same as calling `.parse` or calling `run_parser` directly

### you can combine parsers using `>>`

```ipython
In [12]: abparser = aparser >> bparser

In [13]: abparser.parse("abc")
Out[13]: (Right (['a', 'b'], 'c'))

In [14]: abparser.parse("bca")
Out[14]: <pyparsec.pyparsec.Left at 0x7f5fdd58ab38>
```
`aparser >> bparser` is read `aparser is followed by bparser`

### How about Or? can we do ors?
```
In [15]: aorb = aparser | bparser

In [16]: aorb.parse("adef")
Out[16]: (Right ('a', 'def'))

In [17]: aorb.parse("bdef")
Out[17]: (Right ('b', 'def'))
```

### Parsing greetings

```ipython

In [2]: from pyparsec import *

In [3]: sentp = letters >> char(",") >> many(whitespace) >> letters >> optionally(char("!"))

In [4]: sent = "Hello, World!"

In [5]: sentp.parse(sent)
Out[5]: (Right (['Hello', ',', ' ', 'World', '!'], ''))
```


### transform!
```ipython
In [8]: sentp = letters.map(lambda l: "".join(l).upper()) >> char(",") >> many(whitespace) >> letters >> optionally(char("!"))

In [9]: sentp.parse(sent)
Out[9]: (Right (['HELLO', ',', ' ', 'World', '!'], ''))
```
you can map a function to be applied on a `list` parsed by a parser.


### suppress
you can also suppress certain parsed values 
```
In [12]: sentp = letters.map(lambda l: "".join(l).upper()) >> char(",").suppress() >> many(whitespace).suppress() >> letters >> optionally(char("!")).suppress()

In [13]: sentp.parse(sent)
Out[13]: (Right (['HELLO', 'World'], ''))
```

```
In [17]: lowerparser = anyOf(string.ascii_lowercase)
In [18]: singlequote = char('"')

In [20]: quotedword = between(singlequote, many1(lowerparser), singlequote)
    ...: print(quotedword('"abc"'))

(Right (['"', 'abc', '"'], ''))
```

```ipython
In [23]: digitparser = anyOf(string.digits)
    ...:

In [24]: adigitlist = sepBy(whitespace.suppress(), digitparser)
    ...:

In [25]: print(run_parser(adigitlist, '1 2 3 4 5'))
    ...:
(Right (['1', '2', '3', '4', '5'], ''))
```

### forward declarations
```ipython
In [4]: valp = forward(lambda:  digits | listp)
   ...: listp = char("[") >> sepBy(char(",").suppress(),many(valp)) >> char("]")
   ...:
   ...: print(run_parser(valp, "4"))
   ...: print(valp("[8,6,7]"))
   ...: print(valp("[1,2,[1,2]]"))
   ...:
(Right ('4', ''))
(Right (['[', '8', '6', '7', ']'], ''))
(Right (['[', '1', '2', '[', '1', '2', ']', ']'], ''))

```

### builtins
```ipython
In [1]: from pyparsec import *

In [2]: letter("abc")
Out[2]: (Right ('a', 'bc'))

In [3]: letters("abc")
Out[3]: (Right ('abc', ''))

In [4]: word("abc")
Out[4]: (Right ('abc', ''))

In [5]: word("123")
Out[5]: <pyparsec.pyparsec.Left at 0x7fea1904c048>

In [6]: digits("123")
Out[6]: (Right ('123', ''))

In [7]: digits_as_int("123")
Out[7]: (Right (123, ''))

In [8]: quotedword('"Hello, World"')
Out[8]: <pyparsec.pyparsec.Left at 0x7fea1904f7b8>

In [9]: quotedword('"Hello"')
Out[9]: (Right (['"', 'Hello', '"'], ''))

```



> It's not production ready, please use pyparsing instead or send me PRs to make it better :)