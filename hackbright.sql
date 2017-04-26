--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: grades; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE grades (
    student_github character varying(30),
    project_title character varying(30),
    grade integer
);


ALTER TABLE grades OWNER TO "user";

--
-- Name: projects; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE projects (
    id integer NOT NULL,
    title character varying(30),
    description text,
    max_grade integer
);


ALTER TABLE projects OWNER TO "user";

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_id_seq OWNER TO "user";

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE projects_id_seq OWNED BY projects.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE students (
    first_name character varying(30),
    last_name character varying(30),
    github character varying(30)
);


ALTER TABLE students OWNER TO "user";

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY projects ALTER COLUMN id SET DEFAULT nextval('projects_id_seq'::regclass);


--
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: user
--

COPY grades (student_github, project_title, grade) FROM stdin;
jhacks	Markov	10
jhacks	Blockly	2
sdevelops	Markov	50
sdevelops	Blockly	100
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: user
--

COPY projects (id, title, description, max_grade) FROM stdin;
1	Markov	Tweets generated from Markov chains	50
2	Blockly	Programmatic Logic Puzzle Game	10
\.


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('projects_id_seq', 2, true);


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: user
--

COPY students (first_name, last_name, github) FROM stdin;
Jane	Hacker	jhacks
Sarah	Developer	sdevelops
Hackbright	Student	hackb
Lady	McPerson	ladyperson
\.


--
-- Name: projects_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

