# Tactical Restrictions During Flank and Rear Engagement

[日本語版](../../systems/flank-rear-engagement.md)

Version 2.8.0 introduces command-and-control disruption when a unit is engaged from its flank or rear, limiting its ability to carry out aggressive maneuvers.

## Restriction Threshold

If the **total troop strength of enemy units engaging a unit from the flank** reaches at least **one-fifth (20%) of the unit's troop strength**, the unit cannot use these tactical stances:

- Charge
- Aggressive
- Normal

The troop strengths of multiple enemy units engaging from the flank are **combined** for this threshold.

## Flank and Rear Sectors

Take the unit's **forward-facing direction as 0°**.

| Sector | Angle relative to facing | Default tactic | Morale loss from engagement |
|---|---|---|---:|
| Rear | 140°–220° | Retreat | 3.8 points per turn |
| Flank | 40°–320°, excluding the rear sector | Defensive | 3 points per turn |

The exact internal evaluation order for sector classification and tactical restrictions is not specified in this release note. The morale penalties shown here are attributable to flank/rear engagement; **other factors may also change morale**.

## Effect on Combat

Flank and rear attacks disrupt command and control, preventing a unit from continuing bold attacks as though it were unopposed.

- [Unit AI](ai.md)
- [Morale](morale.md)
- [Encirclement and Breakthrough](encirclement.md)
- [Version 2.8.0](../updates/v2.8.0.md)
