CREATE DATABASE people;
use people;

CREATE TABLE developers (
  user_id int not null,
  name VARCHAR(64),
  age int
);

INSERT INTO developers
  (user_id, name, age)
VALUES 
  (1, 'Rafael', 24),
  (2, 'Andre', 25);


