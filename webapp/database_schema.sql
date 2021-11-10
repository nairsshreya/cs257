CREATE TABLE parks{
park_code text,
park_name text,
state_code integer,
acreage text,
longitude text,
latitude text
};



CREATE TABLE species{
id serial,
park_code text,
category_id integer,
order_id integer,
family_id integer,
scientific_name text,
common_names text,
nativeness text
};

CREATE TABLE categories{
id serial,
category text
};

CREATE TABLE orders{
id serial
order text
};

CREATE TABLE families{
id serial,
family text
};