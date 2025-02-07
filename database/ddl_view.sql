-- View: source.dm_delta_price
DROP VIEW source.dm_delta_price;
CREATE OR REPLACE VIEW source.dm_delta_price
 AS
 SELECT ap.id AS appler_id,
    ap.model_name,
    ap.model_feature,
    ap.price AS appler_price,
    ip.price AS icity_price,
    ap.price - ip.price AS delta,
    ap.time_updated
   FROM source.appler_price ap
     JOIN source.icity_price ip ON lower(source.clear(ip.model_name::text)) = lower(source.clear(ap.model_name::text)) AND lower(source.clear(ip.model_feature::text)) = lower(source.clear(ap.model_feature::text));

ALTER TABLE source.dm_delta_price
    OWNER TO postgres;


-- View: source.missing_join
DROP VIEW source.missing_join;
CREATE OR REPLACE VIEW source.missing_join
 AS
 SELECT ap.id AS appler_id,
    ap.model_name,
    ap.model_feature,
    ap.price AS appler_price,
    ap.processed_dttm,
    ap.time_updated
   FROM source.appler_price ap
     LEFT JOIN source.icity_price ip ON lower(source.clear(ip.model_name::text)) = lower(source.clear(ap.model_name::text)) AND lower(source.clear(ip.model_feature::text)) = lower(source.clear(ap.model_feature::text))
  WHERE ip.id IS NULL;

ALTER TABLE source.missing_join
    OWNER TO postgres;

-- View: stg.dm_delta_price
DROP VIEW stg.dm_delta_price;
CREATE OR REPLACE VIEW stg.dm_delta_price
 AS
 SELECT appler_id,
    model_name,
    model_feature,
    COALESCE(icity_price +
        CASE
            WHEN COALESCE(delta, 0) >= 0 AND icity_price >= 11000 THEN '-1000'::integer
            WHEN COALESCE(delta, 0) >= 0 THEN 0
            ELSE COALESCE(delta, 0)
        END, appler_price) AS appler_price,
    icity_price,
        CASE
            WHEN COALESCE(delta, 0) >= 0 AND icity_price >= 11000 THEN '-1000'::integer
            WHEN COALESCE(delta, 0) >= 0 THEN 0
            ELSE COALESCE(delta, 0)
        END AS delta,
    date_trunc('seconds'::text, now())::timestamp without time zone AS processed_dttm,
    time_updated
   FROM source.dm_delta_price;

ALTER TABLE stg.dm_delta_price
    OWNER TO postgres;

-- View: dm.delta_price
DROP VIEW dm.delta_price;
CREATE OR REPLACE VIEW dm.delta_price
 AS
 SELECT dp.appler_id,
    dp.model_name,
    dp.model_feature,
    COALESCE(dp.icity_price + COALESCE(cd.custom_delta, dp.delta, 0), dp.appler_price) AS appler_price,
    dp.icity_price,
    COALESCE(cd.custom_delta, dp.delta, 0) AS delta,
    date_trunc('second'::text, now())::timestamp without time zone AS processed_dttm,
    dp.time_updated
   FROM stg.dm_delta_price dp
     LEFT JOIN stg.custom_delta cd ON dp.appler_id = cd.id OR lower(source.clear(dp.model_name::text)) = lower(source.clear(cd.model_name::text)) AND lower(source.clear(dp.model_feature::text)) = lower(source.clear(cd.model_feature::text));

ALTER TABLE dm.delta_price
    OWNER TO postgres;


-- View: dm.message_compile
DROP VIEW dm.message_compile;
CREATE OR REPLACE VIEW dm.message_compile
 AS
 SELECT model_name,
    string_agg(model_feature::text, ';'::text) AS model_features,
    string_agg(appler_price::text, ';'::text) AS prices
   FROM dm.delta_price
  GROUP BY model_name;

ALTER TABLE dm.message_compile
    OWNER TO postgres;