# Unit Tactics Experiment

[日本語版](../../systems/unit-tactics-experiment.md)

[Experiments](../experiments/index.md)

This experiment compares how selectable unit tactical stances affect battle results.

Starting with Version 2.6.1, each unit can use **Charge, Aggressive, Normal, Defensive, or Retreat**. A tactical stance does not directly modify accuracy, attack power, defense, or other combat stats. Instead, it shifts the action selected by the existing situation-evaluation logic toward offense or defense.

## Behavior of Each Tactical Stance

| Stance | Behavior |
|---|---|
| Charge | Ordinary units always choose Attack; commander-in-chief units always choose Advance |
| Aggressive | Shifts one step toward offense: Defense → Support, Support → Advance, Advance → Attack |
| Normal | Uses the normal situation-based decision without modification |
| Defensive | Shifts one step toward defense: Attack → Advance, Advance → Support, Support → Defense |
| Retreat | Always chooses Retreat |

Retreat was not included in the battle comparisons below.

## One-on-One Tactical Comparison

### Conditions

- Eastern Army: 5,000 troops
- Western Army: 5,000 troops
- Western Army stance: Normal
- Eastern Army stance: Charge, Aggressive, or Defensive
- All other conditions were kept the same
- Loss figures are Eastern and Western troop losses

### Results

| Eastern stance | Trials | Eastern wins | Western wins | Avg. Eastern losses | Avg. Western losses | Avg. total losses |
|---|---:|---:|---:|---:|---:|---:|
| Charge | 10 | 3 (30%) | 7 (70%) | 4,659 | 4,335 | 8,994 |
| Aggressive | 12 | 6 (50%) | 6 (50%) | 4,507 | 4,453 | 8,959 |
| Defensive | 10 | 4 (40%) | 6 (60%) | 4,544 | 4,312 | 8,856 |

### Average Losses in Winning Battles Only

| Eastern stance | Eastern losses when Eastern Army won | Western losses when Western Army won |
|---|---:|---:|
| Charge | 3,863 | 4,050 |
| Aggressive | 4,013 | 3,905 |
| Defensive | 3,860 | 3,853 |

### Analysis

Under these conditions, **Aggressive** produced the highest Eastern Army win rate, splitting the results evenly at 50% each. Average losses were also the closest of the three stances: 4,507 for the Eastern Army and 4,453 for the Western Army.

With **Charge**, the Eastern Army won only 30% of the trials and was wiped out in 7 of 10 battles. Even in the battles it lost, however, it inflicted an average of 4,050 losses on the Western Army. Continuous offense made the fighting intense, but the unit was less able to stop attacking when the situation became unfavorable.

With **Defensive**, the Eastern Army won 4 and lost 6. Its average total losses of both armies combined were 8,856, the lowest of the three stances, though the difference was not large. A more defensive decision pattern can suppress overly aggressive attacks, but it may also miss opportunities to finish off the opponent.

In this one-on-one setup, Aggressive was more stable than the extreme continuous offense of Charge.

## Tactical Comparison in a Pincer Attack

This setup uses a front and rear attack against the same enemy unit, similar to the [Pincer Attack Experiment](../formations/pincer-experiment.md).

### Conditions

- Eastern Army: 12,200 troops
- Western front unit: 5,000 troops
  - Formation: Deep
  - Matchlock Ashigaru: 30%
- Western rear unit: 5,000 troops
  - Formation: Crane Wing
  - Matchlock Ashigaru: 45%
- The Western Army attacks the Eastern unit from the front and rear
- Loss figures are Eastern losses and total Western losses

When comparing the front unit's stance, the rear unit was fixed to Charge. When comparing the rear unit's stance, the front unit was fixed to Normal.

### Results

