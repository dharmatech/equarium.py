"""A plain Python script, for transcript mode:

    uv run python -m equarium.transcript docs/transcripts/basics.py
"""

# A value, and an expression with it.
x = 5
#> 5
x * 2
#> 10

# An assignment shows the value it bound; a `;` hides it.
y = x**2 + 1
#> 26
z = y - x + 3
#> 24

print("y is", y)
#> y is 26

names = ["Ada", "Grace", "Barbara"]
#> ['Ada', 'Grace', 'Barbara']
[name.upper() for name in names]
#> ['ADA', 'GRACE', 'BARBARA']

def greet(name):
    return f"Hello, {name}!"

greet(names[0])
#> 'Hello, Ada!'
len(names), sum(len(name) for name in names)
#> (3, 15)

"abc"
#> 'abc'

"abc" + "bcd"
#> 'abcbcd'

123 + 234 + 345
#> 702

123 + 234
#> 357

345
#> 345
