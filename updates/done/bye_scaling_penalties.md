We are going to be completely replacing the BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY with new parameters: SAME_POS_BYE_WEIGHT and DIFF_POS_BYE_WEIGHT
The Bye Week Penalty calculation will be updated to look like the following
1) Collect two lists of players, one that has players of the same position and same bye week as whoever is being scored, and one with players on the roster with a different position and same bye week as whoever is being scored
2) For each list, look at each player and determine what the median score is from their week 1-18 scores. Each player's median value will then be added up to get a total value for each list of players
3) For the first list of same-position players, take the calculated median value from that list and take it to the power of SAME_POS_BYE_WEIGHT (e.g. same_pos_median_total ** SAME_POS_BYE_WEIGHT)
4) For the first list of different-position players, take the calculated median value from that list and take it to the power of DIFF_POS_BYE_WEIGHT (e.g. diff_pos_median_total ** DIFF_POS_BYE_WEIGHT)
5) Add the two values together, and return that total as the Bye Penalty

Update the Simulation as well to replace the old parameters with the new ones