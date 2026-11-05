# Matchlock Units vs. All-Cavalry Units: Formation and Tactics Experiment

[日本語版](../../experiments/flexible-square-matchlock-vs-all-cavalry.md)

[Back to Experiments](index.md)

This experiment compares an **Eastern Army matchlock unit of 5,000 troops** against a **Western Army all-cavalry unit of 4,250 troops**, varying the matchlock ratio, formation, and tactical stance. Each condition was tested 10 times, for **10 conditions and 100 battles in total**.

Under the tested conditions, the best result for the Western Army came from the **All-Cavalry unit in Deep formation using Charge**. It won **all 10 battles** against an Eastern unit in Flexible Square formation with a **60% matchlock ratio and Retreat**, leaving an average of **880 Western troops**.

!!! note "Tactical stance terminology"
    The Japanese source document uses 防御的 (“Defensive”), corresponding to the in-game **守備的 (Defensive)** stance. The tables use **Defensive** throughout.

## Experimental Setup

| Item | Eastern Army: Matchlock Unit | Western Army: All-Cavalry Unit |
|---|---|---|
| Starting troops | **5,000** | **4,250** |
| Formation | Flexible Square or Crane Wing | Flexible Square or Deep |
| Composition | 30%, 45%, or 60% matchlock ratio | All-Cavalry |
| Tactical stance | Retreat, Defensive, or Normal | Normal, Aggressive, or Charge |
| Trials | 10 per condition | 10 per condition |

The Western unit's 4,250 troops correspond to the 15% troop-strength reduction applied when converting a 5,000-troop unit to the [All-Cavalry composition](../systems/all-cavalry-units.md) introduced in Version 2.7.0. The experiment covers **only the 10 listed configurations**, not every possible combination.

## Complete Results

| Eastern formation | Matchlock ratio | Eastern stance | Western formation | Western stance | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---|---|---|---:|---:|---:|---:|
| Flexible Square | 30% | Retreat | Flexible Square | Normal | 3 | 7 | 176 | 629 |
| Flexible Square | 45% | Retreat | Flexible Square | Normal | 7 | 3 | 468 | 221 |
| Flexible Square | 60% | Retreat | Flexible Square | Normal | 9 | 1 | 701 | 98 |
| Flexible Square | 45% | Defensive | Flexible Square | Normal | 5 | 5 | 371 | 408 |
| Flexible Square | 45% | Normal | Flexible Square | Normal | 7 | 3 | 559 | 261 |
| Flexible Square | 60% | Normal | Flexible Square | Normal | 7 | 3 | 476 | 284 |
| Flexible Square | 60% | Retreat | Flexible Square | Aggressive | 7 | 3 | 541 | 181 |
| Flexible Square | 60% | Retreat | Flexible Square | Charge | 7 | 3 | 557 | 210 |
| Crane Wing | 60% | Retreat | Flexible Square | Charge | 2 | 8 | 194 | 491 |
| **Flexible Square** | **60%** | **Retreat** | **Deep** | **Charge** | **0** | **10** | **0** | **880** |

Average survivors are calculated by subtracting **average losses from starting troop strength**. Each win count is out of 10 trials.

## All-Cavalry: Deep Formation with Charge

Keeping the Eastern unit at **Flexible Square, 60% matchlocks, Retreat** and the Western unit at **All-Cavalry, Charge**, changing only the Western formation produced markedly different outcomes.

| Western formation | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|---:|
| Flexible Square | 7 | 3 | 557 | 210 |
| **Deep** | **0** | **10** | **0** | **880** |

With the Western unit in Flexible Square, the Eastern Army won 7 battles. Switching the Western unit to Deep resulted in **10 Western victories out of 10** under these conditions.

## Effect of Matchlock Ratio

Both units use **Flexible Square**. The Eastern unit uses **Retreat** and the Western all-cavalry unit uses **Normal**.

| Eastern matchlock ratio | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|---:|
| 30% | 3 | 7 | 176 | 629 |
| 45% | 7 | 3 | 468 | 221 |
| 60% | 9 | 1 | 701 | 98 |

Under these conditions, the Eastern Army's victories and average surviving strength rose as its matchlock ratio increased.

With the Eastern unit using **Normal** instead, however, both the 45% and 60% configurations produced **7 Eastern victories**. This experiment did not show an increase in wins from raising the matchlock ratio from 45% to 60% when using Normal.

## Effect of the Matchlock Unit's Tactical Stance

Both formations are **Flexible Square**, the Eastern matchlock ratio is **45%**, and the Western stance is **Normal**.

| Eastern stance | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|---:|
| Retreat | 7 | 3 | 468 | 221 |
| Defensive | 5 | 5 | 371 | 408 |
| Normal | 7 | 3 | 559 | 261 |

At 45% matchlocks, Retreat and Normal each won 7 battles, versus 5 for Defensive. Normal left the most Eastern troops on average (**559**).

At **60% matchlocks**, Retreat won **9** battles and Normal won **7**.

## Effect of the All-Cavalry Unit's Tactical Stance

The Eastern unit uses **Flexible Square, 60% matchlocks, Retreat**; the Western all-cavalry unit uses **Flexible Square**.

| Western stance | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|---:|
| Normal | 9 | 1 | 701 | 98 |
| Aggressive | 7 | 3 | 541 | 181 |
| Charge | 7 | 3 | 557 | 210 |

The Western all-cavalry unit won **1 battle with Normal**, compared with **3 each using Aggressive or Charge**.

## Effect of the Matchlock Unit's Formation

The Eastern unit uses **60% matchlocks and Retreat**. The Western unit uses **All-Cavalry, Flexible Square, Charge**.

| Eastern formation | Eastern wins | Western wins | Avg. Eastern survivors | Avg. Western survivors |
|---|---:|---:|---:|---:|
| Flexible Square | 7 | 3 | 557 | 210 |
| Crane Wing | 2 | 8 | 194 | 491 |

Under these conditions, **Flexible Square outperformed Crane Wing** for the Eastern matchlock unit.

## Interpretation and Limitations

- Each condition was tested **10 times**. Smaller win-count differences may reflect trial-to-trial variation.
- Win and loss totals alone cannot establish the precise combat mechanisms involved, such as **the number of shots fired or the time needed to close the distance**.
- Even the 10-of-10 Western wins with Deep and Charge apply to the **specific troop strengths, opponent, and stance configuration tested**; they should not be treated as a universal result.

## Related Pages

- [Experiments](index.md)
- [All-Cavalry Units](../systems/all-cavalry-units.md)
- [Unit Types](../systems/unit-types.md)
- [Flexible Square](../formations/flexible-square.md)
- [Crane Wing](../formations/crane-wing.md)
- [Deep Formation](../formations/deep.md)
- [Unit Tactics Experiment](../systems/unit-tactics-experiment.md)
