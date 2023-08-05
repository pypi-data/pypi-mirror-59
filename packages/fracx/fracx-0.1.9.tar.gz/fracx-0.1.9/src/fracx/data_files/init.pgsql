create extension if not exists postgis;
create table if not exists {TABLE_NAME}
(
	id serial not null,
	api14 varchar(14) not null,
	api10 varchar(10),
	wellname varchar,
	operator varchar,
	frac_start_date date not null,
	frac_end_date date not null,
	status varchar(25),
	tvd integer,
	target_formation varchar(50),
	shllat double precision not null,
	shllon double precision not null,
	bhllat double precision,
	bhllon double precision,
	created_at timestamp with time zone default CURRENT_TIMESTAMP not null,
	updated_at timestamp with time zone default CURRENT_TIMESTAMP not null,
	updated_by varchar default CURRENT_USER not null,
	shl geometry(Point,4326),
	bhl geometry(Point,4326),
	stick geometry(LineString,4326),
	shl_webmercator geometry(Point,3857),
	bhl_webmercator geometry(Point,3857),
	stick_webmercator geometry(LineString,3857),
	constraint {TABLE_NAME}_pkey
		primary key (api14, frac_start_date, frac_end_date)
);

create index if not exists {TABLE_NAME}_api10_index
	on {TABLE_NAME} (api10);

create view {TABLE_NAME}_most_recent_by_api14 as
with most_recent as (
    select
        max({TABLE_NAME}_1.id) as id
    from {TABLE_NAME} {TABLE_NAME}_1
    group by {TABLE_NAME}_1.api14
)
select
    fs.id,
    fs.api14,
    fs.api10,
    fs.operator,
    fs.wellname,
    fs.tvd,
    fs.frac_start_date,
    fs.frac_end_date,
    fs.shllat,
    fs.shllon,
    fs.bhllat,
    fs.bhllon,
    fs.created_at,
    fs.updated_at,
    fs.updated_by,
    fs.shl,
    fs.bhl,
    fs.stick,
    fs.shl_webmercator,
    fs.bhl_webmercator,
    fs.stick_webmercator
from {TABLE_NAME} fs
         join most_recent on fs.id = most_recent.id;



