--
-- PostgreSQL database dump
--


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: coronavirus; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE coronavirus WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE coronavirus OWNER TO postgres;

\connect coronavirus

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: covid19; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA covid19;


ALTER SCHEMA covid19 OWNER TO postgres;

SET default_tablespace = '';

--
-- Name: covid19pa; Type: TABLE; Schema: covid19; Owner: postgres
-- Note: Table for all daily updates from PA DoH
--

CREATE TABLE covid19.covid19pa (
    date date NOT NULL,
    confirmed integer NOT NULL,
    deaths integer NOT NULL,
    new_cases integer,
    growth_ratio real,
    estimated_day real,
    off_by real,
    pct_error real
);


ALTER TABLE covid19.covid19pa OWNER TO postgres;

--
-- Name: covid19us; Type: TABLE; Schema: covid19; Owner: postgres
-- Source: https://github.com/nytimes/covid-19-data
-- Note: Use the `update.sql` script to load this data as it's updated
--

CREATE TABLE covid19.covid19us (
    date date,
    county text,
    state text,
    fips integer,
    cases integer,
    deaths integer
);


ALTER TABLE covid19.covid19us OWNER TO postgres;

--
-- Name: id_seq; Type: SEQUENCE; Schema: covid19; Owner: postgres
--

CREATE SEQUENCE covid19.id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE covid19.id_seq OWNER TO postgres;

--
-- Name: pa_events; Type: TABLE; Schema: covid19; Owner: postgres
-- Note: Table for daily events, used by Grafana annotations and others
--

CREATE TABLE covid19.pa_events (
    id bigint DEFAULT nextval('covid19.id_seq'::regclass) NOT NULL,
    "time" timestamp with time zone,
    timeend timestamp with time zone,
    text text,
    tags text
);


ALTER TABLE covid19.pa_events OWNER TO postgres;

--
-- Name: pa_events pa_events_pkey; Type: CONSTRAINT; Schema: covid19; Owner: postgres
--

ALTER TABLE ONLY covid19.pa_events
    ADD CONSTRAINT pa_events_pkey PRIMARY KEY (id);


--
-- Name: covid19pa unique_date; Type: CONSTRAINT; Schema: covid19; Owner: postgres
--

ALTER TABLE ONLY covid19.covid19pa
    ADD CONSTRAINT unique_date UNIQUE (date);


--
-- Name: idx_date; Type: INDEX; Schema: covid19; Owner: postgres
--

CREATE INDEX idx_date ON covid19.covid19pa USING btree (date) INCLUDE (date);


--
-- Name: SCHEMA covid19; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA covid19 TO postgres;
GRANT USAGE ON SCHEMA covid19 TO grafana;


--
-- Name: TABLE covid19pa; Type: ACL; Schema: covid19; Owner: postgres
--

GRANT ALL ON TABLE covid19.covid19pa TO postgres;
GRANT SELECT ON TABLE covid19.covid19pa TO grafana;


--
-- Name: TABLE covid19us; Type: ACL; Schema: covid19; Owner: postgres
--

GRANT SELECT ON TABLE covid19.covid19us TO grafana;


--
-- Name: TABLE pa_events; Type: ACL; Schema: covid19; Owner: postgres
--

GRANT ALL ON TABLE covid19.pa_events TO postgres;
GRANT SELECT ON TABLE covid19.pa_events TO grafana;


--
-- PostgreSQL database dump complete
--

