CREATE TABLE parks
(
    park_code  text,
    park_name  text,
    state_code text,
    acreage    text,
    longitude  text,
    latitude   text
);



CREATE TABLE species
(
    id              text,
    park_code       text,
    category_id     integer,
    order_id        integer,
    family_id       integer,
    scientific_name text,
    common_names    text,
    nativeness      text
);

CREATE TABLE categories
(
    id       integer,
    category text
);

CREATE TABLE orders
(
    id integer,
    order_name text
);

CREATE TABLE families
(
    id     integer,
    family text
);