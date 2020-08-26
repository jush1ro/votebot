create table POLLS
(
    POLL_ID int not null,
    POLL_TYPE varchar,
	CHAT_ID int,
	SUBJECT_USER_ID int,
	OBJECT_USER_ID int,
	DATETIME timestamp,
    unique (POLL_ID, CHAT_ID, SUBJECT_USER_ID, OBJECT_USER_ID)
);

