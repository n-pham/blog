+++
title = 'Go Rust Python code complexity AI review'
date = 2026-02-28T17:52:39+07:00
draft = false
tags = ['go', 'rust', 'python', 'ai', 'review']
+++
# Go Rust Python code complexity AI review

For AI code complexity review (for example Checkmarx), code complexity varies among Go, Rust and Python.
* Most code branches: Go because of idiomatic error handling `if err != nil`.
* Fewest code branches: Python thanks to list comprehensions, `map`, `filter`, `try/except`.
* Flexible: Rust

  High if using `match` for error handling and branching.

  Low if using `?` operator and iterator chains `map`, `filter`, `collect`.

<table>
<tr>
<th>High Complexity Go</th>
<th>High Complexity Rust</th>
</tr>
<tr>
<td>

```Golang
// estimated complexity 4
func classify(values []string) ([]string, error) {
    var result []string
    for _, v := range values {
        num, err := strconv.Atoi(v)
        if err != nil {
            return nil, fmt.Errorf("invalid")
        }
        if num < 0 {
            result = append(result, "negative")
        } else if num == 0 {
            result = append(result, "zero")
        } else {
            result = append(result, "positive")
        }
    }
    return result, nil
}


```
  
</td>
<td>

```Rust
// estimated complexity 5-6
fn classify(values: Vec<&str>) -> Result<Vec<String>, String> {
    let mut result = Vec::new();

    for v in values {
        match v.parse::<i32>() {
            Ok(num) => {
                if num < 0 {
                    result.push("negative".to_string());
                } else if num == 0 {
                    result.push("zero".to_string());
                } else {
                    result.push("positive".to_string());
                }
            }
            Err(_) => return Err("invalid".to_string()),
        }
    }

    Ok(result)
}
```

</td>
</tr>
<tr>
<th>Low Complexity Python</th>
<th>Low Complexity Rust</th>
</tr>
<tr>
<td>

```Python
# estimated complexity 3
def classify(values):
    try:
        nums = [int(v) for v in values]
    except ValueError:
        raise Exception("invalid")

    return [
        "negative" if num < 0 else
        "zero" if num == 0 else
        "positive"
        for num in nums
    ]









```
  
</td>
<td>

```Rust
// estimated complexity 3
fn classify(values: Vec<&str>) -> Result<Vec<String>, String> {
    let nums: Vec<i32> = values
        .into_iter()
        .map(|v| v.parse::<i32>().map_err(|_| "invalid".to_string()))
        .collect::<Result<Vec<_>, _>>()?;

    let result: Vec<String> = nums
        .into_iter()
        .map(|num| {
            if num < 0 {
                "negative".to_string()
            } else if num == 0 {
                "zero".to_string()
            } else {
                "positive".to_string()
            }
        })
        .collect();

    Ok(result)
}
```

</td>
</tr>
</table>
