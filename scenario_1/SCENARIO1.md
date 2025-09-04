# Berghain Challenge - Scenario 1

You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people while satisfying specific constraints. People arrive one by one, and you must immediately decide whether to let them in or turn them away. Your challenge is to fill the venue with as few rejections as possible while meeting all minimum requirements.

## 📋 SCENARIO 1 CONSTRAINTS
- **young**: 600 people required
- **well_dressed**: 600 people required

## 📊 ATTRIBUTE STATISTICS
**Relative Frequencies (true probabilities):**
- well_dressed: 0.3225
- young: 0.3225

### Correlations
**well_dressed**
- well_dressed: 1
- young: 0.18304299322062992

**young**
well_dressed: 0.18304299322062992
young: 1

**Attribute Correlations:**
- young ↔ well_dressed: 0.18304299322062992 (weak positive correlation)

## 📊 OBSERVED BEHAVIOR
This is from data collected from the real API to determine real distrabution. 

### Joint Probabilities
- **P(young=False, well_dressed=False)**: 0.5024
- **P(young=False, well_dressed=True)**: 0.1827
- **P(young=True, well_dressed=False)**: 0.1753
- **P(young=True, well_dressed=True)**: 0.1396

### Marginal Probabilities
- **P(young=True)**: 0.3149
- **P(well_dressed=True)**: 0.3223

### Observed Correlation
- **corr(young, well_dressed)**: 0.1756

### Independence Check
- **P(both | independent)**: 0.1015
- **P(both | observed)**: 0.1396
- **Ratio**: 1.38

## 🔍 EXPECTED CATEGORY BREAKDOWN
Based on true probabilities, the population distribution is:
- **Both young & well_dressed**: 10.4% (~104 people) - **GOLD!**
- **Young only**: 21.8% (~218 people)
- **Well-dressed only**: 21.8% (~218 people)
- **Neither**: 45.9% (~459 people)

## 🎯 STRATEGY IMPLICATIONS
- Need 600 young people (target: 32.2% of population)
- Need 600 well_dressed people (target: 32.2% of population)
- People with BOTH attributes are only 10.4% of population - these are highly valuable!
- The constraints are tight since you need 60% of each attribute but they only occur in 32.2% of the population

## 🎮 HOW IT WORKS
- People arrive sequentially with binary attributes (young/old, well_dressed/poorly_dressed)
- You must make immediate accept/reject decisions
- The game ends when either:
  - (a) venue is full (1000 people)
  - (b) you rejected 20,000 people

## 🏆 SCORING
Your score is the number of people you rejected before filling the venue (the less the better).

## 💡 KEY INSIGHT
This scenario requires careful optimization since you need 60% of each attribute but they only occur naturally in 32.2% of the population. You'll need to be selective and strategic about who you accept to maximize the overlap between the two required attributes.