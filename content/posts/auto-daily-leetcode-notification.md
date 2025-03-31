+++
title = 'Auto Daily LeetCode Notification'
featured_image = 'images/auto-daily-leetcode-notification.png'
date = 2025-03-30T10:52:39+07:00
draft = false
tags = ['GHA']
+++
# Automating Daily LeetCode Notifications

My simple solution for daily LeetCode notifications: 

💡 Tech Stack:

* GitHub Actions: handles runtime and scheduling.
* curl: fetches data from GraphQL.
* jq: extracts problem details.
* grep: derives new or solved status.
* JS: creates GitHub issues to trigger email notifications.
* flat file: extracts and stores solved problems.


❌ Avoided:

Airflow, Python, Kafka, Redis, and S3


[See it in action]( https://github.com/n-pham/dsa/actions/workflows/notify_leetcode_daily.yaml )



# Auto-append solved problems

```bash
echo "message=$(git log -1 --pretty=%B)" >> $GITHUB_ENV

if [[ $message =~ ^[0-9]+$ ]]; then
  echo "is_integer=true" >> $GITHUB_ENV
fi
```