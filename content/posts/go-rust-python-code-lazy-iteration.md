+++
title = 'Go Rust Python code lazy iteration'
date = 2026-03-20T17:52:39+07:00
draft = false
tags = ['go', 'rust', 'python', 'iteration']
+++
# Go Rust Python code lazy iteration

Python
```Python
def OneTwo():
    yield "One"
    yield "Two"
for val in OneTwo():
    print(val)
```

Go
```Golang
func OneTwo() <-chan string {
    ch := make(chan string)
    go func() {
        defer close(ch)
        ch <- "One"
        ch <- "Two"
    }()
    return ch
}

func OneTwoNew(yield func(string) bool) {
    if !yield("One") {
        return
    }
    if !yield("Two") {
        return
    }
}

func main() {
    for val := range OneTwo {
        fmt.Printf(val)
    }
    for val := range OneTwoNew {
        fmt.Printf(val)
    }
}
```

Rust
```Rust
use std::sync::mpsc;
use std::sync::mpsc::{Receiver, Sender};

fn setup_stream() -> (Sender<&'static str>, Receiver<&'static str>) {
    let (tx, rx) = mpsc::channel();
    tx.send("One").unwrap();
    (tx, rx)
}

fn main() {
    let (tx, rx) = setup_stream();
    tx.send("Two").unwrap();
    drop(tx);

    for val in rx {
        println!("{}", val);
    }
}
```