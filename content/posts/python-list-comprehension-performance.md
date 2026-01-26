+++
title = 'Python List Comprehension Performance'
featured_image = 'images/python-list-comprehension-performance.png'
date = 2026-01-26T14:15:00+07:00
draft = false
tags = ['python', 'list']
+++
# List Comprehension is better than Loop

<table>
<tr>
<th>List Comprehension</th>
<th>Loop</th>
</tr>
<tr>
<td colspan="2">Syntax</td>
</tr>
<tr>
<td>
  
```python
[i * i for i in range(10)]

 
```
  
</td>
<td>

```python
result = [None]*10
for i in range(10):
    result[i] = i * i  # append is slower
```

</td>
</tr>
<tr>
<td colspan="2">Bytecode</td>
</tr>
<tr>
<td>
  
```python
LOAD_FAST i
LOAD_FAST i
BINARY_MULTIPLY 
LIST_APPEND

 
```
  
</td>
<td>

```python
LOAD_FAST i
LOAD_FAST i
BINARY_MULTIPLY 
LOAD_FAST result
LOAD_FAST i
STORE_SUBSCR 
```

</td>
</tr>
</table>

# Comparison Benchmark and Bytecodes

```python
import dis
import timeit


def comprehension_version() -> list[int]:
    return [i * i for i in range(10)]


def loop_version() -> list[int]:
    result = [None] * 10
    for i in range(10):
        result[i] = i * i  # append is slower
    return result


comp_time = timeit.timeit(
    "comprehension_version()", globals=globals(), number=1_000_000
)
loop_time = timeit.timeit("loop_version()", globals=globals(), number=1_000_000)

print("Comprehension version time:", comp_time)  # 0.257528125
print("Loop version time:", loop_time)           # 0.27902224999999997

print("\nlist comprehension (outer) bytecodes:")
for instr in dis.Bytecode(comprehension_version):
    print(instr.opname, instr.argrepr)

# Extract the inner <listcomp> code object
inner_comp = [
    c
    for c in comprehension_version.__code__.co_consts
    if isinstance(c, type(comprehension_version.__code__))
][0]

print("\nlist comprehension (inner <listcomp>) bytecodes:")
for instr in dis.Bytecode(inner_comp):
    print(instr.opname, instr.argrepr)

print("\nfor loop bytecodes:")
for instr in dis.Bytecode(loop_version):
    print(instr.opname, instr.argrepr)

```