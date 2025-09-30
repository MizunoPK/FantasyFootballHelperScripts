# Scoring Overhaul Clarification Questions

**Purpose**: Clarify specific implementation details before beginning the scoring overhaul development.

**Instructions**: Please answer each question below. I will update the TODO file based on your responses.

---

## **1. Normalization Scale Configuration**

You mentioned normalizing fantasy points to 0-100 scale with configurable max value. Should this be:

**A.** Maximum fantasy points value used for normalization (e.g., if max is 350, a player with 175 points = 50/100)?

**B.** The scale ceiling itself (e.g., normalize to 0-80 instead of 0-100)?

**Answer:** [ Both A and B should be true. The value should modify what the max is, then scores should fit between 0 and that number. For example, if the config value is 80, the highest number of fantasy points a player recieved is 350, and we are looking at a player who got 175, then the resulting normalized value would be 40. ]

**What should be the default maximum value for initial implementation?**

**Answer:** [ 100 ]

---

## **2. DRAFT_ORDER Static Values**

For the static point values in DRAFT_ORDER, what magnitude should these be?

**Are these reasonable starting values:** `{FLEX: 50, QB: 25}`?

**Answer:** [ Yes ]

**Should these values be in the simulation config as ranges for optimization (e.g., `DRAFT_ORDER_FLEX_BONUS: [40, 50, 60]`)?**

**Answer:** [ Yes ]

**How should these values scale relative to normalized fantasy points (0-100)?**

**Answer:** [ The #1 position in each round will be starting at 50 points, then you can estimate the follow-up ones based on your own judgement. I will be testing and tweaking these values later. ]

---

## **3. Round Assignment Algorithm**

For assigning existing roster players to rounds: "the first round the system finds that is not yet associated with a player, and that the round's DRAFT_ORDER dictionary's highest scoring position matches the player"

**If multiple players match the same round's highest position, which gets priority?**

**Answer:** [ It doesn't matter. It doesn't matter which player is slotted into Round 1 or 3 for example, all that matters is that there are enough positions already rostered to fill those slots. ]

**Should this use fantasy points as tiebreaker (highest points gets earlier round)?**

**Answer:** [ See previous answer - it does not matter ]

**What happens if no round matches a player's position?**

**Answer:** [ This should never happen. The DRAFT_ORDER variable is set up such that the number of #1 slots of each position line up with the MAX_POSITIONS setting, thus the system should never allow the user to have a roster that does not align with the DRAFT_ORDER's expected positions. You can set up some unit tests to verify this stays true. ]

---

## **4. Matchup Multiplier System**

For Starter Helper matchup multipliers based on team rank differences:

**Should this be similar to ADP ranges (e.g., rank difference 1-5 = 1.15x, 6-10 = 1.10x, etc.)?**

**Answer:** [ Invert it - the higher the difference then the higher the multiplier they recieve should be. For example, if rank 1 offence is facing rank 20 defence, then it is very likely that the very good offence will do well so they should be scoring higher.  ]

**Which team rankings should be used (offensive, defensive, or combined)?**

**Answer:** [ This new multiplier will only apply to QB, RB, WR, and TE players. These positions will all succeed from having a strong offense while facing a weak defense, or fail from a weak offense facing a strong defense. This means that what we care about is the difference between the player's offensive ranking and their opponent's defensive rank. Also, slight change in requirements: always make the calculation be (Defensive Rank of Opponent) - (Offensive Rank of Player's Team). This will make it so positive numbers correspond to >1x multipliers, and negative numbers make for <1x multipliers ]

**What should be the default multiplier ranges for simulation config?**

**Answer:** [ Let's start with <-15=0.8x, -15 to -6 = 0.9x, -5 to 5 = 1.0x, 6 to 15 = 1.1x, 15+=1.2x  ]

---

## **5. Current Week vs Seasonal Points**

In the requirements, you mention "projected points for the player on the current week" for Starter Helper:

**Should this use week-specific projections from the existing week-by-week system?**

**Answer:** [ Yes ]

**Should this respect the current `CURRENT_NFL_WEEK` setting?**

**Answer:** [ Yes ]

**How should this handle bye weeks (zero points or skip player)?**

**Answer:** [ Zero points ]

---

## **6. Injury Status Filtering**

For Starter Helper: "If the player is anything but ACTIVE or QUESTIONABLE, then their score should be zero'd out"

**Should this be absolute zero, or maintain existing injury penalty behavior for other modes?**

**Answer:** [ Maintain the same injury behavior for other modes, just have the starter helper set the player's value to 0 if they don't have those ACTIVE or QUESTIONABLE injuries status. ]

**Should this apply to bench recommendations too, or only starting lineup?**

**Answer:** [ Yes it should apply to all players ]

---

## **7. Integration with Existing Systems**

**Should the enhanced scoring system (ADP, Player Ranking, Team Ranking multipliers) remain exactly as implemented?**

**Answer:** [ Yes ]

**Are the existing multiplier caps removed only for new matchup system, or for all systems?**

**Answer:** [ All systems ]

**Should existing enhanced scoring integration remain unchanged in the new architecture?**

**Answer:** [ Yes ]

---

## **8. Backwards Compatibility**

**Any concerns about maintaining saved roster/draft data compatibility?**

**Answer:** [ No, do not worry about backwards compatability. There are no changes being made to players.csv currently so we shouldn't need to worry about that. ]

**Should there be a migration path or is clean break acceptable?**

**Answer:** [ Clean break is acceptable  ]

---

## **9. Plan Improvements**

Would you like me to suggest any improvements to the implementation plan, such as:

**Creating a feature flag system for gradual rollout?**

**Answer:** [ No need for feature flags, just get it implemented step by step ]

**Implementing logging/debugging features for the new scoring components?**

**Answer:** [ Yes add lots of logging to track exactly what is happening ]

**Adding validation checks for the new configuration parameters?**

**Answer:** [ Yes ]

**Any other improvements or considerations I should add to the plan?**

**Answer:** [ No ]

---

## **10. Additional Questions**

**Are there any other aspects of the scoring overhaul that need clarification?**

**Answer:** [ If you need anhy more clarification then ask me questions ]

**Any specific concerns about the implementation approach or timeline?**

**Answer:** [ I worry for the calculations not being implemented correctly. Please be very liberal with making unit tests and documenting exactly what you are doing ]

**Should I prioritize any particular scoring mode for initial implementation and testing?**

**Answer:** [ No ]

---

**Next Steps**: Once you provide answers, I will update the TODO file with specific implementation details and begin Phase 1 of the scoring overhaul.