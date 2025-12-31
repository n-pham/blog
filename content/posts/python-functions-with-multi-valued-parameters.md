+++
title = 'Python Functions with Multi-Valued Parameters'
featured_image = 'images/python-functions-with-multi-valued-parameters.png'
date = 2025-12-31T14:15:00+07:00
draft = false
tags = ['python']
+++

# Python Functions with Multi-Valued Parameters

`str.strip()` takes a string that is treated as a set of characters.
```python
>>> "  Hello world! ".strip(" !")
'Hello world'
```

`str.startswith` and `str.endswith` accept a tuple of values.
```python
>>> files = ["a/file1.md", "b/file2.py", "c/file3.txt"]
>>> [f for f in files if f.startswith(("a/", "b/"))]
['a/file1.md', 'b/file2.py']
>>> [f for f in files if f.endswith(("md", "txt"))]
['a/file1.md', 'c/file3.txt']
```

`re.split` takes a string that is actually a regex pattern.
```python
>>> import re
>>> files = ["a/file1.md", "b/file2.py", "c/file3.txt"]
>>> [re.split("\/|\.",f)[-2] for f in files]
['file1', 'file2', 'file3']
```