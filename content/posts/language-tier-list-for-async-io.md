+++
title = 'Language Tier List for Async I/O'
date = 2026-11-13T10:00:00+07:00
draft = false
tags = []
+++

My Language Tier List for Async I/O, with sample code highlighting changes:

# Tier C

**Golang**

❌ explicit channel and goroutine

```diff
- func getConfig(path string) (Config, error) {
- 	file, err := os.Open(path)
+ func getConfig(path string) <-chan struct { Config; error } {
+ 	ch := make(chan struct { Config; error }, 1)
+ 	go func() {
+ 		file, err := os.Open(path)
  		if err != nil {
- 			return nil, err
+ 			ch <- struct{ Config; error }{nil, err}
+ 			return
  		}
  		defer file.Close()
  
  		var cfg Config
  		decoder := json.NewDecoder(file)
  		if err := decoder.Decode(&cfg); err != nil {
- 			return nil, err
+ 			ch <- struct{ Config; error }{nil, err}
+ 			return
  		}
  
- 		return cfg, nil
+ 		ch <- struct{ Config; error }{cfg, nil}
+ 	}()
+ 	return ch
  }
```

# Tier B

None

# Tier A

**Rust**

❌ heavy changes for tokio and async function

```diff
  use serde_json::Value;
+ use tokio::io::AsyncReadExt;

- fn get_config(path: &str) -> Result<Value, Box<dyn std::error::Error>> {
-     let file = File::open(path)?;
-     let config = serde_json::from_reader(file)?;
+ async fn get_config(path: &str) -> Result<Value, Box<dyn std::error::Error>> {
+     let mut file = tokio::fs::File::open(path).await?;
+     let mut buf = Vec::new();
+     file.read_to_end(&mut buf).await?;
+     let config = serde_json::from_slice(&buf)?;
      Ok(config)
  }
```

**Java**

✅ single config in `application.properties`

> **spring.threads.virtual.enabled=true**




# Tier A+


**Node.js**

✅ no code change needed

```JavaScript
const fs = require('fs/promises');

async function getConfig(path) {
    const data = await fs.readFile(path, 'utf8');
    return JSON.parse(data);
}
```

# Tier S


**Python**


✅ no code change needed if called from FastAPI async def endpoint


```Python
import json

def get_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)
```