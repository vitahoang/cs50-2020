/*
 In 6.sql, write a SQL query that lists the names of songs that are 
 by Post Malone: 
 - Your query should output a table with a single column for the name of each 
 song.
 - You should not make any assumptions about what Post Malone’s artist_id is.
 */
SELECT
    s.name
FROM
    songs AS s
    LEFT JOIN artists AS a ON s.artist_id = a.id
WHERE 
    a.name = 'Post Malone'