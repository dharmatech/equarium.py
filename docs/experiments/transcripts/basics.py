"""A plain Python script, for transcript mode:

    uv run python -m equarium.transcript docs/experiments/transcripts/basics.py
"""

# A value, and an expression with it.
x = 5
x * 2

# An assignment shows the value it bound; a `;` hides it.
y = x**2 + 1
z = y - x;

print("y is", y)

names = ["Ada", "Grace", "Barbara"]
[name.upper() for name in names]

def greet(name):
    return f"Hello, {name}!"

greet(names[0])
len(names), sum(len(name) for name in names)
