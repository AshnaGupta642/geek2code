--
-- PostgreSQL database dump
--

\restrict aRFeEE35KhsxVpqSnomTYJEuzNUPfrGaw1d4kr8h8aL2EbpWKX4mdSiI66pJPXv

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
-- Name: activity_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_events (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    event_data text,
    event_timestamp timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.activity_events OWNER TO postgres;

--
-- Name: activity_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activity_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_events_id_seq OWNER TO postgres;

--
-- Name: activity_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activity_events_id_seq OWNED BY public.activity_events.id;


--
-- Name: alerts; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.alerts OWNER TO postgres;

--
-- Name: alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alerts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.alerts_id_seq OWNER TO postgres;

--
-- Name: alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;


--
-- Name: caregivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.caregivers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    phone character varying(20),
    relationship_to_patient character varying(50)
);


ALTER TABLE public.caregivers OWNER TO postgres;

--
-- Name: caregivers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.caregivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.caregivers_id_seq OWNER TO postgres;

--
-- Name: caregivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.caregivers_id_seq OWNED BY public.caregivers.id;


--
-- Name: device_tokens; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.device_tokens OWNER TO postgres;

--
-- Name: device_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.device_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.device_tokens_id_seq OWNER TO postgres;

--
-- Name: device_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.device_tokens_id_seq OWNED BY public.device_tokens.id;


--
-- Name: emergency_events; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.emergency_events OWNER TO postgres;

--
-- Name: emergency_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emergency_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.emergency_events_id_seq OWNER TO postgres;

--
-- Name: emergency_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emergency_events_id_seq OWNED BY public.emergency_events.id;


