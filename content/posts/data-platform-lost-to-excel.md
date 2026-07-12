+++
title = 'Data Platform Lost to Excel'
date = 2026-08-31T10:00:00+07:00
draft = false
tags = ['data', ]
+++
# Data Platform Lost to Excel

We built a Data Platform with cutting edge technologies S3, Spark, Trino, Airflow. Every night, data was incrementally loaded, transformed and sitting ready in the warehouse before 7 AM sharp, every single day.                                                                                                            
Several months after release, Finance are still manually updating Excel files. It turns out the reports and tracking they use are living in Excel formulas!

Lessons learned:
* Evaluate system adoption first of all.
* Add "Export to Excel" feature, Excel is often a first-class citizen.