| Front unit | Rear unit | Trials | Western wins | Eastern wins | Avg. Eastern losses | Avg. Western losses | Avg. total losses |
|---|---|---:|---:|---:|---:|---:|---:|
| Normal | Charge | 10 | 6 (60%) | 4 (40%) | 10,575 | 8,445 | 19,020 |
| Defensive | Charge | 10 | 5 (50%) | 5 (50%) | 10,530 | 8,489 | 19,019 |
| Aggressive | Charge | 10 | 4 (40%) | 6 (60%) | 10,316 | 8,556 | 18,872 |
| Normal | Aggressive | 10 | 3 (30%) | 7 (70%) | 10,029 | 8,524 | 18,553 |

### Front Unit Stance

With the rear unit fixed to Charge, the observed Western Army win rates were:

1. Front Normal: 60%
2. Front Defensive: 50%
3. Front Aggressive: 40%

Making the front unit Aggressive did not necessarily improve the overall effect of the pincer attack. If the front unit advanced too quickly, the battle line could move before the rear unit made contact, or the front formation could become disrupted.

With the front unit set to Normal, it could switch among Attack, Advance, Support, and Defense according to the situation. In these trials, that made it more likely to hold the enemy while waiting for the rear unit, and this combination produced the highest observed Western Army win rate.

Defensive produced a result between Normal and Aggressive. It may help preserve the front unit, but if it becomes too passive it can fail to apply enough pressure from the front when the rear unit charges.

### Rear Unit Stance

With the front unit fixed to Normal:

| Rear unit stance | Western win rate | Avg. Eastern losses | Avg. Western losses |
|---|---:|---:|---:|
| Charge | 60% | 10,575 | 8,445 |
| Aggressive | 30% | 10,029 | 8,524 |

Changing the rear unit from Charge to Aggressive reduced the observed Western Army win rate from 60% to 30%. Average Western losses changed little, while average Eastern losses fell by 546 troops.

With Charge, the Eastern unit was wiped out in 6 of 10 battles. With Aggressive, that occurred in 3 of 10. Under this setup, continuous pressure from the rear unit strongly affected whether the battle reached a decisive result.

However, in the three battles won with the rear unit set to Aggressive, average Western losses were 7,990, lower than the 8,208 average in the six wins with Charge. Aggressive won less often, but its successful attacks produced somewhat lower losses.

## Overall Findings

The experiment suggests that tactical stance effectiveness depends on the **role assigned to the unit**, rather than on a simple strongest-to-weakest ranking.

- In one-on-one combat, Aggressive retained situation-based decision making and produced relatively stable results approaching those of Normal
- For the front unit in the pincer attack, Normal was effective at holding the enemy while adapting to the situation
- For the rear unit in the pincer attack, Charge strongly benefited from uninterrupted pressure
- Defensive may help preserve a front unit, but can reduce pressure in a pincer attack
- Charge can be decisive, but in a standalone fight it can also increase the risk of losses and defeat

## Notes

Each condition used 10 to 12 trials, and the trials were not paired one-to-one with the same random seed. Because combat outcomes vary with random factors, differences in win rates should be treated as **observed tendencies under these conditions**, not as definitive performance differences.

Battle outcomes are also determined by factors other than troop losses, including the death of the army commander and unit routs. Some winning battles therefore include high losses, and some losing units were not completely destroyed.

## Normal Tactic vs. Charge Tactic

In a one-on-one battle, the well-balanced **Normal tactic** has the overall advantage.

The **Charge tactic** gains momentum early in the battle, but gradually falls behind the Normal tactic, which can flexibly switch between offense and defense as the situation changes.

With the Normal tactic, a unit temporarily retreats when the situation becomes unfavorable. This can sometimes allow the opponent to gain momentum, but it can also reset an unfavorable situation and disrupt the balance of an enemy formation that is currently in a strong position.

### YouTube Reference Video

[Unit Tactics Comparison Experiment — One-on-One: Normal Tactic (Blue) vs. Charge Tactic (Red)](https://youtu.be/0mD00WVXVvE?si=q2YVq37m12GYEi-v)

