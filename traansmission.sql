--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO postgres;

--
-- Name: geolocations_cachedcoordinate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE geolocations_cachedcoordinate (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    address text,
    address_2 text,
    zip_code character varying(5),
    city character varying(50),
    state character varying(2),
    coordinate geography(Point,4326) NOT NULL
);


ALTER TABLE geolocations_cachedcoordinate OWNER TO postgres;

--
-- Name: geolocations_cachedcoordinate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE geolocations_cachedcoordinate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE geolocations_cachedcoordinate_id_seq OWNER TO postgres;

--
-- Name: geolocations_cachedcoordinate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE geolocations_cachedcoordinate_id_seq OWNED BY geolocations_cachedcoordinate.id;


--
-- Name: geolocations_cacheddistance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE geolocations_cacheddistance (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    start_lat numeric(13,10) NOT NULL,
    end_lat numeric(13,10) NOT NULL,
    start_lon numeric(13,10) NOT NULL,
    end_lon numeric(13,10) NOT NULL,
    distance numeric(9,1) NOT NULL
);


ALTER TABLE geolocations_cacheddistance OWNER TO postgres;

--
-- Name: geolocations_cacheddistance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE geolocations_cacheddistance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE geolocations_cacheddistance_id_seq OWNER TO postgres;

--
-- Name: geolocations_cacheddistance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE geolocations_cacheddistance_id_seq OWNED BY geolocations_cacheddistance.id;


--
-- Name: geolocations_geolocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE geolocations_geolocation (
    id integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    altitude double precision,
    accuracy double precision,
    speed double precision,
    course double precision,
    "timestamp" timestamp with time zone,
    carrier_id integer NOT NULL,
    driver_id integer NOT NULL,
    shipment_id integer,
    display_text text
);


ALTER TABLE geolocations_geolocation OWNER TO postgres;

--
-- Name: geolocations_geolocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE geolocations_geolocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE geolocations_geolocation_id_seq OWNER TO postgres;

--
-- Name: geolocations_geolocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE geolocations_geolocation_id_seq OWNED BY geolocations_geolocation.id;


