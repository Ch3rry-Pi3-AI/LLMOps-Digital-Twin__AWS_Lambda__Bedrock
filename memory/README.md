# 📁 **`/memory`**

The `memory` directory stores **per-session conversation history** for the Digital Twin when running in **local storage mode**.

Each conversation is saved as its own JSON file:

```
/memory/
   ├── abc123.json
   ├── f9d8e1.json
   └── ...
```

## What These Files Contain

Each file holds a chronological list of messages exchanged between the user and the Digital Twin, for example:

```json
[
  { "role": "user", "content": "Hi!", "timestamp": "..." },
  { "role": "assistant", "content": "Hello!", "timestamp": "..." }
]
```

## When This Folder Is Used

* If `USE_S3=false` (default), the backend reads and writes memory **locally** to this folder.
* If `USE_S3=true`, this folder is **ignored**, and memory is stored in an S3 bucket instead.

This folder allows the Twin to maintain conversational context during local development.
