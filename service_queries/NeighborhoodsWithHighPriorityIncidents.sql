SELECT 
    locations.neighborhood, 
    COUNT(calls.callKey) AS highPriorityCalls 
FROM 
    calls
JOIN 
    incidents ON calls.recordld = incidents.recordld
JOIN 
    locations ON incidents.locationRecordId = locations.locationRecordId
WHERE 
    calls.priority = 'High' 
GROUP BY 
    locations.neighborhood 
ORDER BY 
    highPriorityCalls DESC;