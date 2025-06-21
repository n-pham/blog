+++
title = 'Bash command status check'
featured_image = 'images/bash-command-status-check.png'
date = 2025-06-21T17:52:39+07:00
draft = false
tags = ['bash', ]
+++
# Bash command status check

<blockquote>

* Do not check for command output - it might fail to detect failure
* Check for command return value instead 

</blockquote>

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
  
```bash
run_ls() {
    ls "$@" || { echo 'RUN_FAILED'; }
}
# missing \ at the end of line below
CMD_OUTPUT=$(run_ls
               -a
)

if [[ "$CMD_OUTPUT" == *"RUN_FAILED"* ]]; then
    echo 'Fail'
else
    echo 'Pass'
fi


~ ❯ ./test.sh  
./test.sh: line 8: -a: command not found
Pass
```

</td>
<td>

```bash
run_ls() {
    ls "$@" || { return 1; }
}
# missing \ at the end of line below
CMD_OUTPUT=$(run_ls
    -a
)
CMD_STATUS=$?
if [[ $CMD_STATUS -ne 0 ]]; then
    echo 'Fail'
else
    echo 'Pass'
fi


~ ❯ ./test2.sh  
./test2.sh: line 8: -a: command not found
Fail
```

</td>
</tr>
</table>
