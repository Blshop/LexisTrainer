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

--===============================================================================================

CREATE TABLE english(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL DEFAULT 0,
verified boolean NOT NULL DEFAULT False,
delay INTERVAL,
date_repeate date
);

CREATE TABLE english_part(
id integer PRIMARY KEY AUTOINCREMENT,
english_id int,
part_id int,
FOREIGN KEY (english_id) REFERENCES english(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(english_id, part_id)
);

-----------------------------------------------------------------------------------------------

CREATE TABLE russian(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL,
verified boolean NOT NULL,
delay INTERVAL,
date_repeate date
);

CREATE TABLE russian_part(
id integer PRIMARY KEY AUTOINCREMENT,
russian_id int,
part_id int,
FOREIGN KEY (russian_id) REFERENCES russian(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(russian_id, part_id)
);

--------------------------------------------------------------------------------------------------

CREATE TABLE polish(
id integer PRIMARY KEY AUTOINCREMENT,
word varchar(30) UNIQUE,
answer int NOT NULL,
verified boolean NOT NULL,
delay INTERVAL,
date_repeate date
);

CREATE TABLE polish_part(
id integer PRIMARY KEY AUTOINCREMENT,
polish_id int,
part_id int,
FOREIGN KEY (polish_id) REFERENCES polish(id),
FOREIGN KEY (part_id) REFERENCES parts(id),
UNIQUE(polish_id, part_id)
);

--===============================================================================================

CREATE TABLE eng_rus(
eng_part_id int,
rus_part_id int,
FOREIGN KEY (eng_part_id) REFERENCES english_part(id),
FOREIGN KEY (rus_part_id) REFERENCES russian_part(id)
);

CREATE TABLE eng_pol(
eng_part_id int,
pol_part_id int,
FOREIGN KEY (eng_part_id) REFERENCES english_part(id),
FOREIGN KEY (pol_part_id) REFERENCES polish_part(id)
);

CREATE TABLE rus_pol(
pol_part_id int,
rus_part_id int,
FOREIGN KEY (pol_part_id) REFERENCES polish_part(id),
FOREIGN KEY (rus_part_id) REFERENCES russian_part(id)
);