--
-- Name: guardian_groupobjectpermission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE guardian_groupobjectpermission (
    id integer NOT NULL,
    object_pk character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE guardian_groupobjectpermission OWNER TO postgres;

--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE guardian_groupobjectpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE guardian_groupobjectpermission_id_seq OWNER TO postgres;

--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE guardian_groupobjectpermission_id_seq OWNED BY guardian_groupobjectpermission.id;


--
-- Name: guardian_userobjectpermission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE guardian_userobjectpermission (
    id integer NOT NULL,
    object_pk character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    permission_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE guardian_userobjectpermission OWNER TO postgres;

--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE guardian_userobjectpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE guardian_userobjectpermission_id_seq OWNER TO postgres;

--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE guardian_userobjectpermission_id_seq OWNED BY guardian_userobjectpermission.id;


--
-- Name: notifications_day1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day1 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day1 OWNER TO postgres;

--
-- Name: notifications_day15; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day15 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day15 OWNER TO postgres;

--
-- Name: notifications_day15_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day15_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day15_id_seq OWNER TO postgres;

--
-- Name: notifications_day15_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day15_id_seq OWNED BY notifications_day15.id;


--
-- Name: notifications_day1_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day1_id_seq OWNER TO postgres;

--
-- Name: notifications_day1_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day1_id_seq OWNED BY notifications_day1.id;


--
-- Name: notifications_day28; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day28 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day28 OWNER TO postgres;

--
-- Name: notifications_day28_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day28_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day28_id_seq OWNER TO postgres;

--
-- Name: notifications_day28_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day28_id_seq OWNED BY notifications_day28.id;


--
-- Name: notifications_day31; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day31 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day31 OWNER TO postgres;

--
-- Name: notifications_day31_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day31_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day31_id_seq OWNER TO postgres;

--
-- Name: notifications_day31_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day31_id_seq OWNED BY notifications_day31.id;


--
-- Name: notifications_day38; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day38 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day38 OWNER TO postgres;

--
-- Name: notifications_day38_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day38_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day38_id_seq OWNER TO postgres;

--
-- Name: notifications_day38_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day38_id_seq OWNED BY notifications_day38.id;


--
-- Name: notifications_day7; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_day7 (
    id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE notifications_day7 OWNER TO postgres;

--
-- Name: notifications_day7_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_day7_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_day7_id_seq OWNER TO postgres;

--
-- Name: notifications_day7_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_day7_id_seq OWNED BY notifications_day7.id;


--
-- Name: notifications_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_notification (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    parent_object_id integer NOT NULL,
    sender_email character varying(254),
    sender_name character varying(200),
    receiver_name character varying(200),
    receiver_email character varying(254),
    email_subject character varying(256),
    email_content_html text,
    email_content_raw text,
    parent_content_type_id integer NOT NULL,
    receiver_id integer,
    sender_id integer,
    use_html_template boolean NOT NULL,
    email_sent boolean NOT NULL,
    email_content_html_file text,
    email_mergevars text,
    CONSTRAINT notifications_notification_parent_object_id_check CHECK ((parent_object_id >= 0))
);


ALTER TABLE notifications_notification OWNER TO postgres;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_notification_id_seq OWNER TO postgres;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_notification_id_seq OWNED BY notifications_notification.id;


--
-- Name: notifications_shipmentassignmentnotif; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_shipmentassignmentnotif (
    id integer NOT NULL,
    sender_id integer NOT NULL,
    shipment_assignment_id integer NOT NULL
);


ALTER TABLE notifications_shipmentassignmentnotif OWNER TO postgres;

--
-- Name: notifications_shipmentassignmentnotif_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_shipmentassignmentnotif_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_shipmentassignmentnotif_id_seq OWNER TO postgres;

--
-- Name: notifications_shipmentassignmentnotif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_shipmentassignmentnotif_id_seq OWNED BY notifications_shipmentassignmentnotif.id;


--
-- Name: notifications_shipmentassignmentnotif_receivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_shipmentassignmentnotif_receivers (
    id integer NOT NULL,
    shipmentassignmentnotif_id integer NOT NULL,
    genericuser_id integer NOT NULL
);


ALTER TABLE notifications_shipmentassignmentnotif_receivers OWNER TO postgres;

--
-- Name: notifications_shipmentassignmentnotif_receivers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_shipmentassignmentnotif_receivers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_shipmentassignmentnotif_receivers_id_seq OWNER TO postgres;

--
-- Name: notifications_shipmentassignmentnotif_receivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_shipmentassignmentnotif_receivers_id_seq OWNED BY notifications_shipmentassignmentnotif_receivers.id;


--
-- Name: notifications_signupinternalnotif; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_signupinternalnotif (
    id integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE notifications_signupinternalnotif OWNER TO postgres;

--
-- Name: notifications_signupinternalnotif_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_signupinternalnotif_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_signupinternalnotif_id_seq OWNER TO postgres;

--
-- Name: notifications_signupinternalnotif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_signupinternalnotif_id_seq OWNED BY notifications_signupinternalnotif.id;


--
-- Name: notifications_userinvitenotif; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE notifications_userinvitenotif (
    id integer NOT NULL,
    receiver_email character varying(254) NOT NULL,
    receiver_name character varying(200) NOT NULL,
    invite_id integer NOT NULL,
    sender_id integer NOT NULL
);


ALTER TABLE notifications_userinvitenotif OWNER TO postgres;

--
-- Name: notifications_userinvitenotif_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE notifications_userinvitenotif_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_userinvitenotif_id_seq OWNER TO postgres;

--
-- Name: notifications_userinvitenotif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE notifications_userinvitenotif_id_seq OWNED BY notifications_userinvitenotif.id;


--
-- Name: payments_subscription; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE payments_subscription (
    id integer NOT NULL,
    no_users integer,
    no_trucks integer,
    annual_plan boolean NOT NULL,
    payment_ready boolean NOT NULL,
    trial_length integer NOT NULL,
    trial_start timestamp with time zone
);


ALTER TABLE payments_subscription OWNER TO postgres;

--
-- Name: payments_subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE payments_subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE payments_subscription_id_seq OWNER TO postgres;

--
-- Name: payments_subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE payments_subscription_id_seq OWNED BY payments_subscription.id;


--
-- Name: permissions_basepermission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE permissions_basepermission (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    is_set boolean NOT NULL,
    is_editable boolean NOT NULL,
    permission_id integer NOT NULL,
    permission_collection_id integer NOT NULL
);


ALTER TABLE permissions_basepermission OWNER TO postgres;

--
-- Name: permissions_basepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE permissions_basepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE permissions_basepermission_id_seq OWNER TO postgres;

--
-- Name: permissions_basepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE permissions_basepermission_id_seq OWNED BY permissions_basepermission.id;


--
-- Name: permissions_basepermissioncollection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE permissions_basepermissioncollection (
    id integer NOT NULL,
    user_type character varying(200) NOT NULL
);


ALTER TABLE permissions_basepermissioncollection OWNER TO postgres;

--
-- Name: permissions_basepermissioncollection_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE permissions_basepermissioncollection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE permissions_basepermissioncollection_id_seq OWNER TO postgres;

--
-- Name: permissions_basepermissioncollection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE permissions_basepermissioncollection_id_seq OWNED BY permissions_basepermissioncollection.id;


--
-- Name: shipments_addressdetails; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_addressdetails (
    id integer NOT NULL,
    address text,
    address_2 text,
    zip_code character varying(5),
    city character varying(50),
    state character varying(2),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE shipments_addressdetails OWNER TO postgres;

--
-- Name: shipments_addressdetails_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_addressdetails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_addressdetails_id_seq OWNER TO postgres;

--
-- Name: shipments_addressdetails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_addressdetails_id_seq OWNED BY shipments_addressdetails.id;


--
-- Name: shipments_companydivision; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_companydivision (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(30) NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE shipments_companydivision OWNER TO postgres;

--
-- Name: shipments_companydivision_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_companydivision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_companydivision_id_seq OWNER TO postgres;

--
-- Name: shipments_companydivision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_companydivision_id_seq OWNED BY shipments_companydivision.id;


--
-- Name: shipments_companydivisionmembership; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_companydivisionmembership (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    division_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE shipments_companydivisionmembership OWNER TO postgres;

--
-- Name: shipments_companydivisionmembership_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_companydivisionmembership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_companydivisionmembership_id_seq OWNER TO postgres;

--
-- Name: shipments_companydivisionmembership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_companydivisionmembership_id_seq OWNED BY shipments_companydivisionmembership.id;


--
-- Name: shipments_companyinvite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_companyinvite (
    id integer NOT NULL,
    invitee_name character varying(200) NOT NULL,
    invitee_email character varying(254) NOT NULL,
    invitee_dot integer,
    inviter_company_id integer NOT NULL,
    inviter_user_id integer,
    invite_accepted boolean NOT NULL,
    invitee_phone character varying(20),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    invitee_company_type character varying(200) NOT NULL
);


ALTER TABLE shipments_companyinvite OWNER TO postgres;

--
-- Name: shipments_companyinvite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_companyinvite_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_companyinvite_id_seq OWNER TO postgres;

--
-- Name: shipments_companyinvite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_companyinvite_id_seq OWNED BY shipments_companyinvite.id;


--
-- Name: shipments_companyrelation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_companyrelation (
    id integer NOT NULL,
    is_inviter boolean NOT NULL,
    active boolean NOT NULL,
    hidden boolean NOT NULL,
    relation_from_id integer NOT NULL,
    relation_to_id integer NOT NULL,
    sibling_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE shipments_companyrelation OWNER TO postgres;

--
-- Name: shipments_companyrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_companyrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_companyrelation_id_seq OWNER TO postgres;

--
-- Name: shipments_companyrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_companyrelation_id_seq OWNED BY shipments_companyrelation.id;


--
-- Name: shipments_demoaccount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_demoaccount (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    password character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    company_name character varying(200) NOT NULL,
    no_of_shipments integer NOT NULL,
    company_id integer,
    dot integer,
    no_of_connections integer NOT NULL,
    demo_account_type character varying(200) NOT NULL
);


ALTER TABLE shipments_demoaccount OWNER TO postgres;

--
-- Name: shipments_demoaccount_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_demoaccount_connections (
    id integer NOT NULL,
    demoaccount_id integer NOT NULL,
    genericcompany_id integer NOT NULL
);


ALTER TABLE shipments_demoaccount_connections OWNER TO postgres;

--
-- Name: shipments_demoaccount_connections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_demoaccount_connections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_demoaccount_connections_id_seq OWNER TO postgres;

--
-- Name: shipments_demoaccount_connections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_demoaccount_connections_id_seq OWNED BY shipments_demoaccount_connections.id;


--
-- Name: shipments_demoaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_demoaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_demoaccount_id_seq OWNER TO postgres;

--
-- Name: shipments_demoaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_demoaccount_id_seq OWNED BY shipments_demoaccount.id;


--
-- Name: shipments_equipmenttag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_equipmenttag (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    tag_category integer NOT NULL,
    tag_type integer NOT NULL,
    assignee_id integer NOT NULL,
    assignee_content_type_id integer NOT NULL,
    assigner_id integer,
    CONSTRAINT shipments_equipmenttag_assignee_id_check CHECK ((assignee_id >= 0))
);


ALTER TABLE shipments_equipmenttag OWNER TO postgres;

--
-- Name: shipments_equipmenttag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_equipmenttag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_equipmenttag_id_seq OWNER TO postgres;

--
-- Name: shipments_equipmenttag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_equipmenttag_id_seq OWNED BY shipments_equipmenttag.id;


--
-- Name: shipments_filecontext; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_filecontext (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    uuid_value character varying(36) NOT NULL,
    path character varying(256) NOT NULL,
    url_ttl integer NOT NULL
);


ALTER TABLE shipments_filecontext OWNER TO postgres;

--
-- Name: shipments_filecontext_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_filecontext_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_filecontext_id_seq OWNER TO postgres;

--
-- Name: shipments_filecontext_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_filecontext_id_seq OWNED BY shipments_filecontext.id;


--
-- Name: shipments_genericcompany; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_genericcompany (
    id integer NOT NULL,
    company_name character varying(200),
    verified boolean NOT NULL,
    rejected boolean NOT NULL,
    insurance_id integer,
    owner_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    dot integer,
    is_fleet boolean NOT NULL,
    max_requests integer NOT NULL,
    city character varying(50),
    state character varying(2),
    company_type character varying(200) NOT NULL,
    logo_id integer,
    subscription_id integer,
    registration_complete boolean NOT NULL
);


ALTER TABLE shipments_genericcompany OWNER TO postgres;

--
-- Name: shipments_genericcompany_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_genericcompany_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_genericcompany_id_seq OWNER TO postgres;

--
-- Name: shipments_genericcompany_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_genericcompany_id_seq OWNED BY shipments_genericcompany.id;


--
-- Name: shipments_genericuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_genericuser (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    user_id integer,
    profile_photo_id integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    permissions_id integer,
    last_location geography(Point,4326),
    last_location_timestamp timestamp with time zone,
    vehicle_type integer,
    tos_acceptance_id integer,
    company_id integer NOT NULL,
    phone character varying(128),
    user_type character varying(200) NOT NULL,
    inactive boolean NOT NULL
);


ALTER TABLE shipments_genericuser OWNER TO postgres;

--
-- Name: shipments_genericuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_genericuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_genericuser_id_seq OWNER TO postgres;

--
-- Name: shipments_genericuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_genericuser_id_seq OWNED BY shipments_genericuser.id;


--
-- Name: shipments_globalsettings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_globalsettings (
    id integer NOT NULL,
    shipment_id_counter integer NOT NULL,
    current_tos_version integer NOT NULL
);


ALTER TABLE shipments_globalsettings OWNER TO postgres;

--
-- Name: shipments_globalsettings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_globalsettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_globalsettings_id_seq OWNER TO postgres;

--
-- Name: shipments_globalsettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_globalsettings_id_seq OWNED BY shipments_globalsettings.id;


--
-- Name: shipments_insurance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_insurance (
    id integer NOT NULL,
    policy_url character varying(2048)
);


ALTER TABLE shipments_insurance OWNER TO postgres;

--
-- Name: shipments_insurance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_insurance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_insurance_id_seq OWNER TO postgres;

--
-- Name: shipments_insurance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_insurance_id_seq OWNED BY shipments_insurance.id;


--
-- Name: shipments_shipmentlocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentlocation (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    saved boolean NOT NULL,
    contact_id integer,
    dock character varying(100),
    company_name character varying(100),
    appointment_id character varying(100),
    comments text,
    features_id integer,
    location_type integer NOT NULL,
    shipment_id integer NOT NULL,
    time_range_id integer,
    arrival_time timestamp with time zone,
    address_details_id integer,
    next_location_id integer,
    cached_coordinate_id integer,
    cached_distance_id integer
);


ALTER TABLE shipments_shipmentlocation OWNER TO postgres;

--
-- Name: shipments_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_location_id_seq OWNER TO postgres;

--
-- Name: shipments_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_location_id_seq OWNED BY shipments_shipmentlocation.id;


--
-- Name: shipments_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_person (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    email character varying(254),
    phone character varying(128)
);


ALTER TABLE shipments_person OWNER TO postgres;

--
-- Name: shipments_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_person_id_seq OWNER TO postgres;

--
-- Name: shipments_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_person_id_seq OWNED BY shipments_person.id;


--
-- Name: shipments_platform; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_platform (
    id integer NOT NULL,
    platform_type integer NOT NULL,
    identifier character varying(512) NOT NULL,
    allow_notifications boolean NOT NULL,
    user_id integer NOT NULL,
    is_primary_email boolean NOT NULL
);


ALTER TABLE shipments_platform OWNER TO postgres;

--
-- Name: shipments_platform_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_platform_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_platform_id_seq OWNER TO postgres;

--
-- Name: shipments_platform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_platform_id_seq OWNED BY shipments_platform.id;


--
-- Name: shipments_savedlocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_savedlocation (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    saved_location_name character varying(100),
    saved boolean NOT NULL,
    owner_id integer,
    contact_id integer,
    dock character varying(100),
    company_name character varying(100),
    appointment_id character varying(100),
    comments text,
    features_id integer,
    location_type integer NOT NULL,
    time_range_id integer,
    address_details_id integer,
    cached_coordinate_id integer
);


ALTER TABLE shipments_savedlocation OWNER TO postgres;

--
-- Name: shipments_savedlocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_savedlocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_savedlocation_id_seq OWNER TO postgres;

--
-- Name: shipments_savedlocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_savedlocation_id_seq OWNED BY shipments_savedlocation.id;


--
-- Name: shipments_shipment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipment (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    shipment_id character varying(32),
    carrier_is_approved boolean NOT NULL,
    delivery_status integer NOT NULL,
    owner_id integer,
    carrier_id integer,
    owner_user_id integer,
    payout_info_id integer,
    comments text,
    first_location_id integer,
    last_location_id integer,
    next_trip_dist_update timestamp with time zone NOT NULL,
    bol_number character varying(100),
    carrier_assignment_id integer,
    driver_assignment_id integer
);


ALTER TABLE shipments_shipment OWNER TO postgres;

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipment_id_seq OWNER TO postgres;

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipment_id_seq OWNED BY shipments_shipment.id;


--
-- Name: shipments_shipmentassignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentassignment (
    id integer NOT NULL,
    parent_id integer NOT NULL,
    assignee_id integer NOT NULL,
    can_delegate boolean NOT NULL,
    notify boolean NOT NULL,
    r boolean NOT NULL,
    u boolean NOT NULL,
    d boolean NOT NULL,
    assignee_content_type_id integer NOT NULL,
    assigner_id integer,
    parent_content_type_id integer NOT NULL,
    shipment_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    CONSTRAINT shipments_shipmentassignment_assignee_id_check CHECK ((assignee_id >= 0)),
    CONSTRAINT shipments_shipmentassignment_parent_id_check CHECK ((parent_id >= 0))
);


ALTER TABLE shipments_shipmentassignment OWNER TO postgres;

--
-- Name: shipments_shipmentassignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentassignment_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentassignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentassignment_id_seq OWNED BY shipments_shipmentassignment.id;


--
-- Name: shipments_shipmentcarrierassignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentcarrierassignment (
    id integer NOT NULL,
    assignment_id integer
);


ALTER TABLE shipments_shipmentcarrierassignment OWNER TO postgres;

--
-- Name: shipments_shipmentcarrierassignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentcarrierassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentcarrierassignment_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentcarrierassignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentcarrierassignment_id_seq OWNED BY shipments_shipmentcarrierassignment.id;


--
-- Name: shipments_shipmentdriverassignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentdriverassignment (
    id integer NOT NULL,
    assignment_id integer
);


ALTER TABLE shipments_shipmentdriverassignment OWNER TO postgres;

--
-- Name: shipments_shipmentdriverassignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentdriverassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentdriverassignment_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentdriverassignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentdriverassignment_id_seq OWNED BY shipments_shipmentdriverassignment.id;


--
-- Name: shipments_shipmentfeatures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentfeatures (
    id integer NOT NULL,
    weight double precision,
    palletized boolean NOT NULL,
    pallet_number integer,
    pallet_length double precision,
    pallet_width double precision,
    pallet_height double precision,
    extra_details text,
    comments text
);


ALTER TABLE shipments_shipmentfeatures OWNER TO postgres;

--
-- Name: shipments_shipmentfeatures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentfeatures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentfeatures_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentfeatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentfeatures_id_seq OWNED BY shipments_shipmentfeatures.id;


--
-- Name: shipments_shipmentpayout; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentpayout (
    id integer NOT NULL,
    payout numeric(9,2),
    comments text
);


ALTER TABLE shipments_shipmentpayout OWNER TO postgres;

--
-- Name: shipments_shipmentpayout_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentpayout_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentpayout_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentpayout_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentpayout_id_seq OWNED BY shipments_shipmentpayout.id;


--
-- Name: shipments_shipmentrequest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_shipmentrequest (
    id integer NOT NULL,
    rejected boolean NOT NULL,
    carrier_id integer NOT NULL,
    driver_id integer,
    shipment_id integer NOT NULL
);


ALTER TABLE shipments_shipmentrequest OWNER TO postgres;

--
-- Name: shipments_shipmentrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_shipmentrequest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_shipmentrequest_id_seq OWNER TO postgres;

--
-- Name: shipments_shipmentrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_shipmentrequest_id_seq OWNED BY shipments_shipmentrequest.id;


--
-- Name: shipments_timerange; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_timerange (
    id integer NOT NULL,
    time_range_start timestamp with time zone,
    time_range_end timestamp with time zone,
    tz character varying(63) NOT NULL
);


ALTER TABLE shipments_timerange OWNER TO postgres;

--
-- Name: shipments_timerange_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_timerange_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_timerange_id_seq OWNER TO postgres;

--
-- Name: shipments_timerange_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_timerange_id_seq OWNED BY shipments_timerange.id;


--
-- Name: shipments_tosacceptance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_tosacceptance (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    tos_status integer NOT NULL,
    tos_updated_at timestamp with time zone NOT NULL,
    tos_version integer NOT NULL
);


ALTER TABLE shipments_tosacceptance OWNER TO postgres;

--
-- Name: shipments_tosacceptance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_tosacceptance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_tosacceptance_id_seq OWNER TO postgres;

--
-- Name: shipments_tosacceptance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_tosacceptance_id_seq OWNED BY shipments_tosacceptance.id;


--
-- Name: shipments_userinvite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE shipments_userinvite (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    token uuid NOT NULL,
    email character varying(254) NOT NULL,
    user_type character varying(200) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100),
    company_id integer NOT NULL,
    user_id integer,
    assigner_user_id integer
);


ALTER TABLE shipments_userinvite OWNER TO postgres;

--
-- Name: shipments_userinvite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE shipments_userinvite_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shipments_userinvite_id_seq OWNER TO postgres;

--
-- Name: shipments_userinvite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE shipments_userinvite_id_seq OWNED BY shipments_userinvite.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_cachedcoordinate ALTER COLUMN id SET DEFAULT nextval('geolocations_cachedcoordinate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_cacheddistance ALTER COLUMN id SET DEFAULT nextval('geolocations_cacheddistance_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation ALTER COLUMN id SET DEFAULT nextval('geolocations_geolocation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission ALTER COLUMN id SET DEFAULT nextval('guardian_groupobjectpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission ALTER COLUMN id SET DEFAULT nextval('guardian_userobjectpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day1 ALTER COLUMN id SET DEFAULT nextval('notifications_day1_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day15 ALTER COLUMN id SET DEFAULT nextval('notifications_day15_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day28 ALTER COLUMN id SET DEFAULT nextval('notifications_day28_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day31 ALTER COLUMN id SET DEFAULT nextval('notifications_day31_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day38 ALTER COLUMN id SET DEFAULT nextval('notifications_day38_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day7 ALTER COLUMN id SET DEFAULT nextval('notifications_day7_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_notification ALTER COLUMN id SET DEFAULT nextval('notifications_notification_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif ALTER COLUMN id SET DEFAULT nextval('notifications_shipmentassignmentnotif_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif_receivers ALTER COLUMN id SET DEFAULT nextval('notifications_shipmentassignmentnotif_receivers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_signupinternalnotif ALTER COLUMN id SET DEFAULT nextval('notifications_signupinternalnotif_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_userinvitenotif ALTER COLUMN id SET DEFAULT nextval('notifications_userinvitenotif_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY payments_subscription ALTER COLUMN id SET DEFAULT nextval('payments_subscription_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermission ALTER COLUMN id SET DEFAULT nextval('permissions_basepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermissioncollection ALTER COLUMN id SET DEFAULT nextval('permissions_basepermissioncollection_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_addressdetails ALTER COLUMN id SET DEFAULT nextval('shipments_addressdetails_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivision ALTER COLUMN id SET DEFAULT nextval('shipments_companydivision_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivisionmembership ALTER COLUMN id SET DEFAULT nextval('shipments_companydivisionmembership_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite ALTER COLUMN id SET DEFAULT nextval('shipments_companyinvite_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation ALTER COLUMN id SET DEFAULT nextval('shipments_companyrelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount ALTER COLUMN id SET DEFAULT nextval('shipments_demoaccount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount_connections ALTER COLUMN id SET DEFAULT nextval('shipments_demoaccount_connections_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_equipmenttag ALTER COLUMN id SET DEFAULT nextval('shipments_equipmenttag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_filecontext ALTER COLUMN id SET DEFAULT nextval('shipments_filecontext_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany ALTER COLUMN id SET DEFAULT nextval('shipments_genericcompany_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser ALTER COLUMN id SET DEFAULT nextval('shipments_genericuser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_globalsettings ALTER COLUMN id SET DEFAULT nextval('shipments_globalsettings_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_insurance ALTER COLUMN id SET DEFAULT nextval('shipments_insurance_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_person ALTER COLUMN id SET DEFAULT nextval('shipments_person_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_platform ALTER COLUMN id SET DEFAULT nextval('shipments_platform_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation ALTER COLUMN id SET DEFAULT nextval('shipments_savedlocation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment ALTER COLUMN id SET DEFAULT nextval('shipments_shipment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentassignment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentcarrierassignment ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentcarrierassignment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentdriverassignment ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentdriverassignment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentfeatures ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentfeatures_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation ALTER COLUMN id SET DEFAULT nextval('shipments_location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentpayout ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentpayout_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentrequest ALTER COLUMN id SET DEFAULT nextval('shipments_shipmentrequest_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_timerange ALTER COLUMN id SET DEFAULT nextval('shipments_timerange_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_tosacceptance ALTER COLUMN id SET DEFAULT nextval('shipments_tosacceptance_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite ALTER COLUMN id SET DEFAULT nextval('shipments_userinvite_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add token	7	add_token
20	Can change token	7	change_token
21	Can delete token	7	delete_token
22	Can add user object permission	8	add_userobjectpermission
23	Can change user object permission	8	change_userobjectpermission
24	Can delete user object permission	8	delete_userobjectpermission
25	Can add group object permission	9	add_groupobjectpermission
26	Can change group object permission	9	change_groupobjectpermission
27	Can delete group object permission	9	delete_groupobjectpermission
28	Can add file context	10	add_filecontext
29	Can change file context	10	change_filecontext
30	Can delete file context	10	delete_filecontext
31	Can add insurance	11	add_insurance
32	Can change insurance	11	change_insurance
33	Can delete insurance	11	delete_insurance
34	Can add generic company	12	add_genericcompany
35	Can change generic company	12	change_genericcompany
36	Can delete generic company	12	delete_genericcompany
37	Can add tos acceptance	13	add_tosacceptance
38	Can change tos acceptance	13	change_tosacceptance
39	Can delete tos acceptance	13	delete_tosacceptance
40	Can add address details	14	add_addressdetails
41	Can change address details	14	change_addressdetails
42	Can delete address details	14	delete_addressdetails
43	Can add shipment location	15	add_shipmentlocation
44	Can change shipment location	15	change_shipmentlocation
45	Can delete shipment location	15	delete_shipmentlocation
46	Can add saved location	16	add_savedlocation
47	Can change saved location	16	change_savedlocation
48	Can delete saved location	16	delete_savedlocation
49	Can add person	17	add_person
50	Can change person	17	change_person
51	Can delete person	17	delete_person
52	Can add time range	18	add_timerange
53	Can change time range	18	change_timerange
54	Can delete time range	18	delete_timerange
55	Can add shipment features	19	add_shipmentfeatures
56	Can change shipment features	19	change_shipmentfeatures
57	Can delete shipment features	19	delete_shipmentfeatures
58	Can add equipment tag	20	add_equipmenttag
59	Can change equipment tag	20	change_equipmenttag
60	Can delete equipment tag	20	delete_equipmenttag
61	Can add global settings	21	add_globalsettings
62	Can change global settings	21	change_globalsettings
63	Can delete global settings	21	delete_globalsettings
64	Can add shipment	22	add_shipment
65	Can change shipment	22	change_shipment
66	Can delete shipment	22	delete_shipment
67	View Shipment	22	view_shipment
68	Can add platform	23	add_platform
69	Can change platform	23	change_platform
70	Can delete platform	23	delete_platform
71	Can add shipment payout	24	add_shipmentpayout
72	Can change shipment payout	24	change_shipmentpayout
73	Can delete shipment payout	24	delete_shipmentpayout
74	Can add shipment request	25	add_shipmentrequest
75	Can change shipment request	25	change_shipmentrequest
76	Can delete shipment request	25	delete_shipmentrequest
77	Can add company division	26	add_companydivision
78	Can change company division	26	change_companydivision
79	Can delete company division	26	delete_companydivision
80	Can add company division membership	27	add_companydivisionmembership
81	Can change company division membership	27	change_companydivisionmembership
82	Can delete company division membership	27	delete_companydivisionmembership
83	Can add generic user	28	add_genericuser
84	Can change generic user	28	change_genericuser
85	Can delete generic user	28	delete_genericuser
86	Can add company relation	29	add_companyrelation
87	Can change company relation	29	change_companyrelation
88	Can delete company relation	29	delete_companyrelation
89	Can add company invite	30	add_companyinvite
90	Can change company invite	30	change_companyinvite
91	Can delete company invite	30	delete_companyinvite
92	Can add shipment assignment	31	add_shipmentassignment
93	Can change shipment assignment	31	change_shipmentassignment
94	Can delete shipment assignment	31	delete_shipmentassignment
95	Can add shipment carrier assignment	32	add_shipmentcarrierassignment
96	Can change shipment carrier assignment	32	change_shipmentcarrierassignment
97	Can delete shipment carrier assignment	32	delete_shipmentcarrierassignment
98	Can add shipment driver assignment	33	add_shipmentdriverassignment
99	Can change shipment driver assignment	33	change_shipmentdriverassignment
100	Can delete shipment driver assignment	33	delete_shipmentdriverassignment
101	Can add demo account	34	add_demoaccount
102	Can change demo account	34	change_demoaccount
103	Can delete demo account	34	delete_demoaccount
104	Can add user invite	35	add_userinvite
105	Can change user invite	35	change_userinvite
106	Can delete user invite	35	delete_userinvite
107	Can add geolocation	36	add_geolocation
108	Can change geolocation	36	change_geolocation
109	Can delete geolocation	36	delete_geolocation
110	Can add cached coordinate	37	add_cachedcoordinate
111	Can change cached coordinate	37	change_cachedcoordinate
112	Can delete cached coordinate	37	delete_cachedcoordinate
113	Can add cached distance	38	add_cacheddistance
114	Can change cached distance	38	change_cacheddistance
115	Can delete cached distance	38	delete_cacheddistance
116	Can add base permission collection	39	add_basepermissioncollection
117	Can change base permission collection	39	change_basepermissioncollection
118	Can delete base permission collection	39	delete_basepermissioncollection
119	Can add base permission	40	add_basepermission
120	Can change base permission	40	change_basepermission
121	Can delete base permission	40	delete_basepermission
122	Can add notification	41	add_notification
123	Can change notification	41	change_notification
124	Can delete notification	41	delete_notification
125	Can add user invite notif	42	add_userinvitenotif
126	Can change user invite notif	42	change_userinvitenotif
127	Can delete user invite notif	42	delete_userinvitenotif
128	Can add shipment assignment notif	43	add_shipmentassignmentnotif
129	Can change shipment assignment notif	43	change_shipmentassignmentnotif
130	Can delete shipment assignment notif	43	delete_shipmentassignmentnotif
131	Can add signup internal notif	44	add_signupinternalnotif
132	Can change signup internal notif	44	change_signupinternalnotif
133	Can delete signup internal notif	44	delete_signupinternalnotif
134	Can add day1	45	add_day1
135	Can change day1	45	change_day1
136	Can delete day1	45	delete_day1
137	Can add day7	46	add_day7
138	Can change day7	46	change_day7
139	Can delete day7	46	delete_day7
140	Can add day15	47	add_day15
141	Can change day15	47	change_day15
142	Can delete day15	47	delete_day15
143	Can add day28	48	add_day28
144	Can change day28	48	change_day28
145	Can delete day28	48	delete_day28
146	Can add day31	49	add_day31
147	Can change day31	49	change_day31
148	Can delete day31	49	delete_day31
149	Can add day38	50	add_day38
150	Can change day38	50	change_day38
151	Can delete day38	50	delete_day38
152	Can add subscription	51	add_subscription
153	Can change subscription	51	change_subscription
154	Can delete subscription	51	delete_subscription
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 154, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
-1		\N	f	AnonymousUser				f	t	2017-07-07 08:37:44.594762+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY authtoken_token (key, created, user_id) FROM stdin;
8d4c4be5e42462319d77c64525d3fb3894ced4f8	2017-07-07 08:37:44.597575+00	-1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	authtoken	token
8	guardian	userobjectpermission
9	guardian	groupobjectpermission
10	shipments	filecontext
11	shipments	insurance
12	shipments	genericcompany
13	shipments	tosacceptance
14	shipments	addressdetails
15	shipments	shipmentlocation
16	shipments	savedlocation
17	shipments	person
18	shipments	timerange
19	shipments	shipmentfeatures
20	shipments	equipmenttag
21	shipments	globalsettings
22	shipments	shipment
23	shipments	platform
24	shipments	shipmentpayout
25	shipments	shipmentrequest
26	shipments	companydivision
27	shipments	companydivisionmembership
28	shipments	genericuser
29	shipments	companyrelation
30	shipments	companyinvite
31	shipments	shipmentassignment
32	shipments	shipmentcarrierassignment
33	shipments	shipmentdriverassignment
34	shipments	demoaccount
35	shipments	userinvite
36	geolocations	geolocation
37	geolocations	cachedcoordinate
38	geolocations	cacheddistance
39	permissions	basepermissioncollection
40	permissions	basepermission
41	notifications	notification
42	notifications	userinvitenotif
43	notifications	shipmentassignmentnotif
44	notifications	signupinternalnotif
45	notifications	day1
46	notifications	day7
47	notifications	day15
48	notifications	day28
49	notifications	day31
50	notifications	day38
51	payments	subscription
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 51, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-07-07 08:36:32.076027+00
2	auth	0001_initial	2017-07-07 08:36:32.304062+00
3	admin	0001_initial	2017-07-07 08:36:32.366142+00
4	contenttypes	0002_remove_content_type_name	2017-07-07 08:36:32.526065+00
5	auth	0002_alter_permission_name_max_length	2017-07-07 08:36:32.560019+00
6	auth	0003_alter_user_email_max_length	2017-07-07 08:36:32.595108+00
7	auth	0004_alter_user_username_opts	2017-07-07 08:36:32.627479+00
8	auth	0005_alter_user_last_login_null	2017-07-07 08:36:32.665583+00
9	auth	0006_require_contenttypes_0002	2017-07-07 08:36:32.667969+00
10	authtoken	0001_initial	2017-07-07 08:36:32.708427+00
11	shipments	0001_initial	2017-07-07 08:36:34.648425+00
12	shipments	0002_carrier_test_migrations_var	2017-07-07 08:36:34.708971+00
13	shipments	0003_remove_carrier_test_migrations_var	2017-07-07 08:36:34.750602+00
14	shipments	0004_globalsettings	2017-07-07 08:36:34.766289+00
15	shipments	0005_location_location_name	2017-07-07 08:36:34.810622+00
16	shipments	0006_auto_20150401_1414	2017-07-07 08:36:35.406577+00
17	shipments	0007_auto_20150401_1417	2017-07-07 08:36:35.500841+00
18	shipments	0008_auto_20150402_1019	2017-07-07 08:36:36.110455+00
19	shipments	0009_shipper_tos	2017-07-07 08:36:36.205749+00
20	shipments	0010_auto_20150410_1658	2017-07-07 08:36:36.305982+00
21	shipments	0011_auto_20150414_1201	2017-07-07 08:36:37.115079+00
22	shipments	0012_tosacceptance	2017-07-07 08:36:37.228225+00
23	shipments	0013_auto_20150416_1134	2017-07-07 08:36:37.448331+00
24	shipments	0014_auto_20150417_1229	2017-07-07 08:36:37.559478+00
25	shipments	0015_auto_20150427_1758	2017-07-07 08:36:37.944556+00
26	shipments	0016_auto_20150501_1535	2017-07-07 08:36:38.848807+00
27	shipments	0017_filecontext_url_ttl	2017-07-07 08:36:38.90229+00
28	shipments	0018_tosacceptance_shipper_user	2017-07-07 08:36:38.965557+00
29	shipments	0019_savedlocation	2017-07-07 08:36:39.035334+00
30	geolocations	0001_initial	2017-07-07 08:36:39.117149+00
31	geolocations	0002_auto_20150601_1237	2017-07-07 08:36:39.240214+00
32	geolocations	0003_auto_20150622_1247	2017-07-07 08:36:40.078491+00
33	geolocations	0004_auto_20150623_1012	2017-07-07 08:36:40.188847+00
34	geolocations	0005_geolocation_display_text	2017-07-07 08:36:40.301508+00
35	geolocations	0006_auto_20150902_1635	2017-07-07 08:36:40.437029+00
36	geolocations	0007_auto_20150909_1231	2017-07-07 08:36:40.59417+00
37	geolocations	0008_cachedcoordinate_cacheddistance	2017-07-07 08:36:40.641901+00
38	guardian	0001_initial	2017-07-07 08:36:41.30971+00
39	shipments	0020_responsestatus	2017-07-07 08:36:41.340999+00
40	shipments	0021_auto_20150519_1810	2017-07-07 08:36:42.01707+00
41	shipments	0022_auto_20150522_1228	2017-07-07 08:36:43.671408+00
42	shipments	0023_auto_20150526_1454	2017-07-07 08:36:47.473113+00
43	shipments	0024_auto_20150526_1859	2017-07-07 08:36:47.486851+00
44	shipments	0025_auto_20150528_1039	2017-07-07 08:36:47.931987+00
45	shipments	0026_auto_20150601_1237	2017-07-07 08:36:48.709275+00
46	shipments	0027_auto_20150602_1557	2017-07-07 08:36:48.729113+00
47	shipments	0028_auto_20150609_1703	2017-07-07 08:36:50.003417+00
48	shipments	0029_auto_20150611_1725	2017-07-07 08:36:50.099877+00
49	shipments	0030_remove_tosacceptance_user	2017-07-07 08:36:50.188628+00
50	shipments	0031_auto_20150619_1135	2017-07-07 08:36:50.377424+00
51	shipments	0032_shipment_carrier_company	2017-07-07 08:36:50.467036+00
52	shipments	0033_auto_20150618_1250	2017-07-07 08:36:50.656223+00
53	shipments	0034_auto_20150618_1757	2017-07-07 08:36:50.917585+00
54	shipments	0035_globalsettings_current_tos_version	2017-07-07 08:36:50.936821+00
55	shipments	0036_auto_20150625_1708	2017-07-07 08:36:51.040179+00
56	shipments	0037_auto_20150728_0734	2017-07-07 08:36:51.139286+00
57	shipments	0038_demoaccount	2017-07-07 08:36:51.265731+00
58	shipments	0039_auto_20150901_1744	2017-07-07 08:36:51.55707+00
59	shipments	0040_auto_20150901_1746	2017-07-07 08:36:51.573591+00
60	shipments	0041_auto_20150901_1753	2017-07-07 08:36:52.429759+00
61	shipments	0042_auto_20150902_1031	2017-07-07 08:36:52.584418+00
62	shipments	0043_genericcompany_company_type	2017-07-07 08:36:52.76483+00
63	shipments	0044_auto_20150902_1635	2017-07-07 08:36:55.111524+00
64	shipments	0045_auto_20150902_1803	2017-07-07 08:36:55.279233+00
65	shipments	0046_auto_20150909_1100	2017-07-07 08:36:55.356269+00
66	shipments	0047_auto_20150909_1115	2017-07-07 08:36:55.660592+00
67	shipments	0048_auto_20150909_1122	2017-07-07 08:36:55.879261+00
68	shipments	0049_auto_20150909_1231	2017-07-07 08:36:56.25207+00
69	shipments	0050_auto_20150909_1635	2017-07-07 08:36:56.798206+00
70	shipments	0051_auto_20150909_1733	2017-07-07 08:36:57.240318+00
71	shipments	0052_auto_20150909_1845	2017-07-07 08:36:58.007449+00
72	permissions	0001_initial	2017-07-07 08:36:58.307292+00
73	shipments	0053_auto_20150911_1333	2017-07-07 08:36:58.822573+00
74	shipments	0054_auto_20150915_1710	2017-07-07 08:36:59.416911+00
75	shipments	0055_auto_20150918_1737	2017-07-07 08:36:59.512578+00
76	shipments	0056_companyinvite_invite_accepted	2017-07-07 08:36:59.594251+00
77	shipments	0057_auto_20151002_1138	2017-07-07 08:36:59.910328+00
78	shipments	0058_auto_20151006_1515	2017-07-07 08:37:01.625637+00
79	shipments	0059_companyinvite_invitee_phone	2017-07-07 08:37:01.742243+00
80	shipments	0060_auto_20151008_0938	2017-07-07 08:37:02.573014+00
81	shipments	0061_auto_20151009_1625	2017-07-07 08:37:03.855659+00
82	shipments	0062_auto_20151012_1059	2017-07-07 08:37:04.072249+00
83	shipments	0063_auto_20151019_1205	2017-07-07 08:37:04.328776+00
84	shipments	0064_auto_20151019_1808	2017-07-07 08:37:04.487378+00
85	shipments	0065_auto_20151020_1332	2017-07-07 08:37:05.354661+00
86	shipments	0066_auto_20151020_1057	2017-07-07 08:37:05.372551+00
87	shipments	0067_auto_20151020_1455	2017-07-07 08:37:13.143165+00
88	shipments	0068_auto_20151020_1702	2017-07-07 08:37:13.464782+00
89	shipments	0069_auto_20151022_1237	2017-07-07 08:37:13.62841+00
90	shipments	0070_auto_20151022_1625	2017-07-07 08:37:13.794036+00
91	shipments	0071_auto_20151026_1639	2017-07-07 08:37:14.007411+00
92	shipments	0072_auto_20151026_1639	2017-07-07 08:37:14.018624+00
93	shipments	0073_auto_20151026_1651	2017-07-07 08:37:14.197633+00
94	shipments	0074_auto_20151026_1654	2017-07-07 08:37:14.37221+00
95	shipments	0075_auto_20151026_1702	2017-07-07 08:37:15.227094+00
96	shipments	0076_auto_20151113_1459	2017-07-07 08:37:18.358818+00
97	shipments	0077_auto_20151113_1507	2017-07-07 08:37:18.638896+00
98	shipments	0078_auto_20151113_1522	2017-07-07 08:37:18.650939+00
99	shipments	0079_auto_20151114_1216	2017-07-07 08:37:19.757683+00
100	shipments	0080_auto_20151116_1822	2017-07-07 08:37:19.959676+00
101	shipments	0081_auto_20151117_1528	2017-07-07 08:37:20.39404+00
102	shipments	0082_auto_20151117_1529	2017-07-07 08:37:20.416278+00
103	shipments	0083_auto_20151117_1542	2017-07-07 08:37:22.775441+00
104	shipments	0084_auto_20151118_2152	2017-07-07 08:37:23.769165+00
105	shipments	0085_auto_20151119_2226	2017-07-07 08:37:25.179679+00
106	shipments	0086_auto_20151124_1509	2017-07-07 08:37:25.194114+00
107	shipments	0087_auto_20151125_1835	2017-07-07 08:37:25.6312+00
108	shipments	0088_auto_20151130_1144	2017-07-07 08:37:26.009105+00
109	shipments	0089_auto_20151208_1410	2017-07-07 08:37:26.174192+00
110	shipments	0090_auto_20160128_1156	2017-07-07 08:37:27.814219+00
111	shipments	0091_auto_20160201_1644	2017-07-07 08:37:28.264852+00
112	shipments	0092_auto_20160203_1505	2017-07-07 08:37:28.735556+00
113	shipments	0093_remove_shipmentlocation_distance_to_next_location	2017-07-07 08:37:28.959273+00
114	shipments	0094_savedlocation_cached_coordinate	2017-07-07 08:37:29.178855+00
115	shipments	0095_remove_addressdetails_coordinate	2017-07-07 08:37:29.380291+00
116	shipments	0096_auto_20160221_1112	2017-07-07 08:37:29.815511+00
117	shipments	0097_auto_20160224_2150	2017-07-07 08:37:30.031736+00
118	shipments	0098_auto_20160225_1524	2017-07-07 08:37:30.055029+00
119	shipments	0099_auto_20160225_1559	2017-07-07 08:37:30.922335+00
120	shipments	0100_auto_20160225_1604	2017-07-07 08:37:31.532661+00
121	shipments	0101_shipment_bol_number	2017-07-07 08:37:31.623473+00
122	shipments	0102_auto_20160321_1626	2017-07-07 08:37:31.952774+00
123	shipments	0103_auto_20160323_1708	2017-07-07 08:37:32.125543+00
124	permissions	0002_auto_20160128_1156	2017-07-07 08:37:33.256476+00
125	permissions	0003_auto_20160225_1613	2017-07-07 08:37:33.277054+00
126	permissions	0004_auto_20160225_1623	2017-07-07 08:37:33.434303+00
127	permissions	0005_auto_20160225_1623	2017-07-07 08:37:33.590235+00
128	permissions	0006_auto_20160323_1708	2017-07-07 08:37:33.754729+00
129	permissions	0007_auto_20160325_1523	2017-07-07 08:37:33.914717+00
130	shipments	0104_auto_20160323_1709	2017-07-07 08:37:33.917475+00
131	shipments	0105_auto_20160325_1523	2017-07-07 08:37:34.258564+00
132	shipments	0106_userinvite_assigner_user	2017-07-07 08:37:34.447211+00
133	shipments	0107_auto_20160407_1057	2017-07-07 08:37:35.039971+00
134	shipments	0108_auto_20160421_1521	2017-07-07 08:37:35.880483+00
135	shipments	0109_auto_20160421_1542	2017-07-07 08:37:35.901208+00
136	shipments	0110_auto_20160422_1126	2017-07-07 08:37:36.095233+00
137	shipments	0111_auto_20160502_1636	2017-07-07 08:37:36.255078+00
138	shipments	0112_auto_20160509_1513	2017-07-07 08:37:36.561658+00
139	shipments	0113_auto_20160509_1530	2017-07-07 08:37:36.764775+00
140	shipments	0114_auto_20160510_1152	2017-07-07 08:37:36.996336+00
141	shipments	0115_auto_20160510_1344	2017-07-07 08:37:37.106711+00
142	payments	0001_initial	2017-07-07 08:37:37.123933+00
143	shipments	0116_genericcompany_subscription	2017-07-07 08:37:37.221007+00
144	shipments	0117_auto_20160609_0954	2017-07-07 08:37:37.431754+00
145	shipments	0118_remove_genericcompany_max_users	2017-07-07 08:37:37.563463+00
146	shipments	0119_auto_20160622_0944	2017-07-07 08:37:37.67897+00
147	shipments	0120_auto_20160622_1433	2017-07-07 08:37:37.91739+00
148	shipments	0121_auto_20160623_1121	2017-07-07 08:37:38.15877+00
149	notifications	0001_initial	2017-07-07 08:37:41.018617+00
150	notifications	0002_signupinternalnotif	2017-07-07 08:37:41.287241+00
151	notifications	0003_notification_use_html_template	2017-07-07 08:37:41.573495+00
152	notifications	0004_notification_email_sent	2017-07-07 08:37:41.866771+00
153	notifications	0005_auto_20160623_1308	2017-07-07 08:37:43.619679+00
154	payments	0002_auto_20160613_1201	2017-07-07 08:37:44.001571+00
155	payments	0003_auto_20160622_1217	2017-07-07 08:37:44.12788+00
156	permissions	0008_auto_20160622_1433	2017-07-07 08:37:44.283065+00
157	permissions	0009_auto_20160623_1121	2017-07-07 08:37:44.441962+00
158	sessions	0001_initial	2017-07-07 08:37:44.473217+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_migrations_id_seq', 158, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: geolocations_cachedcoordinate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY geolocations_cachedcoordinate (id, created_at, updated_at, address, address_2, zip_code, city, state, coordinate) FROM stdin;
\.


--
-- Name: geolocations_cachedcoordinate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('geolocations_cachedcoordinate_id_seq', 1, false);


--
-- Data for Name: geolocations_cacheddistance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY geolocations_cacheddistance (id, created_at, updated_at, start_lat, end_lat, start_lon, end_lon, distance) FROM stdin;
\.


--
-- Name: geolocations_cacheddistance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('geolocations_cacheddistance_id_seq', 1, false);


--
-- Data for Name: geolocations_geolocation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY geolocations_geolocation (id, latitude, longitude, altitude, accuracy, speed, course, "timestamp", carrier_id, driver_id, shipment_id, display_text) FROM stdin;
\.


--
-- Name: geolocations_geolocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('geolocations_geolocation_id_seq', 1, false);


--
-- Data for Name: guardian_groupobjectpermission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY guardian_groupobjectpermission (id, object_pk, content_type_id, group_id, permission_id) FROM stdin;
\.


--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('guardian_groupobjectpermission_id_seq', 1, false);


--
-- Data for Name: guardian_userobjectpermission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY guardian_userobjectpermission (id, object_pk, content_type_id, permission_id, user_id) FROM stdin;
\.


--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('guardian_userobjectpermission_id_seq', 1, false);


--
-- Data for Name: notifications_day1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day1 (id, receiver_id) FROM stdin;
\.


--
-- Data for Name: notifications_day15; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day15 (id, receiver_id) FROM stdin;
\.


--
-- Name: notifications_day15_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day15_id_seq', 1, false);


--
-- Name: notifications_day1_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day1_id_seq', 1, false);


--
-- Data for Name: notifications_day28; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day28 (id, receiver_id) FROM stdin;
\.


--
-- Name: notifications_day28_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day28_id_seq', 1, false);


--
-- Data for Name: notifications_day31; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day31 (id, receiver_id) FROM stdin;
\.


--
-- Name: notifications_day31_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day31_id_seq', 1, false);


--
-- Data for Name: notifications_day38; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day38 (id, receiver_id) FROM stdin;
\.


--
-- Name: notifications_day38_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day38_id_seq', 1, false);


--
-- Data for Name: notifications_day7; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_day7 (id, receiver_id) FROM stdin;
\.


--
-- Name: notifications_day7_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_day7_id_seq', 1, false);


--
-- Data for Name: notifications_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_notification (id, created_at, updated_at, parent_object_id, sender_email, sender_name, receiver_name, receiver_email, email_subject, email_content_html, email_content_raw, parent_content_type_id, receiver_id, sender_id, use_html_template, email_sent, email_content_html_file, email_mergevars) FROM stdin;
\.


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_notification_id_seq', 1, false);


--
-- Data for Name: notifications_shipmentassignmentnotif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_shipmentassignmentnotif (id, sender_id, shipment_assignment_id) FROM stdin;
\.


--
-- Name: notifications_shipmentassignmentnotif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_shipmentassignmentnotif_id_seq', 1, false);


--
-- Data for Name: notifications_shipmentassignmentnotif_receivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_shipmentassignmentnotif_receivers (id, shipmentassignmentnotif_id, genericuser_id) FROM stdin;
\.


--
-- Name: notifications_shipmentassignmentnotif_receivers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_shipmentassignmentnotif_receivers_id_seq', 1, false);


--
-- Data for Name: notifications_signupinternalnotif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_signupinternalnotif (id, company_id) FROM stdin;
\.


--
-- Name: notifications_signupinternalnotif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_signupinternalnotif_id_seq', 1, false);


--
-- Data for Name: notifications_userinvitenotif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications_userinvitenotif (id, receiver_email, receiver_name, invite_id, sender_id) FROM stdin;
\.


--
-- Name: notifications_userinvitenotif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('notifications_userinvitenotif_id_seq', 1, false);


--
-- Data for Name: payments_subscription; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY payments_subscription (id, no_users, no_trucks, annual_plan, payment_ready, trial_length, trial_start) FROM stdin;
\.


--
-- Name: payments_subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('payments_subscription_id_seq', 1, false);


--
-- Data for Name: permissions_basepermission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY permissions_basepermission (id, name, is_set, is_editable, permission_id, permission_collection_id) FROM stdin;
\.


--
-- Name: permissions_basepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('permissions_basepermission_id_seq', 1, false);


--
-- Data for Name: permissions_basepermissioncollection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY permissions_basepermissioncollection (id, user_type) FROM stdin;
\.


--
-- Name: permissions_basepermissioncollection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('permissions_basepermissioncollection_id_seq', 1, false);


--
-- Data for Name: shipments_addressdetails; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_addressdetails (id, address, address_2, zip_code, city, state, created_at, updated_at) FROM stdin;
\.


--
-- Name: shipments_addressdetails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_addressdetails_id_seq', 1, false);


--
-- Data for Name: shipments_companydivision; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_companydivision (id, created_at, updated_at, name, company_id) FROM stdin;
\.


--
-- Name: shipments_companydivision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_companydivision_id_seq', 1, false);


--
-- Data for Name: shipments_companydivisionmembership; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_companydivisionmembership (id, created_at, updated_at, division_id, user_id) FROM stdin;
\.


--
-- Name: shipments_companydivisionmembership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_companydivisionmembership_id_seq', 1, false);


--
-- Data for Name: shipments_companyinvite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_companyinvite (id, invitee_name, invitee_email, invitee_dot, inviter_company_id, inviter_user_id, invite_accepted, invitee_phone, created_at, updated_at, invitee_company_type) FROM stdin;
\.


--
-- Name: shipments_companyinvite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_companyinvite_id_seq', 1, false);


--
-- Data for Name: shipments_companyrelation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_companyrelation (id, is_inviter, active, hidden, relation_from_id, relation_to_id, sibling_id, created_at, updated_at) FROM stdin;
\.


--
-- Name: shipments_companyrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_companyrelation_id_seq', 1, false);


--
-- Data for Name: shipments_demoaccount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_demoaccount (id, created_at, updated_at, email, password, first_name, last_name, phone, company_name, no_of_shipments, company_id, dot, no_of_connections, demo_account_type) FROM stdin;
\.


--
-- Data for Name: shipments_demoaccount_connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_demoaccount_connections (id, demoaccount_id, genericcompany_id) FROM stdin;
\.


--
-- Name: shipments_demoaccount_connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_demoaccount_connections_id_seq', 1, false);


--
-- Name: shipments_demoaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_demoaccount_id_seq', 1, false);


--
-- Data for Name: shipments_equipmenttag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_equipmenttag (id, created_at, updated_at, tag_category, tag_type, assignee_id, assignee_content_type_id, assigner_id) FROM stdin;
\.


--
-- Name: shipments_equipmenttag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_equipmenttag_id_seq', 1, false);


--
-- Data for Name: shipments_filecontext; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_filecontext (id, created_at, updated_at, uuid_value, path, url_ttl) FROM stdin;
\.


--
-- Name: shipments_filecontext_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_filecontext_id_seq', 1, false);


--
-- Data for Name: shipments_genericcompany; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_genericcompany (id, company_name, verified, rejected, insurance_id, owner_id, created_at, updated_at, dot, is_fleet, max_requests, city, state, company_type, logo_id, subscription_id, registration_complete) FROM stdin;
\.


--
-- Name: shipments_genericcompany_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_genericcompany_id_seq', 1, false);


--
-- Data for Name: shipments_genericuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_genericuser (id, email, first_name, last_name, user_id, profile_photo_id, created_at, updated_at, permissions_id, last_location, last_location_timestamp, vehicle_type, tos_acceptance_id, company_id, phone, user_type, inactive) FROM stdin;
\.


--
-- Name: shipments_genericuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_genericuser_id_seq', 1, false);


--
-- Data for Name: shipments_globalsettings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_globalsettings (id, shipment_id_counter, current_tos_version) FROM stdin;
\.


--
-- Name: shipments_globalsettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_globalsettings_id_seq', 1, false);


--
-- Data for Name: shipments_insurance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_insurance (id, policy_url) FROM stdin;
\.


--
-- Name: shipments_insurance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_insurance_id_seq', 1, false);


--
-- Name: shipments_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_location_id_seq', 1, false);


--
-- Data for Name: shipments_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_person (id, created_at, updated_at, first_name, last_name, email, phone) FROM stdin;
\.


--
-- Name: shipments_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_person_id_seq', 1, false);


--
-- Data for Name: shipments_platform; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_platform (id, platform_type, identifier, allow_notifications, user_id, is_primary_email) FROM stdin;
\.


--
-- Name: shipments_platform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_platform_id_seq', 1, false);


--
-- Data for Name: shipments_savedlocation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_savedlocation (id, created_at, updated_at, saved_location_name, saved, owner_id, contact_id, dock, company_name, appointment_id, comments, features_id, location_type, time_range_id, address_details_id, cached_coordinate_id) FROM stdin;
\.


--
-- Name: shipments_savedlocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_savedlocation_id_seq', 1, false);


--
-- Data for Name: shipments_shipment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipment (id, created_at, updated_at, shipment_id, carrier_is_approved, delivery_status, owner_id, carrier_id, owner_user_id, payout_info_id, comments, first_location_id, last_location_id, next_trip_dist_update, bol_number, carrier_assignment_id, driver_assignment_id) FROM stdin;
\.


--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipment_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentassignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentassignment (id, parent_id, assignee_id, can_delegate, notify, r, u, d, assignee_content_type_id, assigner_id, parent_content_type_id, shipment_id, created_at, updated_at) FROM stdin;
\.


--
-- Name: shipments_shipmentassignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentassignment_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentcarrierassignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentcarrierassignment (id, assignment_id) FROM stdin;
\.


--
-- Name: shipments_shipmentcarrierassignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentcarrierassignment_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentdriverassignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentdriverassignment (id, assignment_id) FROM stdin;
\.


--
-- Name: shipments_shipmentdriverassignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentdriverassignment_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentfeatures; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentfeatures (id, weight, palletized, pallet_number, pallet_length, pallet_width, pallet_height, extra_details, comments) FROM stdin;
\.


--
-- Name: shipments_shipmentfeatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentfeatures_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentlocation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentlocation (id, created_at, updated_at, saved, contact_id, dock, company_name, appointment_id, comments, features_id, location_type, shipment_id, time_range_id, arrival_time, address_details_id, next_location_id, cached_coordinate_id, cached_distance_id) FROM stdin;
\.


--
-- Data for Name: shipments_shipmentpayout; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentpayout (id, payout, comments) FROM stdin;
\.


--
-- Name: shipments_shipmentpayout_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentpayout_id_seq', 1, false);


--
-- Data for Name: shipments_shipmentrequest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_shipmentrequest (id, rejected, carrier_id, driver_id, shipment_id) FROM stdin;
\.


--
-- Name: shipments_shipmentrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_shipmentrequest_id_seq', 1, false);


--
-- Data for Name: shipments_timerange; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_timerange (id, time_range_start, time_range_end, tz) FROM stdin;
\.


--
-- Name: shipments_timerange_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_timerange_id_seq', 1, false);


--
-- Data for Name: shipments_tosacceptance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_tosacceptance (id, created_at, tos_status, tos_updated_at, tos_version) FROM stdin;
\.


--
-- Name: shipments_tosacceptance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_tosacceptance_id_seq', 1, false);


--
-- Data for Name: shipments_userinvite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY shipments_userinvite (id, created_at, updated_at, token, email, user_type, first_name, last_name, company_id, user_id, assigner_user_id) FROM stdin;
\.


--
-- Name: shipments_userinvite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('shipments_userinvite_id_seq', 1, false);


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY spatial_ref_sys  FROM stdin;
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: geolocations_cachedcoordinate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_cachedcoordinate
    ADD CONSTRAINT geolocations_cachedcoordinate_pkey PRIMARY KEY (id);


--
-- Name: geolocations_cacheddistance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_cacheddistance
    ADD CONSTRAINT geolocations_cacheddistance_pkey PRIMARY KEY (id);


--
-- Name: geolocations_geolocation_carrier_id_2b8cf1d3507a7bd5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation
    ADD CONSTRAINT geolocations_geolocation_carrier_id_2b8cf1d3507a7bd5_uniq UNIQUE (carrier_id, driver_id, "timestamp");


--
-- Name: geolocations_geolocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation
    ADD CONSTRAINT geolocations_geolocation_pkey PRIMARY KEY (id);


--
-- Name: guardian_groupobjectpermission_group_id_1692da556eb7175b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_group_id_1692da556eb7175b_uniq UNIQUE (group_id, permission_id, object_pk);


--
-- Name: guardian_groupobjectpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_pkey PRIMARY KEY (id);


--
-- Name: guardian_userobjectpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_pkey PRIMARY KEY (id);


--
-- Name: guardian_userobjectpermission_user_id_3d019018f740de5f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_user_id_3d019018f740de5f_uniq UNIQUE (user_id, permission_id, object_pk);


--
-- Name: notifications_day15_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day15
    ADD CONSTRAINT notifications_day15_pkey PRIMARY KEY (id);


--
-- Name: notifications_day15_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day15
    ADD CONSTRAINT notifications_day15_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_day1_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day1
    ADD CONSTRAINT notifications_day1_pkey PRIMARY KEY (id);


--
-- Name: notifications_day1_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day1
    ADD CONSTRAINT notifications_day1_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_day28_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day28
    ADD CONSTRAINT notifications_day28_pkey PRIMARY KEY (id);


--
-- Name: notifications_day28_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day28
    ADD CONSTRAINT notifications_day28_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_day31_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day31
    ADD CONSTRAINT notifications_day31_pkey PRIMARY KEY (id);


--
-- Name: notifications_day31_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day31
    ADD CONSTRAINT notifications_day31_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_day38_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day38
    ADD CONSTRAINT notifications_day38_pkey PRIMARY KEY (id);


--
-- Name: notifications_day38_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day38
    ADD CONSTRAINT notifications_day38_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_day7_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day7
    ADD CONSTRAINT notifications_day7_pkey PRIMARY KEY (id);


--
-- Name: notifications_day7_receiver_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day7
    ADD CONSTRAINT notifications_day7_receiver_id_key UNIQUE (receiver_id);


--
-- Name: notifications_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_notification
    ADD CONSTRAINT notifications_notification_pkey PRIMARY KEY (id);


--
-- Name: notifications_shipmentassignm_shipmentassignmentnotif_id_ge_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif_receivers
    ADD CONSTRAINT notifications_shipmentassignm_shipmentassignmentnotif_id_ge_key UNIQUE (shipmentassignmentnotif_id, genericuser_id);


--
-- Name: notifications_shipmentassignmentnotif_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif
    ADD CONSTRAINT notifications_shipmentassignmentnotif_pkey PRIMARY KEY (id);


--
-- Name: notifications_shipmentassignmentnotif_receivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif_receivers
    ADD CONSTRAINT notifications_shipmentassignmentnotif_receivers_pkey PRIMARY KEY (id);


--
-- Name: notifications_signupinternalnotif_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_signupinternalnotif
    ADD CONSTRAINT notifications_signupinternalnotif_pkey PRIMARY KEY (id);


--
-- Name: notifications_userinvitenotif_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_userinvitenotif
    ADD CONSTRAINT notifications_userinvitenotif_pkey PRIMARY KEY (id);


--
-- Name: payments_subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY payments_subscription
    ADD CONSTRAINT payments_subscription_pkey PRIMARY KEY (id);


--
-- Name: permissions_basepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermission
    ADD CONSTRAINT permissions_basepermission_pkey PRIMARY KEY (id);


--
-- Name: permissions_basepermissioncollection_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermissioncollection
    ADD CONSTRAINT permissions_basepermissioncollection_pkey PRIMARY KEY (id);


--
-- Name: shipments_addressdetails_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_addressdetails
    ADD CONSTRAINT shipments_addressdetails_pkey PRIMARY KEY (id);


--
-- Name: shipments_companydivision_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivision
    ADD CONSTRAINT shipments_companydivision_pkey PRIMARY KEY (id);


--
-- Name: shipments_companydivisionmembership_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivisionmembership
    ADD CONSTRAINT shipments_companydivisionmembership_pkey PRIMARY KEY (id);


--
-- Name: shipments_companyinvit_inviter_company_id_612d6f7f1d8fdb75_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite
    ADD CONSTRAINT shipments_companyinvit_inviter_company_id_612d6f7f1d8fdb75_uniq UNIQUE (inviter_company_id, invitee_dot);


--
-- Name: shipments_companyinvite_inviter_company_id_766b3b36959b37e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite
    ADD CONSTRAINT shipments_companyinvite_inviter_company_id_766b3b36959b37e_uniq UNIQUE (inviter_company_id, invitee_email);


--
-- Name: shipments_companyinvite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite
    ADD CONSTRAINT shipments_companyinvite_pkey PRIMARY KEY (id);


--
-- Name: shipments_companyrelatio_relation_from_id_62ad0c3657cd24e9_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation
    ADD CONSTRAINT shipments_companyrelatio_relation_from_id_62ad0c3657cd24e9_uniq UNIQUE (relation_from_id, relation_to_id);


--
-- Name: shipments_companyrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation
    ADD CONSTRAINT shipments_companyrelation_pkey PRIMARY KEY (id);


--
-- Name: shipments_demoaccount_connect_demoaccount_id_genericcompany_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount_connections
    ADD CONSTRAINT shipments_demoaccount_connect_demoaccount_id_genericcompany_key UNIQUE (demoaccount_id, genericcompany_id);


--
-- Name: shipments_demoaccount_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount_connections
    ADD CONSTRAINT shipments_demoaccount_connections_pkey PRIMARY KEY (id);


--
-- Name: shipments_demoaccount_dot_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount
    ADD CONSTRAINT shipments_demoaccount_dot_key UNIQUE (dot);


--
-- Name: shipments_demoaccount_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount
    ADD CONSTRAINT shipments_demoaccount_email_key UNIQUE (email);


--
-- Name: shipments_demoaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount
    ADD CONSTRAINT shipments_demoaccount_pkey PRIMARY KEY (id);


--
-- Name: shipments_equipmenttag_assignee_id_6743320a88405c48_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_equipmenttag
    ADD CONSTRAINT shipments_equipmenttag_assignee_id_6743320a88405c48_uniq UNIQUE (assignee_id, assignee_content_type_id, tag_type, tag_category);


--
-- Name: shipments_equipmenttag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_equipmenttag
    ADD CONSTRAINT shipments_equipmenttag_pkey PRIMARY KEY (id);


--
-- Name: shipments_filecontext_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_filecontext
    ADD CONSTRAINT shipments_filecontext_pkey PRIMARY KEY (id);


--
-- Name: shipments_genericcompany_dot1_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_genericcompany_dot1_key UNIQUE (dot);


--
-- Name: shipments_genericcompany_insurance_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_genericcompany_insurance_id_key UNIQUE (insurance_id);


--
-- Name: shipments_genericcompany_logo_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_genericcompany_logo_id_key UNIQUE (logo_id);


--
-- Name: shipments_genericcompany_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_genericcompany_pkey PRIMARY KEY (id);


--
-- Name: shipments_genericcompany_subscription_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_genericcompany_subscription_id_key UNIQUE (subscription_id);


--
-- Name: shipments_genericuser_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_email_key UNIQUE (email);


--
-- Name: shipments_genericuser_permissions_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_permissions_id_key UNIQUE (permissions_id);


--
-- Name: shipments_genericuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_pkey PRIMARY KEY (id);


--
-- Name: shipments_genericuser_profile_photo_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_profile_photo_id_key UNIQUE (profile_photo_id);


--
-- Name: shipments_genericuser_tos_acceptance_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_tos_acceptance_id_key UNIQUE (tos_acceptance_id);


--
-- Name: shipments_genericuser_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_user_id_key UNIQUE (user_id);


--
-- Name: shipments_globalsettings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_globalsettings
    ADD CONSTRAINT shipments_globalsettings_pkey PRIMARY KEY (id);


--
-- Name: shipments_insurance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_insurance
    ADD CONSTRAINT shipments_insurance_pkey PRIMARY KEY (id);


--
-- Name: shipments_location_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_location_contact_id_key UNIQUE (contact_id);


--
-- Name: shipments_location_features_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_location_features_id_key UNIQUE (features_id);


--
-- Name: shipments_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_location_pkey PRIMARY KEY (id);


--
-- Name: shipments_location_time_range_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_location_time_range_id_key UNIQUE (time_range_id);


--
-- Name: shipments_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_person
    ADD CONSTRAINT shipments_person_pkey PRIMARY KEY (id);


--
-- Name: shipments_platform_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_platform
    ADD CONSTRAINT shipments_platform_pkey PRIMARY KEY (id);


--
-- Name: shipments_savedlocation_address_details_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_savedlocation_address_details_id_key UNIQUE (address_details_id);


--
-- Name: shipments_savedlocation_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_savedlocation_contact_id_key UNIQUE (contact_id);


--
-- Name: shipments_savedlocation_features_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_savedlocation_features_id_key UNIQUE (features_id);


--
-- Name: shipments_savedlocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_savedlocation_pkey PRIMARY KEY (id);


--
-- Name: shipments_savedlocation_time_range_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_savedlocation_time_range_id_key UNIQUE (time_range_id);


--
-- Name: shipments_shipment_carrier_assignment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_carrier_assignment_id_key UNIQUE (carrier_assignment_id);


--
-- Name: shipments_shipment_driver_assignment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_driver_assignment_id_key UNIQUE (driver_assignment_id);


--
-- Name: shipments_shipment_first_location_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_first_location_id_key UNIQUE (first_location_id);


--
-- Name: shipments_shipment_last_location_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_last_location_id_key UNIQUE (last_location_id);


--
-- Name: shipments_shipment_payout_info_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_payout_info_id_key UNIQUE (payout_info_id);


--
-- Name: shipments_shipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipments_shipment_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentassignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment
    ADD CONSTRAINT shipments_shipmentassignment_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentcarrierassignment_assignment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentcarrierassignment
    ADD CONSTRAINT shipments_shipmentcarrierassignment_assignment_id_key UNIQUE (assignment_id);


--
-- Name: shipments_shipmentcarrierassignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentcarrierassignment
    ADD CONSTRAINT shipments_shipmentcarrierassignment_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentdriverassignment_assignment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentdriverassignment
    ADD CONSTRAINT shipments_shipmentdriverassignment_assignment_id_key UNIQUE (assignment_id);


--
-- Name: shipments_shipmentdriverassignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentdriverassignment
    ADD CONSTRAINT shipments_shipmentdriverassignment_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentfeatures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentfeatures
    ADD CONSTRAINT shipments_shipmentfeatures_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentlocation_address_details_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_shipmentlocation_address_details_id_key UNIQUE (address_details_id);


--
-- Name: shipments_shipmentpayout_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentpayout
    ADD CONSTRAINT shipments_shipmentpayout_pkey PRIMARY KEY (id);


--
-- Name: shipments_shipmentrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentrequest
    ADD CONSTRAINT shipments_shipmentrequest_pkey PRIMARY KEY (id);


--
-- Name: shipments_timerange_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_timerange
    ADD CONSTRAINT shipments_timerange_pkey PRIMARY KEY (id);


--
-- Name: shipments_tosacceptance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_tosacceptance
    ADD CONSTRAINT shipments_tosacceptance_pkey PRIMARY KEY (id);


--
-- Name: shipments_userinvite_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT shipments_userinvite_email_key UNIQUE (email);


--
-- Name: shipments_userinvite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT shipments_userinvite_pkey PRIMARY KEY (id);


--
-- Name: shipments_userinvite_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT shipments_userinvite_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_7222ec672cd32dcd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_7222ec672cd32dcd_like ON authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: geolocations_cachedcoordinate_coordinate_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX geolocations_cachedcoordinate_coordinate_id ON geolocations_cachedcoordinate USING gist (coordinate);


--
-- Name: geolocations_geolocation_17565772; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX geolocations_geolocation_17565772 ON geolocations_geolocation USING btree (driver_id);


--
-- Name: geolocations_geolocation_c77cffaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX geolocations_geolocation_c77cffaa ON geolocations_geolocation USING btree (shipment_id);


--
-- Name: geolocations_geolocation_ed09056b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX geolocations_geolocation_ed09056b ON geolocations_geolocation USING btree (carrier_id);


--
-- Name: guardian_groupobjectpermission_0e939a4f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_groupobjectpermission_0e939a4f ON guardian_groupobjectpermission USING btree (group_id);


--
-- Name: guardian_groupobjectpermission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_groupobjectpermission_417f1b1c ON guardian_groupobjectpermission USING btree (content_type_id);


--
-- Name: guardian_groupobjectpermission_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_groupobjectpermission_8373b171 ON guardian_groupobjectpermission USING btree (permission_id);


--
-- Name: guardian_userobjectpermission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_userobjectpermission_417f1b1c ON guardian_userobjectpermission USING btree (content_type_id);


--
-- Name: guardian_userobjectpermission_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_userobjectpermission_8373b171 ON guardian_userobjectpermission USING btree (permission_id);


--
-- Name: guardian_userobjectpermission_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX guardian_userobjectpermission_e8701ad4 ON guardian_userobjectpermission USING btree (user_id);


--
-- Name: notifications_notification_1446a827; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_notification_1446a827 ON notifications_notification USING btree (parent_content_type_id);


--
-- Name: notifications_notification_924b1846; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_notification_924b1846 ON notifications_notification USING btree (sender_id);


--
-- Name: notifications_notification_d41c2251; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_notification_d41c2251 ON notifications_notification USING btree (receiver_id);


--
-- Name: notifications_shipmentassignmentnotif_924b1846; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_shipmentassignmentnotif_924b1846 ON notifications_shipmentassignmentnotif USING btree (sender_id);


--
-- Name: notifications_shipmentassignmentnotif_dced54d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_shipmentassignmentnotif_dced54d1 ON notifications_shipmentassignmentnotif USING btree (shipment_assignment_id);


--
-- Name: notifications_shipmentassignmentnotif_receivers_49169a5b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_shipmentassignmentnotif_receivers_49169a5b ON notifications_shipmentassignmentnotif_receivers USING btree (shipmentassignmentnotif_id);


--
-- Name: notifications_shipmentassignmentnotif_receivers_e5bbc5df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_shipmentassignmentnotif_receivers_e5bbc5df ON notifications_shipmentassignmentnotif_receivers USING btree (genericuser_id);


--
-- Name: notifications_signupinternalnotif_447d3092; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_signupinternalnotif_447d3092 ON notifications_signupinternalnotif USING btree (company_id);


--
-- Name: notifications_userinvitenotif_28a44ea5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_userinvitenotif_28a44ea5 ON notifications_userinvitenotif USING btree (invite_id);


--
-- Name: notifications_userinvitenotif_924b1846; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notifications_userinvitenotif_924b1846 ON notifications_userinvitenotif USING btree (sender_id);


--
-- Name: permissions_basepermission_23be6630; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX permissions_basepermission_23be6630 ON permissions_basepermission USING btree (permission_collection_id);


--
-- Name: permissions_basepermission_8373b171; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX permissions_basepermission_8373b171 ON permissions_basepermission USING btree (permission_id);


--
-- Name: shipments_companydivision_447d3092; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companydivision_447d3092 ON shipments_companydivision USING btree (company_id);


--
-- Name: shipments_companydivisionmembership_9ff3405c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companydivisionmembership_9ff3405c ON shipments_companydivisionmembership USING btree (division_id);


--
-- Name: shipments_companydivisionmembership_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companydivisionmembership_e8701ad4 ON shipments_companydivisionmembership USING btree (user_id);


--
-- Name: shipments_companyinvite_6e1810ba; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companyinvite_6e1810ba ON shipments_companyinvite USING btree (inviter_user_id);


--
-- Name: shipments_companyinvite_702ddb79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companyinvite_702ddb79 ON shipments_companyinvite USING btree (inviter_company_id);


--
-- Name: shipments_companyrelation_c9f430f8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companyrelation_c9f430f8 ON shipments_companyrelation USING btree (relation_to_id);


--
-- Name: shipments_companyrelation_da8f6ecf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companyrelation_da8f6ecf ON shipments_companyrelation USING btree (relation_from_id);


--
-- Name: shipments_companyrelation_ecb096c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_companyrelation_ecb096c3 ON shipments_companyrelation USING btree (sibling_id);


--
-- Name: shipments_demoaccount_447d3092; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_demoaccount_447d3092 ON shipments_demoaccount USING btree (company_id);


--
-- Name: shipments_demoaccount_connections_291df9c9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_demoaccount_connections_291df9c9 ON shipments_demoaccount_connections USING btree (genericcompany_id);


--
-- Name: shipments_demoaccount_connections_f428c985; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_demoaccount_connections_f428c985 ON shipments_demoaccount_connections USING btree (demoaccount_id);


--
-- Name: shipments_demoaccount_email_d13fd6f9d43950b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_demoaccount_email_d13fd6f9d43950b_like ON shipments_demoaccount USING btree (email varchar_pattern_ops);


--
-- Name: shipments_equipmenttag_490b4fcb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_equipmenttag_490b4fcb ON shipments_equipmenttag USING btree (assignee_content_type_id);


--
-- Name: shipments_equipmenttag_a5910953; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_equipmenttag_a5910953 ON shipments_equipmenttag USING btree (assigner_id);


--
-- Name: shipments_genericcompany_5e7b1936; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_genericcompany_5e7b1936 ON shipments_genericcompany USING btree (owner_id);


--
-- Name: shipments_genericuser_73e6726d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_genericuser_73e6726d ON shipments_genericuser USING btree (company_id);


--
-- Name: shipments_genericuser_email_9a35a1165eff503_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_genericuser_email_9a35a1165eff503_like ON shipments_genericuser USING btree (email varchar_pattern_ops);


--
-- Name: shipments_genericuser_last_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_genericuser_last_location_id ON shipments_genericuser USING gist (last_location);


--
-- Name: shipments_location_c77cffaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_location_c77cffaa ON shipments_shipmentlocation USING btree (shipment_id);


--
-- Name: shipments_platform_e8701ad4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_platform_e8701ad4 ON shipments_platform USING btree (user_id);


--
-- Name: shipments_savedlocation_11e46a51; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_savedlocation_11e46a51 ON shipments_savedlocation USING btree (cached_coordinate_id);


--
-- Name: shipments_savedlocation_5e7b1936; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_savedlocation_5e7b1936 ON shipments_savedlocation USING btree (owner_id);


--
-- Name: shipments_shipment_5e7b1936; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipment_5e7b1936 ON shipments_shipment USING btree (owner_id);


--
-- Name: shipments_shipment_68d3ca96; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipment_68d3ca96 ON shipments_shipment USING btree (owner_user_id);


--
-- Name: shipments_shipment_8ef9de64; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipment_8ef9de64 ON shipments_shipment USING btree (carrier_id);


--
-- Name: shipments_shipmentassignment_1446a827; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentassignment_1446a827 ON shipments_shipmentassignment USING btree (parent_content_type_id);


--
-- Name: shipments_shipmentassignment_490b4fcb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentassignment_490b4fcb ON shipments_shipmentassignment USING btree (assignee_content_type_id);


--
-- Name: shipments_shipmentassignment_a5910953; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentassignment_a5910953 ON shipments_shipmentassignment USING btree (assigner_id);


--
-- Name: shipments_shipmentassignment_c77cffaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentassignment_c77cffaa ON shipments_shipmentassignment USING btree (shipment_id);


--
-- Name: shipments_shipmentlocation_11e46a51; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentlocation_11e46a51 ON shipments_shipmentlocation USING btree (cached_coordinate_id);


--
-- Name: shipments_shipmentlocation_9b0c834e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentlocation_9b0c834e ON shipments_shipmentlocation USING btree (next_location_id);


--
-- Name: shipments_shipmentlocation_e00b6916; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentlocation_e00b6916 ON shipments_shipmentlocation USING btree (cached_distance_id);


--
-- Name: shipments_shipmentrequest_17565772; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentrequest_17565772 ON shipments_shipmentrequest USING btree (driver_id);


--
-- Name: shipments_shipmentrequest_c77cffaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentrequest_c77cffaa ON shipments_shipmentrequest USING btree (shipment_id);


--
-- Name: shipments_shipmentrequest_ed09056b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_shipmentrequest_ed09056b ON shipments_shipmentrequest USING btree (carrier_id);


--
-- Name: shipments_userinvite_21ef16fd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_userinvite_21ef16fd ON shipments_userinvite USING btree (assigner_user_id);


--
-- Name: shipments_userinvite_447d3092; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_userinvite_447d3092 ON shipments_userinvite USING btree (company_id);


--
-- Name: shipments_userinvite_email_c8ce3fbfbf5005a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX shipments_userinvite_email_c8ce3fbfbf5005a_like ON shipments_userinvite USING btree (email varchar_pattern_ops);


--
-- Name: D0a7cd4c0bcff68acf4d306c0656a0d3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT "D0a7cd4c0bcff68acf4d306c0656a0d3" FOREIGN KEY (permissions_id) REFERENCES permissions_basepermissioncollection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D0e9395ad10cd26125d591ea471b0e68; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT "D0e9395ad10cd26125d591ea471b0e68" FOREIGN KEY (cached_coordinate_id) REFERENCES geolocations_cachedcoordinate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D10e0213eeb0d58862d6803b37ee806b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif_receivers
    ADD CONSTRAINT "D10e0213eeb0d58862d6803b37ee806b" FOREIGN KEY (shipmentassignmentnotif_id) REFERENCES notifications_shipmentassignmentnotif(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D156fa6c70950fa3c6775c02fdb4c6bc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation
    ADD CONSTRAINT "D156fa6c70950fa3c6775c02fdb4c6bc" FOREIGN KEY (relation_from_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D1ad257ad172829a6f287f64da3eff38; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT "D1ad257ad172829a6f287f64da3eff38" FOREIGN KEY (next_location_id) REFERENCES shipments_shipmentlocation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D4430e37103e93d50c0ca000788dbfbd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT "D4430e37103e93d50c0ca000788dbfbd" FOREIGN KEY (cached_coordinate_id) REFERENCES geolocations_cachedcoordinate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D4fb23213b148b813244d2d726bf6197; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT "D4fb23213b148b813244d2d726bf6197" FOREIGN KEY (cached_distance_id) REFERENCES geolocations_cacheddistance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D5c50dde621d132df91a530bde1233b6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_notification
    ADD CONSTRAINT "D5c50dde621d132df91a530bde1233b6" FOREIGN KEY (parent_content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D5f6fe63b956076d0b120a6a13a2a825; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermission
    ADD CONSTRAINT "D5f6fe63b956076d0b120a6a13a2a825" FOREIGN KEY (permission_collection_id) REFERENCES permissions_basepermissioncollection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D67dda798d7fa48dbcc4bdbfe7ce6098; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT "D67dda798d7fa48dbcc4bdbfe7ce6098" FOREIGN KEY (address_details_id) REFERENCES shipments_addressdetails(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D6d4acc8671e2193fd242f1388001e32; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT "D6d4acc8671e2193fd242f1388001e32" FOREIGN KEY (address_details_id) REFERENCES shipments_addressdetails(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D8a5fd63d5d2dc8c23486692382f93a3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment
    ADD CONSTRAINT "D8a5fd63d5d2dc8c23486692382f93a3" FOREIGN KEY (parent_content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D8bb25285ba3731c909b5bdafd7ce8e4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment
    ADD CONSTRAINT "D8bb25285ba3731c909b5bdafd7ce8e4" FOREIGN KEY (assignee_content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D91b5ba75edc77e455cc93bf9f07cbfa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentcarrierassignment
    ADD CONSTRAINT "D91b5ba75edc77e455cc93bf9f07cbfa" FOREIGN KEY (assignment_id) REFERENCES shipments_shipmentassignment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token_user_id_1d10c57f535fb363_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_1d10c57f535fb363_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: b046aba57bbfcad282aaa9836d13f71a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite
    ADD CONSTRAINT b046aba57bbfcad282aaa9836d13f71a FOREIGN KEY (inviter_company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: b76145cdb79daaa67d1c36d2c7abe3f2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT b76145cdb79daaa67d1c36d2c7abe3f2 FOREIGN KEY (driver_assignment_id) REFERENCES shipments_shipmentdriverassignment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: c1eb17c43ad08b49382c2282ff3f4a12; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_equipmenttag
    ADD CONSTRAINT c1eb17c43ad08b49382c2282ff3f4a12 FOREIGN KEY (assignee_content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: c6d937b3e8efc9186838e33af3ad4fa0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif
    ADD CONSTRAINT c6d937b3e8efc9186838e33af3ad4fa0 FOREIGN KEY (shipment_assignment_id) REFERENCES shipments_shipmentassignment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: da347fbde115eeaf23956bf0c1cbe737; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount_connections
    ADD CONSTRAINT da347fbde115eeaf23956bf0c1cbe737 FOREIGN KEY (genericcompany_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: e12a69e638dcc2e926df2b1f9d4be789; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentdriverassignment
    ADD CONSTRAINT e12a69e638dcc2e926df2b1f9d4be789 FOREIGN KEY (assignment_id) REFERENCES shipments_shipmentassignment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: e47adc227fb80475c063a60d870a7773; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT e47adc227fb80475c063a60d870a7773 FOREIGN KEY (first_location_id) REFERENCES shipments_shipmentlocation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: edb4274470d6bb6d52f0f6f17de07d45; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT edb4274470d6bb6d52f0f6f17de07d45 FOREIGN KEY (carrier_assignment_id) REFERENCES shipments_shipmentcarrierassignment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: f62e43f3b715a078a8c4ff9ffdffb66a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT f62e43f3b715a078a8c4ff9ffdffb66a FOREIGN KEY (last_location_id) REFERENCES shipments_shipmentlocation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: geolo_carrier_id_55c9ad0802b68cd_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation
    ADD CONSTRAINT geolo_carrier_id_55c9ad0802b68cd_fk_shipments_genericcompany_id FOREIGN KEY (carrier_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: geolocat_driver_id_67bc6b5b21d0a574_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation
    ADD CONSTRAINT geolocat_driver_id_67bc6b5b21d0a574_fk_shipments_genericuser_id FOREIGN KEY (driver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: geolocati_shipment_id_1c67fa4c2f8eb9e6_fk_shipments_shipment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geolocations_geolocation
    ADD CONSTRAINT geolocati_shipment_id_1c67fa4c2f8eb9e6_fk_shipments_shipment_id FOREIGN KEY (shipment_id) REFERENCES shipments_shipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guar_content_type_id_1d41cfa581d8d978_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guar_content_type_id_1d41cfa581d8d978_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guar_content_type_id_597c953df5d1232d_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guar_content_type_id_597c953df5d1232d_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_g_permission_id_6db56426ae60788a_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_g_permission_id_6db56426ae60788a_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_groupobject_group_id_713e154dfd2f5937_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobject_group_id_713e154dfd2f5937_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_u_permission_id_2e655ff0bbafb1c1_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_u_permission_id_2e655ff0bbafb1c1_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_userobjectper_user_id_4727c7e419caead5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectper_user_id_4727c7e419caead5_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: not_genericuser_id_260dcbbf7c4663ff_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif_receivers
    ADD CONSTRAINT not_genericuser_id_260dcbbf7c4663ff_fk_shipments_genericuser_id FOREIGN KEY (genericuser_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notif_company_id_c21654211fc7525_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_signupinternalnotif
    ADD CONSTRAINT notif_company_id_c21654211fc7525_fk_shipments_genericcompany_id FOREIGN KEY (company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_426c37301b8291af_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day1
    ADD CONSTRAINT notifi_receiver_id_426c37301b8291af_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_426c38d483519551_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day7
    ADD CONSTRAINT notifi_receiver_id_426c38d483519551_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_4bcbccb7ce4428a1_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day28
    ADD CONSTRAINT notifi_receiver_id_4bcbccb7ce4428a1_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_5bf0bd9a924c65c7_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_notification
    ADD CONSTRAINT notifi_receiver_id_5bf0bd9a924c65c7_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_67f8bd152d8c6fcc_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day38
    ADD CONSTRAINT notifi_receiver_id_67f8bd152d8c6fcc_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_67f8c61221119771_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day31
    ADD CONSTRAINT notifi_receiver_id_67f8c61221119771_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifi_receiver_id_76d7e4ec360f9a55_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_day15
    ADD CONSTRAINT notifi_receiver_id_76d7e4ec360f9a55_fk_shipments_genericuser_id FOREIGN KEY (receiver_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifica_sender_id_2419fea1a09e018d_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_notification
    ADD CONSTRAINT notifica_sender_id_2419fea1a09e018d_fk_shipments_genericuser_id FOREIGN KEY (sender_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifica_sender_id_29e99c3ee641a04e_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_shipmentassignmentnotif
    ADD CONSTRAINT notifica_sender_id_29e99c3ee641a04e_fk_shipments_genericuser_id FOREIGN KEY (sender_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notificat_invite_id_4fb33aa18a57024f_fk_shipments_userinvite_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_userinvitenotif
    ADD CONSTRAINT notificat_invite_id_4fb33aa18a57024f_fk_shipments_userinvite_id FOREIGN KEY (invite_id) REFERENCES shipments_userinvite(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notificat_sender_id_cd14f4b644c70d1_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY notifications_userinvitenotif
    ADD CONSTRAINT notificat_sender_id_cd14f4b644c70d1_fk_shipments_genericuser_id FOREIGN KEY (sender_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payout_info_id_1a8266620e3546bc_fk_shipments_shipmentpayout_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT payout_info_id_1a8266620e3546bc_fk_shipments_shipmentpayout_id FOREIGN KEY (payout_info_id) REFERENCES shipments_shipmentpayout(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permission_permission_id_301fc5a870187316_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permissions_basepermission
    ADD CONSTRAINT permission_permission_id_301fc5a870187316_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: relation_to_id_680aae2ccdb25c71_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation
    ADD CONSTRAINT relation_to_id_680aae2ccdb25c71_fk_shipments_genericcompany_id FOREIGN KEY (relation_to_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: s_assigner_user_id_664f938f27382975_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT s_assigner_user_id_664f938f27382975_fk_shipments_genericuser_id FOREIGN KEY (assigner_user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: s_features_id_1ba3885924ee162c_fk_shipments_shipmentfeatures_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT s_features_id_1ba3885924ee162c_fk_shipments_shipmentfeatures_id FOREIGN KEY (features_id) REFERENCES shipments_shipmentfeatures(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: s_features_id_647162188edb1708_fk_shipments_shipmentfeatures_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT s_features_id_647162188edb1708_fk_shipments_shipmentfeatures_id FOREIGN KEY (features_id) REFERENCES shipments_shipmentfeatures(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: s_profile_photo_id_4a64f9bc0f5a2e9a_fk_shipments_filecontext_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT s_profile_photo_id_4a64f9bc0f5a2e9a_fk_shipments_filecontext_id FOREIGN KEY (profile_photo_id) REFERENCES shipments_filecontext(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sh_division_id_4523a274dc4cefa4_fk_shipments_companydivision_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivisionmembership
    ADD CONSTRAINT sh_division_id_4523a274dc4cefa4_fk_shipments_companydivision_id FOREIGN KEY (division_id) REFERENCES shipments_companydivision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sh_inviter_user_id_3de4c5737a8272d0_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyinvite
    ADD CONSTRAINT sh_inviter_user_id_3de4c5737a8272d0_fk_shipments_genericuser_id FOREIGN KEY (inviter_user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sh_subscription_id_627b4f9464e5d105_fk_payments_subscription_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT sh_subscription_id_627b4f9464e5d105_fk_payments_subscription_id FOREIGN KEY (subscription_id) REFERENCES payments_subscription(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shi_demoaccount_id_5df410c67be1bd5e_fk_shipments_demoaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount_connections
    ADD CONSTRAINT shi_demoaccount_id_5df410c67be1bd5e_fk_shipments_demoaccount_id FOREIGN KEY (demoaccount_id) REFERENCES shipments_demoaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shi_sibling_id_1047324246ceb7b9_fk_shipments_companyrelation_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companyrelation
    ADD CONSTRAINT shi_sibling_id_1047324246ceb7b9_fk_shipments_companyrelation_id FOREIGN KEY (sibling_id) REFERENCES shipments_companyrelation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_carrier_id_56d713adaba99f77_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentrequest
    ADD CONSTRAINT ship_carrier_id_56d713adaba99f77_fk_shipments_genericcompany_id FOREIGN KEY (carrier_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_carrier_id_7987ea6f13449227_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT ship_carrier_id_7987ea6f13449227_fk_shipments_genericcompany_id FOREIGN KEY (carrier_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_company_id_12d015ec9a9ca58d_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivision
    ADD CONSTRAINT ship_company_id_12d015ec9a9ca58d_fk_shipments_genericcompany_id FOREIGN KEY (company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_company_id_13a65a8162cf03ad_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT ship_company_id_13a65a8162cf03ad_fk_shipments_genericcompany_id FOREIGN KEY (company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_company_id_734d797892537356_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT ship_company_id_734d797892537356_fk_shipments_genericcompany_id FOREIGN KEY (company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_company_id_7faa5670a7d28dbb_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_demoaccount
    ADD CONSTRAINT ship_company_id_7faa5670a7d28dbb_fk_shipments_genericcompany_id FOREIGN KEY (company_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ship_owner_user_id_7fa4591c0314c831_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT ship_owner_user_id_7fa4591c0314c831_fk_shipments_genericuser_id FOREIGN KEY (owner_user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipme_assigner_id_3b2904721a997d46_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_equipmenttag
    ADD CONSTRAINT shipme_assigner_id_3b2904721a997d46_fk_shipments_genericuser_id FOREIGN KEY (assigner_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipme_owner_id_658525fc99762825_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipme_owner_id_658525fc99762825_fk_shipments_genericcompany_id FOREIGN KEY (owner_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipme_time_range_id_2bb7d7c114c47166_fk_shipments_timerange_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipme_time_range_id_2bb7d7c114c47166_fk_shipments_timerange_id FOREIGN KEY (time_range_id) REFERENCES shipments_timerange(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipme_time_range_id_61e83fb81a22d032_fk_shipments_timerange_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipme_time_range_id_61e83fb81a22d032_fk_shipments_timerange_id FOREIGN KEY (time_range_id) REFERENCES shipments_timerange(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipmen_assigner_id_b9f615f9882e255_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment
    ADD CONSTRAINT shipmen_assigner_id_b9f615f9882e255_fk_shipments_genericuser_id FOREIGN KEY (assigner_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipmen_insurance_id_4f5b8e82eeb3c845_fk_shipments_insurance_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipmen_insurance_id_4f5b8e82eeb3c845_fk_shipments_insurance_id FOREIGN KEY (insurance_id) REFERENCES shipments_insurance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipmen_owner_id_6773194eaeaf87a_fk_shipments_genericcompany_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipment
    ADD CONSTRAINT shipmen_owner_id_6773194eaeaf87a_fk_shipments_genericcompany_id FOREIGN KEY (owner_id) REFERENCES shipments_genericcompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments__logo_id_4d5ddbfff9d5df33_fk_shipments_filecontext_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments__logo_id_4d5ddbfff9d5df33_fk_shipments_filecontext_id FOREIGN KEY (logo_id) REFERENCES shipments_filecontext(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments__user_id_330acc8adf775a40_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_platform
    ADD CONSTRAINT shipments__user_id_330acc8adf775a40_fk_shipments_genericuser_id FOREIGN KEY (user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments__user_id_4c1f1f5ed7844db0_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_companydivisionmembership
    ADD CONSTRAINT shipments__user_id_4c1f1f5ed7844db0_fk_shipments_genericuser_id FOREIGN KEY (user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments__user_id_5f0cdc513aacda25_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_userinvite
    ADD CONSTRAINT shipments__user_id_5f0cdc513aacda25_fk_shipments_genericuser_id FOREIGN KEY (user_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_genericuser_user_id_1cd5d7516abe44f8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT shipments_genericuser_user_id_1cd5d7516abe44f8_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_lo_contact_id_10be357510731e86_fk_shipments_person_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_lo_contact_id_10be357510731e86_fk_shipments_person_id FOREIGN KEY (contact_id) REFERENCES shipments_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_owner_id_5bf6c65c3ae09116_fk_shipments_genericuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericcompany
    ADD CONSTRAINT shipments_owner_id_5bf6c65c3ae09116_fk_shipments_genericuser_id FOREIGN KEY (owner_id) REFERENCES shipments_genericuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_sa_contact_id_7f1558d39aa0d12e_fk_shipments_person_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_savedlocation
    ADD CONSTRAINT shipments_sa_contact_id_7f1558d39aa0d12e_fk_shipments_person_id FOREIGN KEY (contact_id) REFERENCES shipments_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_shipment_id_3e44825f2f156dfd_fk_shipments_shipment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentlocation
    ADD CONSTRAINT shipments_shipment_id_3e44825f2f156dfd_fk_shipments_shipment_id FOREIGN KEY (shipment_id) REFERENCES shipments_shipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_shipment_id_4c9c42f85166badc_fk_shipments_shipment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentrequest
    ADD CONSTRAINT shipments_shipment_id_4c9c42f85166badc_fk_shipments_shipment_id FOREIGN KEY (shipment_id) REFERENCES shipments_shipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shipments_shipment_id_4d8b68a705cc2945_fk_shipments_shipment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_shipmentassignment
    ADD CONSTRAINT shipments_shipment_id_4d8b68a705cc2945_fk_shipments_shipment_id FOREIGN KEY (shipment_id) REFERENCES shipments_shipment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tos_acceptance_id_cf9351596eb307_fk_shipments_tosacceptance_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY shipments_genericuser
    ADD CONSTRAINT tos_acceptance_id_cf9351596eb307_fk_shipments_tosacceptance_id FOREIGN KEY (tos_acceptance_id) REFERENCES shipments_tosacceptance(id) DEFERRABLE INITIALLY DEFERRED;


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

