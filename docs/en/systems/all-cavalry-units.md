# All-Cavalry Units

[日本語版](../../systems/all-cavalry-units.md)

Starting with Version 2.7.0, a unit can use either the **Normal** or **All-Cavalry** unit composition.

The unit composition described here is a unit-wide setting and is separate from the troop type of each individual soldier dot.

## Normal Units

Normal units use the existing mixed composition of Spear Ashigaru, Matchlock Ashigaru, cavalry, and other troop types.

## All-Cavalry Units

Selecting All-Cavalry configures the unit as an All-Cavalry unit.

To balance its mobility, the following restrictions apply.

| Item | Rule |
|---|---|
| Maximum troop strength for selection | **6,600 troops** |
| Troop strength after conversion | **15% reduction** |
| Troop-increase allowance | Consumes **1.15×** the added troops |
| Cavalry movement speed | **1.5×** Ashigaru speed |

### Troop-Strength Example

Converting a Normal unit with 5,000 troops to All-Cavalry gives:

**5,000 × 0.85 = 4,250 troops**

### Troop-Increase Allowance Example

Increasing an All-Cavalry unit by 1,000 troops consumes:

**1,000 × 1.15 = 1,150 troops**

from the army's troop-increase allowance.

## Fictional Grand Battle Scenarios

In Fictional Grand Battle scenarios, **four medium-sized units** are randomly converted into All-Cavalry units.

This changes which units receive the All-Cavalry composition from battle to battle. The 15% troop-strength reduction described above applies to units converted in this way.

## Relationship to Scoring

Starting with Version 2.7.0, the troop-exchange portion of a unit's score is normalized by its **troop strength at the start of battle**.

As a result, an All-Cavalry unit whose troop strength has been reduced by 15% is evaluated relative to its own starting strength rather than only by absolute troop numbers.

See [Results and Rankings](../gameplay/results-and-rankings.md) for details.

## Related Pages

- [All-Cavalry Units vs. Matchlock Units in Flexible Square Formation](../experiments/flexible-square-matchlock-vs-all-cavalry.md)

- [Unit Types](unit-types.md)
- [Unit AI](ai.md)
- [Unit Tactics Experiment](unit-tactics-experiment.md)
- [Version 2.7.0](../updates/v2.7.0.md)
