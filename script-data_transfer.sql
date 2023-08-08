INSERT INTO english (word, answer, verified, delay, repeat_date)
SELECT DISTINCT word, answer, verified, repeat_delay, learned_date FROM english_temp;

INSERT INTO russian (word, answer, verified, delay, repeat_date)
SELECT DISTINCT word, answer, verified, repeat_delay, learned_date FROM russian_temp;


INSERT INTO english_part (word_id, part_id)
SELECT e.id, p.id
FROM english_temp et 
JOIN english e ON et.word = e.word
JOIN parts p ON p.part = et.part;

INSERT INTO russian_part (word_id, part_id)
SELECT r.id, p.id
FROM russian_temp rt 
JOIN russian r ON rt.word = r.word
JOIN parts p ON p.part = rt.part;


INSERT INTO english_russian(main_part_id, sec_part_id)
SELECT ep.id, rp.id
FROM english_temp et 
JOIN english e ON et.word = e.word
JOIN parts p ON p.part = et.part
JOIN "translation" t ON t.english_id = et.id
JOIN russian_temp rt ON rt.id = t.russian_id 
JOIN russian r ON r.word = rt.word 
JOIN english_part ep ON ep.word_id = e.id
JOIN russian_part rp ON rp.word_id = r.id
WHERE ep.part_id = rp.part_id;
