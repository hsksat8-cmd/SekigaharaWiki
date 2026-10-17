# Unit AI

[日本語版](../../systems/ai.md)

Units act autonomously according to morale, fatigue, positioning, battlefield conditions, and other factors.

## Version 2.1.0

Unit behavior was adjusted to feel more natural.

## Version 2.2.0

Unit behavior was revised to resemble the actions of Sengoku-period commanders rather than following purely game-like logic. Temporary retreat at low morale was also added.

## Scenario-Dependent Participation

The conditions for joining, observing, and defecting vary by scenario. In **Historical**, Kobayakawa, Mori, Shimazu, and others react to the battle situation. Fixed scenarios such as **Kobayakawa Observes** and **Mori Active** change the behavior conditions of specific forces. Random battle scenarios add random elements to participation timing, commander traits, and other conditions. See the [Scenario List](../scenarios/index.md) for details.

## Version 2.6.1: Unit Tactical Stances

Each unit can now be assigned **Charge, Aggressive, Normal, Defensive, or Retreat**. The stance can be stored as part of a sub-scenario and can also be changed during battle through user commands for controllable units.

A tactical stance does not directly modify attack power, defense, or accuracy. Instead, it shifts the action selected by the existing situation-evaluation logic toward offense or defense.

| Stance | Behavior |
|---|---|
| Charge | Ordinary units always choose Attack; commander-in-chief units always choose Advance |
| Aggressive | Shifts one step toward offense: Defense → Support, Support → Advance, Advance → Attack |
| Normal | Uses the normal situation-based decision without modification |
| Defensive | Shifts one step toward defense: Attack → Advance, Advance → Support, Support → Defense |
| Retreat | Always chooses Retreat |

See the [Unit Tactics Experiment](unit-tactics-experiment.md) for the comparison results.
See [Experiments](../experiments/index.md) for all experiment results collected in one section.

