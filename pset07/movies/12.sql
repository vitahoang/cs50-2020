/* 
 In 12.sql, write a SQL query to list the titles of all movies in which both 
 Johnny Depp and Helena Bonham Carter starred:
 - Your query should output a table with a single column for the 
 title of each movie.
 - You may assume that there is only one person in the database with the name 
 Johnny Depp.
 - You may assume that there is only one person in the database with the 
 name Helena Bonham Carter.
 */
SELECT
    title
FROM
    (
        SELECT
            m.title,
            GROUP_CONCAT(p.name) AS star_names
        FROM
            stars AS s
            LEFT JOIN movies AS m ON m.id = s.movie_id
            LEFT JOIN people AS p ON p.id = s.person_id
        GROUP BY
            m.title
    )
WHERE
    star_names LIKE "%Johnny Depp%Bonham Carter%"