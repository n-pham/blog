+++
title = 'Python-dotenv not updated vars'
featured_image = 'images/python-dotenv-not-updated-vars.png'
date = 2025-03-18T10:52:39+07:00
draft = false
tags = ['python']
+++
# Python-dotenv not updated vars

`python-dotenv` by default does not override existing environment variables.

Always use `load_dotenv(..., override=True)` to make sure our configs are updated.

<table>
<!-- <tr>
<th>Before</th>
<th>After</th>
</tr> -->
<tr>
<td>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
🔴
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
🔴
<br/>
<br/>
<br/>

</td>
<td>
  
```bash
export FOO=gotcha

echo 'FOO=BAR' > demo.env

cat << EOF > demo.py
from dotenv import load_dotenv
import os

load_dotenv('demo.env')


print(os.environ['FOO'])
EOF

python demo.py
gotcha

echo $FOO
gotcha
```
  
</td>
<td>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
🟢
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
🟢
<br/>
<br/>
<br/>

</td>
<td>

```bash
export FOO=gotcha

echo 'FOO=BAR' > demo.env

cat << EOF > demo2.py
from dotenv import load_dotenv
import os

load_dotenv('demo.env',
            override=True)

print(os.environ['FOO'])
EOF

python demo2.py
BAR

echo $FOO
gotcha
```

</td>
</tr>
</table>
