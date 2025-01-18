CREATE TABLE raw_data_layer.product 
(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	model_nm VARCHAR(256) NOT NULL,
	model_feature VARCHAR(256) NOT NULL,
	price INT,
	price_unit_nm VARCHAR(64) DEFAULT 'тыс.р'
)