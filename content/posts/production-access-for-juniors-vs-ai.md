+++
title = 'Production Access for Juniors vs AI'
date = 2026-09-14T10:00:00+07:00
draft = false
tags = ['ai', ]
+++
# Production Access for Juniors vs AI

Juniors are blocked from Production, meanwhile seniors grant Production access to unsupervised AI agents.

Naive solution: add an instruction in the master prompt that says AI must not run on production. It fails because AI might not follow instructions, and there is no definition of what production is.

Deterministic solution: implement a hook that enforces a manual 'APPROVE' confirmation for any AI action using a Production API key hash.
