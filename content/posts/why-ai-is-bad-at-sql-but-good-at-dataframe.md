+++
title = 'Why AI is Bad at SQL but Good at DataFrame'
date = 2026-05-15T10:00:00+07:00
draft = false
tags = ['ai', 'sql']
+++


# Why AI is Bad at SQL but Good at DataFrame

<table>
<tr>
<th>Logic</th>
<th>DataFrame</th>
<th>SQL</th>
</tr>
<tr>
<td>Filter before Agg</td>
<td>.<b>filter()</b>.groupBy().agg()</td>
<td>(<b>WHERE</b>) AS cte, ... GROUP BY</td>
</tr>
<tr>
<td>Filter after Agg</td>
<td>.groupBy().agg().<b>filter()</b></td>
<td>GROUP BY ... <b>HAVING</b></td>
</tr>
<tr>
<td>Filter in Window</td>
<td>.withColumn().<b>filter()</b></td>
<td>OVER() ... <b>QUALIFY</b></td>
</tr>
<tr>
<td>Cross Join</td>
<td>.cross<b>Join</b>(df2)</td>
<td><b>CROSS JOIN</b> / ,</td>
</tr>
<tr>
<td>Exists / SemiJoin</td>
<td><b>.join</b>(df2, "id", "left_semi")</td>
<td><b>WHERE EXISTS</b> (SELECT 1 FROM)</td>
</tr>
<tr>
<td>Not Exists / AntiJoin</td>
<td><b>.join</b>(df2, "id", "left_anti")</td>
<td><b>WHERE NOT EXISTS</b> / EXCEPT</td>
</tr>
<tr>
<td>Hint Broadcast Join</td>
<td>.join(df2.<b>hint</b>("broadcast"), "id")</td>
<td><b>/*+ Broadcast(df2) */</b></td>
</tr>
<tr>
<td>Hint Merge Join</td>
<td>.join(df2.<b>hint</b>("merge"), "id")</td>
<td><b>SET enable_hashjoin = off;<br>SELECT ...;<br>RESET enable_hashjoin;</b></td>
</tr>
<tr>
<td>Partition Pruning</td>
<td>.filter(col("year") == 2026)<br>DAG will <b>always</b> do partition-pruning</td>
<td>WHERE ... AND year = 2026<br>Complex WHERE may <b>miss</b> partition pruning</td>
</tr>
</table>

<br>

* For DataFrame, code is a stream of tokens in the exact same order of the logic, with the same consistent keywords.
* For SQL, both humans and AI must constantly look ahead or look back to place the right keyword in the right clause.
* For me, why must I keep learning new SQL syntax while I have been writing SQL since 2004!
