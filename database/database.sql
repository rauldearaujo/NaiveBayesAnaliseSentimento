create database analisetweets;

create table tweets (id bigint primary key, tokens text, original text, classe text);
alter table tweets add column emojis text;
alter table tweets add column data bigint;

create table tweetsClassificados (id bigint primary key, classe text);

#Exemplo de conversão de data para milisegundos
SELECT EXTRACT(EPOCH FROM TIMESTAMP '2011-05-17') * 1000;

delete from tweets where classe != 'positive' and classe != 'negative' and classe != 'NoEmoji'