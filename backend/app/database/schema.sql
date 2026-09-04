--
-- PostgreSQL database dump
--

\restrict il85irthc0pOAb0e18qjutsYCz6FIPgicKq6gVcOAj0XHJoarUmhj8hjhh4RwVk

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_events (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    event_data text,
    event_timestamp timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: activity_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.activity_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: activity_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.activity_events_id_seq OWNED BY public.activity_events.id;


--
-- Name: alerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alerts (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    alert_type character varying(50) NOT NULL,
    message text NOT NULL,
    severity character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    resolved_at timestamp with time zone
);


--
-- Name: alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.alerts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;


--
-- Name: caregivers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.caregivers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    phone character varying(20),
    relationship_to_patient character varying(50)
);


--
-- Name: caregivers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.caregivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: caregivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.caregivers_id_seq OWNED BY public.caregivers.id;


--
-- Name: device_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.device_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token character varying(500) NOT NULL,
    platform character varying(20) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: device_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.device_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: device_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.device_tokens_id_seq OWNED BY public.device_tokens.id;


--
-- Name: emergency_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emergency_events (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    trigger character varying(50) NOT NULL,
    latitude double precision,
    longitude double precision,
    "timestamp" timestamp with time zone NOT NULL,
    status character varying(30) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: emergency_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.emergency_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: emergency_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.emergency_events_id_seq OWNED BY public.emergency_events.id;


--
-- Name: family_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.family_members (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    name character varying(100) NOT NULL,
    relationship character varying(50) NOT NULL,
    phone character varying(20),
    photo_url character varying(500),
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    is_caregiver boolean DEFAULT false NOT NULL,
    user_id integer
);


--
-- Name: family_members_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.family_members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: family_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.family_members_id_seq OWNED BY public.family_members.id;


--
-- Name: game_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_results (
    id integer NOT NULL,
    session_id character varying(100) NOT NULL,
    patient_id integer NOT NULL,
    game_id character varying(20) NOT NULL,
    score double precision NOT NULL,
    accuracy double precision NOT NULL,
    mistakes integer NOT NULL,
    duration_seconds integer NOT NULL,
    attempts integer NOT NULL,
    hints_used integer NOT NULL,
    response_time double precision,
    difficulty character varying(20) NOT NULL,
    completed_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: game_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.game_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: game_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.game_results_id_seq OWNED BY public.game_results.id;


--
-- Name: game_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_sessions (
    id integer NOT NULL,
    session_id character varying(100) NOT NULL,
    patient_id integer NOT NULL,
    game_id character varying(20) NOT NULL,
    difficulty character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    started_at timestamp with time zone NOT NULL,
    completed_at timestamp with time zone
);


--
-- Name: game_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.game_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: game_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.game_sessions_id_seq OWNED BY public.game_sessions.id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.games (
    id integer NOT NULL,
    game_id character varying(20) NOT NULL,
    name character varying(100) NOT NULL,
    game_type character varying(50) NOT NULL,
    difficulty character varying(20) NOT NULL,
    description text,
    offline_supported boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    accuracy_meters double precision,
    "timestamp" timestamp with time zone NOT NULL
);


--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: medicines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medicines (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    name character varying(150) NOT NULL,
    dosage character varying(100),
    instructions text,
    start_date date,
    end_date date,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: medicines_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.medicines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: medicines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.medicines_id_seq OWNED BY public.medicines.id;


--
-- Name: memories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memories (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    title character varying(200) NOT NULL,
    story_text text,
    summary text,
    cover_photo_url character varying(500),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    memory_type character varying(50) DEFAULT 'general'::character varying NOT NULL,
    tags text,
    people text,
    event_date date,
    location character varying(200),
    audio_url character varying(500),
    is_private boolean DEFAULT false NOT NULL,
    is_approved boolean DEFAULT false NOT NULL
);


--
-- Name: memories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.memories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.memories_id_seq OWNED BY public.memories.id;


--
-- Name: memory_elements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memory_elements (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    element_type character varying(20) NOT NULL,
    label character varying(200) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: memory_elements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.memory_elements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memory_elements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.memory_elements_id_seq OWNED BY public.memory_elements.id;


--
-- Name: memory_media; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memory_media (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    media_type character varying(20) NOT NULL,
    media_url character varying(500) NOT NULL,
    caption character varying(300),
    created_at timestamp with time zone NOT NULL
);


--
-- Name: memory_media_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.memory_media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memory_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.memory_media_id_seq OWNED BY public.memory_media.id;


--
-- Name: memory_relationships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memory_relationships (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    source_element_id integer NOT NULL,
    target_element_id integer NOT NULL,
    relationship_type character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: memory_relationships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.memory_relationships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memory_relationships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.memory_relationships_id_seq OWNED BY public.memory_relationships.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    patient_id integer,
    notification_type character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    message text NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    read_at timestamp with time zone
);


--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: patient_caregivers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patient_caregivers (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    caregiver_id integer NOT NULL
);


--
-- Name: patient_caregivers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patient_caregivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: patient_caregivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patient_caregivers_id_seq OWNED BY public.patient_caregivers.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date_of_birth date,
    language character varying(10) NOT NULL,
    address character varying(500),
    emergency_contact character varying(20)
);


--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: reminder_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reminder_history (
    id integer NOT NULL,
    reminder_id integer NOT NULL,
    patient_id integer NOT NULL,
    scheduled_at timestamp with time zone NOT NULL,
    completed_at timestamp with time zone,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: reminder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reminder_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reminder_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reminder_history_id_seq OWNED BY public.reminder_history.id;


--
-- Name: reminders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reminders (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    medicine_id integer,
    reminder_type character varying(30) NOT NULL,
    reminder_text character varying(500) NOT NULL,
    scheduled_time time without time zone NOT NULL,
    repeat_pattern character varying(30) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    voice_recording_id integer
);


--
-- Name: reminders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reminders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reminders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reminders_id_seq OWNED BY public.reminders.id;


--
-- Name: safe_zones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.safe_zones (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    name character varying(100) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    radius_meters double precision NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: safe_zones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.safe_zones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: safe_zones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.safe_zones_id_seq OWNED BY public.safe_zones.id;


--
-- Name: sync_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sync_events (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    device_id character varying(100) NOT NULL,
    event_id character varying(100) NOT NULL,
    event_type character varying(50) NOT NULL,
    event_data text,
    event_timestamp timestamp with time zone NOT NULL,
    synced_at timestamp with time zone NOT NULL
);


--
-- Name: sync_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sync_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sync_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sync_events_id_seq OWNED BY public.sync_events.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: voice_recordings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.voice_recordings (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    memory_id integer,
    audio_url character varying(500) NOT NULL,
    language character varying(10) NOT NULL,
    recording_type character varying(30) NOT NULL,
    duration_seconds integer,
    created_at timestamp with time zone NOT NULL,
    family_member_id integer
);


--
-- Name: voice_recordings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.voice_recordings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: voice_recordings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.voice_recordings_id_seq OWNED BY public.voice_recordings.id;


--
-- Name: activity_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_events ALTER COLUMN id SET DEFAULT nextval('public.activity_events_id_seq'::regclass);


--
-- Name: alerts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);


--
-- Name: caregivers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caregivers ALTER COLUMN id SET DEFAULT nextval('public.caregivers_id_seq'::regclass);


--
-- Name: device_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.device_tokens ALTER COLUMN id SET DEFAULT nextval('public.device_tokens_id_seq'::regclass);


--
-- Name: emergency_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_events ALTER COLUMN id SET DEFAULT nextval('public.emergency_events_id_seq'::regclass);


--
-- Name: family_members id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.family_members ALTER COLUMN id SET DEFAULT nextval('public.family_members_id_seq'::regclass);


--
-- Name: game_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_results ALTER COLUMN id SET DEFAULT nextval('public.game_results_id_seq'::regclass);


--
-- Name: game_sessions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_sessions ALTER COLUMN id SET DEFAULT nextval('public.game_sessions_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: medicines id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicines ALTER COLUMN id SET DEFAULT nextval('public.medicines_id_seq'::regclass);


--
-- Name: memories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memories ALTER COLUMN id SET DEFAULT nextval('public.memories_id_seq'::regclass);


--
-- Name: memory_elements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_elements ALTER COLUMN id SET DEFAULT nextval('public.memory_elements_id_seq'::regclass);


--
-- Name: memory_media id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_media ALTER COLUMN id SET DEFAULT nextval('public.memory_media_id_seq'::regclass);


--
-- Name: memory_relationships id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_relationships ALTER COLUMN id SET DEFAULT nextval('public.memory_relationships_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: patient_caregivers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient_caregivers ALTER COLUMN id SET DEFAULT nextval('public.patient_caregivers_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: reminder_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminder_history ALTER COLUMN id SET DEFAULT nextval('public.reminder_history_id_seq'::regclass);


--
-- Name: reminders id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminders ALTER COLUMN id SET DEFAULT nextval('public.reminders_id_seq'::regclass);


--
-- Name: safe_zones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.safe_zones ALTER COLUMN id SET DEFAULT nextval('public.safe_zones_id_seq'::regclass);


--
-- Name: sync_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sync_events ALTER COLUMN id SET DEFAULT nextval('public.sync_events_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: voice_recordings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voice_recordings ALTER COLUMN id SET DEFAULT nextval('public.voice_recordings_id_seq'::regclass);


--
-- Name: activity_events activity_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_events
    ADD CONSTRAINT activity_events_pkey PRIMARY KEY (id);


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: caregivers caregivers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_pkey PRIMARY KEY (id);


--
-- Name: caregivers caregivers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_user_id_key UNIQUE (user_id);


--
-- Name: device_tokens device_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_pkey PRIMARY KEY (id);


--
-- Name: device_tokens device_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_token_key UNIQUE (token);


--
-- Name: emergency_events emergency_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_events
    ADD CONSTRAINT emergency_events_pkey PRIMARY KEY (id);


--
-- Name: family_members family_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_pkey PRIMARY KEY (id);


--
-- Name: family_members family_members_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_user_id_key UNIQUE (user_id);


--
-- Name: game_results game_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_pkey PRIMARY KEY (id);


--
-- Name: game_sessions game_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: medicines medicines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_pkey PRIMARY KEY (id);


--
-- Name: memories memories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_pkey PRIMARY KEY (id);


--
-- Name: memory_elements memory_elements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_elements
    ADD CONSTRAINT memory_elements_pkey PRIMARY KEY (id);


--
-- Name: memory_media memory_media_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_media
    ADD CONSTRAINT memory_media_pkey PRIMARY KEY (id);


--
-- Name: memory_relationships memory_relationships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: patient_caregivers patient_caregivers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: patients patients_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_user_id_key UNIQUE (user_id);


--
-- Name: reminder_history reminder_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_pkey PRIMARY KEY (id);


--
-- Name: reminders reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_pkey PRIMARY KEY (id);


--
-- Name: safe_zones safe_zones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.safe_zones
    ADD CONSTRAINT safe_zones_pkey PRIMARY KEY (id);


--
-- Name: sync_events sync_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sync_events
    ADD CONSTRAINT sync_events_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: voice_recordings voice_recordings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_pkey PRIMARY KEY (id);


--
-- Name: ix_activity_events_event_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_events_event_type ON public.activity_events USING btree (event_type);


--
-- Name: ix_activity_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_events_id ON public.activity_events USING btree (id);


--
-- Name: ix_activity_events_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_events_patient_id ON public.activity_events USING btree (patient_id);


--
-- Name: ix_alerts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alerts_id ON public.alerts USING btree (id);


--
-- Name: ix_alerts_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alerts_patient_id ON public.alerts USING btree (patient_id);


--
-- Name: ix_caregivers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_caregivers_id ON public.caregivers USING btree (id);


--
-- Name: ix_device_tokens_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_device_tokens_user_id ON public.device_tokens USING btree (user_id);


--
-- Name: ix_emergency_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_emergency_events_id ON public.emergency_events USING btree (id);


--
-- Name: ix_emergency_events_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_emergency_events_patient_id ON public.emergency_events USING btree (patient_id);


--
-- Name: ix_family_members_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_family_members_id ON public.family_members USING btree (id);


--
-- Name: ix_family_members_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_family_members_patient_id ON public.family_members USING btree (patient_id);


--
-- Name: ix_game_results_game_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_results_game_id ON public.game_results USING btree (game_id);


--
-- Name: ix_game_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_results_id ON public.game_results USING btree (id);


--
-- Name: ix_game_results_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_results_patient_id ON public.game_results USING btree (patient_id);


--
-- Name: ix_game_results_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_results_session_id ON public.game_results USING btree (session_id);


--
-- Name: ix_game_sessions_game_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_sessions_game_id ON public.game_sessions USING btree (game_id);


--
-- Name: ix_game_sessions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_sessions_id ON public.game_sessions USING btree (id);


--
-- Name: ix_game_sessions_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_game_sessions_patient_id ON public.game_sessions USING btree (patient_id);


--
-- Name: ix_game_sessions_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_game_sessions_session_id ON public.game_sessions USING btree (session_id);


--
-- Name: ix_games_game_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_games_game_id ON public.games USING btree (game_id);


--
-- Name: ix_games_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_games_id ON public.games USING btree (id);


--
-- Name: ix_locations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_locations_id ON public.locations USING btree (id);


--
-- Name: ix_locations_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_locations_patient_id ON public.locations USING btree (patient_id);


--
-- Name: ix_medicines_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_medicines_id ON public.medicines USING btree (id);


--
-- Name: ix_medicines_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_medicines_patient_id ON public.medicines USING btree (patient_id);


--
-- Name: ix_memories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memories_id ON public.memories USING btree (id);


--
-- Name: ix_memories_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memories_patient_id ON public.memories USING btree (patient_id);


--
-- Name: ix_memory_elements_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_elements_id ON public.memory_elements USING btree (id);


--
-- Name: ix_memory_elements_memory_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_elements_memory_id ON public.memory_elements USING btree (memory_id);


--
-- Name: ix_memory_media_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_media_id ON public.memory_media USING btree (id);


--
-- Name: ix_memory_media_memory_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_media_memory_id ON public.memory_media USING btree (memory_id);


--
-- Name: ix_memory_relationships_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_relationships_id ON public.memory_relationships USING btree (id);


--
-- Name: ix_memory_relationships_memory_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_memory_relationships_memory_id ON public.memory_relationships USING btree (memory_id);


--
-- Name: ix_notifications_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_patient_id ON public.notifications USING btree (patient_id);


--
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: ix_patient_caregivers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_patient_caregivers_id ON public.patient_caregivers USING btree (id);


--
-- Name: ix_patients_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_patients_id ON public.patients USING btree (id);


--
-- Name: ix_reminder_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminder_history_id ON public.reminder_history USING btree (id);


--
-- Name: ix_reminder_history_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminder_history_patient_id ON public.reminder_history USING btree (patient_id);


--
-- Name: ix_reminder_history_reminder_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminder_history_reminder_id ON public.reminder_history USING btree (reminder_id);


--
-- Name: ix_reminders_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminders_id ON public.reminders USING btree (id);


--
-- Name: ix_reminders_medicine_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminders_medicine_id ON public.reminders USING btree (medicine_id);


--
-- Name: ix_reminders_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminders_patient_id ON public.reminders USING btree (patient_id);


--
-- Name: ix_reminders_voice_recording_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reminders_voice_recording_id ON public.reminders USING btree (voice_recording_id);


--
-- Name: ix_safe_zones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_safe_zones_id ON public.safe_zones USING btree (id);


--
-- Name: ix_safe_zones_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_safe_zones_patient_id ON public.safe_zones USING btree (patient_id);


--
-- Name: ix_sync_events_event_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_events_event_id ON public.sync_events USING btree (event_id);


--
-- Name: ix_sync_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_events_id ON public.sync_events USING btree (id);


--
-- Name: ix_sync_events_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_events_patient_id ON public.sync_events USING btree (patient_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_voice_recordings_family_member_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_voice_recordings_family_member_id ON public.voice_recordings USING btree (family_member_id);


--
-- Name: ix_voice_recordings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_voice_recordings_id ON public.voice_recordings USING btree (id);


--
-- Name: ix_voice_recordings_memory_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_voice_recordings_memory_id ON public.voice_recordings USING btree (memory_id);


--
-- Name: ix_voice_recordings_patient_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_voice_recordings_patient_id ON public.voice_recordings USING btree (patient_id);


--
-- Name: activity_events activity_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_events
    ADD CONSTRAINT activity_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: alerts alerts_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: caregivers caregivers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: device_tokens device_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: emergency_events emergency_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emergency_events
    ADD CONSTRAINT emergency_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: family_members family_members_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: family_members family_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reminders fk_reminders_voice_recording; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT fk_reminders_voice_recording FOREIGN KEY (voice_recording_id) REFERENCES public.voice_recordings(id);


--
-- Name: voice_recordings fk_voice_recordings_family_member; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT fk_voice_recordings_family_member FOREIGN KEY (family_member_id) REFERENCES public.family_members(id);


--
-- Name: game_results game_results_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_results game_results_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: game_results game_results_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.game_sessions(session_id);


--
-- Name: game_sessions game_sessions_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_sessions game_sessions_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: locations locations_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: medicines medicines_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: memories memories_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: memory_elements memory_elements_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_elements
    ADD CONSTRAINT memory_elements_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_media memory_media_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_media
    ADD CONSTRAINT memory_media_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_relationships memory_relationships_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_relationships memory_relationships_source_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_source_element_id_fkey FOREIGN KEY (source_element_id) REFERENCES public.memory_elements(id);


--
-- Name: memory_relationships memory_relationships_target_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_target_element_id_fkey FOREIGN KEY (target_element_id) REFERENCES public.memory_elements(id);


--
-- Name: notifications notifications_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: patient_caregivers patient_caregivers_caregiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_caregiver_id_fkey FOREIGN KEY (caregiver_id) REFERENCES public.caregivers(id);


--
-- Name: patient_caregivers patient_caregivers_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: patients patients_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reminder_history reminder_history_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: reminder_history reminder_history_reminder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_reminder_id_fkey FOREIGN KEY (reminder_id) REFERENCES public.reminders(id);


--
-- Name: reminders reminders_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicines(id);


--
-- Name: reminders reminders_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: safe_zones safe_zones_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.safe_zones
    ADD CONSTRAINT safe_zones_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: sync_events sync_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sync_events
    ADD CONSTRAINT sync_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: voice_recordings voice_recordings_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: voice_recordings voice_recordings_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- PostgreSQL database dump complete
--

\unrestrict il85irthc0pOAb0e18qjutsYCz6FIPgicKq6gVcOAj0XHJoarUmhj8hjhh4RwVk

