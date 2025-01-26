create table stg.delta_price
(
	model_name text not null,
	model_feature text not null,
	appler_price int,
	icity_price int,
	delta int GENERATED ALWAYS AS (appler_price - icity_price) stored,
	primary key (model_name, model_feature)
)