--
-- Name: face_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.face_profiles (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    family_member_id integer NOT NULL,
    person_name character varying(100) NOT NULL,
    face_image_url character varying(500),
    embedding_reference character varying(500),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.face_profiles OWNER TO postgres;

--
-- Name: face_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.face_profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.face_profiles_id_seq OWNER TO postgres;

--
-- Name: face_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.face_profiles_id_seq OWNED BY public.face_profiles.id;


--
-- Name: family_members; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.family_members OWNER TO postgres;

--
-- Name: family_members_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.family_members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.family_members_id_seq OWNER TO postgres;

--
-- Name: family_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.family_members_id_seq OWNED BY public.family_members.id;


--
-- Name: game_results; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.game_results OWNER TO postgres;

--
-- Name: game_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_results_id_seq OWNER TO postgres;

--
-- Name: game_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_results_id_seq OWNED BY public.game_results.id;


--
-- Name: game_sessions; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.game_sessions OWNER TO postgres;

--
-- Name: game_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_sessions_id_seq OWNER TO postgres;

--
-- Name: game_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_sessions_id_seq OWNED BY public.game_sessions.id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.games OWNER TO postgres;

--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.games_id_seq OWNER TO postgres;

--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    accuracy_meters double precision,
    "timestamp" timestamp with time zone NOT NULL
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.locations_id_seq OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: medicines; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.medicines OWNER TO postgres;

--
-- Name: medicines_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medicines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medicines_id_seq OWNER TO postgres;

--
-- Name: medicines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medicines_id_seq OWNED BY public.medicines.id;


--
-- Name: memories; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.memories OWNER TO postgres;

--
-- Name: memories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memories_id_seq OWNER TO postgres;

--
-- Name: memories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memories_id_seq OWNED BY public.memories.id;


--
-- Name: memory_elements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memory_elements (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    element_type character varying(20) NOT NULL,
    label character varying(200) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.memory_elements OWNER TO postgres;

--
-- Name: memory_elements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memory_elements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memory_elements_id_seq OWNER TO postgres;

--
-- Name: memory_elements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memory_elements_id_seq OWNED BY public.memory_elements.id;


--
-- Name: memory_media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memory_media (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    media_type character varying(20) NOT NULL,
    media_url character varying(500) NOT NULL,
    caption character varying(300),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.memory_media OWNER TO postgres;

--
-- Name: memory_media_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memory_media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memory_media_id_seq OWNER TO postgres;

--
-- Name: memory_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memory_media_id_seq OWNED BY public.memory_media.id;


--
-- Name: memory_relationships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memory_relationships (
    id integer NOT NULL,
    memory_id integer NOT NULL,
    source_element_id integer NOT NULL,
    target_element_id integer NOT NULL,
    relationship_type character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.memory_relationships OWNER TO postgres;

--
-- Name: memory_relationships_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memory_relationships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memory_relationships_id_seq OWNER TO postgres;

--
-- Name: memory_relationships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memory_relationships_id_seq OWNED BY public.memory_relationships.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: patient_caregivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patient_caregivers (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    caregiver_id integer NOT NULL
);


ALTER TABLE public.patient_caregivers OWNER TO postgres;

--
-- Name: patient_caregivers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patient_caregivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patient_caregivers_id_seq OWNER TO postgres;

--
-- Name: patient_caregivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patient_caregivers_id_seq OWNED BY public.patient_caregivers.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date_of_birth date,
    language character varying(10) NOT NULL,
    address character varying(500),
    emergency_contact character varying(20)
);


ALTER TABLE public.patients OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patients_id_seq OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: reminder_history; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.reminder_history OWNER TO postgres;

--
-- Name: reminder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reminder_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reminder_history_id_seq OWNER TO postgres;

--
-- Name: reminder_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reminder_history_id_seq OWNED BY public.reminder_history.id;


--
-- Name: reminders; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.reminders OWNER TO postgres;

--
-- Name: reminders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reminders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reminders_id_seq OWNER TO postgres;

--
-- Name: reminders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reminders_id_seq OWNED BY public.reminders.id;


--
-- Name: safe_zones; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.safe_zones OWNER TO postgres;

--
-- Name: safe_zones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.safe_zones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.safe_zones_id_seq OWNER TO postgres;

--
-- Name: safe_zones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.safe_zones_id_seq OWNED BY public.safe_zones.id;


--
-- Name: sync_events; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.sync_events OWNER TO postgres;

--
-- Name: sync_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sync_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sync_events_id_seq OWNER TO postgres;

--
-- Name: sync_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sync_events_id_seq OWNED BY public.sync_events.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: voice_recordings; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.voice_recordings OWNER TO postgres;

--
-- Name: voice_recordings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.voice_recordings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.voice_recordings_id_seq OWNER TO postgres;

--
-- Name: voice_recordings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voice_recordings_id_seq OWNED BY public.voice_recordings.id;


--
-- Name: activity_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_events ALTER COLUMN id SET DEFAULT nextval('public.activity_events_id_seq'::regclass);


--
-- Name: alerts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);


--
-- Name: caregivers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregivers ALTER COLUMN id SET DEFAULT nextval('public.caregivers_id_seq'::regclass);


--
-- Name: device_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device_tokens ALTER COLUMN id SET DEFAULT nextval('public.device_tokens_id_seq'::regclass);


--
-- Name: emergency_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_events ALTER COLUMN id SET DEFAULT nextval('public.emergency_events_id_seq'::regclass);


--
-- Name: face_profiles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_profiles ALTER COLUMN id SET DEFAULT nextval('public.face_profiles_id_seq'::regclass);


--
-- Name: family_members id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family_members ALTER COLUMN id SET DEFAULT nextval('public.family_members_id_seq'::regclass);


--
-- Name: game_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_results ALTER COLUMN id SET DEFAULT nextval('public.game_results_id_seq'::regclass);


--
-- Name: game_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_sessions ALTER COLUMN id SET DEFAULT nextval('public.game_sessions_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: medicines id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicines ALTER COLUMN id SET DEFAULT nextval('public.medicines_id_seq'::regclass);


--
-- Name: memories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories ALTER COLUMN id SET DEFAULT nextval('public.memories_id_seq'::regclass);


--
-- Name: memory_elements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_elements ALTER COLUMN id SET DEFAULT nextval('public.memory_elements_id_seq'::regclass);


--
-- Name: memory_media id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_media ALTER COLUMN id SET DEFAULT nextval('public.memory_media_id_seq'::regclass);


--
-- Name: memory_relationships id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_relationships ALTER COLUMN id SET DEFAULT nextval('public.memory_relationships_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: patient_caregivers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_caregivers ALTER COLUMN id SET DEFAULT nextval('public.patient_caregivers_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: reminder_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminder_history ALTER COLUMN id SET DEFAULT nextval('public.reminder_history_id_seq'::regclass);


--
-- Name: reminders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders ALTER COLUMN id SET DEFAULT nextval('public.reminders_id_seq'::regclass);


--
-- Name: safe_zones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.safe_zones ALTER COLUMN id SET DEFAULT nextval('public.safe_zones_id_seq'::regclass);


--
-- Name: sync_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sync_events ALTER COLUMN id SET DEFAULT nextval('public.sync_events_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: voice_recordings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_recordings ALTER COLUMN id SET DEFAULT nextval('public.voice_recordings_id_seq'::regclass);


--
-- Data for Name: activity_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_events (id, patient_id, event_type, event_data, event_timestamp, created_at) FROM stdin;
1	1	APP_OPENED	{"screen":"home"}	2026-09-03 21:00:00+05:30	2026-09-03 16:18:30.594661+05:30
2	2	GAME_COMPLETED	G001 completed	2026-09-03 19:00:00+05:30	2026-09-03 23:02:07.734735+05:30
3	2	VOICE_COMMAND	Asked for today's date	2026-09-03 19:30:00+05:30	2026-09-03 23:02:19.219746+05:30
4	2	ORIENTATION_COMPLETED	Daily orientation completed successfully	2026-09-03 20:00:00+05:30	2026-09-03 23:02:30.044905+05:30
\.


--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alerts (id, patient_id, alert_type, message, severity, status, created_at, resolved_at) FROM stdin;
1	1	TEST_ALERT	This is a test alert	MEDIUM	RESOLVED	2026-09-03 16:39:11.757617+05:30	2026-09-03 16:39:54.233975+05:30
2	2	SAFE_ZONE_EXIT	Patient is outside the configured safe zone.	HIGH	ACTIVE	2026-09-03 20:31:25.450557+05:30	\N
3	2	SOS	Emergency SOS has been triggered by the patient.	HIGH	ACTIVE	2026-09-03 20:55:00.75262+05:30	\N
5	2	SOS	Emergency SOS has been triggered by the patient.	HIGH	ACTIVE	2026-09-04 13:18:02.033138+05:30	\N
6	2	SAFE_ZONE_EXIT	Patient is outside the configured safe zone.	HIGH	ACTIVE	2026-09-04 13:25:09.629423+05:30	\N
4	2	MISSED_REMINDERS	Patient has missed 3 reminders in the last 7 days.	MEDIUM	RESOLVED	2026-09-03 22:44:27.863159+05:30	2026-09-04 13:51:03.990247+05:30
7	2	MISSED_REMINDERS	Patient has missed 8 reminders in the last 7 days.	MEDIUM	ACTIVE	2026-09-04 13:51:47.729614+05:30	\N
\.


--
-- Data for Name: caregivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.caregivers (id, user_id, phone, relationship_to_patient) FROM stdin;
\.


--
-- Data for Name: device_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.device_tokens (id, user_id, token, platform, is_active, created_at, updated_at) FROM stdin;
1	4	test-device-token-12345	android	t	2026-09-04 13:00:59.999066+05:30	2026-09-04 13:00:59.999072+05:30
\.


--
-- Data for Name: emergency_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emergency_events (id, patient_id, trigger, latitude, longitude, "timestamp", status, created_at) FROM stdin;
1	2	SOS_BUTTON	28.6139	77.209	2026-09-03 17:20:00+05:30	ALERT_SENT	2026-09-03 20:55:00.739406+05:30
2	2	MANUAL_SOS	28.6139	77.209	2026-09-04 13:30:00+05:30	ALERT_SENT	2026-09-04 13:18:02.021646+05:30
\.


--
-- Data for Name: face_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.face_profiles (id, patient_id, family_member_id, person_name, face_image_url, embedding_reference, created_at) FROM stdin;
1	2	5	Test Caregiver	/uploads/faces/example.jpg	\N	2026-09-08 17:29:59.192833+05:30
\.


--
-- Data for Name: family_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.family_members (id, patient_id, name, relationship, phone, photo_url, is_active, created_at, is_caregiver, user_id) FROM stdin;
1	1	Rahul	Son	9876543210	https://example.com/rahul.jpg	t	2026-09-02 21:15:28.901667+05:30	f	\N
2	1	Priya	Daughter	\N	\N	t	2026-09-02 21:36:32.303486+05:30	f	\N
3	1	Rahul	Son	\N	\N	t	2026-09-02 21:36:56.251757+05:30	t	\N
4	2	Test Caregiver	Daughter	9999999999	\N	f	2026-09-03 00:55:14.067799+05:30	f	\N
5	2	Test Caregiver	Daughter	9999999999	\N	t	2026-09-03 01:02:05.497113+05:30	t	3
\.


--
-- Data for Name: game_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_results (id, session_id, patient_id, game_id, score, accuracy, mistakes, duration_seconds, attempts, hints_used, response_time, difficulty, completed_at, created_at) FROM stdin;
1	2bc742b0-c8d4-467d-8baf-fd8005de9633	2	G001	85	85	1	42	1	0	4.2	easy	2026-09-03 21:30:00+05:30	2026-09-03 21:32:56.027592+05:30
\.


--
-- Data for Name: game_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_sessions (id, session_id, patient_id, game_id, difficulty, status, started_at, completed_at) FROM stdin;
1	2bc742b0-c8d4-467d-8baf-fd8005de9633	2	G001	easy	COMPLETED	2026-09-03 21:28:08.39049+05:30	2026-09-03 21:30:00+05:30
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.games (id, game_id, name, game_type, difficulty, description, offline_supported, is_active, created_at) FROM stdin;
1	G001	Photo Matching	photo_matching	easy	Match familiar people or objects with the correct pair.	t	t	2026-09-03 21:13:20.372405+05:30
2	G002	Memory Sequence	sequence	easy	Remember and reproduce a sequence of items.	t	t	2026-09-03 21:13:20.372409+05:30
3	G003	Pattern Recognition	pattern	easy	Identify and complete familiar visual patterns.	t	t	2026-09-03 21:13:20.37241+05:30
4	G004	Jigsaw Puzzle	jigsaw	easy	Arrange pieces to complete a familiar picture.	t	t	2026-09-03 21:13:20.372411+05:30
5	G005	Music Memory	music_memory	easy	Recognize familiar songs and sounds.	t	t	2026-09-03 21:13:20.372411+05:30
6	G006	Memory Recall	memory_recall	easy	Recall information from the patient's personal memories.	t	t	2026-09-03 21:13:20.372412+05:30
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (id, patient_id, latitude, longitude, accuracy_meters, "timestamp") FROM stdin;
1	1	28.6139	77.209	10.5	2026-09-03 16:50:00+05:30
2	2	28.6139	77.209	10.5	2026-09-03 16:50:00+05:30
3	2	28.6139	77.209	10	2026-09-03 17:00:00+05:30
4	2	28.62	77.22	10	2026-09-03 17:05:00+05:30
5	2	28.62	77.22	10	2026-09-03 17:10:00+05:30
6	2	28.62	77.22	10	2026-09-04 13:30:00+05:30
\.


--
-- Data for Name: medicines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medicines (id, patient_id, name, dosage, instructions, start_date, end_date, is_active, created_at) FROM stdin;
1	1	string	1000mg	string	2026-09-02	2026-09-02	f	2026-09-02 21:55:16.714454+05:30
2	1	crocine	100mg	2 times a day	2026-09-02	2026-09-02	t	2026-09-02 23:37:08.171837+05:30
\.


--
-- Data for Name: memories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memories (id, patient_id, title, story_text, summary, cover_photo_url, created_at, updated_at, memory_type, tags, people, event_date, location, audio_url, is_private, is_approved) FROM stdin;
1	1	Family Trip to manali	We went to kasol with my husband and children during the summer holidays.	A family trip to Shillong.	https://example.com/shillong.jpg	2026-09-02 20:56:28.478403+05:30	2026-09-02 20:58:40.052626+05:30	general	\N	\N	\N	\N	\N	f	f
2	2	My Wedding Day	I remember my wedding day. My family gathered at our home and we celebrated together.	A beautiful family celebration that I remember fondly.	\N	2026-09-03 22:15:22.90127+05:30	2026-09-03 22:17:42.834215+05:30	family_event	wedding,family,celebration,memories	husband,daughter,brother	1995-02-14	Guwahati, Assam	\N	f	f
\.


--
-- Data for Name: memory_elements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memory_elements (id, memory_id, element_type, label, description, created_at) FROM stdin;
\.


--
-- Data for Name: memory_media; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memory_media (id, memory_id, media_type, media_url, caption, created_at) FROM stdin;
\.


--
-- Data for Name: memory_relationships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memory_relationships (id, memory_id, source_element_id, target_element_id, relationship_type, created_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, patient_id, notification_type, title, message, is_read, created_at, read_at) FROM stdin;
1	4	2	TEST	Memora Test Notification	Notification service is working.	f	2026-09-04 13:07:47.272544+05:30	\N
2	3	2	TEST_CAREGIVER	Memora Caregiver Test	Caregiver notification service is working.	f	2026-09-04 13:07:47.282885+05:30	\N
3	3	2	SOS	Emergency Alert	The patient has triggered an SOS emergency alert.	f	2026-09-04 13:18:02.040497+05:30	\N
4	3	2	SAFE_ZONE_EXIT	Safe Zone Alert	The patient has exited the configured safe zone.	f	2026-09-04 13:25:09.637769+05:30	\N
5	3	2	MISSED_REMINDERS	Missed Medicine Reminder	The patient has missed 8 reminders in the last 7 days.	f	2026-09-04 13:51:47.735273+05:30	\N
\.


--
-- Data for Name: patient_caregivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patient_caregivers (id, patient_id, caregiver_id) FROM stdin;
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients (id, user_id, date_of_birth, language, address, emergency_contact) FROM stdin;
1	1	2026-09-02	en		string
2	4	2026-09-02	northeast	northeast	4567618268
\.


--
-- Data for Name: reminder_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reminder_history (id, reminder_id, patient_id, scheduled_at, completed_at, status, created_at) FROM stdin;
1	1	1	2026-09-02 15:30:00+05:30	2026-09-02 23:44:36.820268+05:30	COMPLETED	2026-09-02 23:44:36.823438+05:30
2	2	2	2026-09-03 14:30:00+05:30	\N	MISSED	2026-09-03 22:44:18.891828+05:30
3	2	2	2026-09-03 14:30:00+05:30	\N	MISSED	2026-09-03 22:44:24.975124+05:30
4	2	2	2026-09-03 14:30:00+05:30	\N	MISSED	2026-09-03 22:44:27.810356+05:30
5	2	2	2026-09-03 14:30:00+05:30	\N	MISSED	2026-09-03 22:44:48.621039+05:30
6	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:40:42.954063+05:30
7	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:40:53.66969+05:30
8	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:40:57.215336+05:30
9	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:51:47.681795+05:30
10	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:51:48.565321+05:30
11	3	2	2026-09-04 14:30:00+05:30	\N	MISSED	2026-09-04 13:51:49.393422+05:30
\.


--
-- Data for Name: reminders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reminders (id, patient_id, medicine_id, reminder_type, reminder_text, scheduled_time, repeat_pattern, status, created_at, updated_at, voice_recording_id) FROM stdin;
1	1	2	MEDICINE	Please take your medicine	10:00:00	DAILY	ACTIVE	2026-09-02 23:37:57.489601+05:30	2026-09-02 23:37:57.489608+05:30	\N
2	2	\N	MEDICINE	Take morning medicine	09:00:00	DAILY	ACTIVE	2026-09-03 22:43:20.566602+05:30	2026-09-03 22:43:20.566606+05:30	\N
3	2	\N	MEDICINE	Please take your morning medicine	09:00:00	DAILY	ACTIVE	2026-09-04 00:22:40.130794+05:30	2026-09-04 00:22:40.130801+05:30	2
\.


--
-- Data for Name: safe_zones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.safe_zones (id, patient_id, name, latitude, longitude, radius_meters, is_active) FROM stdin;
1	2	Home	28.6139	77.209	300	t
\.


--
-- Data for Name: sync_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sync_events (id, patient_id, device_id, event_id, event_type, event_data, event_timestamp, synced_at) FROM stdin;
1	2	phone_001	offline_001	GAME_COMPLETED	{"game_id": "G001", "score": 80}	2026-09-03 20:05:00+05:30	2026-09-03 21:03:58.14321+05:30
2	2	phone_001	offline_002	REMINDER_COMPLETED	{"reminder_id": 1}	2026-09-03 20:10:00+05:30	2026-09-03 21:03:58.143215+05:30
3	2	test-device-001	offline-test-001	REMINDER_MISSED	{"reminder_id": 3, "status": "MISSED"}	2026-09-04 09:01:00+05:30	2026-09-04 14:31:59.452798+05:30
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password_hash, role, created_at) FROM stdin;
1	Test Patient	testpatient@gmail.com	$2b$12$knpKlRlJWEPRpUzMNO.xq.VwQiHMZWYBmWr1aMMNjbo2HpOxqkVIG	patient	2026-09-02 19:55:50.124943+05:30
2	Test Caregiver	caregiver@test.com	$2b$12$KEz9Egd3VB2rZyTAF/cbMeO4DoeDciatzI67OFq3QmvmDbLOxeyLS	caregiver	2026-09-03 00:24:46.764693+05:30
3	Test Caregiver2	caregiver2@test.com	$2b$12$2evjXuX8MbbVqEJPNT/YlOCa5Ty96AIgGu1KB1H7TLF6Dc2vmlbOi	caregiver	2026-09-03 00:41:45.040472+05:30
4	patient2	testpatient2@gmail.com	$2b$12$vEr70GOBBcOzO.DrTYKhluFdpxndlIxH8njL4wvomuJNCEYrp7nDS	patient	2026-09-03 00:46:11.498043+05:30
\.


--
-- Data for Name: voice_recordings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.voice_recordings (id, patient_id, memory_id, audio_url, language, recording_type, duration_seconds, created_at, family_member_id) FROM stdin;
1	2	\N	/audio/test_memory.mp3	hi	MEMORY_STORY	30	2026-09-03 23:54:46.727599+05:30	\N
2	2	2	/audio/wedding_memory.mp3	hi	MEMORY_STORY	45	2026-09-03 23:59:01.203898+05:30	5
3	2	\N	/audio/f85db336-2ba7-4b61-b3a6-a298f509c4d9.mp3	en	VOICE_RECORDING	\N	2026-09-04 12:07:22.497793+05:30	\N
4	2	2	/audio/e6532ef6-4f32-4475-9cfd-4bda20927ddc.mp3	en	VOICE_RECORDING	10	2026-09-04 12:46:32.853226+05:30	5
\.


--
-- Name: activity_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.activity_events_id_seq', 4, true);


--
-- Name: alerts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alerts_id_seq', 7, true);


--
-- Name: caregivers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.caregivers_id_seq', 1, false);


--
-- Name: device_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.device_tokens_id_seq', 1, true);


--
-- Name: emergency_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emergency_events_id_seq', 2, true);


--
-- Name: face_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.face_profiles_id_seq', 1, true);


--
-- Name: family_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.family_members_id_seq', 5, true);


--
-- Name: game_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_results_id_seq', 1, true);


--
-- Name: game_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_sessions_id_seq', 1, true);


--
-- Name: games_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.games_id_seq', 6, true);


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_id_seq', 6, true);


--
-- Name: medicines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medicines_id_seq', 2, true);


--
-- Name: memories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memories_id_seq', 2, true);


--
-- Name: memory_elements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memory_elements_id_seq', 1, false);


--
-- Name: memory_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memory_media_id_seq', 1, false);


--
-- Name: memory_relationships_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memory_relationships_id_seq', 1, false);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 5, true);


--
-- Name: patient_caregivers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patient_caregivers_id_seq', 1, false);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patients_id_seq', 2, true);


--
-- Name: reminder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reminder_history_id_seq', 11, true);


--
-- Name: reminders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reminders_id_seq', 3, true);


--
-- Name: safe_zones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.safe_zones_id_seq', 1, true);


--
-- Name: sync_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sync_events_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: voice_recordings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voice_recordings_id_seq', 4, true);


--
-- Name: activity_events activity_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_events
    ADD CONSTRAINT activity_events_pkey PRIMARY KEY (id);


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: caregivers caregivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_pkey PRIMARY KEY (id);


--
-- Name: caregivers caregivers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_user_id_key UNIQUE (user_id);


--
-- Name: device_tokens device_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_pkey PRIMARY KEY (id);


--
-- Name: device_tokens device_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_token_key UNIQUE (token);


--
-- Name: emergency_events emergency_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_events
    ADD CONSTRAINT emergency_events_pkey PRIMARY KEY (id);


--
-- Name: face_profiles face_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_profiles
    ADD CONSTRAINT face_profiles_pkey PRIMARY KEY (id);


--
-- Name: family_members family_members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_pkey PRIMARY KEY (id);


--
-- Name: family_members family_members_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_user_id_key UNIQUE (user_id);


--
-- Name: game_results game_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_pkey PRIMARY KEY (id);


--
-- Name: game_sessions game_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: medicines medicines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_pkey PRIMARY KEY (id);


--
-- Name: memories memories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_pkey PRIMARY KEY (id);


--
-- Name: memory_elements memory_elements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_elements
    ADD CONSTRAINT memory_elements_pkey PRIMARY KEY (id);


--
-- Name: memory_media memory_media_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_media
    ADD CONSTRAINT memory_media_pkey PRIMARY KEY (id);


--
-- Name: memory_relationships memory_relationships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: patient_caregivers patient_caregivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: patients patients_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_user_id_key UNIQUE (user_id);


--
-- Name: reminder_history reminder_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_pkey PRIMARY KEY (id);


--
-- Name: reminders reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_pkey PRIMARY KEY (id);


--
-- Name: safe_zones safe_zones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.safe_zones
    ADD CONSTRAINT safe_zones_pkey PRIMARY KEY (id);


--
-- Name: sync_events sync_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sync_events
    ADD CONSTRAINT sync_events_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: voice_recordings voice_recordings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_pkey PRIMARY KEY (id);


--
-- Name: ix_activity_events_event_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_events_event_type ON public.activity_events USING btree (event_type);


--
-- Name: ix_activity_events_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_events_id ON public.activity_events USING btree (id);


--
-- Name: ix_activity_events_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_events_patient_id ON public.activity_events USING btree (patient_id);


--
-- Name: ix_alerts_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_alerts_id ON public.alerts USING btree (id);


--
-- Name: ix_alerts_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_alerts_patient_id ON public.alerts USING btree (patient_id);


--
-- Name: ix_caregivers_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_caregivers_id ON public.caregivers USING btree (id);


--
-- Name: ix_device_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_device_tokens_user_id ON public.device_tokens USING btree (user_id);


--
-- Name: ix_emergency_events_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emergency_events_id ON public.emergency_events USING btree (id);


--
-- Name: ix_emergency_events_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emergency_events_patient_id ON public.emergency_events USING btree (patient_id);


--
-- Name: ix_face_profiles_family_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_face_profiles_family_member_id ON public.face_profiles USING btree (family_member_id);


--
-- Name: ix_face_profiles_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_face_profiles_id ON public.face_profiles USING btree (id);


--
-- Name: ix_face_profiles_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_face_profiles_patient_id ON public.face_profiles USING btree (patient_id);


--
-- Name: ix_family_members_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_family_members_id ON public.family_members USING btree (id);


--
-- Name: ix_family_members_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_family_members_patient_id ON public.family_members USING btree (patient_id);


--
-- Name: ix_game_results_game_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_results_game_id ON public.game_results USING btree (game_id);


--
-- Name: ix_game_results_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_results_id ON public.game_results USING btree (id);


--
-- Name: ix_game_results_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_results_patient_id ON public.game_results USING btree (patient_id);


--
-- Name: ix_game_results_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_results_session_id ON public.game_results USING btree (session_id);


--
-- Name: ix_game_sessions_game_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_sessions_game_id ON public.game_sessions USING btree (game_id);


--
-- Name: ix_game_sessions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_sessions_id ON public.game_sessions USING btree (id);


--
-- Name: ix_game_sessions_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_game_sessions_patient_id ON public.game_sessions USING btree (patient_id);


--
-- Name: ix_game_sessions_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_game_sessions_session_id ON public.game_sessions USING btree (session_id);


--
-- Name: ix_games_game_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_games_game_id ON public.games USING btree (game_id);


--
-- Name: ix_games_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_games_id ON public.games USING btree (id);


--
-- Name: ix_locations_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_locations_id ON public.locations USING btree (id);


--
-- Name: ix_locations_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_locations_patient_id ON public.locations USING btree (patient_id);


--
-- Name: ix_medicines_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_medicines_id ON public.medicines USING btree (id);


--
-- Name: ix_medicines_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_medicines_patient_id ON public.medicines USING btree (patient_id);


--
-- Name: ix_memories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memories_id ON public.memories USING btree (id);


--
-- Name: ix_memories_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memories_patient_id ON public.memories USING btree (patient_id);


--
-- Name: ix_memory_elements_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_elements_id ON public.memory_elements USING btree (id);


--
-- Name: ix_memory_elements_memory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_elements_memory_id ON public.memory_elements USING btree (memory_id);


--
-- Name: ix_memory_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_media_id ON public.memory_media USING btree (id);


--
-- Name: ix_memory_media_memory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_media_memory_id ON public.memory_media USING btree (memory_id);


--
-- Name: ix_memory_relationships_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_relationships_id ON public.memory_relationships USING btree (id);


--
-- Name: ix_memory_relationships_memory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memory_relationships_memory_id ON public.memory_relationships USING btree (memory_id);


--
-- Name: ix_notifications_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_patient_id ON public.notifications USING btree (patient_id);


--
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: ix_patient_caregivers_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_patient_caregivers_id ON public.patient_caregivers USING btree (id);


--
-- Name: ix_patients_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_patients_id ON public.patients USING btree (id);


--
-- Name: ix_reminder_history_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminder_history_id ON public.reminder_history USING btree (id);


--
-- Name: ix_reminder_history_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminder_history_patient_id ON public.reminder_history USING btree (patient_id);


--
-- Name: ix_reminder_history_reminder_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminder_history_reminder_id ON public.reminder_history USING btree (reminder_id);


--
-- Name: ix_reminders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminders_id ON public.reminders USING btree (id);


--
-- Name: ix_reminders_medicine_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminders_medicine_id ON public.reminders USING btree (medicine_id);


--
-- Name: ix_reminders_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminders_patient_id ON public.reminders USING btree (patient_id);


--
-- Name: ix_reminders_voice_recording_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reminders_voice_recording_id ON public.reminders USING btree (voice_recording_id);


--
-- Name: ix_safe_zones_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_safe_zones_id ON public.safe_zones USING btree (id);


--
-- Name: ix_safe_zones_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_safe_zones_patient_id ON public.safe_zones USING btree (patient_id);


--
-- Name: ix_sync_events_event_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sync_events_event_id ON public.sync_events USING btree (event_id);


--
-- Name: ix_sync_events_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sync_events_id ON public.sync_events USING btree (id);


--
-- Name: ix_sync_events_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sync_events_patient_id ON public.sync_events USING btree (patient_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_voice_recordings_family_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_voice_recordings_family_member_id ON public.voice_recordings USING btree (family_member_id);


--
-- Name: ix_voice_recordings_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_voice_recordings_id ON public.voice_recordings USING btree (id);


--
-- Name: ix_voice_recordings_memory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_voice_recordings_memory_id ON public.voice_recordings USING btree (memory_id);


--
-- Name: ix_voice_recordings_patient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_voice_recordings_patient_id ON public.voice_recordings USING btree (patient_id);


--
-- Name: activity_events activity_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_events
    ADD CONSTRAINT activity_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: alerts alerts_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: caregivers caregivers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregivers
    ADD CONSTRAINT caregivers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: device_tokens device_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device_tokens
    ADD CONSTRAINT device_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: emergency_events emergency_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_events
    ADD CONSTRAINT emergency_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: face_profiles face_profiles_family_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_profiles
    ADD CONSTRAINT face_profiles_family_member_id_fkey FOREIGN KEY (family_member_id) REFERENCES public.family_members(id);


--
-- Name: face_profiles face_profiles_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_profiles
    ADD CONSTRAINT face_profiles_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: family_members family_members_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: family_members family_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family_members
    ADD CONSTRAINT family_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reminders fk_reminders_voice_recording; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT fk_reminders_voice_recording FOREIGN KEY (voice_recording_id) REFERENCES public.voice_recordings(id);


--
-- Name: voice_recordings fk_voice_recordings_family_member; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT fk_voice_recordings_family_member FOREIGN KEY (family_member_id) REFERENCES public.family_members(id);


--
-- Name: game_results game_results_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_results game_results_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: game_results game_results_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_results
    ADD CONSTRAINT game_results_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.game_sessions(session_id);


--
-- Name: game_sessions game_sessions_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: game_sessions game_sessions_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_sessions
    ADD CONSTRAINT game_sessions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: locations locations_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: medicines medicines_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: memories memories_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: memory_elements memory_elements_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_elements
    ADD CONSTRAINT memory_elements_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_media memory_media_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_media
    ADD CONSTRAINT memory_media_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_relationships memory_relationships_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: memory_relationships memory_relationships_source_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_source_element_id_fkey FOREIGN KEY (source_element_id) REFERENCES public.memory_elements(id);


--
-- Name: memory_relationships memory_relationships_target_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memory_relationships
    ADD CONSTRAINT memory_relationships_target_element_id_fkey FOREIGN KEY (target_element_id) REFERENCES public.memory_elements(id);


--
-- Name: notifications notifications_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: patient_caregivers patient_caregivers_caregiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_caregiver_id_fkey FOREIGN KEY (caregiver_id) REFERENCES public.caregivers(id);


--
-- Name: patient_caregivers patient_caregivers_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_caregivers
    ADD CONSTRAINT patient_caregivers_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: patients patients_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reminder_history reminder_history_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: reminder_history reminder_history_reminder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminder_history
    ADD CONSTRAINT reminder_history_reminder_id_fkey FOREIGN KEY (reminder_id) REFERENCES public.reminders(id);


--
-- Name: reminders reminders_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicines(id);


--
-- Name: reminders reminders_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: safe_zones safe_zones_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.safe_zones
    ADD CONSTRAINT safe_zones_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: sync_events sync_events_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sync_events
    ADD CONSTRAINT sync_events_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: voice_recordings voice_recordings_memory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_memory_id_fkey FOREIGN KEY (memory_id) REFERENCES public.memories(id);


--
-- Name: voice_recordings voice_recordings_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_recordings
    ADD CONSTRAINT voice_recordings_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- PostgreSQL database dump complete
--

\unrestrict aRFeEE35KhsxVpqSnomTYJEuzNUPfrGaw1d4kr8h8aL2EbpWKX4mdSiI66pJPXv

