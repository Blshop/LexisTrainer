CREATE TABLE parts(
id integer PRIMARY KEY AUTOINCREMENT,
part varchar(10) UNIQUE NOT NULL
);

INSERT INTO parts (part)
VALUES 
("noun") ,
("verb") ,
("adjective") ,
("adverb") ,
("misc")
;

CREATE TABLE languages(
id integer PRIMARY KEY AUTOINCREMENT,
'language' varchar(15) UNIQUE NOT NULL
);

INSERT INTO languages('language')
VALUES
('russian'),
('english'),
('polish');

--===============================================================================================

CREATE TABLE english(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL DEFAULT 0,
verified boolean NOT NULL DEFAULT False,
delay integer,
repeat_date date
);

CREATE TABLE english_part(
id integer PRIMARY KEY AUTOINCREMENT,
word_id int,
part_id int,
FOREIGN KEY (word_id) REFERENCES english(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(word_id, part_id)
);

-----------------------------------------------------------------------------------------------

CREATE TABLE russian(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL,
verified boolean NOT NULL,
delay integer,
repeat_date date
);

CREATE TABLE russian_part(
id integer PRIMARY KEY AUTOINCREMENT,
word_id int,
part_id int,
FOREIGN KEY (word_id) REFERENCES russian(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(word_id, part_id)
);

--------------------------------------------------------------------------------------------------

CREATE TABLE polish(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL,
verified boolean NOT NULL,
delay integer,
repeat_date date
);

CREATE TABLE polish_part(
id integer PRIMARY KEY AUTOINCREMENT,
word_id int,
part_id int,
FOREIGN KEY (word_id) REFERENCES polish(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(word_id, part_id)
);

--===============================================================================================

CREATE TABLE english_russian(
main_part_id int,
sec_part_id int,
FOREIGN KEY (main_part_id) REFERENCES english_part(id),
FOREIGN KEY (sec_part_id) REFERENCES russian_part(id)
);

CREATE TABLE english_polish(
main_part_id int,
sec_part_id int,
FOREIGN KEY (main_part_id) REFERENCES english_part(id),
FOREIGN KEY (sec_part_id) REFERENCES polish_part(id)
);

CREATE TABLE russian_polish(
main_word_id int,
sec_word_id int,
FOREIGN KEY (main_word_id) REFERENCES polish_part(id),
FOREIGN KEY (sec_word_id) REFERENCES russian_part(id)
);

