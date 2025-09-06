# Berghain Challenge - Scenario 3

You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people while satisfying specific constraints. People arrive one by one, and you must immediately decide whether to let them in or turn them away. Your challenge is to fill the venue with as few rejections as possible while meeting all minimum requirements.

## 📋 SCENARIO 3 CONSTRAINTS
- **underground_veteran**: 500 people required
- **international**: 650 people required
- **fashion_forward**: 550 people required
- **queer_friendly**: 250 people required
- **vinyl_collector**: 200 people required
- **german_speaker**: 800 people required

## 📊 ATTRIBUTE STATISTICS
**Relative Frequencies (true probabilities):**
- underground_veteran: 0.6794999999999999
- international: 0.5735
- fashion_forward: 0.6910000000000002
- queer_friendly: 0.04614
- vinyl_collector: 0.044539999999999996
- german_speaker: 0.4565000000000001

### Correlations
**underground_veteran**
- underground_veteran: 1
- international: -0.08110175777152992
- fashion_forward: -0.1696563475505309
- queer_friendly: 0.03719928376753885
- vinyl_collector: 0.07223521156389842
- german_speaker: 0.11188766703422799

**international**
- underground_veteran: -0.08110175777152992
- international: 1
- fashion_forward: 0.375711059360155
- queer_friendly: 0.0036693314388711686
- vinyl_collector: -0.03083247098181075
- german_speaker: -0.7172529382519395

**fashion_forward**
- underground_veteran: -0.1696563475505309
- international: 0.375711059360155
- fashion_forward: 1
- queer_friendly: -0.0034530926793377476
- vinyl_collector: -0.11024719606358546
- german_speaker: -0.3521024461597403

**queer_friendly**
- underground_veteran: 0.03719928376753885
- international: 0.0036693314388711686
- fashion_forward: -0.0034530926793377476
- queer_friendly: 1
- vinyl_collector: 0.47990640803167306
- german_speaker: 0.04797381132680503

**vinyl_collector**
- underground_veteran: 0.07223521156389842
- international: -0.03083247098181075
- fashion_forward: -0.11024719606358546
- queer_friendly: 0.47990640803167306
- vinyl_collector: 1
- german_speaker: 0.09984452286269897

**german_speaker**
- underground_veteran: 0.11188766703422799
- international: -0.7172529382519395
- fashion_forward: -0.3521024461597403
- queer_friendly: 0.04797381132680503
- vinyl_collector: 0.09984452286269897
- german_speaker: 1

**Attribute Correlations:**
- underground_veteran ↔ international: -0.08110175777152992 (weak negative correlation)
- underground_veteran ↔ fashion_forward: -0.1696563475505309 (weak negative correlation)
- underground_veteran ↔ queer_friendly: 0.03719928376753885 (weak positive correlation)
- underground_veteran ↔ vinyl_collector: 0.07223521156389842 (weak positive correlation)
- underground_veteran ↔ german_speaker: 0.11188766703422799 (weak positive correlation)
- international ↔ fashion_forward: 0.375711059360155 (moderate positive correlation)
- international ↔ queer_friendly: 0.0036693314388711686 (very weak positive correlation)
- international ↔ vinyl_collector: -0.03083247098181075 (weak negative correlation)
- international ↔ german_speaker: -0.7172529382519395 (strong negative correlation)
- fashion_forward ↔ queer_friendly: -0.0034530926793377476 (very weak negative correlation)
- fashion_forward ↔ vinyl_collector: -0.11024719606358546 (weak negative correlation)
- fashion_forward ↔ german_speaker: -0.3521024461597403 (moderate negative correlation)
- queer_friendly ↔ vinyl_collector: 0.47990640803167306 (moderate positive correlation)
- queer_friendly ↔ german_speaker: 0.04797381132680503 (weak positive correlation)
- vinyl_collector ↔ german_speaker: 0.09984452286269897 (weak positive correlation)

## 📊 OBSERVED BEHAVIOR
This is from data collected from the real API to determine real distribution. 

