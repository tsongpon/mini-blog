from yoyo import step

create_table = """create table card
(
    id varchar(36) not null
    primary key,
    name varchar(255) not null,
    status varchar(15) null,
    content text null,
    category varchar(15) null,
    author varchar(30) not null,
    createdtime timestamp not null,
    modifiedtime timestamp not null
)
"""

rollback = "drop table card"

step(create_table, rollback)
