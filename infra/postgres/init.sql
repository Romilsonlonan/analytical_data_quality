CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS trusted;
CREATE SCHEMA IF NOT EXISTS refined;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS governance.audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    user_name VARCHAR(100),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS governance.data_quality_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_name VARCHAR(255) NOT NULL,
    check_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    expectations JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON governance.audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_table ON governance.audit_log(table_name);
CREATE INDEX IF NOT EXISTS idx_data_quality_timestamp ON governance.data_quality_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_data_quality_dataset ON governance.data_quality_log(dataset_name);

CREATE OR REPLACE FUNCTION governance.update_audit()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO governance.audit_log (event_type, table_name, old_data, new_data, user_name)
    VALUES (
        TG_OP,
        TG_TABLE_NAME,
        CASE WHEN TG_OP = 'UPDATE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END,
        current_user
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON SCHEMA staging IS 'Raw data in initial transformation stage';
COMMENT ON SCHEMA trusted IS 'Cleaned and validated data';
COMMENT ON SCHEMA refined IS 'Business-level aggregated data';
COMMENT ON SCHEMA governance IS 'Audit, lineage and quality tracking';