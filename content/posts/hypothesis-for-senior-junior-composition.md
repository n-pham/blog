+++
title = 'Hypothesis for Senior Junior Composition'
featured_image = 'images/hypothesis-for-senior-junior-composition.png'
date = 2026-11-03T10:00:00+07:00
draft = false
tags = ['management']
+++

![Hypothesis for Senior Junior Composition](../../images/hypothesis-for-senior-junior-composition.png)

<!--
```python
# /// script
# dependencies = [
#     "matplotlib",
#     "numpy",
#     "scipy",
# ]
# ///

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

labels = ['0 Senior , 5 Juniors', 
          '1 Senior , 4 Juniors', 
          '2 Seniors, 3 Juniors', 
          '3 Seniors, 2 Juniors', 
          '4 Seniors, 1 Junior ', 
          '5 Seniors, 0 Junior ']

eff_factors = [0.40, 0.51, 0.65, 0.75, 0.83, 0.90]


fig, ax = plt.subplots(figsize=(10, 6.5), dpi=120)
# fig.patch.set_facecolor('#0f172a')
# ax.set_facecolor('#0f172a')

# 1. Bar Chart Visualization (Uniform styling)
bars = ax.bar(labels, eff_factors, color='#3b82f6', alpha=0.45, edgecolor='#60a5fa', linewidth=1.5, width=0.55)

# 2. Gaussian / Normal Distribution Fit Curve Overlay
x_nums = np.arange(len(eff_factors))
mu, std = norm.fit(eff_factors)

# Fit smooth continuous x-axis points
x_smooth = np.linspace(0, len(eff_factors) - 1, 300)
p = norm.pdf(x_smooth, loc=2.2, scale=1.8)
p_scaled = min(eff_factors) + (p - min(p)) * (max(eff_factors) - min(eff_factors)) / (max(p) - min(p))

ax.scatter(x_nums, eff_factors, color='#f43f5e', zorder=5, s=50)

# 3. Calculate and Annotate Delta Gains Between Successive Points
deltas = [eff_factors[i+1] - eff_factors[i] for i in range(len(eff_factors)-1)]
highlight_index = 1  # 1S-4J -> 2S-3J is index 1

for i in range(len(deltas)):
    x1, y1 = i, eff_factors[i]
    x2, y2 = i + 1, eff_factors[i+1]
    delta = deltas[i]
    
    # Position callout arrow and delta label
    if i == highlight_index:
        # PEAK JUMP LINE HIGHLIGHT
        ax.plot([x1, x2], [y1, y2], color='#10b981', linestyle='-', alpha=0.95, linewidth=3.0)
        
        ax.annotate(f'Peak!\n+ {delta:.2f} increase',
                    xy=(x2 - 0.5, (y1 + y2) / 2),
                    xytext=(x2 - 0.85, (y1 + y2) / 2 + 0.12),
                    arrowprops=dict(facecolor='#10b981', edgecolor='#34d399', shrink=0.08, width=2, headwidth=8),
                    fontsize=10, fontweight='bold', color='#34d399',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#064e3b", ec="#10b981", lw=1.5, alpha=0.9),
                    ha='center')
    else:
        # Standard Delta Annotations
        ax.annotate(f'+{delta:.2f}',
                    xy=((x1 + x2) / 2, (y1 + y2) / 2 + 0.015),
                    fontsize=8.5, fontweight='bold', color='#cbd5e1',
                    ha='center', va='bottom',
                    bbox=dict(boxstyle="round,pad=0.2", fc="#1e293b", ec="#475569", alpha=0.7))

        # Connecting dotted indicator lines for standard deltas
        ax.plot([x1, x2], [y1, y2], color='#94a3b8', linestyle=':', alpha=0.6, linewidth=1.2)

# Chart Value Annotations on Top of Bars
# for bar, val in zip(bars, eff_factors):
#     yval = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.015, f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#f8fafc')

# 4. Styling & Axes Configuration
ax.set_ylim(0.30, 1.05)
ax.set_ylabel('Effective Factor (0.40 to 0.90)', fontsize=11, fontweight='semibold', color='#2d3748', labelpad=10)
ax.set_xlabel('Senior Junior Composition - 5 Members', fontsize=11, fontweight='semibold', color='#2d3748', labelpad=12)
ax.set_title('Hypothesis for Senior Junior Composition', fontsize=13, fontweight='bold', color='#1a202c', pad=15)

# Custom Grid and Spines styling
ax.grid(True, axis='y', linestyle='--', alpha=0.15, color='#94a3b8')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#334155')
ax.spines['bottom'].set_color('#334155')
ax.tick_params(colors='#94a3b8', labelsize=9)

# Legend positioning
ax.legend(loc='upper left', frameon=True, facecolor='#1e293b', edgecolor='#334155', fontsize=9.5)

plt.tight_layout()
plt.show()
```
-->