# Visual evidence index

All `.png` and `.svg` figures were generated from recorded execution CSVs and the original canonical milestone ledger. The PNG previews are for README/documentation; SVG retains vector layout.

- `cpu_three_intensity_hold_5ms` and `cpu_three_intensity_hold_50ms`: timing readout by intensity.
- `cpu_history_paired_5ms` and `cpu_history_paired_50ms`: high-minus-idle contrast per actual balanced triplet.
- `canonical_116_milestones`: counts by original roadmap phase.

Regenerate from active `workplace/` root:

```sh
python3 09_RESULTS_VISUALS/build_graphs.py
```

Requires matplotlib for the report layer only. Plotting is independent of the experimental machine. No synthetic analog samples or random points are created.

- `canonical_repeat_acceptance.png` shows the **actual 21/23 and 24/24** sequential native gate outcomes, preserving the failed run rather than averaging it away.
