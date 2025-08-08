-- ===============================
-- Database Schema for CVE Project
-- ===============================

CREATE TABLE vendor (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    vendor_id INTEGER NOT NULL REFERENCES vendor(id) ON DELETE CASCADE,
    CONSTRAINT product_name_vendor_id_key UNIQUE (name, vendor_id)
);

CREATE TABLE cwe (
    id SERIAL PRIMARY KEY,
    cwe_id TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE cve (
    cve_id TEXT PRIMARY KEY,
    source_identifier TEXT,
    published TIMESTAMP,
    last_modified TIMESTAMP,
    description TEXT,
    vuln_status TEXT,
    cve_tags TEXT[]
);

CREATE TABLE cve_description (
    id SERIAL PRIMARY KEY,
    cve_id TEXT REFERENCES cve(cve_id),
    lang TEXT,
    description TEXT
);

CREATE TABLE reference (
    id SERIAL PRIMARY KEY,
    cve_id TEXT REFERENCES cve(cve_id),
    url TEXT NOT NULL UNIQUE,
    source TEXT,
    tags TEXT[]
);

CREATE TABLE cve_reference (
    id SERIAL PRIMARY KEY,
    cve_id TEXT REFERENCES cve(cve_id),
    reference_id INTEGER REFERENCES reference(id)
);

CREATE TABLE cve_change_history (
    cve_id TEXT,
    event_name TEXT,
    change_id TEXT PRIMARY KEY,
    change_date TIMESTAMP,
    source_identifier TEXT,
    action TEXT,
    type TEXT,
    old_value TEXT,
    new_value TEXT
);

CREATE TABLE cvss (
    cve_id TEXT NOT NULL REFERENCES cve(cve_id),
    version TEXT NOT NULL,
    base_score NUMERIC,
    base_severity TEXT,
    vector_string TEXT,
    exploitability_score DOUBLE PRECISION,
    impact_score DOUBLE PRECISION,
    attack_vector TEXT,
    attack_complexity TEXT,
    privileges_required TEXT,
    user_interaction TEXT,
    scope TEXT,
    confidentiality_impact TEXT,
    integrity_impact TEXT,
    availability_impact TEXT,
    access_vector TEXT,
    access_complexity TEXT,
    authentication TEXT,
    PRIMARY KEY (cve_id, version)
);

CREATE TABLE cpe_match (
    id SERIAL PRIMARY KEY,
    criteria TEXT,
    match_criteria_id TEXT,
    vulnerable BOOLEAN,
    vendor TEXT,
    product TEXT,
    version TEXT
);

CREATE TABLE cve_cpe_match (
    id SERIAL PRIMARY KEY,
    cve_id TEXT REFERENCES cve(cve_id),
    cpe_match_id INTEGER REFERENCES cpe_match(id)
);

CREATE TABLE cve_cwe (
    cve_id TEXT NOT NULL REFERENCES cve(cve_id) ON DELETE CASCADE,
    cwe_id TEXT NOT NULL REFERENCES cwe(cwe_id) ON DELETE CASCADE,
    source TEXT,
    PRIMARY KEY (cve_id, cwe_id)
);

CREATE TABLE cve_product (
    cve_id TEXT NOT NULL REFERENCES cve(cve_id),
    vendor_id INTEGER NOT NULL REFERENCES vendor(id),
    product_id INTEGER NOT NULL REFERENCES product(id),
    PRIMARY KEY (cve_id, vendor_id, product_id)
);

CREATE TABLE cve_weakness (
    id SERIAL PRIMARY KEY,
    cve_id TEXT REFERENCES cve(cve_id),
    source TEXT,
    type TEXT,
    cwe_id TEXT,
    description TEXT
);

