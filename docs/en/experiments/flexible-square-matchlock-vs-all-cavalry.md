# All-Cavalry Units vs. Matchlock Units in Flexible Square Formation

[日本語版](../../experiments/flexible-square-matchlock-vs-all-cavalry.md)

[Back to Experiments](index.md)

This experiment pits an **Eastern Army matchlock unit** against a **Western Army all-cavalry unit**, comparing how the Eastern unit's **matchlock ratio and tactical stance** affect the outcome. Both units use the **Flexible Square** formation. There were **10 trials per condition, across 6 conditions (60 battles in total)**.

The Eastern unit with a **60% matchlock ratio and the Retreat tactic** won **9 of 10 battles**, the highest win count among the tested conditions. At a 45% matchlock ratio, both Retreat and Normal won 7 of 10, while Defensive won 5 of 10.

## Experimental Setup

| Item | Eastern Army: Matchlock Unit | Western Army: All-Cavalry Unit |
|---|---|---|
| Troops | **5,000** | **4,250** |
| Formation | Flexible Square | Flexible Square |
| Composition | 30%, 45%, or 60% Matchlock Ashigaru | All-Cavalry |
| Tactical stance | Retreat, Defensive, or Normal | Normal |
| Trials | 10 per tested condition | 10 per tested condition |

At a **30% matchlock ratio**, only Retreat was tested. At **60%**, Retreat and Normal were tested. **Not every matchlock-ratio/stance combination was tested.**

The Western unit's 4,250 troops correspond to the 15% troop-strength reduction applied when converting a 5,000-troop unit to the [All-Cavalry composition](../systems/all-cavalry-units.md) introduced in Version 2.7.0.

## Complete Results

| Eastern matchlock ratio | Eastern stance | Eastern wins | Western wins | Avg. Eastern losses | Avg. Western losses | Avg. Eastern survivors | Avg. Western survivors |
|---|---|---:|---:|---:|---:|---:|---:|
| 30% | Retreat | 3 | 7 | 4,824 | 3,621 | 176 | 629 |
| 45% | Retreat | 7 | 3 | 4,532 | 4,029 | 468 | 221 |
| **60%** | **Retreat** | **9** | **1** | **4,299** | **4,152** | **701** | **98** |
| 45% | Defensive | 5 | 5 | 4,629 | 3,842 | 371 | 408 |
| 45% | Normal | 7 | 3 | 4,441 | 3,989 | 559 | 261 |
| 60% | Normal | 7 | 3 | 4,524 | 3,966 | 476 | 284 |

Average surviving troops were calculated by subtracting **average losses from starting troop strength** for each army.

## Differences by Matchlock Ratio

With the **Retreat** tactic, the Eastern unit won more battles as its matchlock ratio increased.

| Eastern matchlock ratio | Eastern wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|
| 30% | 3 / 10 | 176 | 629 |
| 45% | 7 / 10 | 468 | 221 |
| 60% | 9 / 10 | 701 | 98 |

Under these conditions, combining **Retreat with a high matchlock ratio** produced favorable results against the all-cavalry unit.

With **Normal**, however, both the 45% and 60% matchlock configurations won **7 of 10 battles**. The Eastern unit had an average of **559** survivors at 45%, compared with **476** at 60%. These results do **not** establish that 60% is better than 45% when using Normal.

## Differences by Tactical Stance

At a **45% matchlock ratio**, Retreat and Normal each won 7 battles, while Defensive won 5. The Eastern unit had the most average survivors with Normal (**559**), compared with Retreat (**468**) and Defensive (**371**).

At a **60% matchlock ratio**, Retreat won 9 battles and Normal won 7. Average Eastern survivors were also higher with Retreat (**701**) than with Normal (**476**) in these trials.

## Interpretation and Limitations

- Each condition was tested only **10 times**. Differences of around two wins may reflect trial-to-trial variation.
- The aggregate results do not show exactly **how matchlock fire and close combat separately contributed** to the outcomes.
- Untested combinations, such as Normal or Defensive at a 30% matchlock ratio, cannot be evaluated from these results.

These findings apply to the tested matchup of **5,000 Eastern troops against 4,250 Western all-cavalry troops**, both in Flexible Square formation; they should not automatically be generalized to other formations or troop strengths.

## Related Pages

- [Experiments](index.md)
- [All-Cavalry Units](../systems/all-cavalry-units.md)
- [Unit Types](../systems/unit-types.md)
- [Flexible Square Formation](../formations/flexible-square.md)
- [Unit Tactics Experiment](../systems/unit-tactics-experiment.md)