### Joint Probabilities
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.2606859024844276
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.1567981671081836
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.15173265554521373
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.10150712393498962
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.06502828094794874
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.0439428653254099
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.02534545714899406
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.021998281663922103
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.019886160234839263
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.016252595403450993
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.013800386625617528
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.013191809264695353
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.013156010596405813
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.01267272857449703
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.007213431660342235
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.006873344311591608
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.00678384764086776
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.004958115558101239
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.004206343524020906
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.0039199541777045896
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.0033650748192167253
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0029712894680317893
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.00289969213145271
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0028638934631631703
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0025596047827020833
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.002398510775399155
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0020763227607932984
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.002022624758358989
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.00191522875349037
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.0018615307510560608
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.0015930407388845135
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0015751414047397436
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.0014856447340158947
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0015214434023054343
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.0013424500608577362
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0012350540559891172
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.001252953390133887
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.0011276580511204984
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.0010739600486861889
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0010202620462518794
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0009486647096728001
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.0009307653755280304
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.000859168038948951
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0008233693706594115
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.0008054700365146416
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.0007159733657907926
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0006980740316460227
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0006801746975012529
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.0006622753633564832
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.0006443760292117133
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.0005190806901983246
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.00041168468532970574
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0003758860170401661
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0003579866828953963
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0003579866828953963
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0003579866828953963
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.0003579866828953963
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.00032218801460585667
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.0002684900121715472
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.0002684900121715472
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.00017899334144769814
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.00016109400730292834
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.0001252953390133887
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 5.369800243430944e-05

### Independence Check
Found 64 unique person types with empirical distribution from real API data.

## 🎯 ADVANCED SCORING
**Advanced Score**: 7.996 vs threshold 0.100 (×1.5 multi-bonus)

**Score Breakdown:**
- underground_veteran: urgency=0.50, rarity=1.5, contrib=0.74
- international: urgency=0.65, rarity=1.7, contrib=1.13  
- fashion_forward: urgency=0.55, rarity=1.4, contrib=0.80

**Total Contribution**: 2.67

## 🔍 EXPECTED CATEGORY BREAKDOWN
Based on true probabilities, the population distribution is:
- **All six attributes**: 0.5% (~5 people) - **PLATINUM!**
- **Five attributes**: 4.2% (~42 people) - **GOLD!**
- **Four attributes**: 15.8% (~158 people) - **SILVER!**
- **Three attributes**: 28.9% (~289 people)
- **Two attributes**: 28.7% (~287 people)
- **One attribute**: 17.8% (~178 people)
- **No attributes**: 4.1% (~41 people)

## 🎯 STRATEGY IMPLICATIONS
- Need 800 german_speaker people (target: 80% of population) - **CRITICAL PRIORITY**
- Need 650 international people (target: 65% of population) - **HIGH PRIORITY**
- Need 550 fashion_forward people (target: 55% of population) - **HIGH PRIORITY**
- Need 500 underground_veteran people (target: 50% of population) - **MEDIUM PRIORITY**
- Need 250 queer_friendly people (target: 25% of population) - **CRITICAL PRIORITY**
- Need 200 vinyl_collector people (target: 20% of population) - **CRITICAL PRIORITY**
- Queer_friendly and vinyl_collector people are extremely rare (only 4.6% and 4.5%) - accept them whenever possible!
- German speakers are also valuable since you need 80% of the venue to speak German

## 🎮 HOW IT WORKS
- People arrive sequentially with binary attributes (underground_veteran, international, fashion_forward, queer_friendly, vinyl_collector, german_speaker)
- You must make immediate accept/reject decisions
- The game ends when either:
  - (a) venue is full (1000 people)
  - (b) you rejected 20,000 people

## 🏆 SCORING
Your score is the number of people you rejected before filling the venue (the less the better).

## 💡 KEY INSIGHT
This scenario has critical bottlenecks with queer_friendly and vinyl_collector people (only 4.6% and 4.5% frequency respectively) - you need 250 and 200 of them but they're extremely rare. You'll need to be extremely selective about accepting people who aren't queer_friendly or vinyl_collectors, and prioritize these rare individuals above all else. The high requirements for german_speaker (80%) and international (65%) also make this challenging since you need to balance multiple constraints while ensuring you don't miss the rare queer_friendly and vinyl_collector individuals.
