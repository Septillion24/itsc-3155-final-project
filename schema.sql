CREATE TABLE IF NOT EXISTS Users (
    UserID PRIMARY KEY,
    Username varchar(255),
    Email varchar(255),
    FirstName varchar(255),
    LastName varchar(255)
);
CREATE TABLE IF NOT EXISTS FriendRelationship (
    id serial PRIMARY KEY,
    user1 int REFERENCES Users(UserID),
    user2 int REFERENCES Users(UserID)
);
CREATE TABLE IF NOT EXISTS Post (
    PostID serial PRIMARY KEY,
    Owner int REFERENCES Users(UserID),
    Title varchar(255),
    ImageURL varchar(255),
    TextContent text,
    Timestamp timestamp without time zone
);

CREATE TABLE IF NOT EXISTS Comment (
    CommentID serial PRIMARY KEY,
    Owner int REFERENCES Users(UserID),
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
    Owner int REFERENCES Users(UserID),
    PollID int REFERENCES Poll(PollID),
    VoteFor boolean,
    Timestamp timestamp without time zone
);

