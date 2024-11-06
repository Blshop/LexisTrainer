
SELECT count(*)from(
SELECT word, answer, verified, learned_date, repeat_delay
FROM english_temp et 
GROUP BY word, answer, verified,learned_date, repeat_delay);


SELECT count(DISTINCT word) FROM english_temp et ;
SELECT count(DISTINCT(word)) FROM russian_temp et; 

SELECT DISTINCT word, verified FROM english_temp et 
WHERE word NOT in(
SELECT DISTINCT(trim(word)) FROM english_temp et );


SELECT et.word,et.answer, rt.word 
FROM english_temp et 
JOIN "translation" t ON t.english_id = et.id
JOIN russian_temp rt ON rt.id  = t.russian_id 
WHERE et.word = "sweet"

SELECT word FROM russian_temp rt WHERE word = ''\


SELECT word, count(word) from(
SELECT DISTINCT word, answer, verified, learned_date, repeat_delay FROM russian_temp et)
GROUP BY word 
HAVING count(word) > 1

SELECT * FROM english_temp et WHERE word = 'working';

UPDATE english_temp 
SET learned_date = '2023-02-15', repeat_delay = 5
WHERE id = 1441

SELECT *
FROM english_temp et 
JOIN "translation" t ON t.english_id = et.id 
--JOIN russian_temp rt ON rt.id = t.russian_id 
WHERE et.word = 'article'

SELECT * FROM english_temp et 
WHERE et.word = 'article'


SELECT * FROM "translation" t 
where t.english_id = 691

SELECT *
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id 
JOIN russian r ON r.id = rp.word_id 
WHERE r.word_desc = 'возлюбленный'

SELECT * FROM english_russian er 
WHERE main_part_id = 1674


SELECT r.word_desc ,group_concat(e.word_desc)
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id 
JOIN russian r ON r.id = rp.word_id 
WHERE r.english_answer = 0 AND r.english_verified = TRUE 
GROUP BY r.word_desc 


SELECT e.word_desc ,group_concat(r.word_desc)
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id 
JOIN russian r ON r.id = rp.word_id 
WHERE e.russian_answer = 0 AND e.russian_verified = TRUE 
GROUP BY e.word_desc 

SELECT * 
FROM russian r 
WHERE r.word_desc = 'Ã�Â»Ã�Â°Ã�Â²Ã�ÂºÃ�Â°'



SELECT *
FROM english e 
left JOIN english_part ep ON ep.word_id = e.id
left JOIN english_russian er ON er.main_part_id = ep.id
WHERE ep.id = 461



SELECT r.id, r.word_desc, e.word_desc, ep.id, er.main_part_id, er.sec_part_id  FROM russian r 
FULL JOIN russian_part rp ON rp.word_id  = r.id 
FULL JOIN english_russian er ON er.sec_part_id = rp.id
FULL JOIN english_part ep ON ep.id = er.main_part_id
FULL JOIN english e ON e.id = ep.word_id 
WHERE r.word_desc = 'возлюбленный'

DELETE FROM english 
WHERE word_desc = 'be fond (of)'

DELETE FROM english_russian 
WHERE main_part_id = 1070 AND sec_part_id = 758



SELECT e.word_desc ,group_concat(r.word_desc)
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id 
JOIN russian r ON r.id = rp.word_id 
WHERE e.russian_verified = TRUE 
GROUP BY e.word_desc 




SELECT r.word_desc ,group_concat(e.word_desc)
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id
JOIN russian r ON r.id = rp.word_id 
WHERE r.english_verified = TRUE 
GROUP BY r.word_desc




SELECT *
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
WHERE e.word_desc  = "thoroughly"

DELETE FROM english_part 
WHERE id = 715

SELECT *
FROM english e 
WHERE e.word_desc  = "perch"

DELETE FROM english 
WHERE id = 664



SELECT *
FROM russian r 
JOIN russian_part rp ON rp.word_id = r.id 
WHERE r.word_desc  = "скотина"

DELETE FROM russian_part 
WHERE id = 818

SELECT *
FROM russian r 
WHERE r.word_desc  = "шоколадный"

DELETE FROM russian 
WHERE id = 811

DELETE FROM english 
WHERE id in(
SELECT * 
FROM english e 
WHERE e.id NOT in(
SELECT e.id 
FROM english e 
JOIN english_part ep ON ep.word_id = e.id 
JOIN english_russian er ON er.main_part_id = ep.id 
JOIN russian_part rp ON rp.id = er.sec_part_id 
JOIN russian r ON r.id = rp.word_id ))


DELETE FROM russian
WHERE id in(
SELECT r.id 
FROM russian r 
WHERE r.id NOT in(
SELECT r.id 
FROM russian r 
JOIN russian_part rp ON rp.word_id = r.id 
JOIN english_russian er ON er.sec_part_id = rp.id 
JOIN english_part ep ON ep.id = er.main_part_id 
JOIN english e ON e.id = ep.word_id ))

