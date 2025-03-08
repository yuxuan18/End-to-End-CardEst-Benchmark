COPY badges FROM '/badges.csv' DELIMITER ',' CSV HEADER;
COPY comments FROM '/comments.csv' DELIMITER ',' CSV HEADER;
COPY postHistory FROM '/postHistory.csv' DELIMITER ',' CSV HEADER;
COPY postLinks FROM '/postLinks.csv' DELIMITER ',' CSV HEADER;
COPY posts FROM '/posts.csv' DELIMITER ',' CSV HEADER;
COPY tags FROM '/tags.csv' DELIMITER ',' CSV HEADER;
COPY users FROM '/users.csv' DELIMITER ',' CSV HEADER;
COPY votes FROM '/votes.csv' DELIMITER ',' CSV HEADER;
