"""
Python Standard Library - Kath Hodge

\\Built-in library
and
or
sorted
seek
readlines
read
r+
w
a
min
max
range
<> - Comparison operators
round
abs
pow

\\Math library
.ceil
.floor
.gcd

\\itertools library
.permutations 'all combinations
.combination 'unique combo
.count
.repeat
.cycle

\\sys library
.argv
.weekday
zipfile
.ZipFile
	.extract
	.infolist

\\tempfile library - bytes

\\datetime library
datetime.datetime
.strftime %a %A %d
%b %B %m
%H %M %S %p
%y %Y
.timedelta 'future dates

\\calendar
.month year month
.weekday
.isleap


\\time
.sleep

\\html.parser.HTMLParser

feed()
HTMLParser()

\\textwrap

.fill()  - initial indent/subsequent indent
.dedent()
.shorten() - limits characters

\\urllib
.request
..urlopen(url)
.read() - but decode to utf 8 first text.decode('utf-8')
\\json
json.loads(decoded text) - is named tuple, call attributes by ['name']


\\\\Advance python - Joe Marini

\\chapter 2
PEP 8

Spaces instead of tabs
79 Character limit, 72 for docstrings/comments
import at top, each one line
functions/class separated two lines
within, separated one line
no spaces around function calls, indexes, keyword arguments

bytes - encode/decode

\\chapter 3 - utilities

any/all returns boolean on sets of data
min/max returns min max of value in list
sum - sums list
map() - maps one value to another, creates new sequence of values
iter(list, 'sentinel value where the loop stops')
enumerate() loop with index
zip() can be used on two list to return both list at same time stops at shortest list


filter() 

def filterFunc(x):
    if x % 3 != 0:
        return False
    return True

# TODO: use filter to remove items on a list

odds = [1,2,3,4,5,6,7,8,9,10,11,12,13]
print(list(filter(filterFunc,odds)))

isupper() - returns boolean if char is upper

def filterFunc2(x):
    if x.isupper():
        return False
    return True

letters = 'abDcdEFGhiJkLmnOp'

lowers = list(filter(filterFunc2,letters))
print(lowers)

#itertools
.accumulate() - aggregates values
.chain() - combines two sets of data into one list per item
.dropwhile() - ignore until triggered
.takewhile() - returns until triggered

\\chapter 4
\\.__doc__
import Commands
import PyPDF2

print(PyPDF2.PdfFileReader.__doc__)
PEP 257

\\ variable arguments
*args - multiple args - to be added on last arg

\\Lambda
small, anonymous functions
can be passed as arguments where you need a function
typically used in a place just when needed

in line function

\\arg (arg,*,specific=None)
* disallows non specified argument for preceeding arguments

\\collections
import collections
namedtuple - named tuple
OrderedDict,defaultdict - Dicts with special properties
Counter - Counts distinct values
deque - double-ended list object

"""

print(map.__doc__)