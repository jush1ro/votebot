create table if not exists POLLS
(
    POLL_ID         int unique not null,
    POLL_TYPE       varchar,
    CHAT_ID         int,
    SUBJECT_USER_ID int,
    OBJECT_USER_ID  int,
    DATETIME        timestamp
);

