SELECT 
    description, 
    COUNT(*) AS total_incidents 
FROM 
    incidents 
GROUP BY 
    description 
ORDER BY 
    total_incidents DESC;