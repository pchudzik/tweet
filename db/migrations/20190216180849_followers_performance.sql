-- migrate:up
alter table followers add column id serial not null;
alter table followers drop constraint followers_pkey;
alter table followers add primary key(id);


-- migrate:down

