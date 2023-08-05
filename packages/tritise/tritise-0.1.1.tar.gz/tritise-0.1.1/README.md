# tritise

A small python library to handle trivial time series in an SQLite database.

## Installation

`pip install tritise`

## Example

```python
from tritise import Tritise
t = Tritise('test.sqlite')
t.add(1.1)
t.add(2)
t.add(3.0)
print(t.all())
print(t.last().value)

from dateutil.parser import parse
t.add(-1, tag='historic', timestamp=parse('1.1.2000'))
t.add(5, tag='historic', timestamp=parse('15.3.2001'))
t.add(200, tag='historic', timestamp=parse('21.9.2002'))

t.all('historic')
t.range(start_date = parse('1.1.2001'), end_date = parse('31.12.2001'), tag = 'historic')
```

## Command line tool

Tritise ships a command line tool (`tritise`) to inspect the created databases.

Run `tritise --help` for more information.

### CLI Example

`tritise dump -d test.sqlite`

