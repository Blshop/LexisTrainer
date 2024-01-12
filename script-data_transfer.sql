INSERT INTO english (word_desc, answer, russian, delay, repeat_date)
SELECT DISTINCT word, answer, verified, repeat_delay, learned_date FROM english_temp;

INSERT INTO russian (word_desc, answer, english, delay, repeat_date)
SELECT DISTINCT word, answer, verified, repeat_delay, learned_date FROM russian_temp;


INSERT INTO english_part (word_id, part_id)
SELECT e.id, p.id
FROM english_temp et 
JOIN english e ON et.word = e.word_desc
JOIN parts p ON p.part_desc = et.part;

INSERT INTO russian_part (word_id, part_id)
SELECT r.id, p.id
FROM russian_temp rt 
JOIN russian r ON rt.word = r.word_desc
JOIN parts p ON p.part_desc = rt.part;


INSERT INTO english_russian(main_part_id, sec_part_id)
SELECT ep.id, rp.id
FROM english_temp et 
JOIN english e ON et.word = e.word_desc
JOIN parts p ON p.part_desc = et.part
JOIN "translation" t ON t.english_id = et.id
JOIN russian_temp rt ON rt.id = t.russian_id 
JOIN russian r ON r.word_desc = rt.word 
JOIN english_part ep ON ep.word_id = e.id
JOIN russian_part rp ON rp.word_id = r.id
WHERE ep.part_id = rp.part_id;
