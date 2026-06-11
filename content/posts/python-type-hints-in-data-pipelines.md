+++
title = 'Python Type Hints in Data Pipelines'
featured_image = 'images/python-types.png'
date = 2026-06-11T10:10:00+07:00
draft = false
tags = ['python', 'clean-code', 'engineering']
+++
# TL;DR
* Type hints make data transformations self-documenting.
* Use `Protocol` for structural typing in pipeline steps.
* Leverage `Annotated` for metadata like PII or Units.

# Why Types Matter for Data

## 1. Documenting Transformations
When a function takes a `DataFrame`, what's inside? Type hints combined with `TypedDict` or `Pydantic` models can clarify expectations.

```python
from typing import List, TypedDict

class UserRecord(TypedDict):
    id: int
    name: str
    is_active: bool

def process_users(data: List[UserRecord]) -> List[UserRecord]:
    return [u for u in data if u['is_active']]
```

## 2. Structural Typing with Protocols
In data engineering, we often care about what an object *does* rather than what it *is*. `typing.Protocol` allows for flexible, testable pipeline components.

```python
from typing import Protocol

class DataSink(Protocol):
    def write(self, data: dict) -> None: ...

def run_pipeline(sink: DataSink):
    sink.write({"status": "complete"})
```

## 3. Metadata with Annotated
You can use `Annotated` to tag fields with extra info that tools like `mypy` or custom linters can use.

```python
from typing import Annotated

PII = Annotated[str, "sensitive"]
email: PII = "user@example.com"
```
