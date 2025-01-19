CREATE TABLE source.icity_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
	PRIMARY KEY (model_nm, model_feature)
);
CREATE TABLE source.appler_price 
(
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	unit_nm VARCHAR(64) DEFAULT 'Руб.',
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
