+++
title = 'Claude Code Light Sandbox'
featured_image = 'images/claude-code-light-sandbox.png'
date = 2026-10-30T10:00:00+07:00
draft = false
tags = ['ai', ]
+++

# Claude Code Light Sandbox

Claude Code inherits our logged-in cloud sessions and will happily run "clean_up.py" against even Production.

A standard sandbox requires heavy file and tool synchronization.

What works for me is simply an alias that unsets the cloud sessions and configs.

```zsh
# ~/.zshrc
cc() {
    env \
      -u AWS_SECRET_ACCESS_KEY \
      AWS_CONFIG_FILE="/tmp/empty_claude_aws_config" \
      claude "$@"
}
```
