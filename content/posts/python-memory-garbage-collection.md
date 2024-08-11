+++
title = 'Python Memory & Garbage Collection'
featured_image = 'images/python-memory-garbage-collection.png'
date = 2023-09-13T15:52:39+07:00
draft = false
tags = ['python', 'memory', 'garbagecollector']
+++
# Out-of-memory issue
Working with big data frames sometimes hangs the system with an out-of-memory error. For Spark, this issue can still happen when you collect data back into master node.

The out-of-memory issue can be prevented in the following two ways:

# 1: signal Garbage Collector asap
```
(venv) ➜  ~ python -m memory_profiler t.py
Line #    Mem usage    Increment  Occurrences   Line Contents
======    =========    =========  ===========   =============
    35  150.836 MiB  150.836 MiB           1   @profile
    36                                         def func():
    37  192.664 MiB   41.828 MiB           1       df1 = <big df 1>
    38 1347.035 MiB 1154.371 MiB           1       df2 = <big df 2>
```

In the code above 2 big data frames `df1` and `df2` exist in memory at the same time. `df1` takes 41.828 MiB and `df2` takes 1154.371 MiB (*Increment* column).

A better way to use memory is to load and process each data frame at a time, and `del` it asap.

```
(venv) ➜  ~ python -m memory_profiler t.py
Line #    Mem usage    Increment  Occurrences   Line Contents
======    =========    =========  ===========   =============
    35  150.738 MiB  150.738 MiB           1   @profile
    36                                         def func():
    37  192.449 MiB   41.711 MiB           1       df1 = <big df 1>
    38  191.016 MiB   -1.434 MiB           1       del df1
    39 1373.656 MiB 1182.641 MiB           1       df2 = <big df 2>
    40  334.859 MiB -1038.797 MiB          1       del df2
```

In the code above command `del df1` signals Garbage Collector to release the memory (it decided to only release 1.434 MiB). The command `del df2` could release up to 1038.797 MiB.

# 2: use chunked/iterator output
If your code uses a single very big data frame that may not fit in memory, then enable the chunked/iterator option - most APIs already include this option.

```
(venv) ➜  ~ python -m memory_profiler t.py
Line #   Mem usage    Increment Occurrences   Line Contents
======   =========    ========= ===========   =============
    35 150.836 MiB  150.836 MiB          1   @profile
    36                                       def func():
    37 167.367 MiB   16.531 MiB          1       df_iter = <chunked>
    38 779.520 MiB   76.082 MiB         31       for df in df_iter:
    39 779.520 MiB -452.129 MiB         30           df.shape
```

In the code above the chunked API splits the very big output into 30 chunks (*Occurrences* column).

Memory usage does not increase because on every iteration the variable `df` is assigned a new chunk and Garbage Collector releases the memory used by old chunk.

# Note: Monitor Memory in Python
* `pip install memory-profiler`
* decorate the function with `@profile`
* run the file with `-m memory_profiler`
