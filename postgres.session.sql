CREATE TABLE IF NOT EXISTS POSTS(
    postID serial,
    username varchar(255),
    content varchar(255),
    commentIDs INT []
);

CREATE TABLE IF NOT EXISTS POST_COMMENTS(
    commentID serial,
    username varchar(255),
    content varchar(255)
);

CREATE TABLE IF NOT EXISTS USERS(
    username varchar(255),
    password varchar(255)
);

INSERT INTO POSTS (username, content, commentIDs) VALUES
('user123', 'Just saw a ghost in my backyard! #spooky', '{1,2}'),
('user234', 'Anyone else hear whispers at night?', '{3}'),
('user345', 'Captured an EVP saying "hello" in an abandoned hospital.', '{}'),
('user456', 'Experienced poltergeist activity at my friend’s house.', '{4,5}');

INSERT INTO POST_COMMENTS (username, content) VALUES
('user345', 'Wow, that sounds scary! Did you get it on video?'),
('user234', 'I’ve heard similar stories about that place.'),
('user456', 'Yes! I thought I was the only one.'),
('user123', 'That’s classic poltergeist. Was anything moved?'),
('user345', 'You should contact a paranormal investigator.');

INSERT INTO USERS (username, password) VALUES
('user123', 'password1'),
('user234', 'password2'),
('user345', 'password3'),
('user456', 'password4');