-- Table: source.appler_price
DROP TABLE IF EXISTS source.appler_price;
CREATE TABLE IF NOT EXISTS source.appler_price
(
    model_name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    model_feature character varying(256) COLLATE pg_catalog."default" NOT NULL,
    price integer,
    unit_nm character varying(64) COLLATE pg_catalog."default" DEFAULT 'Руб.'::character varying,
    processed_dttm timestamp without time zone NOT NULL DEFAULT date_trunc('second'::text, now()),
    time_updated timestamp without time zone NOT NULL DEFAULT (date_trunc('second'::text, now()))::timestamp without time zone,
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT appler_price_pkey PRIMARY KEY (model_name, model_feature)
);

TABLESPACE pg_default;

ALTER TABLE IF EXISTS source.appler_price
    OWNER to postgres;


-- Table: source.icity_price
DROP TABLE IF EXISTS source.icity_price;
CREATE TABLE IF NOT EXISTS source.icity_price
(
    model_name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    model_feature character varying(256) COLLATE pg_catalog."default" NOT NULL,
    price integer,
    unit_nm character varying(64) COLLATE pg_catalog."default" DEFAULT 'Руб.'::character varying,
    processed_dttm timestamp without time zone NOT NULL DEFAULT date_trunc('second'::text, now()),
    time_updated timestamp without time zone NOT NULL DEFAULT (date_trunc('second'::text, now()))::timestamp without time zone,
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT icity_price_pkey PRIMARY KEY (model_name, model_feature)
);

TABLESPACE pg_default;

ALTER TABLE IF EXISTS source.icity_price
    OWNER to postgres;


-- Table: stg.delta_price
DROP TABLE IF EXISTS stg.delta_price;
CREATE TABLE IF NOT EXISTS stg.delta_price
(
    id integer NOT NULL,
    model_name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    model_feature character varying(256) COLLATE pg_catalog."default" NOT NULL,
    appler_price integer GENERATED ALWAYS AS ((icity_price + COALESCE(delta, 0))) STORED,
    icity_price integer,
    delta integer,
    processed_dttm timestamp without time zone,
    time_updated timestamp without time zone,
    CONSTRAINT appler_price_pkey PRIMARY KEY (id, model_name, model_feature)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS stg.delta_price
    OWNER to postgres;

-- Table: stg.custom_delta
DROP TABLE IF EXISTS stg.custom_delta;
CREATE TABLE IF NOT EXISTS stg.custom_delta
(
    id integer NOT NULL,
    custom_delta integer,
    CONSTRAINT custom_delta_pkey PRIMARY KEY (id)
)