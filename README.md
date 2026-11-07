# equarium

Solve physics problems from core equations with SymPy.

Start from the fundamental equations, say what you know and what you want, and let the solver derive the rest — symbolically first, then numerically.

This is a rebuild of [combine-equations.py](https://github.com/dharmatech/combine-equations.py), using what that project taught.

## Docs

- [Implementation series](docs/design/implementation/README.md): one
  numbered folder per series of changes, from the
  [project setup](docs/design/implementation/000-project-setup/README.md)
  on.

## Development

```bash
uv sync
uv run pytest
uv run pyright
```
