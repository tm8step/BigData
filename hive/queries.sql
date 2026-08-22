-- Query Example 1 - Counting all Instances of a Malignant Diagnosis

SELECT COUNT(diagnosis)
FROM WiscCancerData 
WHERE diagnosis LIKE 'M';

Results:  212


-- Query Example 2:  Finding the Average of a column
SELECT AVG(`Radius Mean`)
FROM WiscCancerData;

Results: 14.1272
