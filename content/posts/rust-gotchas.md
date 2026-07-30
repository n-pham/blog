+++
title = 'Rust Gotchas'
date = 2026-09-07T10:00:00+07:00
draft = false
tags = ['rust']
+++

# Rust Gotcha 1

```rust
fn main() {
   let mut n: usize = 0;
   n -= 1;
   if n >= 0 { println!(">= 0"); }
   else { println!("< 0"); }
}
// Output is `>= 0` or Panic in debug mode
```

## The Problem
`usize` is an unsigned integer type, so it cannot be negative. Comparing `n >= 0` is always true. When you perform `n -= 1` on a `usize` that is `0`, it causes an underflow:
- In **debug** builds, this triggers a **panic**.
- In **release** builds, it performs **two's complement wrapping**, resulting in the maximum possible value for `usize`.

## The Fix
Use explicit methods for safer arithmetic:

*   **`saturating_sub`**: If the result would be negative, it returns 0 instead.
*   **`checked_sub`**: Returns `None` if an underflow would occur, allowing you to handle the error gracefully.
*   **`wrapping_sub`**: Intentionally wraps around (the default release behavior) without panicking.

```rust
fn main() {
   let mut n: usize = 0;
   
   // Using saturating_sub
   let res = n.saturating_sub(1);
   println!("{}", res); // Output: 0
   
   // Using checked_sub
   match n.checked_sub(1) {
       Some(val) => println!("{}", val),
       None => println!("Underflow avoided!"),
   }
}
```