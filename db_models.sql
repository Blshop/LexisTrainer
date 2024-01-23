CREATE TABLE parts(
id integer PRIMARY KEY AUTOINCREMENT,
part_desc varchar(10) UNIQUE NOT NULL
);

INSERT INTO parts (part_desc)
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
('english'),
('russian'),
('polish');

--===============================================================================================

CREATE TABLE english(
id integer PRIMARY KEY AUTOINCREMENT,
word_desc varchar(30) UNIQUE,
russian_answer int NOT NULL DEFAULT 0,
russian_verified boolean NOT NULL DEFAULT False,
russian_delay integer DEFAULT 5,
russian_repeat_date date,
polish_answer int NOT NULL DEFAULT 0,
polish_verified boolean NOT NULL DEFAULT False,
polish_delay integer DEFAULT 5,
polish_repeat_date date
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
word_desc varchar(30) UNIQUE,
english_answer int NOT NULL DEFAULT 0,
english_verified boolean NOT NULL DEFAULT False,
english_delay integer DEFAULT 5,
english_repeat_date date,
polish_answer int NOT NULL DEFAULT 0,
polish_verified boolean NOT NULL DEFAULT False,
polish_delay integer DEFAULT 5,
polish_repeat_date date
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
word_desc varchar(30) UNIQUE,
russian_answer int NOT NULL DEFAULT 0,
russian_verified boolean NOT NULL DEFAULT False,
russian_delay integer DEFAULT 5,
russian_repeat_date date,
english_answer int NOT NULL DEFAULT 0,
english_verified boolean NOT NULL DEFAULT False,
english_delay integer DEFAULT 5,
english_repeat_date date
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

