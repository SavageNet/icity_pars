CREATE TABLE source.icity_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
	processed_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	time_updated TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	PRIMARY KEY (model_nm, model_feature)
);
CREATE TABLE source.appler_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
	processed_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	time_updated TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,	
	PRIMARY KEY (model_nm, model_feature)
);
CREATE TABLE stg.icity_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
	processed_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	is_deleted_flg SMALLINT NOT NULL DEFAULT 0,
	effective_from_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	effective_to_dttm TIMESTAMP NOT NULL DEFAULT '5999-12-31'::TIMESTAMP,
	PRIMARY KEY (model_nm, model_feature, effective_from_dttm)
);
CREATE TABLE stg.appler_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
	processed_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	is_deleted_flg SMALLINT NOT NULL DEFAULT 0,
	effective_from_dttm TIMESTAMP NOT NULL DEFAULT DATE_TRUNC('second', NOW())::TIMESTAMP,
	effective_to_dttm TIMESTAMP NOT NULL DEFAULT '5999-12-31'::TIMESTAMP,
	PRIMARY KEY (model_nm, model_feature, effective_from_dttm)
);
CREATE TABLE IF NOT EXISTS dicts.model_to_emoji
(
    clear_model_name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    emoji character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT color_to_emoji_pkey PRIMARY KEY (clear_model_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dicts.model_to_emoji
    OWNER to postgres
;
CREATE TABLE IF NOT EXISTS dicts.feature_to_emoji
(
    clear_feature character varying(256) COLLATE pg_catalog."default" NOT NULL,
    emoji character varying(8) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dicts.feature_to_emoji
    OWNER to postgres
;