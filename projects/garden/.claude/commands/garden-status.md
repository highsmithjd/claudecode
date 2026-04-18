# Garden Status

Read garden.json and display a full status report:

1. For each bed, show:
   - Dimensions and location
   - Every plant currently in the bed with its status (seedling, transplanted, etc.)
   - Days since last watering and the last watering date
   - Upcoming harvest dates sorted by soonest, calculated from date_planted + days_to_maturity

2. Show any plants started indoors but not yet transplanted, with their planned transplant bed and earliest transplant date

3. Flag anything that needs attention:
   - Watering overdue (more than 5 days since last log)
   - Plants past their estimated maturity date with no harvest logged
   - Any pest or disease entries that are unresolved

4. If the harvest_log has entries, show the most recent 3 harvests

Keep the output concise and scannable.
