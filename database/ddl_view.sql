-- View: source.dm_delta_price
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

