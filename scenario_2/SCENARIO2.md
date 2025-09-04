# Berghain Challenge - Scenario 2

You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people while satisfying specific constraints. People arrive one by one, and you must immediately decide whether to let them in or turn them away. Your challenge is to fill the venue with as few rejections as possible while meeting all minimum requirements.

## 📋 SCENARIO 2 CONSTRAINTS
- **techno_lover**: 650 people required
- **well_connected**: 450 people required
- **creative**: 300 people required
- **berlin_local**: 750 people required

## 📊 ATTRIBUTE STATISTICS
**Relative Frequencies (true probabilities):**
- techno_lover: 0.6265000000000001
- well_connected: 0.4700000000000001
- creative: 0.06227
- berlin_local: 0.398
  
### Correlations
**techno_lover**
- techno_lover: 1
- well_connected: -0.4696169332674324
- creative: 0.09463317039891586
- berlin_local: -0.6549403815606182

**well_connected**
- techno_lover: -0.4696169332674324
- well_connected: 1
- creative: 0.14197259140471485
- berlin_local: 0.5724067808436452

**creative**
- techno_lover: 0.09463317039891586
- well_connected: 0.14197259140471485
- creative: 1
- berlin_local: 0.14446459505650772

**berlin_local**: 
- techno_lover: -0.6549403815606182
- well_connected: 0.5724067808436452
- creative: 0.14446459505650772
- berlin_local: 1

**Correlations:**
- techno_lover ↔ well_connected: -0.4696169332674324 (negative correlation)
- techno_lover ↔ creative: 0.09463317039891586 (weak positive correlation)
- techno_lover ↔ berlin_local: -0.6549403815606182 (strong negative correlation)
- well_connected ↔ creative: 0.14197259140471485 (weak positive correlation)
- well_connected ↔ berlin_local: 0.5724067808436452 (moderate positive correlation)
- creative ↔ berlin_local: 0.14446459505650772 (weak positive correlation)

## 📊 OBSERVED BEHAVIOR
This is from data collected from the real API to determine real distribution. 

### Joint Probabilities
- **P(berlin_local=False, creative=False, techno_lover=True, well_connected=True)**: 0.0981
- **P(berlin_local=False, creative=False, techno_lover=True, well_connected=False)**: 0.4128
- **P(berlin_local=True, creative=False, techno_lover=False, well_connected=True)**: 0.2525
- **P(berlin_local=True, creative=False, techno_lover=True, well_connected=False)**: 0.0122
- **P(berlin_local=True, creative=True, techno_lover=True, well_connected=True)**: 0.0257
- **P(berlin_local=True, creative=False, techno_lover=False, well_connected=False)**: 0.0486
- **P(berlin_local=True, creative=False, techno_lover=True, well_connected=True)**: 0.0472
- **P(berlin_local=False, creative=False, techno_lover=False, well_connected=True)**: 0.0320
- **P(berlin_local=False, creative=False, techno_lover=False, well_connected=False)**: 0.0343
- **P(berlin_local=True, creative=True, techno_lover=True, well_connected=False)**: 0.0080
- **P(berlin_local=True, creative=True, techno_lover=False, well_connected=True)**: 0.0076
- **P(berlin_local=False, creative=True, techno_lover=True, well_connected=True)**: 0.0111
- **P(berlin_local=False, creative=True, techno_lover=False, well_connected=True)**: 0.0034
- **P(berlin_local=False, creative=True, techno_lover=True, well_connected=False)**: 0.0045
- **P(berlin_local=True, creative=True, techno_lover=False, well_connected=False)**: 0.0012
- **P(berlin_local=False, creative=True, techno_lover=False, well_connected=False)**: 0.0008

### Marginal Probabilities
- **P(techno_lover=True)**: 0.6265
- **P(well_connected=True)**: 0.4700
- **P(creative=True)**: 0.0623
- **P(berlin_local=True)**: 0.3980

### Observed Correlation
- **corr(techno_lover, well_connected)**: -0.4696
- **corr(techno_lover, creative)**: 0.0946
- **corr(techno_lover, berlin_local)**: -0.6549
- **corr(well_connected, creative)**: 0.1420
- **corr(well_connected, berlin_local)**: 0.5724
- **corr(creative, berlin_local)**: 0.1445

### Independence Check
Found 16 unique person types with empirical distribution from real API data.

## 🔍 EXPECTED CATEGORY BREAKDOWN
Based on true probabilities, the population distribution is:
- **All four attributes**: 0.8% (~8 people) - **PLATINUM!**
- **Three attributes**: 8.2% (~82 people) - **GOLD!**
- **Two attributes**: 32.1% (~321 people) - **SILVER!**
- **One attribute**: 45.2% (~452 people)
- **No attributes**: 13.7% (~137 people)

## 🎯 STRATEGY IMPLICATIONS
- Need 650 techno_lover people (target: 62.7% of population) - **HIGH PRIORITY**
- Need 750 berlin_local people (target: 39.8% of population) - **HIGH PRIORITY**
- Need 450 well_connected people (target: 47.0% of population) - **MEDIUM PRIORITY**
- Need 300 creative people (target: 6.2% of population) - **CRITICAL PRIORITY**
- Creative people are extremely rare (only 6.2%) - accept them whenever possible!
- Berlin locals are also valuable since you need 75% of the venue to be locals

## 🎮 HOW IT WORKS
- People arrive sequentially with binary attributes (techno_lover, well_connected, creative, berlin_local)
- You must make immediate accept/reject decisions
- The game ends when either:
  - (a) venue is full (1000 people)
  - (b) you rejected 20,000 people

## 🏆 SCORING
Your score is the number of people you rejected before filling the venue (the less the better).

## 💡 KEY INSIGHT
This scenario has a critical bottleneck with creative people (only 6.2% frequency) - you need 300 of them but they're extremely rare. You'll need to be extremely selective about accepting people who aren't creative, and prioritize creative people above all else. The high requirements for techno_lover (65%) and berlin_local (75%) also make this challenging since you need to balance multiple constraints while ensuring you don't miss the rare creative individuals.

## Notes

### Strategy Pseudocode
```
FOR each person arriving:
    IF person.creative == True:
        ACCEPT person  // Always accept creative people (rare 6.2%)
        
    ELSE IF person.creative == False:
        IF person.techno_lover == True AND person.well_connected == True AND person.berlin_local == True:
            IF well_connected_count < 450:
                ACCEPT person  // Phase 1: Build well_connected constraint
                well_connected_count += 1
            ELSE IF techno_lover_count < 650:
                ACCEPT person  // Phase 2: Build techno_lover constraint
                techno_lover_count += 1
            ELSE:
                // Both well_connected and techno_lover constraints met
                // Now focus on berlin_local and creative constraints
                IF person.berlin_local == True AND person.creative == True:
                    ACCEPT person  // Phase 3: Fill remaining berlin_local + creative
                ELSE:
                    REJECT person
        ELSE:
            REJECT person  // Doesn't meet current criteria
            
    // Once all constraints are met, accept everyone remaining
    IF all_constraints_satisfied():
        ACCEPT person
```

### Strategy Phases
1. **Phase 1**: Accept creative people + well_connected techno_lover berlin_locals until well_connected = 450
2. **Phase 2**: Accept non-creative techno_lover berlin_locals until techno_lover = 650  
3. **Phase 3**: Accept only berlin_local + creative people until both constraints met
4. **Phase 4**: Accept everyone remaining to fill venue