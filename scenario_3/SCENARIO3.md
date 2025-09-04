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
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.024882
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.266712
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.156024
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.150536
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.044650
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.001497
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.100461
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.018334
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.013594
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.016026
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.064230
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.014966
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.021701
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.002681
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)**: 0.007546
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.002869
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.003367
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.004428
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.000935
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.000561
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.002432
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000748
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.001808
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.002744
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.001996
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.012285
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.000374
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.012222
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.001497
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.002869
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.008044
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000935
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000437
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)**: 0.006174
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.001933
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.000499
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000748
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.000998
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.001185
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000686
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.001434
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.004240
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.002494
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.001871
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.001122
- **P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000249
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000249
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.002619
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.000249
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000249
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000561
- **P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000935
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)**: 0.001122
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.000624
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000998
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.001372
- **P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000748
- **P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)**: 0.000499
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)**: 0.000499
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000062
- **P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)**: 0.000561
- **P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000125
- **P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)**: 0.000125
- **P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)**: 0.000374

### Marginal Probabilities
- **P(underground_veteran=True)**: 0.6795
- **P(international=True)**: 0.5735
- **P(fashion_forward=True)**: 0.6910
- **P(queer_friendly=True)**: 0.0461
- **P(vinyl_collector=True)**: 0.0445
- **P(german_speaker=True)**: 0.4565

### Observed Correlation
- **corr(underground_veteran, international)**: -0.0811
- **corr(underground_veteran, fashion_forward)**: -0.1697
- **corr(underground_veteran, queer_friendly)**: 0.0372
- **corr(underground_veteran, vinyl_collector)**: 0.0722
- **corr(underground_veteran, german_speaker)**: 0.1119
- **corr(international, fashion_forward)**: 0.3757
- **corr(international, queer_friendly)**: 0.0037
- **corr(international, vinyl_collector)**: -0.0308
- **corr(international, german_speaker)**: -0.7173
- **corr(fashion_forward, queer_friendly)**: -0.0035
- **corr(fashion_forward, vinyl_collector)**: -0.1102
- **corr(fashion_forward, german_speaker)**: -0.3521
- **corr(queer_friendly, vinyl_collector)**: 0.4799
- **corr(queer_friendly, german_speaker)**: 0.0480
- **corr(vinyl_collector, german_speaker)**: 0.0998

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
