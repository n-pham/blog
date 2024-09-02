+++
title = 'Python List & Set syntax recommendation'
featured_image = 'images/python-list-set-syntax-recommendation.png'
date = 2024-09-02T14:15:00+07:00
draft = false
tags = ['python', 'list', 'set', 'union', 'intersection']
+++
# List vs Set commonly-used syntax inconsistencies


<table>
<tr>
<th>List</th>
<th>Set</th>
</tr>
<tr>
<td>
  
```python
>>> ls = [1, 2]
>>> ls.append(3)

>>> ls
[1, 2, 3]
```
  
</td>
<td>

```python
>>> s = {1, 2}
>>> s.union({3})
{1, 2, 3}
>>> s
{1, 2}
```

</td>
</tr>
<tr>
<td>
  
```python
>>> ls = [1, 2]
>>> ls.extend([3, 4])

>>> ls
[1, 2, 3, 4]
```
  
</td>
<td>

```python
>>> s = {1, 2}
>>> s.union({3, 4})
{1, 2, 3, 4}
>>> s
{1, 2}
```

</td>
</tr>
<tr>
<td>
  
```python
>>> ls = [1, 2]
>>> [x for x in ls if x in [2, 3]]
[2]
>>> ls
[1, 2]
```
  
</td>
<td>

```python
>>> s = {1, 2}
>>> s.intersection({2, 3})
{2}
>>> s
{1, 2}
```

</td>
</tr>
<tr>
<td>

List:

* Different syntax among union with 1<br/>or multiple elements, or intersection
* Updates original list
  
</td>
<td>

Set:

* Similar syntax for union and intersection<br/>&nbsp;
* Never updates original set

</td>
</tr>
</table>


# List & Set common syntax recommendation

<table>
<tr>
<th>List</th>
<th>Set</th>
</tr>
<tr>
<td>
  
```python
>>> ls = [1, 2]                   
>>> ls + [3]
[1, 2, 3]
>>> ls + [3, 4]
[1, 2, 3, 4]
>>> [x for x in ls if x in [2, 3]]
[2]
>>> ls
[1, 2]
```
  
</td>
<td>

```python
>>> s = {1, 2}                    
>>> s | {3}
{1, 2, 3}
>>> s | {3, 4}
{1, 2, 3, 4}
>>> s & {2, 3}
{2}
>>> s
{1, 2}
```

</td>
</tr>
<tr>
<td colspan="2">

* Similar syntax for both List and Set
* Original list or set is never updated

</td>
</tr>
</table>