+++
title = 'Language Tier List for Code Flow'
date = 2026-11-04T10:00:00+07:00
draft = false
tags = []
+++

My Language Tier List for Code Flow, with sample code for reading JSON file:

# Tier C

**SQL**

❌ constant looking up and down

❌ fails to read JSONs that have an extra column


**Golang**

❌ explicit `defer` tries to keep code flow linear

❌ then mandatory error handling breaks it


```golang
package main

import (
	"encoding/json"
	"os"
)

type Config map[string]interface{}

func getConfig(path string) (Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var cfg Config
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&cfg); err != nil {
		return nil, err
	}

	return cfg, nil
}
```

# Tier B

**Java**

❌ mandatory checked exception handling breaks code flow

✅ try with resources closes them automatically

```java
import java.nio.file.Files;
import java.nio.file.Paths;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public JsonNode getConfig(String path) throws Exception {
    try (var reader = Files.newBufferedReader(Paths.get(path))) {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readTree(reader);
    } catch (Exception e) {
        throw e;
    }
}
```

**Node.js**

❌ `await` keeps code flow linear and flattened, but requires tracking function colors (async/sync)

✅ resources and exceptions are handled automatically

```JavaScript
const fs = require('fs/promises');

async function getConfig(path) {
    const data = await fs.readFile(path, 'utf8');
    return JSON.parse(data);
}
```

# Tier A

**Python**

❌ unchecked exceptions keep code flow linear, but complicate debugging and monitoring

✅ `with` automatically closes resources


```Python
import json

def get_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)
```


# Tier S

**Rust**

✅ `Result` and `?` keep code flow linear and flattened while avoiding exceptions

✅ Ownership automatically closes resources

```Rust
use std::fs::File;
use serde_json::Value;

fn get_config(path: &str) -> Result<Value, Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let config = serde_json::from_reader(file)?;
    Ok(config)
}
```
