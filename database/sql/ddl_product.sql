CREATE TABLE raw_data_layer.icity_product 
(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	price_unit_nm VARCHAR(64) DEFAULT 'Руб.',
	time_upadated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE raw_data_layer.appler_product 
(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	price_unit_nm VARCHAR(64) DEFAULT 'Руб.',
	time_upadated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE OR REPLACE VIEW AS 
(
	SELECT 
		a.id,
		a.model_nm,
		a.model_feature,
		a.price - i.price AS delta,
		a.price_unit_nm,
		now() AS time_updated
	FROM raw_data_layer.appler_product a
	INNER JOIN raw_data_layer.icity_product i ON 1 = 1 
		AND a.model_nm::text = i.model_nm::text 
		AND a.model_feature::text = i.model_feature::text
);
