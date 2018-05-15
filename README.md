# pyparsec
python parser combinators (parsec) library (under development)

## Examples

```ipython

In [2]: from pyparsec import *

In [3]: aparser = parseChar("a")

In [4]: bparser = parseChar("b")

In [5]: aparser("abc")
Out[5]: (Right ('a', 'bc'))

In [6]: bparser("abc")
Out[6]: <pyparsec.pyparsec.Left at 0x7f5fdd6746a0>

In [7]: bparser("bca")
Out[7]: (Right ('b', 'ca'))
```
so to create a parser for 1 character you use `parseChar`
and to run parser you call it with input string 

```ipython
In [8]: aparser.parse("abc")
Out[8]: (Right ('a', 'bc'))

In [9]: aparser("abc")
Out[9]: (Right ('a', 'bc'))

In [10]: runParser(aparser, "abc")
Out[10]: (Right ('a', 'bc'))
```
using `__call__` is the same as calling `.parse` or calling `runParser` directly

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

In [3]: sentp = letters >> parseChar(",") >> many(whitespaceParser) >> letters >> optionally(parseChar("!"))

In [4]: sent = "Hello, World!"

In [5]: sentp.parse(sent)
Out[5]: (Right (['Hello', ',', ' ', 'World', '!'], ''))
```


### transform!
```ipython
In [8]: sentp = letters.map(lambda l: "".join(l).upper()) >> parseChar(",") >> many(whitespaceParser) >> letters >> optionally(parseChar("!"))

In [9]: sentp.parse(sent)
Out[9]: (Right (['HELLO', ',', ' ', 'World', '!'], ''))
```
you can map a function to be applied on a `list` parsed by a parser.


### suppress
you can also suppress certain parsed values 
```
In [12]: sentp = letters.map(lambda l: "".join(l).upper()) >> parseChar(",").suppress() >> many(whitespaceParser).suppress() >> letters >> optionally(parseCh
    ...: ar("!")).suppress()

In [13]: sentp.parse(sent)
Out[13]: (Right (['HELLO', 'World'], ''))
```

```
In [17]: lowerparser = anyOf(string.ascii_lowercase)
In [18]: singlequote = parseChar('"')

In [20]: quotedword = between(singlequote, many1(lowerparser), singlequote)
    ...: print(quotedword('"abc"'))

(Right (['"', 'abc', '"'], ''))
```

```ipython
In [23]: digitparser = anyOf(string.digits)
    ...:

In [24]: adigitlist = sepBy(whitespaceParser.suppress(), digitparser)
    ...:

In [25]: print(runParser(adigitlist, '1 2 3 4 5'))
    ...:
(Right (['1', '2', '3', '4', '5'], ''))
```

### forward declarations
```ipython
In [4]: nump = digitparser
   ...: valp = forward(lambda:  digitparser | listp)
   ...: listp = parseChar("[") >> sepBy(parseChar(",").suppress(),many(valp)) >> parseChar("]")
   ...:
   ...: print(runParser(valp, "4"))
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

In [2]: letter_p("abc")
Out[2]: (Right ('a', 'bc'))

In [3]: letters_p("abc")
Out[3]: (Right ('abc', ''))

In [4]: word_p("abc")
Out[4]: (Right ('abc', ''))

In [5]: word_p("123")
Out[5]: <pyparsec.pyparsec.Left at 0x7fea1904c048>

In [6]: num_p("123")
Out[6]: (Right ('123', ''))

In [7]: int_p("123")
Out[7]: (Right (123, ''))

In [8]: quotedword_p('"Hello, World"')
Out[8]: <pyparsec.pyparsec.Left at 0x7fea1904f7b8>

In [9]: quotedword_p('"Hello"')
Out[9]: (Right (['"', 'Hello', '"'], ''))

In [7]: commasepareted_p('1,2,3')
Out[7]: (Right (['1', '2', '3'], ''))

In [8]: commasepareted_p('a,b,c')
Out[8]: (Right (['a', 'b', 'c'], ''))

In [9]: commasepareted_p('"a","b","c"')
Out[9]: (Right (['a', 'b', 'c'], ''))
```



> It's not production ready, please use pyparsing instead or send me PRs to make it better :)