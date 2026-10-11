+++
title = 'Python Lazy Import Compatible Code'
date = 2026-10-11T10:00:00+07:00
draft = false
tags = ['Python']
+++
# Python Lazy Import Compatible Code

Make lazy import work automatically in future switching to Python 3.15.

<table>
<tr>
<td>
  
```python
# This check fails in 3.15+


try:
    from xgboost import XGBClassifier
    XGB_EXISTS = True
except Exception:  # pragma: no cover
    XGB_EXISTS = False


if XGB_EXISTS:
    xgb_model = XGBClassifier()
```
  
</td>
<td>
  
```python
# Works both before and after 3.15

from importlib.util import find_spec 

XGB_EXISTS = find_spec("xgboost") is not None
if XGB_EXISTS:
    from xgboost import XGBClassifier
else:
    XGBClassifier = None  # pragma: no cover

if XGB_EXISTS:
    xgb_model = XGBClassifier()
```
  
</td>
</tr>
<tr>
<td>
</td>
<td>

```python
# init in 3.15+

import sys

LAZY_PACKAGES = {"boto3", "xgboost"}

if hasattr(sys, "set_lazy_imports"):
    sys.set_lazy_imports_filter(
        lambda _, imported, __: imported.split(".")[0] in LAZY_PACKAGES)
    sys.set_lazy_imports("all")
```

</td>
</tr>
</table>
