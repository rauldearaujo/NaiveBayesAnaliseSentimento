create database analisetweets;

create table tweets (id bigint primary key, tokens text, original text, classe text);
alter table tweets add column emojis text;