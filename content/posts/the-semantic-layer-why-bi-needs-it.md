+++
title = 'The Semantic Layer: Why BI Needs It'
featured_image = 'images/semantic-layer.png'
date = 2026-06-11T11:40:00+07:00
draft = false
tags = ['bi', 'semantic-layer', 'metrics']
+++
# TL;DR
* Define metrics once (e.g., "Revenue") and use them everywhere (Tableau, Looker, Python).
* Avoid "Metric Drift" where different dashboards show different totals.
* Tools: dbt Semantic Layer, Cube, or Looker's LookML.

# One Version of the Truth
If Revenue = `price * quantity` in one dashboard but `(price * quantity) - discount` in another, trust is lost. The semantic layer centralizes this logic in code.
