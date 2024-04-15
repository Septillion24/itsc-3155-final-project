CREATE TABLE IF NOT EXISTS User (
    UserID serial PRIMARY KEY,
    Username varchar(255),
    Email varchar(255),
    FirstName varchar(255),
    LastName varchar(255),
    Password varchar(255)
);
CREATE TABLE IF NOT EXISTS FriendRelationship (
    id serial PRIMARY KEY,
    user1 int REFERENCES User(UserID),
    user2 int REFERENCES User(UserID)
);
CREATE TABLE IF NOT EXISTS Post (
    PostID serial PRIMARY KEY,
    Owner int REFERENCES User(UserID),
    Title varchar(255),
    ImageID int,
    TextContent text,
    Timestamp timestamp without time zone
);
CREATE TABLE IF NOT EXISTS Image (
    ImageID serial PRIMARY KEY,
    URL text,
    Author int REFERENCES User(UserID)
);
CREATE TABLE IF NOT EXISTS Comment (
    CommentID serial PRIMARY KEY,
    Owner int REFERENCES User(UserID),
    PostID int REFERENCES Post(PostID),
    Content text,
    Timestamp timestamp
);
CREATE TABLE IF NOT EXISTS Poll (
    PollID serial PRIMARY KEY,
    PostID int REFERENCES Post(PostID),
    VotesFor int,
    VotesAgainst int
);
CREATE TABLE IF NOT EXISTS Vote (
    VoteID serial PRIMARY KEY,
    Owner int REFERENCES User(UserID),
    PollID int REFERENCES Poll(PollID),
    VoteFor boolean,
    Timestamp timestamp without time zone
);

INSERT INTO User (Username, Email, FirstName, LastName, Password) VALUES
('john_doe', 'john.doe@example.com', 'John', 'Doe', 'hashedpassword1'),
('jane_smith', 'jane.smith@example.com', 'Jane', 'Smith', 'hashedpassword2');

INSERT INTO FriendRelationship (user1, user2) VALUES
(1, 2);

INSERT INTO Post (Owner, Title, ImageID, TextContent, Timestamp) VALUES
(1, 'First Post', NULL, 'This is the content of the first post.', CURRENT_TIMESTAMP),
(2, 'Second Post', NULL, 'Content of the second post here.', CURRENT_TIMESTAMP);

INSERT INTO Image (URL, Author) VALUES
('http://example.com/image1.jpg', 1),
('http://example.com/image2.jpg', 2);


INSERT INTO Comment (Owner, PostID, Content, Timestamp) VALUES
(2, 1, 'Nice post!', CURRENT_TIMESTAMP),
(1, 2, 'Thank you!', CURRENT_TIMESTAMP);


INSERT INTO Poll (PostID, VotesFor, VotesAgainst) VALUES
(1, 1, 1);


INSERT INTO Vote (Owner, PollID, VoteFor, Timestamp) VALUES
(1, 1, TRUE, CURRENT_TIMESTAMP),
(2, 1, FALSE, CURRENT_TIMESTAMP);
