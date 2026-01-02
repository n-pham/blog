+++
title = 'Python Structural Pattern Match'
featured_image = 'images/python-structural-pattern-match.png'
date = 2026-01-02T14:15:00+07:00
draft = false
tags = ['python']
+++

# Python Structural Pattern Match

`match` in Python 3.10+ is much more powerful than traditional switch/case in other languages.

For example, to merge overlapping intervals `[[1,3],[2,6],[8,10],[10,15]]` into `[[1,6],[8,15]]`.

<table>
<tr>
<th>Without <code>match</code></th>
<th>With <code>match</code></th>
</tr>
<tr>
<td>
  
```python
intervals.sort()
result = []
for interval in intervals:

    if not result:
        result.append(interval)
    # repeated, unclear index access
    elif result[-1][1] >= interval[0]:
        result[-1][1] = max(
            result[-1][1], interval[1]
        )
    else:
        result.append(interval)
```
  
</td>
<td>

```python
intervals.sort()
result = []
for interval in intervals:
    match (result, interval):
        case ([], _):
            result.append(interval)
        # Structural Pattern Match with constraint
        case ([*x, [low, high]], [new_low, new_high]) if (
            high >= new_low
        ):
            result[-1] = [low, max(high, new_high)]
        case _:
            result.append(interval)
```
</td>
</tr>
</table>

