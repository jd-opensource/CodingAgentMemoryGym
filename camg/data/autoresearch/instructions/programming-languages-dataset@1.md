# OpenMLE-fast task

Task ID: `programming-languages-dataset@1`

Native metric: `ProgrammingLanguageIdentificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2811 bytes)
- `data/sample_submission.csv` (6904 bytes); columns: ["id", "language"]
- `data/test.csv` (146233 bytes); columns: ["id", "code_preview", "num_lines", "num_chars"]
- `data/train.csv` (345599 bytes); columns: ["id", "code_preview", "num_lines", "num_chars", "language"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (666 lines)
test.csv (5993 lines)
train.csv (13791 lines)```

-> sample_submission.csv has 665 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 5.00 - 2198.00, 0 nan values
language (object) has 21 unique values. Some example values: ['Go', 'PHP', 'HTML', 'Python']

-> test.csv has 665 rows and 4 columns.
Here is some information about the columns:
code_preview (object) has 590 unique values. Some example values: ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n<html lang="en">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<titl...', '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">\n<html lang="en">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<title...', "const {resolve} = require('path');\nconst Webpack = require('webpack');\nconst {\n  GITHUB_URL,\n  getVersionString,\n} = require('react-devtools-extensions/utils');\nconst {resolveFeatureFlags} = require('...", 'function Comment({comment, commentSource}) {\n  const currentUserID = comment.viewer.id;\n  const environment = RelayEnvironment.forUser(currentUserID);\n  const commentID = nullthrows(comment.id);\n  use...']
id (int64) has range: 5.00 - 2198.00, 0 nan values
num_chars (int64) has range: 18.00 - 78664.00, 0 nan values
num_lines (int64) has range: 6.00 - 966.00, 0 nan values

-> train.csv has 1535 rows and 5 columns.
Here is some information about the columns:
code_preview (object) has 1384 unique values. Some example values: ['Licensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/lice...', '<?php\n\nnamespace App\\Events;\n\nuse Illuminate\\Broadcasting\\InteractsWithSockets;\nuse Illuminate\\Broadcasting\\PrivateChannel;\nuse Illuminate\\Contracts\\Broadcasting\\ShouldBroadcast;\nuse Illuminate\\Founda...', '\ufeff// Copyright (c) Microsoft Corporation\n\nusing System;\nusing System.Text.Json;\nusing System.Text.Json.Serialization;\n\nusing Microsoft.PowerToys.Settings.UI.Library.Interfaces;\n\nnamespace Microsoft.Pow...', 'export {\n  __CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,\n  __COMPILER_RUNTIME,\n  Children,\n  Component,\n  Fragment,\n  Profiler,\n  PureComponent,\n  StrictMode,\n  Suspense,\n  cloneEle...']
id (int64) has range: 1.00 - 2200.00, 0 nan values
language (object) has 22 unique values. Some example values: ['C++', 'C#', 'PHP', 'TypeScript']
num_chars (int64) has range: 56.00 - 23517.00, 0 nan values
num_lines (int64) has range: 6.00 - 727.00, 0 nan values
