--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
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


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: api_component_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_component_type (
    "APIComponentTypeID" bigint NOT NULL,
    "APIComponentTypeName" character varying(50),
    "GFFSmall" double precision,
    "GFFMedium" double precision,
    "GFFLarge" double precision,
    "GFFRupture" double precision,
    "GFFTotal" double precision,
    "HoleCostSmall" double precision,
    "HoleCostMedium" double precision,
    "HoleCostLarge" double precision,
    "HoleCostRupture" double precision,
    "OutageSmall" double precision,
    "OutageMedium" double precision,
    "OutageLarge" double precision,
    "OutageRupture" double precision
);


ALTER TABLE public.api_component_type OWNER TO postgres;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id bigint NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id bigint,
    permission_id bigint
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id bigint NOT NULL,
    name character varying(255),
    content_type_id bigint,
    codename character varying(100)
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id bigint NOT NULL,
    password character varying(128),
    last_login timestamp without time zone,
    is_superuser bigint,
    username character varying(150) NOT NULL,
    first_name character varying(30),
    last_name character varying(150),
    email character varying(254),
    is_staff bigint,
    is_active bigint,
    date_joined timestamp without time zone
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id bigint,
    group_id bigint
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint,
    permission_id bigint
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: componentmaster_ComponentID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."componentmaster_ComponentID_seq"
    START WITH 9
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."componentmaster_ComponentID_seq" OWNER TO postgres;

--
-- Name: component_master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.component_master (
    "ComponentID" bigint DEFAULT nextval('public."componentmaster_ComponentID_seq"'::regclass) NOT NULL,
    "ComponentNumber" character varying(100),
    "EquipmentID" bigint,
    "ComponentTypeID" bigint,
    "ComponentName" character varying(150),
    "ComponentDesc" character varying(250),
    "IsEquipmentLinked" bigint,
    "APIComponentTypeID" bigint,
    "Create" timestamp without time zone
);


ALTER TABLE public.component_master OWNER TO postgres;

--
-- Name: component_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.component_type (
    "ComponentTypeID" bigint NOT NULL,
    "ComponentTypeName" character varying(50),
    "ComponentTypeCode" character varying(50)
);


ALTER TABLE public.component_type OWNER TO postgres;

--
-- Name: designcode_DesignCodeID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."designcode_DesignCodeID_seq"
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."designcode_DesignCodeID_seq" OWNER TO postgres;

--
-- Name: design_code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.design_code (
    "DesignCodeID" bigint DEFAULT nextval('public."designcode_DesignCodeID_seq"'::regclass) NOT NULL,
    "DesignCode" character varying(100),
    "DesignCodeApp" character varying(100),
    "SiteID" bigint
);


ALTER TABLE public.design_code OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id bigint NOT NULL,
    action_time timestamp without time zone,
    object_id text,
    object_repr character varying(200),
    action_flag bigint,
    change_message text,
    content_type_id bigint,
    user_id bigint
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id bigint NOT NULL,
    app_label character varying(100),
    model character varying(100)
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255),
    name character varying(255),
    applied timestamp without time zone
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text,
    expire_date timestamp without time zone
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: dm_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dm_category (
    "DMCategoryID" bigint NOT NULL,
    "DMCategoryName" character varying(100)
);


ALTER TABLE public.dm_category OWNER TO postgres;

--
-- Name: dm_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dm_items (
    "DMItemID" bigint NOT NULL,
    "DMDescription" character varying(100),
    "DMSeq" bigint,
    "DMCategoryID" bigint,
    "DMCode" character varying(50),
    "HasDF" bigint,
    "FailureMode" character varying(50)
);


ALTER TABLE public.dm_items OWNER TO postgres;

--
-- Name: equipmentmaster_EquipmentID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."equipmentmaster_EquipmentID_seq"
    START WITH 8
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."equipmentmaster_EquipmentID_seq" OWNER TO postgres;

--
-- Name: equipment_master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipment_master (
    "EquipmentID" bigint DEFAULT nextval('public."equipmentmaster_EquipmentID_seq"'::regclass) NOT NULL,
    "EquipmentNumber" character varying(100),
    "EquipmentTypeID" bigint,
    "EquipmentName" character varying(150),
    "CommissionDate" timestamp without time zone,
    "DesignCodeID" bigint,
    "SiteID" bigint,
    "FacilityID" bigint,
    "ManufacturerID" bigint,
    "PFDNo" character varying(100),
    "ProcessDescription" character varying(250),
    "EquipmentDesc" character varying(250),
    "Create" timestamp without time zone
);


ALTER TABLE public.equipment_master OWNER TO postgres;

--
-- Name: equipment_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipment_type (
    "EquipmentTypeID" bigint NOT NULL,
    "EquipmentTypeCode" character varying(50),
    "EquipmentTypeName" character varying(50)
);


ALTER TABLE public.equipment_type OWNER TO postgres;

--
-- Name: facility_FacilityID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."facility_FacilityID_seq"
    START WITH 9
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."facility_FacilityID_seq" OWNER TO postgres;

--
-- Name: facility; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facility (
    "FacilityID" bigint DEFAULT nextval('public."facility_FacilityID_seq"'::regclass) NOT NULL,
    "SiteID" bigint,
    "FacilityName" character varying(100),
    "ManagementFactor" double precision,
    "Create" timestamp without time zone
);


ALTER TABLE public.facility OWNER TO postgres;

--
-- Name: facility_risk_target; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facility_risk_target (
    "FacilityID" bigint NOT NULL,
    "RiskTarget_FC" double precision,
    "RiskTarget_AC" double precision
);


ALTER TABLE public.facility_risk_target OWNER TO postgres;

--
-- Name: manufacturer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.manufacturer (
    "ManufacturerID" integer NOT NULL,
    "ManufacturerName" character varying(100) NOT NULL,
    "SiteID" bigint
);


ALTER TABLE public.manufacturer OWNER TO postgres;

--
-- Name: manufacturer_ManufacturerID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."manufacturer_ManufacturerID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."manufacturer_ManufacturerID_seq" OWNER TO postgres;

--
-- Name: manufacturer_ManufacturerID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."manufacturer_ManufacturerID_seq" OWNED BY public.manufacturer."ManufacturerID";


--
-- Name: rw_assessment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_assessment (
    "ID" integer NOT NULL,
    "EquipmentID" integer NOT NULL,
    "ComponentID" integer NOT NULL,
    "AssessmentDate" timestamp without time zone,
    "RiskAnalysisPeriod" integer NOT NULL,
    "IsEquipmentLinked" smallint NOT NULL,
    "ProposalName" character varying(100),
    "Create" timestamp without time zone
);


ALTER TABLE public.rw_assessment OWNER TO postgres;

--
-- Name: rw_assessment_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."rw_assessment_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."rw_assessment_ID_seq" OWNER TO postgres;

--
-- Name: rw_assessment_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."rw_assessment_ID_seq" OWNED BY public.rw_assessment."ID";


--
-- Name: rw_ca_level1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_ca_level1 (
    "ID" integer NOT NULL,
    "Release_Phase" character varying(50),
    fact_di double precision,
    fact_mit double precision,
    fact_ait double precision,
    "CA_cmd" double precision,
    "CA_inj_flame" double precision,
    "CA_inj_toxic" double precision,
    "CA_inj_ntnf" double precision,
    "FC_cmd" double precision,
    "FC_affa" double precision,
    "FC_prod" double precision,
    "FC_inj" double precision,
    "FC_envi" double precision,
    "FC_total" double precision,
    "FCOF_Category" character varying(50)
);


ALTER TABLE public.rw_ca_level1 OWNER TO postgres;

--
-- Name: rw_ca_tank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_ca_tank (
    "ID" integer NOT NULL,
    "Hydraulic_Water" double precision,
    "Hydraulic_Fluid" double precision,
    "Seepage_Velocity" double precision,
    "Flow_Rate_D1" double precision,
    "Flow_Rate_D2" double precision,
    "Flow_Rate_D3" double precision,
    "Flow_Rate_D4" double precision,
    "Leak_Duration_D1" double precision,
    "Leak_Duration_D2" double precision,
    "Leak_Duration_D3" double precision,
    "Leak_Duration_D4" double precision,
    "Release_Volume_Leak_D1" double precision,
    "Release_Volume_Leak_D2" double precision,
    "Release_Volume_Leak_D3" double precision,
    "Release_Volume_Leak_D4" double precision,
    "Release_Volume_Rupture" double precision,
    "Liquid_Height" double precision,
    "Volume_Fluid" double precision,
    "Time_Leak_Ground" double precision,
    "Volume_SubSoil_Leak_D1" double precision,
    "Volume_SubSoil_Leak_D4" double precision,
    "Volume_Ground_Water_Leak_D1" double precision,
    "Volume_Ground_Water_Leak_D4" double precision,
    "Barrel_Dike_Leak" double precision,
    "Barrel_Dike_Rupture" double precision,
    "Barrel_Onsite_Leak" double precision,
    "Barrel_Onsite_Rupture" double precision,
    "Barrel_Offsite_Leak" double precision,
    "Barrel_Offsite_Rupture" double precision,
    "Barrel_Water_Leak" double precision,
    "Barrel_Water_Rupture" double precision,
    "FC_Environ_Leak" double precision,
    "FC_Environ_Rupture" double precision,
    "FC_Environ" double precision,
    "Material_Factor" double precision,
    "Component_Damage_Cost" double precision,
    "Business_Cost" double precision,
    "Consequence" double precision,
    "ConsequenceCategory" character varying(50)
);


ALTER TABLE public.rw_ca_tank OWNER TO postgres;

--
-- Name: rw_coating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_coating (
    "ID" integer NOT NULL,
    "ExternalCoating" smallint,
    "ExternalInsulation" smallint,
    "InternalCladding" smallint,
    "InternalCoating" smallint,
    "InternalLining" smallint,
    "ExternalCoatingDate" timestamp without time zone,
    "ExternalCoatingQuality" character varying(50),
    "ExternalInsulationType" character varying(50),
    "InsulationCondition" character varying(50),
    "InsulationContainsChloride" smallint,
    "InternalLinerCondition" character varying(50),
    "InternalLinerType" character varying(50),
    "CladdingCorrosionRate" double precision,
    "SupportConfigNotAllowCoatingMaint" smallint
);


ALTER TABLE public.rw_coating OWNER TO postgres;

--
-- Name: rw_component; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_component (
    "ID" integer NOT NULL,
    "NominalDiameter" double precision,
    "NominalThickness" double precision,
    "CurrentThickness" double precision,
    "MinReqThickness" double precision,
    "CurrentCorrosionRate" double precision,
    "BranchDiameter" character varying(50),
    "BranchJointType" character varying(50),
    "BrinnelHardness" character varying(50),
    "ChemicalInjection" smallint,
    "HighlyInjectionInsp" smallint,
    "ComplexityProtrusion" character varying(50),
    "CorrectiveAction" character varying(50),
    "CracksPresent" smallint,
    "CyclicLoadingWitin15_25m" character varying(50),
    "DamageFoundInspection" smallint,
    "DeltaFATT" double precision,
    "NumberPipeFittings" character varying(50),
    "PipeCondition" character varying(50),
    "PreviousFailures" character varying(50),
    "ShakingAmount" character varying(50),
    "ShakingDetected" smallint,
    "ShakingTime" character varying(50),
    "TrampElements" smallint,
    "ShellHeight" double precision,
    "ReleasePreventionBarrier" smallint,
    "ConcreteFoundation" smallint,
    "SeverityOfVibration" character varying(50)
);


ALTER TABLE public.rw_component OWNER TO postgres;

--
-- Name: rw_damagemachinsm_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."rw_damagemachinsm_ID_seq"
    START WITH 13
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 9223372036854773807
    CACHE 1;


ALTER TABLE public."rw_damagemachinsm_ID_seq" OWNER TO postgres;

--
-- Name: rw_damage_mechanism; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_damage_mechanism (
    "ID_DM" integer NOT NULL,
    "DMItemID" integer NOT NULL,
    "IsActive" smallint,
    "Notes" character varying(255),
    "ExpectedTypeID" integer,
    "IsEL" smallint,
    "ELValue" double precision,
    "IsDF" smallint,
    "IsUserDisabled" smallint,
    "DF1" double precision,
    "DF2" double precision,
    "DF3" double precision,
    "DFBase" double precision,
    "RLI" double precision,
    "HighestInspectionEffectiveness" character varying(50),
    "SecondInspectionEffectiveness" character varying(50),
    "NumberOfInspections" integer,
    "LastInspDate" timestamp without time zone,
    "InspDueDate" timestamp without time zone,
    "ID" bigint DEFAULT nextval('public."rw_damagemachinsm_ID_seq"'::regclass) NOT NULL
);


ALTER TABLE public.rw_damage_mechanism OWNER TO postgres;

--
-- Name: rw_data_chart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_data_chart (
    "ID" bigint NOT NULL,
    risk_target double precision,
    risk_age_1 double precision,
    risk_age_2 double precision,
    risk_age_3 double precision,
    risk_age_4 double precision,
    risk_age_5 double precision,
    risk_age_6 double precision,
    risk_age_7 double precision,
    risk_age_8 double precision,
    risk_age_9 double precision,
    risk_age_10 double precision,
    risk_age_11 double precision,
    risk_age_12 double precision,
    risk_age_13 double precision,
    risk_age_14 double precision,
    risk_age_15 double precision
);


ALTER TABLE public.rw_data_chart OWNER TO postgres;

--
-- Name: rw_equipment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_equipment (
    "ID" integer NOT NULL,
    "CommissionDate" timestamp without time zone NOT NULL,
    "AdminUpsetManagement" smallint NOT NULL,
    "ContainsDeadlegs" smallint,
    "CyclicOperation" smallint,
    "HighlyDeadlegInsp" smallint,
    "DowntimeProtectionUsed" smallint,
    "ExternalEnvironment" character varying(50),
    "HeatTraced" smallint,
    "InterfaceSoilWater" smallint,
    "LinerOnlineMonitoring" smallint,
    "MaterialExposedToClExt" smallint,
    "MinReqTemperaturePressurisation" double precision,
    "OnlineMonitoring" character varying(100),
    "PresenceSulphidesO2" smallint,
    "PresenceSulphidesO2Shutdown" smallint,
    "PressurisationControlled" smallint,
    "PWHT" smallint,
    "SteamOutWaterFlush" smallint,
    "ManagementFactor" double precision,
    "ThermalHistory" character varying(50),
    "YearLowestExpTemp" smallint,
    "Volume" double precision,
    "TypeOfSoil" character varying(50),
    "EnvironmentSensitivity" character varying(50),
    "DistanceToGroundWater" double precision,
    "AdjustmentSettle" character varying(100),
    "ComponentIsWelded" smallint,
    "TankIsMaintained" smallint
);


ALTER TABLE public.rw_equipment OWNER TO postgres;

--
-- Name: rw_extcor_temperature; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_extcor_temperature (
    "ID" integer NOT NULL,
    "Minus12ToMinus8" double precision,
    "Minus8ToPlus6" double precision,
    "Plus6ToPlus32" double precision,
    "Plus32ToPlus71" double precision,
    "Plus71ToPlus107" double precision,
    "Plus107ToPlus121" double precision,
    "Plus121ToPlus135" double precision,
    "Plus135ToPlus162" double precision,
    "Plus162ToPlus176" double precision,
    "MoreThanPlus176" double precision
);


ALTER TABLE public.rw_extcor_temperature OWNER TO postgres;

--
-- Name: rw_full_fcof; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_full_fcof (
    "ID" integer NOT NULL,
    "FCoFValue" double precision,
    "FCoFCategory" character varying(50),
    "AIL" smallint,
    envcost double precision,
    equipcost double precision,
    prodcost double precision,
    popdens double precision,
    injcost double precision
);


ALTER TABLE public.rw_full_fcof OWNER TO postgres;

--
-- Name: rw_full_pof; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_full_pof (
    "ID" integer NOT NULL,
    "ThinningAP1" double precision,
    "ThinningAP2" double precision,
    "ThinningAP3" double precision,
    "SCCAP1" double precision,
    "SCCAP2" double precision,
    "SCCAP3" double precision,
    "ExternalAP1" double precision,
    "ExternalAP2" double precision,
    "ExternalAP3" double precision,
    "BrittleAP1" double precision,
    "BrittleAP2" double precision,
    "BrittleAP3" double precision,
    "HTHA_AP1" double precision,
    "HTHA_AP2" double precision,
    "HTHA_AP3" double precision,
    "FatigueAP1" double precision,
    "FatigueAP2" double precision,
    "FatigueAP3" double precision,
    "FMS" double precision,
    "ThinningType" character varying(7),
    "GFFTotal" double precision,
    "ThinningLocalAP1" double precision,
    "ThinningLocalAP2" double precision,
    "ThinningLocalAP3" double precision,
    "ThinningGeneralAP1" double precision,
    "ThinningGeneralAP2" double precision,
    "ThinningGeneralAP3" double precision,
    "TotalDFAP1" double precision,
    "TotalDFAP2" double precision,
    "TotalDFAP3" double precision,
    "PoFAP1" double precision,
    "PoFAP2" double precision,
    "PoFAP3" double precision,
    "PoFAP1Category" character varying(50),
    "PoFAP2Category" character varying(50),
    "PoFAP3Category" character varying(50)
);


ALTER TABLE public.rw_full_pof OWNER TO postgres;

--
-- Name: rw_input_ca_level1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_input_ca_level1 (
    "ID" integer NOT NULL,
    "API_FLUID" character varying(50),
    "SYSTEM" character varying(50),
    "Release_Duration" character varying(50),
    "Detection_Type" character varying(50),
    "Isulation_Type" character varying(50),
    "Mitigation_System" character varying(150),
    "Equipment_Cost" double precision,
    "Injure_Cost" double precision,
    "Evironment_Cost" double precision,
    "Toxic_Percent" double precision,
    "Personal_Density" double precision,
    "Material_Cost" double precision,
    "Production_Cost" double precision,
    "Mass_Inventory" double precision,
    "Mass_Component" double precision,
    "Stored_Pressure" double precision,
    "Stored_Temp" double precision
);


ALTER TABLE public.rw_input_ca_level1 OWNER TO postgres;

--
-- Name: rw_input_ca_tank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_input_ca_tank (
    "ID" integer NOT NULL,
    "FLUID_HEIGHT" double precision,
    "SHELL_COURSE_HEIGHT" double precision,
    "TANK_DIAMETTER" double precision,
    "Prevention_Barrier" smallint,
    "Environ_Sensitivity" character varying(50),
    "P_lvdike" double precision,
    "P_onsite" double precision,
    "P_offsite" double precision,
    "Soil_Type" character varying(150),
    "TANK_FLUID" character varying(150),
    "API_FLUID" character varying(50),
    "SW" double precision,
    "ProductionCost" double precision
);


ALTER TABLE public.rw_input_ca_tank OWNER TO postgres;

--
-- Name: rw_inspection_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_inspection_history (
    "ID" integer NOT NULL,
    "InspectionPlanName" character varying(100),
    "InspectionCoverageName" character varying(100),
    "EquipmentNumber" character varying(50),
    "ComponentNumber" character varying(50),
    "DM" character varying(150),
    "InspectionType" character varying(250),
    "InspectionDate" timestamp without time zone,
    "InspectionEffective" character varying(50)
);


ALTER TABLE public.rw_inspection_history OWNER TO postgres;

--
-- Name: rw_inspection_history_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."rw_inspection_history_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."rw_inspection_history_ID_seq" OWNER TO postgres;

--
-- Name: rw_inspection_history_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."rw_inspection_history_ID_seq" OWNED BY public.rw_inspection_history."ID";


--
-- Name: rw_material; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_material (
    "ID" integer NOT NULL,
    "MaterialName" character varying(100),
    "DesignPressure" double precision,
    "DesignTemperature" double precision,
    "MinDesignTemperature" double precision,
    "BrittleFractureThickness" double precision,
    "CorrosionAllowance" double precision,
    "SigmaPhase" double precision,
    "SulfurContent" character varying(50),
    "HeatTreatment" character varying(50),
    "ReferenceTemperature" double precision,
    "PTAMaterialCode" character varying(70),
    "HTHAMaterialCode" character varying(50),
    "IsPTA" smallint,
    "IsHTHA" smallint,
    "Austenitic" smallint,
    "Temper" smallint,
    "CarbonLowAlloy" smallint,
    "NickelBased" smallint,
    "ChromeMoreEqual12" smallint,
    "AllowableStress" double precision,
    "CostFactor" double precision
);


ALTER TABLE public.rw_material OWNER TO postgres;

--
-- Name: rw_stream; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rw_stream (
    "ID" integer NOT NULL,
    "AmineSolution" character varying(50),
    "AqueousOperation" smallint,
    "AqueousShutdown" smallint,
    "ToxicConstituent" smallint,
    "Caustic" smallint,
    "Chloride" double precision,
    "CO3Concentration" double precision,
    "Cyanide" smallint,
    "ExposedToGasAmine" smallint,
    "ExposedToSulphur" smallint,
    "ExposureToAmine" character varying(50),
    "H2S" smallint,
    "H2SInWater" double precision,
    "Hydrogen" smallint,
    "H2SPartialPressure" double precision,
    "Hydrofluoric" smallint,
    "MaterialExposedToClInt" smallint,
    "MaxOperatingPressure" double precision,
    "MaxOperatingTemperature" double precision,
    "MinOperatingPressure" double precision,
    "MinOperatingTemperature" double precision,
    "CriticalExposureTemperature" double precision,
    "NaOHConcentration" double precision,
    "ReleaseFluidPercentToxic" double precision,
    "WaterpH" double precision,
    "TankFluidName" character varying(50),
    "FluidHeight" double precision,
    "FluidLeaveDikePercent" double precision,
    "FluidLeaveDikeRemainOnSitePercent" double precision,
    "FluidGoOffSitePercent" double precision
);


ALTER TABLE public.rw_stream OWNER TO postgres;

--
-- Name: sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sites (
    "SiteID" integer NOT NULL,
    "SiteName" character varying(100),
    "Create" timestamp without time zone
);


ALTER TABLE public.sites OWNER TO postgres;

--
-- Name: sites_SiteID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."sites_SiteID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."sites_SiteID_seq" OWNER TO postgres;

--
-- Name: sites_SiteID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."sites_SiteID_seq" OWNED BY public.sites."SiteID";


--
-- Name: tbl_204_dm_htha; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_204_dm_htha (
    "ID" integer NOT NULL,
    "Susceptibility" text,
    "No Inspection" integer,
    "1D" integer,
    "1C" integer,
    "1B" integer,
    "2D" integer,
    "2C" integer,
    "2B" integer
);


ALTER TABLE public.tbl_204_dm_htha OWNER TO postgres;

--
-- Name: tbl_204_dm_htha_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_204_dm_htha_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_204_dm_htha_ID_seq" OWNER TO postgres;

--
-- Name: tbl_204_dm_htha_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_204_dm_htha_ID_seq" OWNED BY public.tbl_204_dm_htha."ID";


--
-- Name: tbl_213_dm_impact_exemption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_213_dm_impact_exemption (
    "ID" integer NOT NULL,
    "ComponentThickness" double precision,
    "CurveA" double precision,
    "CurveB" double precision,
    "CurveC" double precision,
    "CurveD" double precision
);


ALTER TABLE public.tbl_213_dm_impact_exemption OWNER TO postgres;

--
-- Name: tbl_213_dm_impact_exemption_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_213_dm_impact_exemption_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_213_dm_impact_exemption_ID_seq" OWNER TO postgres;

--
-- Name: tbl_213_dm_impact_exemption_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_213_dm_impact_exemption_ID_seq" OWNED BY public.tbl_213_dm_impact_exemption."ID";


--
-- Name: tbl_214_dm_not_pwht; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_214_dm_not_pwht (
    "ID" integer NOT NULL,
    "Tmin-Tref" integer,
    "6.4" double precision,
    "12.7" double precision,
    "25.4" double precision,
    "38.1" double precision,
    "50.8" double precision,
    "63.5" double precision,
    "76.2" double precision,
    "88.9" double precision,
    "101.6" double precision
);


ALTER TABLE public.tbl_214_dm_not_pwht OWNER TO postgres;

--
-- Name: tbl_214_dm_not_pwht_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_214_dm_not_pwht_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_214_dm_not_pwht_ID_seq" OWNER TO postgres;

--
-- Name: tbl_214_dm_not_pwht_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_214_dm_not_pwht_ID_seq" OWNED BY public.tbl_214_dm_not_pwht."ID";


--
-- Name: tbl_215_dm_pwht; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_215_dm_pwht (
    "ID" integer NOT NULL,
    "Tmin-Tref" integer,
    "6.4" double precision,
    "12.7" double precision,
    "25.4" double precision,
    "38.1" double precision,
    "50.8" double precision,
    "63.5" double precision,
    "76.2" double precision,
    "88.9" double precision,
    "101.6" double precision
);


ALTER TABLE public.tbl_215_dm_pwht OWNER TO postgres;

--
-- Name: tbl_215_dm_pwht_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_215_dm_pwht_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_215_dm_pwht_ID_seq" OWNER TO postgres;

--
-- Name: tbl_215_dm_pwht_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_215_dm_pwht_ID_seq" OWNED BY public.tbl_215_dm_pwht."ID";


--
-- Name: tbl_3b21_si_conversion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_3b21_si_conversion (
    "conversionFactory" integer NOT NULL,
    "SIUnits" double precision,
    "USUnits" double precision
);


ALTER TABLE public.tbl_3b21_si_conversion OWNER TO postgres;

--
-- Name: tbl_3b21_si_conversion_conversionFactory_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_3b21_si_conversion_conversionFactory_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_3b21_si_conversion_conversionFactory_seq" OWNER TO postgres;

--
-- Name: tbl_3b21_si_conversion_conversionFactory_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_3b21_si_conversion_conversionFactory_seq" OWNED BY public.tbl_3b21_si_conversion."conversionFactory";


--
-- Name: tbl_511_dfb_thin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_511_dfb_thin (
    "ID" integer NOT NULL,
    art double precision,
    "E" integer,
    insp integer,
    "D" integer,
    "C" integer,
    "B" integer,
    "A" integer
);


ALTER TABLE public.tbl_511_dfb_thin OWNER TO postgres;

--
-- Name: tbl_511_dfb_thin_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_511_dfb_thin_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_511_dfb_thin_ID_seq" OWNER TO postgres;

--
-- Name: tbl_511_dfb_thin_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_511_dfb_thin_ID_seq" OWNED BY public.tbl_511_dfb_thin."ID";


--
-- Name: tbl_512_dfb_thin_tank_bottom; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_512_dfb_thin_tank_bottom (
    "ID" integer NOT NULL,
    art double precision,
    "E" integer,
    insp integer,
    "D" integer,
    "C" integer,
    "B" integer,
    "A" integer
);


ALTER TABLE public.tbl_512_dfb_thin_tank_bottom OWNER TO postgres;

--
-- Name: tbl_512_dfb_thin_tank_bottom_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_512_dfb_thin_tank_bottom_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_512_dfb_thin_tank_bottom_ID_seq" OWNER TO postgres;

--
-- Name: tbl_512_dfb_thin_tank_bottom_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_512_dfb_thin_tank_bottom_ID_seq" OWNED BY public.tbl_512_dfb_thin_tank_bottom."ID";


--
-- Name: tbl_52_ca_properties_level_1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_52_ca_properties_level_1 (
    "ID" integer NOT NULL,
    "Fluid" text,
    "MW" double precision,
    "Density" double precision,
    "NBP" double precision,
    "Ambient" text,
    ideal integer,
    "A" double precision,
    "B" double precision,
    "C" double precision,
    "D" double precision,
    "E" double precision,
    "Auto" double precision
);


ALTER TABLE public.tbl_52_ca_properties_level_1 OWNER TO postgres;

--
-- Name: tbl_52_ca_properties_level_1_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_52_ca_properties_level_1_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_52_ca_properties_level_1_ID_seq" OWNER TO postgres;

--
-- Name: tbl_52_ca_properties_level_1_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_52_ca_properties_level_1_ID_seq" OWNED BY public.tbl_52_ca_properties_level_1."ID";


--
-- Name: tbl_58_ca_component_dm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_58_ca_component_dm (
    "ID" integer NOT NULL,
    "Fluid" text,
    "CAINL_gas_a" double precision,
    "CAINL_gas_b" double precision,
    "CAINL_liquid_a" double precision,
    "CAINL_liquid_b" double precision,
    "CAIL_gas_a" double precision,
    "CAIL_gas_b" double precision,
    "CAIL_liquid_a" double precision,
    "CAIL_liquid_b" double precision,
    "IAINL_gas_a" double precision,
    "IAINL_gas_b" double precision,
    "IAINL_liquid_a" double precision,
    "IAINL_liquid_b" double precision,
    "IAIL_gas_a" double precision,
    "IAIL_gas_b" double precision,
    "IAIL_liquid_a" double precision,
    "IAIL_liquid_b" double precision
);


ALTER TABLE public.tbl_58_ca_component_dm OWNER TO postgres;

--
-- Name: tbl_58_ca_component_dm_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_58_ca_component_dm_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_58_ca_component_dm_ID_seq" OWNER TO postgres;

--
-- Name: tbl_58_ca_component_dm_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_58_ca_component_dm_ID_seq" OWNED BY public.tbl_58_ca_component_dm."ID";


--
-- Name: tbl_59_component_damage_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_59_component_damage_person (
    "ID" integer NOT NULL,
    "Fluid" text,
    "CAINL_gas_a" double precision,
    "CAINL_gas_b" double precision,
    "CAINL_liquid_a" double precision,
    "CAINL_liquid_b" double precision,
    "CALL_gas_a" double precision,
    "CALL_gas_b" double precision,
    "CALL_liquid_a" double precision,
    "CALL_liquid_b" double precision,
    "IAINL_gas_a" double precision,
    "IAINL_gas_b" double precision,
    "IAINL_liquid_a" double precision,
    "IAINL_liquid_b" double precision,
    "IAIL_gas_a" double precision,
    "IAIL_gas_b" double precision,
    "IAIL_liquid_a" double precision,
    "IAIL_liquid_b" double precision
);


ALTER TABLE public.tbl_59_component_damage_person OWNER TO postgres;

--
-- Name: tbl_59_component_damage_person_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_59_component_damage_person_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_59_component_damage_person_ID_seq" OWNER TO postgres;

--
-- Name: tbl_59_component_damage_person_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_59_component_damage_person_ID_seq" OWNED BY public.tbl_59_component_damage_person."ID";


--
-- Name: tbl_64_dm_linning_inorganic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_64_dm_linning_inorganic (
    "ID" integer NOT NULL,
    "YearsSinceLastInspection" integer,
    "Strip lined alloy" double precision,
    "Castable refractory" double precision,
    "Castable refractory severe condition" integer,
    "Glass lined" integer,
    "Acid Brick" integer,
    "Fibreglass" integer
);


ALTER TABLE public.tbl_64_dm_linning_inorganic OWNER TO postgres;

--
-- Name: tbl_64_dm_linning_inorganic_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_64_dm_linning_inorganic_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_64_dm_linning_inorganic_ID_seq" OWNER TO postgres;

--
-- Name: tbl_64_dm_linning_inorganic_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_64_dm_linning_inorganic_ID_seq" OWNED BY public.tbl_64_dm_linning_inorganic."ID";


--
-- Name: tbl_65_dm_linning_organic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_65_dm_linning_organic (
    "ID" integer NOT NULL,
    "YearInService" integer,
    "MoreThan6Years" integer,
    "WithinLast6Years" integer,
    "WithinLast3Years" double precision
);


ALTER TABLE public.tbl_65_dm_linning_organic OWNER TO postgres;

--
-- Name: tbl_65_dm_linning_organic_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_65_dm_linning_organic_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_65_dm_linning_organic_ID_seq" OWNER TO postgres;

--
-- Name: tbl_65_dm_linning_organic_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_65_dm_linning_organic_ID_seq" OWNED BY public.tbl_65_dm_linning_organic."ID";


--
-- Name: tbl_71_properties_storage_tank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_71_properties_storage_tank (
    "ID" integer NOT NULL,
    "Fluid" text,
    "Level 1 Consequence Analysis Representative Fluid" text,
    "Molecular Weight" integer,
    "Liquid Density" double precision,
    "Liquid Density Viscosity" double precision
);


ALTER TABLE public.tbl_71_properties_storage_tank OWNER TO postgres;

--
-- Name: tbl_71_properties_storage_tank_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_71_properties_storage_tank_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_71_properties_storage_tank_ID_seq" OWNER TO postgres;

--
-- Name: tbl_71_properties_storage_tank_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_71_properties_storage_tank_ID_seq" OWNED BY public.tbl_71_properties_storage_tank."ID";


--
-- Name: tbl_74_scc_dm_pwht; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_74_scc_dm_pwht (
    "ID" integer NOT NULL,
    "SVI" integer,
    "E" integer,
    "1D" integer,
    "1C" integer,
    "1B" integer,
    "1A" integer,
    "2D" integer,
    "2C" integer,
    "2B" integer,
    "2A" integer,
    "3D" integer,
    "3C" integer,
    "3B" integer,
    "3A" integer,
    "4D" integer,
    "4C" integer,
    "4B" integer,
    "4A" integer,
    "5D" integer,
    "5C" integer,
    "5B" integer,
    "5A" integer,
    "6D" integer,
    "6C" integer,
    "6B" integer,
    "6A" integer
);


ALTER TABLE public.tbl_74_scc_dm_pwht OWNER TO postgres;

--
-- Name: tbl_74_scc_dm_pwht_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."tbl_74_scc_dm_pwht_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."tbl_74_scc_dm_pwht_ID_seq" OWNER TO postgres;

--
-- Name: tbl_74_scc_dm_pwht_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."tbl_74_scc_dm_pwht_ID_seq" OWNED BY public.tbl_74_scc_dm_pwht."ID";


--
-- Name: manufacturer ManufacturerID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturer ALTER COLUMN "ManufacturerID" SET DEFAULT nextval('public."manufacturer_ManufacturerID_seq"'::regclass);


--
-- Name: rw_assessment ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_assessment ALTER COLUMN "ID" SET DEFAULT nextval('public."rw_assessment_ID_seq"'::regclass);


--
-- Name: rw_inspection_history ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_inspection_history ALTER COLUMN "ID" SET DEFAULT nextval('public."rw_inspection_history_ID_seq"'::regclass);


--
-- Name: sites SiteID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites ALTER COLUMN "SiteID" SET DEFAULT nextval('public."sites_SiteID_seq"'::regclass);


--
-- Name: tbl_204_dm_htha ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_204_dm_htha ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_204_dm_htha_ID_seq"'::regclass);


--
-- Name: tbl_213_dm_impact_exemption ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_213_dm_impact_exemption ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_213_dm_impact_exemption_ID_seq"'::regclass);


--
-- Name: tbl_214_dm_not_pwht ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_214_dm_not_pwht ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_214_dm_not_pwht_ID_seq"'::regclass);


--
-- Name: tbl_215_dm_pwht ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_215_dm_pwht ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_215_dm_pwht_ID_seq"'::regclass);


--
-- Name: tbl_3b21_si_conversion conversionFactory; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_3b21_si_conversion ALTER COLUMN "conversionFactory" SET DEFAULT nextval('public."tbl_3b21_si_conversion_conversionFactory_seq"'::regclass);


--
-- Name: tbl_511_dfb_thin ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_511_dfb_thin ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_511_dfb_thin_ID_seq"'::regclass);


--
-- Name: tbl_512_dfb_thin_tank_bottom ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_512_dfb_thin_tank_bottom ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_512_dfb_thin_tank_bottom_ID_seq"'::regclass);


--
-- Name: tbl_52_ca_properties_level_1 ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_52_ca_properties_level_1 ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_52_ca_properties_level_1_ID_seq"'::regclass);


--
-- Name: tbl_58_ca_component_dm ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_58_ca_component_dm ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_58_ca_component_dm_ID_seq"'::regclass);


--
-- Name: tbl_59_component_damage_person ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_59_component_damage_person ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_59_component_damage_person_ID_seq"'::regclass);


--
-- Name: tbl_64_dm_linning_inorganic ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_64_dm_linning_inorganic ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_64_dm_linning_inorganic_ID_seq"'::regclass);


--
-- Name: tbl_65_dm_linning_organic ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_65_dm_linning_organic ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_65_dm_linning_organic_ID_seq"'::regclass);


--
-- Name: tbl_71_properties_storage_tank ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_71_properties_storage_tank ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_71_properties_storage_tank_ID_seq"'::regclass);


--
-- Name: tbl_74_scc_dm_pwht ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_74_scc_dm_pwht ALTER COLUMN "ID" SET DEFAULT nextval('public."tbl_74_scc_dm_pwht_ID_seq"'::regclass);


--
-- Data for Name: api_component_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.api_component_type ("APIComponentTypeID", "APIComponentTypeName", "GFFSmall", "GFFMedium", "GFFLarge", "GFFRupture", "GFFTotal", "HoleCostSmall", "HoleCostMedium", "HoleCostLarge", "HoleCostRupture", "OutageSmall", "OutageMedium", "OutageLarge", "OutageRupture") FROM stdin;
1	COLBTM	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10000	25000	50000	100000	2	4	5	21
2	COLMID	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10000	25000	50000	100000	2	4	5	21
3	COLTOP	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10000	25000	50000	100000	2	4	5	21
4	COMPC	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	0	3.0000000000000001e-005	10000	20000	100000	300000	2	3	7	14
5	COMPR	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5000	10000	50000	100000	2	3	7	14
6	COURSE-1	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
7	COURSE-10	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
8	COURSE-2	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
9	COURSE-3	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
10	COURSE-4	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
11	COURSE-5	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
12	COURSE-6	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
13	COURSE-7	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
14	COURSE-8	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
15	COURSE-9	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
16	DRUM	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5000	12000	20000	40000	2	3	3	7
17	FILTER	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2000	4000	10000	0	1	1	1
18	FINFAN	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2000	20000	60000	0	0	0	0
19	HEXSS	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2000	20000	60000	0	0	0	0
20	HEXTS	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2000	20000	60000	0	0	0	0
21	HEXTUBE	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2000	20000	60000	0	0	0	0
22	KODRUM	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5000	12000	20000	40000	2	3	3	7
23	PIPE-1	2.8e-005	0	0	2.6000000000000001e-006	3.0599999999999998e-005	5	0	0	20	0	0	0	1
24	PIPE-10	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5	40	80	240	0	2	3	4
25	PIPE-12	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5	60	120	360	0	3	4	4
26	PIPE-16	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5	80	160	500	0	3	4	5
27	PIPE-2	2.8e-005	0	0	2.6000000000000001e-006	3.0599999999999998e-005	5	0	0	40	0	0	0	1
28	PIPE-4	7.9999999999999996e-006	2.0000000000000002e-005	0	2.6000000000000001e-006	3.0599999999999998e-005	5	10	0	60	0	1	0	2
29	PIPE-6	7.9999999999999996e-006	2.0000000000000002e-005	0	2.6000000000000001e-006	3.0599999999999998e-005	5	20	0	120	0	1	2	3
30	PIPE-8	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	5	30	60	180	0	2	3	3
31	PIPEGT16	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10	120	240	700	1	4	5	7
32	PUMP1S	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2500	5000	5000	0	0	0	0
33	PUMP2S	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2500	5000	5000	0	0	0	0
34	PUMPR	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	1000	2500	5000	10000	0	0	0	0
35	REACTOR	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10000	24000	40000	80000	4	6	6	14
36	TANKBOTTOM	0.00072000000000000005	0	0	1.9999999999999999e-006	0.00072199999999999999	5000	0	0	120000	5	0	0	50
37	OTHER	7.9999999999999996e-006	2.0000000000000002e-005	1.9999999999999999e-006	5.9999999999999997e-007	3.0599999999999998e-005	10000	25000	50000	100000	2	4	5	21
38	TANKROOFFIXED	6.9999999999999994e-005	2.5000000000000001e-005	5.0000000000000004e-006	9.9999999999999995e-008	0.0001	5000	12000	20000	40000	2	3	3	7
39	TANKROOFFLOAT	0.00072000000000000005	0	0	1.9999999999999999e-006	0.00072199999999999999	5000	0	0	120000	5	0	0	50
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
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
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$100000$gqKSpQPaMBAx$gUdV6YCJbGb6MusnlDYOTav6TppevDxEf0Puyw1VHGw=	2018-01-24 10:47:58	1	vuna			anhvu01011994@gmail.com	1	1	2017-12-19 08:50:49
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: component_master; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.component_master ("ComponentID", "ComponentNumber", "EquipmentID", "ComponentTypeID", "ComponentName", "ComponentDesc", "IsEquipmentLinked", "APIComponentTypeID", "Create") FROM stdin;
2	Component 2	2	4	component vuna	hello this is test	0	2	2018-03-15 14:11:39.215269
3	vuna	1	1	VUNA	cdvfdvf	1	1	2018-03-15 14:11:39.215269
4	vuna2	1	1	222	1111	1	7	2018-03-15 14:11:39.215269
6	vuna test 3	8	15	vuna component name	aaaa	0	38	2018-03-15 14:11:39.215269
8	BTM_DEMO1	2	12	tank bottom demo	demo tank proposal	1	36	2018-03-15 14:11:39.215269
9	SHELL_DM1	2	8	demo shell	this is data for shell demo	1	6	2018-03-15 14:11:39.215269
11	COMPONENT_POSTGRES	10	12	POSTGRES_COMPONENT_1	this is component demo postgres\r\n	0	36	2018-03-15 14:11:39.215269
1	N01	1	1	vuna	1	1	1	2018-03-15 14:11:39.215269
13	SHELL_DM2	10	8	DEMO SHELL POSTGRESQL		0	6	2018-03-15 14:11:39.215269
14	COMPONENT_POSGRES_2	11	8	DEMO SHELL POSGRES 2	this component demo postgres 2	0	6	2018-03-15 14:11:39.215269
18	VUNA_DEMO_COMPONENT	7	8	vuna demo	abcd	1	12	2018-04-03 15:32:23.823556
7	vuna261	1	1	vu test	fffff	1	16	2018-03-15 14:11:39.215269
43	COM_EXCEL_1	24	3	Component Hoang	No Desc	0	3	2018-05-03 11:44:23.333248
44	COM_EXCEL_2	25	3	Component Hoang	No Desc	0	3	2018-05-03 11:44:23.333248
45	EXCEL_COM_TANK_1	26	8	Oppo	N/A	1	6	2018-05-03 11:44:23.333248
46	EXCEL_COM_TANK_2	27	12	Apple	N/A	1	36	2018-05-03 11:44:23.333248
47	EXCEL_COM_TANK_3	28	12	Apple	N/A	1	36	2018-05-03 11:44:23.333248
\.


--
-- Data for Name: component_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.component_type ("ComponentTypeID", "ComponentTypeName", "ComponentTypeCode") FROM stdin;
1	Cylindrical Section	CylindricalSection
3	Elliptical Head	EllipticalHead
4	Torispherical Head	TorisphericalHead
6	Bend / Elbow	Elbow
7	Cylindrical Shell	CylindricalShell
8	Shell	Shell
9	Spherical Shell	SphericalShell
10	Hemispherical Head	HemisphericalHead
11	Reducer	Reducer
12	Tank Bottom	TankBottom
13	Nozzle	Nozzle
14	Fixed Roof	TANKROOFFIXED
15	Floating Roof	TANKROOFFLOAT
\.


--
-- Data for Name: design_code; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.design_code ("DesignCodeID", "DesignCode", "DesignCodeApp", "SiteID") FROM stdin;
2	XO08	vuna	4
1	XO07	123	4
4	POSTGRESQL_DEMO	PG_DEMO	4
8	Lab 411 Code	None	3
9	Div II	None	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2017-12-25 09:11:27	36	TANKBOTTOM	2	[{"changed": {"fields": ["outagemedium"]}}]	7	1
2	2017-12-25 09:11:58	36	TANKBOTTOM	2	[{"changed": {"fields": ["outagemedium"]}}]	7	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
3	auth	group
2	auth	permission
4	auth	user
5	contenttypes	contenttype
7	polls	apicomponenttype
10	polls	dmcategory
9	polls	dmitems
8	polls	equipmenttype
13	polls	tbl204dmhtha
14	polls	tbl511dfbthin
11	polls	tbl52capropertieslevel1
12	polls	tbl74sccdmpwht
6	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-12-19 08:47:53
2	auth	0001_initial	2017-12-19 08:47:54
3	admin	0001_initial	2017-12-19 08:47:55
4	admin	0002_logentry_remove_auto_add	2017-12-19 08:47:55
5	contenttypes	0002_remove_content_type_name	2017-12-19 08:47:55
6	auth	0002_alter_permission_name_max_length	2017-12-19 08:47:55
7	auth	0003_alter_user_email_max_length	2017-12-19 08:47:55
8	auth	0004_alter_user_username_opts	2017-12-19 08:47:55
9	auth	0005_alter_user_last_login_null	2017-12-19 08:47:55
10	auth	0006_require_contenttypes_0002	2017-12-19 08:47:55
11	auth	0007_alter_validators_add_error_messages	2017-12-19 08:47:55
12	auth	0008_alter_user_username_max_length	2017-12-19 08:47:56
13	auth	0009_alter_user_last_name_max_length	2017-12-19 08:47:56
14	sessions	0001_initial	2017-12-19 08:47:56
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
2e234civ2obb95x25wgjbg4e5u7ascj8	NDVlYTNkODQ5MzFhY2E3ODcyM2U1ZjNmOGJkMDRkY2I3MDFiMGFhYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZjI4NDhlODgwYjFkMGJlZTczM2JhMzgxMmYwOWU2Y2EyYzczN2VkIn0=	2018-01-22 04:36:16
3dfx2qtjccg4hi1mxay0joe9mwnb296v	NDVlYTNkODQ5MzFhY2E3ODcyM2U1ZjNmOGJkMDRkY2I3MDFiMGFhYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZjI4NDhlODgwYjFkMGJlZTczM2JhMzgxMmYwOWU2Y2EyYzczN2VkIn0=	2018-02-07 10:47:58
c8k4fqqgw6jyaeulsompvbpfu2fsfph3	NDVlYTNkODQ5MzFhY2E3ODcyM2U1ZjNmOGJkMDRkY2I3MDFiMGFhYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZjI4NDhlODgwYjFkMGJlZTczM2JhMzgxMmYwOWU2Y2EyYzczN2VkIn0=	2018-01-26 07:18:45
lntnsawuubgu5w0xtbeeekctmywwszjo	NDVlYTNkODQ5MzFhY2E3ODcyM2U1ZjNmOGJkMDRkY2I3MDFiMGFhYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZjI4NDhlODgwYjFkMGJlZTczM2JhMzgxMmYwOWU2Y2EyYzczN2VkIn0=	2018-01-31 06:14:00
miqq0bto3tirlk8olfns4oukmzj0uz1q	NDVlYTNkODQ5MzFhY2E3ODcyM2U1ZjNmOGJkMDRkY2I3MDFiMGFhYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZjI4NDhlODgwYjFkMGJlZTczM2JhMzgxMmYwOWU2Y2EyYzczN2VkIn0=	2018-01-23 04:56:44
rln4md0ps6et5bxvrqjer862emo185k0	ZjJlNmUyOTk4MjcxODk3MTU2NzMwMTdhMmZmMzBiNzRkZDc1NDI1Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDE1MjRkNDY4ZmRkMjg3ZWExODYxZGRjOTkwN2ExYWEyMTg1ZDJlIn0=	2018-01-08 08:45:09
uom6l3fpxwmfzw3vyh8dkmh0q6rlksmw	ZjJlNmUyOTk4MjcxODk3MTU2NzMwMTdhMmZmMzBiNzRkZDc1NDI1Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDE1MjRkNDY4ZmRkMjg3ZWExODYxZGRjOTkwN2ExYWEyMTg1ZDJlIn0=	2018-01-02 08:51:38
\.


--
-- Data for Name: dm_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dm_category ("DMCategoryID", "DMCategoryName") FROM stdin;
1	1. Mechanical and Metallurgical Mechanisms
2	2. Uniform or Localized Metal Loss
3	3. High Temperature Corrosion
4	4. Environmental-Assisted Mechanisms
5	5. Others
\.


--
-- Data for Name: dm_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dm_items ("DMItemID", "DMDescription", "DMSeq", "DMCategoryID", "DMCode", "HasDF", "FailureMode") FROM stdin;
1	885F Embrittlement	1	1	dm885F	1	Rupture
2	Brittle Fracture	2	1	dmBrittleFracture	1	Rupture
3	Cavitation	3	1	dmCavitation	0	Leakage
4	Creep Rupture	4	1	dmCreepRupture	0	Rupture
5	Dissimilar Metal Weld Cracking	5	1	dmDissimilarMetalWeldCracking	0	Rupture
6	Erosion/Erosion-Corrosion	6	1	dmErosionCorrosion	0	Leakage
7	Graphitisation	7	1	dmGraphitisation	0	Mixed
8	Internal Thinning	1	2	dmInternalThinning	1	Mixed
9	Internal Lining Degradation	2	2	dmInternalLiningDegradation	1	Mixed
10	Vibration-Induced Mechanical Fatigue	10	1	dmPipingMechanicalFatigue	1	Mixed
11	Refractory Degradation	11	1	dmRefractoryDegradation	0	Mixed
12	Reheat Cracking	12	1	dmReheatCracking	0	Rupture
13	Short Term Overheating	13	1	dmShortTermOverheating	0	Rupture
14	Sigma Phase Embrittlement	14	1	dmSigmaPhaseEmbrittlement	1	Rupture
15	Spheroidisation (Softening)	15	1	dmSpheroidisation	0	Leakage
16	Steam Blanketing	16	1	dmSteamBlanketing	0	Leakage
17	Strain Aging	17	1	dmStrainAging	0	Rupture
18	Temper Embrittlement	18	1	dmTemperEmbrittlement	1	Rupture
19	Thermal Fatigue	19	1	dmThermalFatigue	0	Rupture
20	Thermal Shock	20	1	dmThermalShock	0	Rupture
22	Other Mechanical or Metallurgical	22	1	dmMechanicalMetallurgical	0	Rupture
23	Amine Corrosion	23	2	dmAmineCorrosion	0	Mixed
24	Ammonium Bisulphide Corrosion	24	2	dmAmmoniumBisulphideCorrosion	0	Mixed
25	Ammonium Chloride Corrosion	25	2	dmAmmoniumChlorideCorrosion	0	Mixed
26	Atmospheric Corrosion	26	2	dmAtmosphericCorrosion	0	Mixed
27	Boiler Water Condensate Corrosion	27	2	dmBoilerWaterCondensateCorrosion	0	Leakage
28	Caustic Corrosion	28	2	dmCausticCorrosion	0	Leakage
29	Chloride Stress Corrosion Under Insulation	29	2	dmChlorideStressCorrosionUnderInsulation	0	Mixed
30	CO2 Corrosion	30	2	dmCO2Corrosion	0	Mixed
31	Cooling Water Corrosion	31	2	dmCoolingWaterCorrosion	0	Leakage
32	Corrosion Under Insulation	32	2	dmCorrosionUnderInsulation	1	Leakage
33	Dealloying	33	2	dmDealloying	0	Leakage
34	External Corrosion	34	2	dmExternalDamageFerriticComponent	1	Mixed
35	Flue Gas Dew Point Corrosion	35	2	dmFlueGasDewPointCorrosion	0	Mixed
36	Galvanic Corrosion	36	2	dmGalvanicCorrosion	0	Leakage
37	Graphite Corrosion	37	2	dmGraphiteCorrosion	0	Mixed
38	High Temperature H2/H2S Corrosion	38	2	dmHighTemperatureH2_H2SCorrosion	0	Mixed
39	Hydrochloric Acid Corrosion	39	2	dmHydrochloricAcidCorrosion	0	Mixed
40	Hydrofluoric Acid Corrosion	40	2	dmHydrofluoricAcidCorrosion	0	Mixed
41	Microbiologically-Induced Corrosion	41	2	dmMicrobiologicallyInducedCorrosion	0	Mixed
42	Naphthenic Acid Corrosion	42	2	dmNaphthenicAcidCorrosion	0	Leakage
43	Phenol (Carbonic Acid) Corrosion	43	2	dmPhenolCarbonicAcidCorrosion	0	Mixed
44	Soil Corrosion	44	2	dmSoilCorrosion	0	Mixed
45	Sour Water Corrosion	45	2	dmSourWaterCorrosion	0	Mixed
46	Sulphuric Acid Corrosion	46	2	dmSulphuricAcidCorrosion	0	Mixed
47	Titanium Hydriding	47	2	dmTitaniumHydriding	0	Rupture
48	Other, Metal Loss	48	2	dmOtherMetalLoss	0	Rupture
49	Carburisation	49	3	dmCarburisation	0	Rupture
50	Decarburisation	50	3	dmDecarburisation	0	Leakage
51	Fuel Ash Corrosion	51	3	dmFuelAshCorrosion	0	Leakage
52	Metal Dusting	52	3	dmMetalDusting	0	Leakage
53	Nitriding	53	3	dmNitriding	0	Rupture
54	Oxidation	54	3	dmOxidation	0	Leakage
55	Sulphidation	55	3	dmSulphidation	0	Leakage
56	Other High Temperature Corrosion	56	3	dmOtherHighTemperatureCorrosion	0	Rupture
57	Amine Stress Corrosion Cracking	57	4	dmAmineStressCorrosionCracking	1	Leakage
58	Ammonia Stress Corrosion Cracking	58	4	dmAmmoniaStressCorrosionCracking	0	Leakage
59	Blistering	59	4	dmBlistering	0	Rupture
60	Carbonate Stress Corrosion Cracking	60	4	dmCarbonateStressCorrosionCracking	1	Leakage
61	Caustic Stress Corrosion Cracking	61	4	dmCausticStressCorrosionCracking	1	Leakage
62	Chloride Stress Corrosion Cracking	62	4	dmChlorideStressCorrosionCracking	1	Leakage
63	Chloride Stress Corrosion Cracking Under Insulation	63	4	dmChlorideStressCorrosionCrackingUnderInsulation	1	Leakage
64	Corrosion Fatigue	64	4	dmCorrosionFatigue	0	Rupture
65	Deaerator Cracking	65	4	dmDeaeratorCracking	0	Rupture
66	External Chloride Stress Corrosion Cracking	66	4	dmExternalChlorideStressCorrosionCracking	1	Leakage
67	HF Produced HIC/SOHIC	67	4	dmHFProducedHIC_SOHIC	1	Leakage
68	High Temperature Hydrogen Attack	68	4	dmHighTemperatureHydrogenAttack	1	Rupture
69	HIC/SOHIC-H2S	70	4	dmHIC_SOHIC_H2S	1	Rupture
70	Hydrogen Stress Cracking (HF)	71	4	dmHydrogenStressCrackingHSCHF	1	Rupture
71	Liquid Metal Embrittlement	72	4	dmLiquidMetalEmbrittlement	0	Rupture
72	Polythionic Acid Stress Corrosion Cracking	73	4	dmPolythionicAcidStressCorrosionCracking	1	Leakage
73	Sulphide Stress Corrosion Cracking (H2S)	74	4	dmSulphideStressCorrosionCrackingH2S	1	Rupture
74	Other Environment-Assisted	75	4	dmOtherEnvironmentAssisted	0	Rupture
75	Aluminium Chloride (General + Localised Corrosion)	76	5	dmAluminiumChloride	0	Mixed
76	Ammonia (General + Localised Corrosion)	77	5	dmAmmonia	0	Mixed
77	Cladding Disbondment	78	5	dmCladdingDisbondment	0	Mixed
78	Cyanides (General + Localised Corrosion)	79	5	dmCyanides	0	Mixed
79	Formic Acid (General + Localised Corrosion)	80	5	dmFormicAcid	0	Mixed
80	Hydrogen Sulphide (General + Localised Corrosion)	81	5	dmHydrogenSulphide	0	Mixed
81	Localised Corrosion of Stainless Steel	82	5	dmLocalisedCorrosionStainlessSteel	0	Leakage
82	Oxygen (General + Localised Corrosion)	83	5	dmOxygen	0	Mixed
83	Polythionic Acid (General + Localised Corrosion)	84	5	dmPolythionicAcid	0	Mixed
84	Under Deposit Attack (Metal Thinning)	85	5	dmUnderDepositAttackMetalThinning	0	Mixed
85	Water (General + Localised Corrosion)	86	5	dmWater	0	Mixed
86	Hydrogen Embrittlement	69	3	dmHydrogenEmbrittlement	0	Rupture
\.


--
-- Data for Name: equipment_master; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipment_master ("EquipmentID", "EquipmentNumber", "EquipmentTypeID", "EquipmentName", "CommissionDate", "DesignCodeID", "SiteID", "FacilityID", "ManufacturerID", "PFDNo", "ProcessDescription", "EquipmentDesc", "Create") FROM stdin;
1	EQ01	1	Vuna Eq Demo	1990-01-04 16:25:33	1	3	1	1	1	abc	abc	2018-03-15 14:10:34.633622
2	EQ02	2	Demo 2	2000-05-04 16:26:56	1	4	2	1				2018-03-15 14:10:34.633622
3	EQ03	1	vunatest	2017-12-31 00:00:00	1	4	2	1	1	1	1	2018-03-15 14:10:34.633622
4	EQ261	15	1	2017-11-26 00:00:00	2	4	3	1	1	q	q	2018-03-15 14:10:34.633622
7	EQ2611	11	vunatest	2017-10-01 00:00:00	2	4	3	1	N01	abc	abc	2018-03-15 14:10:34.633622
8	EQ05	11	vunatest	2018-01-02 00:00:00	2	8	9	5	NO1	aaaaa	aaaaa	2018-03-15 14:10:34.633622
10	POSTGRESQL_DEMO1	3	postgresql demo	2017-10-01 00:00:00	2	11	11	2	NO:01	postgres demo 1	postgres demo 1\r\n	2018-03-15 14:10:34.633622
11	POSTGRESQL_DEMO2	11	postgresql demo 2	2010-02-25 00:00:00	1	11	11	1	NO_02	this is equipment test for postgres database	demo for postgres database using model	2018-03-15 14:10:34.633622
24	EQ_EXCEL_1	1	Pressure Machine	1995-12-12 00:00:00	8	3	1	9	No	No	No	2018-05-03 11:44:23.342248
25	EQ_EXCEL_2	2	Oil Tube	1995-12-12 00:00:00	8	3	1	10	No	No	No	2018-05-03 11:44:23.342248
26	EXCEL_TANK_DEMO_1	11	NewTank	1995-09-09 00:00:00	9	3	1	11	N/A	N/A	N/A	2018-05-03 11:44:23.342248
27	EXCEL_TANK_DEMO_2	11	Tank Bottom	1995-09-09 00:00:00	9	3	1	11	N/A	N/A	N/A	2018-05-03 11:44:23.342248
28	EXCEL_TANK_DEMO_3	11	Shell	1995-09-09 00:00:00	9	3	1	11	N/A	N/A	N/A	2018-05-03 11:44:23.342248
\.


--
-- Data for Name: equipment_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipment_type ("EquipmentTypeID", "EquipmentTypeCode", "EquipmentTypeName") FROM stdin;
1	ACCUM	Accumulator
2	AIRCO	Air Cooler
3	COLUM	Column
4	VEVES	Vertical Vessel
5	SPVES	Spherical Vessel
6	FIHEA	Fired Heater
7	PIPIN	Piping
8	PUMP	Pump
9	PLEXC	Plate Exchanger
10	STEXC	Shell and Tube Exchanger
11	TANK	Tank
12	HOVES	Horizontal Vessel
13	REVAL	Relief Valve
14	TOWER	Tower
15	FILTE	Filter
\.


--
-- Data for Name: facility; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facility ("FacilityID", "SiteID", "FacilityName", "ManagementFactor", "Create") FROM stdin;
2	4	CORTEK Facility Demo	0.10000000000000001	2018-03-15 11:57:05.236424
3	4	vunafacility	0.10000000000000001	2018-03-15 11:57:05.236424
8	8	facility test	0.26000000000000001	2018-03-15 11:57:05.236424
9	8	facility test 1	0.38	2018-03-15 11:57:05.236424
11	11	Postgres demo	0.10000000000000001	2018-03-15 11:57:05.236424
23	4	vunafacility2	0.10000000000000001	2018-04-02 15:24:37.030015
1	3	VuNA Facility	0.20999999999999999	2018-03-15 11:57:05.236424
\.


--
-- Data for Name: facility_risk_target; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facility_risk_target ("FacilityID", "RiskTarget_FC", "RiskTarget_AC") FROM stdin;
2	1000000	10000
3	100000	100
8	1000000000	20000
9	1000000	100
11	120000	1000
23	1000000	10000
1	30000	10002
\.


--
-- Data for Name: manufacturer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.manufacturer ("ManufacturerID", "ManufacturerName", "SiteID") FROM stdin;
2	manu test1	4
1	Vuna Manu 1	4
3	manufacture test2	3
5	manufacture test4	4
9	Vung Tau	3
10	Viet Nam	3
11	Lab411	3
\.


--
-- Data for Name: rw_assessment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_assessment ("ID", "EquipmentID", "ComponentID", "AssessmentDate", "RiskAnalysisPeriod", "IsEquipmentLinked", "ProposalName", "Create") FROM stdin;
123	2	2	2017-12-31 00:00:00	36	0	VuNA	2018-03-15 11:50:49.1856
124	1	7	2017-12-31 00:00:00	36	1	vu test	2018-03-15 11:50:49.1856
157	1	7	2017-12-31 00:00:00	36	1	vuna demo data	2018-03-15 11:50:49.1856
158	1	7	2017-12-31 00:00:00	36	1	vuna demo data	2018-03-15 11:50:49.1856
146	1	4	2018-02-11 00:00:00	36	1	vunaproposal	2018-03-15 11:50:49.1856
181	2	2	2010-08-27 00:00:00	36	0	vuna demo data	2018-03-15 11:50:49.1856
148	1	4	2018-02-11 00:00:00	36	1	vunaproposal	2018-03-15 11:50:49.1856
220	1	7	2018-03-02 00:00:00	36	1	postgresql demo 2	2018-03-15 11:50:49.1856
222	10	11	2018-02-25 00:00:00	36	0	demo postgres	2018-03-15 11:50:49.1856
225	10	11	2018-02-25 00:00:00	36	0	demo postgres	2018-03-15 11:50:49.1856
228	10	11	2018-02-26 00:00:00	36	0	vuna tank bottom demo 1	2018-03-15 11:50:49.1856
231	11	14	2018-03-08 00:00:00	36	0	shell demo postgres	2018-03-15 11:50:49.1856
149	1	4	2018-02-11 00:00:00	36	1	vunaproposal	2018-03-15 11:50:49.1856
80	1	1	2017-12-31 00:00:00	36	1	vunatest1	2018-03-15 11:50:49.1856
99	1	1	2017-12-31 00:00:00	36	1	vunatest1	2018-03-15 11:50:49.1856
298	1	1	2018-04-10 00:00:00	36	1	1	2018-04-10 12:52:11.493139
247	10	11	2018-03-22 00:00:00	36	0	demo	2018-03-22 14:50:49.103203
291	11	14	2018-04-09 00:00:00	36	0	demo_newvsersion	2018-04-09 16:11:40.41705
306	2	9	2018-04-12 00:00:00	36	1	a	2018-04-12 15:48:14.02054
261	1	1	2018-04-06 00:00:00	36	1	demo	2018-04-06 16:04:53.645094
312	1	1	2018-04-19 00:00:00	36	1	lab411	2018-04-18 10:52:14.676536
177	2	8	2017-08-01 00:00:00	36	1	vuna tank bottom demo 1	2018-03-15 11:50:49.1856
346	24	43	2018-04-24 00:00:00	36	0	New Excel Proposal 05-03-18	2018-05-03 11:44:23.350249
347	25	44	2018-04-24 00:00:00	36	0	New Excel Proposal 05-03-18	2018-05-03 11:44:23.350249
348	26	45	1999-09-09 00:00:00	36	1	New Excel Proposal 05-03-18	2018-05-03 11:44:23.350249
349	27	46	1999-09-09 00:00:00	36	1	New Excel Proposal 05-03-18	2018-05-03 11:44:23.350249
350	28	47	1999-09-09 00:00:00	36	1	New Excel Proposal 05-03-18	2018-05-03 11:44:23.350249
142	1	4	2018-01-28 00:00:00	36	1	vunaproposal	2018-03-15 11:50:49.1856
76	1	1	2017-12-31 00:00:00	36	1	vunatest1	2018-03-15 11:50:49.1856
68	1	1	2017-12-31 00:00:00	36	1	vunaproposal	2018-03-15 11:50:49.1856
\.


--
-- Data for Name: rw_ca_level1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_ca_level1 ("ID", "Release_Phase", fact_di, fact_mit, fact_ait, "CA_cmd", "CA_inj_flame", "CA_inj_toxic", "CA_inj_ntnf", "FC_cmd", "FC_affa", "FC_prod", "FC_inj", "FC_envi", "FC_total", "FCOF_Category") FROM stdin;
123	Gas	0	0.050000000000000003	0.83972821742605896	0	0	0	3083.7151677400302	29019.607843137299	0	243790.84967320299	154185758.38700199	0	154458568.84451801	E
124	Powder	0	0.20000000000000001	0	0	0	0	0	13490.1960784314	0	190849.67320261401	0	0	204339.86928104601	C
157	Liquid	0.25	0.20000000000000001	0.65987210231814497	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
158	Liquid	0.25	0.20000000000000001	0.65987210231814497	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
181	Gas	0.25	0.20000000000000001	0	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
220	Liquid	0.25	0.20000000000000001	0.6598721023181453	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
261	Gas	0	0.14999999999999999	0	611.11178728289269	57.900212912144212	0	0	24183.006535947712	916667.68092433899	1023381.7454878032	579.00212912144218	0	1964811.4350772114	D
312	Gas	0	0.25	0	2555.4697088379803	25.513391860599761	0	0	24183.006535947712	5110939.4176759608	2460746.0266753696	25513.391860599761	0	7621381.8427478774	D
76	Gas	0	0.25	0	2555.4697088379803	25.513391860599761	0	0	24183.006535947712	12777348.544189902	4068488.6685219607	1275669.593029988	0	18145689.812277798	E
142	Liquid	0.25	0.20000000000000001	0.6598721023181453	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
146	Liquid	0.25	0.20000000000000001	0.6598721023181453	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
148	Liquid	0.25	0.20000000000000001	0.6598721023181453	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
149	Liquid	0.25	0.14999999999999999	1	0	0	0	4.5381264326280231e-007	11309.999999999998	0	661400	0.00022690632163140117	0	672710.00022690627	C
80	Gas	0	0.25	0	2555.4697088379803	25.513391860599761	0	0	24183.006535947712	5110939.4176759608	2460746.0266753696	1275669.593029988	0	8871538.0439172648	D
99	Gas	0	0.25	0	2555.4697088379803	25.513391860599761	0	0	24183.006535947712	5110939.4176759608	2460746.0266753696	25513.391860599761	0	7621381.8427478774	D
298	Liquid	0	0.14999999999999999	0.6598721023181453	\N	\N	\N	\N	\N	\N	\N	\N	\N	100000000	E
68	Gas	0	0.20000000000000001	0	2723.4142946486586	27.482989843974753	0	0	24183.006535947712	5446828.589297317	2546748.3000779902	687074.74609936879	0	8704834.6420106236	D
\.


--
-- Data for Name: rw_ca_tank; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_ca_tank ("ID", "Hydraulic_Water", "Hydraulic_Fluid", "Seepage_Velocity", "Flow_Rate_D1", "Flow_Rate_D2", "Flow_Rate_D3", "Flow_Rate_D4", "Leak_Duration_D1", "Leak_Duration_D2", "Leak_Duration_D3", "Leak_Duration_D4", "Release_Volume_Leak_D1", "Release_Volume_Leak_D2", "Release_Volume_Leak_D3", "Release_Volume_Leak_D4", "Release_Volume_Rupture", "Liquid_Height", "Volume_Fluid", "Time_Leak_Ground", "Volume_SubSoil_Leak_D1", "Volume_SubSoil_Leak_D4", "Volume_Ground_Water_Leak_D1", "Volume_Ground_Water_Leak_D4", "Barrel_Dike_Leak", "Barrel_Dike_Rupture", "Barrel_Onsite_Leak", "Barrel_Onsite_Rupture", "Barrel_Offsite_Leak", "Barrel_Offsite_Rupture", "Barrel_Water_Leak", "Barrel_Water_Rupture", "FC_Environ_Leak", "FC_Environ_Rupture", "FC_Environ", "Material_Factor", "Component_Damage_Cost", "Business_Cost", "Consequence", "ConsequenceCategory") FROM stdin;
222	47.520000000000003	8.1058691670822967	24.563239900249382	0	\N	\N	0	360	\N	\N	360	0	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	0	\N	0	\N	0	0	0	0	0	0	0	100000000	E
225	47.520000000000003	8.1058691670822967	24.563239900249382	0	\N	\N	0	360	\N	\N	360	0	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	0	\N	0	\N	0	0	0	0	0	0	0	100000000	E
228	47.520000000000003	8.1058691670822967	24.563239900249382	0	\N	\N	0	360	\N	\N	360	0	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	0	\N	0	\N	0	0	0	0	0	0	0	100000000	E
231	\N	\N	\N	0	0	0	0	1	1	1	1	0	20.408265357679099	40.816530715358297	61.224796073037403	0.061224796073037401	0	0	1	7.1428928751876999	0.061224796073037401	0	0	7.1428928751876999	0.061224796073037401	0	0	0	0	0	0	71.428928751876995	0.61224796073037402	72.041176712607395	0	0	0	72.041176712607395	A
247	47.520000000000003	8.1058691670822967	24.563239900249382	0	\N	\N	0	360	\N	\N	360	0	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	0	\N	0	\N	0	0	0	0	0	0	0	100000000	E
291	\N	\N	\N	12.847322498182068	51.389289992728273	3288.9145595346095	780684529.75809073	1	1	1	1	12.847322498182068	51.389289992728273	3288.9145595346095	10279.900501661443	10.279900501661441	12	14685.572145230633	1	186.28617622363998	10.279900501661441	5.3672773093555293	0.2961844932538682	180.69759093693077	9.9715034866115975	0.11177170573418437	0.0061679403009968683	0.10953627161950069	0.0060445814949769304	5.3672773093555293	0.2961844932538682	28703.719177243413	1583.9681888979953	30287.687366141407	1.2	9047.9999999999982	46140	85475.687366141414	B
306	\N	\N	\N	0	0	0	0	1	1	1	1	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	100000000	E
177	47.520000000000003	33.538656461538459	101.6322923076923	135.54187127854112	\N	\N	0	1.5892249366743645	\N	\N	360	215.40652179936438	\N	\N	0	8.6162608719745742e-008	12	215.40652179936438	0	215.40652179936438	0	0	0	\N	7.5823095673376255e-008	\N	1.0339513046369488e-009	\N	1.8611123483465077e-010	\N	9.119450506897889e-009	0.015509269569554238	5.3882648988980193e-006	0.015514657834453136	1	25690173.388888847	51246.537396121887	25741419.941799626	E
348	\N	\N	\N	24.878733039407511	99.514932157630042	6368.9556580883227	61699381.336493298	1	1	1	1	24.878733039407511	99.514932157630042	1048.8624121682933	449.51246235784004	0.44951246235784004	45	2247.5623117892001	1	94.736966775407424	0.44951246235784004	5.3052701394228166	0.02517269789203902	85.26327009786668	0.40456121612205603	1.8947393355081488	0.0089902492471568007	2.2736872026097785	0.010788299096588161	5.3052701394228166	0.02517269789203902	28610.563966173046	135.75276363206757	28746.316729805112	\N	90479.999999999985	0	119226.3167298051	C
\.


--
-- Data for Name: rw_coating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_coating ("ID", "ExternalCoating", "ExternalInsulation", "InternalCladding", "InternalCoating", "InternalLining", "ExternalCoatingDate", "ExternalCoatingQuality", "ExternalInsulationType", "InsulationCondition", "InsulationContainsChloride", "InternalLinerCondition", "InternalLinerType", "CladdingCorrosionRate", "SupportConfigNotAllowCoatingMaint") FROM stdin;
123	0	1	1	1	1	\N	\N	Calcium Silicate	Average	1	Good	Castable refractory	0.29999999999999999	1
124	0	0	1	1	0	\N	\N	Asbestos	Above average	0	Average	Acid Brick	0.10000000000000001	1
157	1	0	0	0	0	2017-07-30 00:00:00	High coating quality	Asbestos	Above average	0	Average	Acid Brick	0	0
158	0	0	0	0	0	\N	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
312	0	0	1	0	0	\N	\N	\N	\N	0	\N	\N	0.10000000000000001	0
181	0	0	0	0	0	\N	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
220	0	0	0	0	0	\N	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
222	1	0	0	0	0	2017-06-25 00:00:00	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
225	0	0	0	0	0	2018-03-05 00:00:00	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
228	0	0	0	0	0	2018-03-05 00:00:00	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
231	0	0	0	0	0	\N	\N	Asbestos	Above average	0	Average	Acid Brick	0	0
247	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
291	1	1	1	1	1	2018-04-12 00:00:00	No coating or poor quality	Asbestos	Above average	1	Good	Castable refractory severe condition	0.20000000000000001	1
306	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
142	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
146	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
148	1	0	0	0	0	2001-02-08 00:00:00	Medium coating quality	\N	\N	0	\N	\N	0	1
76	1	1	0	1	1	2013-04-01 00:00:00	Medium coating quality	Pearlite	Average	1	Poor	Organic	0.10000000000000001	1
149	1	1	1	0	1	2001-02-08 00:00:00	Medium coating quality	Pearlite	Below average	1	Poor	Acid Brick	0.20000000000000001	1
80	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0.10000000000000001	0
99	0	0	1	0	0	\N	\N	\N	\N	0	\N	\N	0.10000000000000001	0
177	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
298	1	1	0	0	1	2010-04-10 00:00:00	Medium coating quality	Fibreglass	Below average	1	Average	Glass lined	0	0
261	0	0	0	0	0	\N	\N	\N	\N	0	\N	\N	0	0
346	0	1	0	0	1	2017-10-20 00:00:00	No coating or poor quality	Asbestos	Below average	0	Good	Acid Brick	15	1
347	0	1	0	0	1	2017-10-20 00:00:00	Medium coating quality	Foam Glass	Above average	0	Poor	Glass lined	15	1
348	1	1	1	1	1	2000-01-11 00:00:00	Medium coating quality	Calcium Silicate	Above average	1	Average	Castable refractory	23	1
349	1	1	1	1	1	2000-01-11 00:00:00	Medium coating quality	Calcium Silicate	Above average	1	Average	Castable refractory	23	1
350	1	1	1	1	1	2000-01-11 00:00:00	Medium coating quality	Calcium Silicate	Above average	1	Average	Castable refractory	23	1
68	0	1	1	1	1	\N	\N	Asbestos	Above average	1	Poor	Acid Brick	0.28999999999999998	1
\.


--
-- Data for Name: rw_component; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_component ("ID", "NominalDiameter", "NominalThickness", "CurrentThickness", "MinReqThickness", "CurrentCorrosionRate", "BranchDiameter", "BranchJointType", "BrinnelHardness", "ChemicalInjection", "HighlyInjectionInsp", "ComplexityProtrusion", "CorrectiveAction", "CracksPresent", "CyclicLoadingWitin15_25m", "DamageFoundInspection", "DeltaFATT", "NumberPipeFittings", "PipeCondition", "PreviousFailures", "ShakingAmount", "ShakingDetected", "ShakingTime", "TrampElements", "ShellHeight", "ReleasePreventionBarrier", "ConcreteFoundation", "SeverityOfVibration") FROM stdin;
123	98	19.050000000000001	19.050000000000001	17.68	0.28999999999999998	All branches greater than 2" Nominal OD	Piping tee weldolets	Greater than 237	1	1	Average	Experience	1	PRV chatter	1	2.7000000000000002	6 to 10	Good condition	None	Moderate	1	2 to 13 weeks	1	\N	\N	\N	\N
124	99	19.050000000000001	17	17	0.29999999999999999	All branches greater than 2" Nominal OD	Piping tee weldolets	Greater than 237	1	1	Average	Engineering Analysis	1	PRV chatter	1	2.7000000000000002	6 to 10	Broken gussets or gussets welded directly to pipe	None	Minor	1	13 to 52 weeks	1	\N	0	0	\N
157	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
158	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
181	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
220	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
222	99	0	0	0	0	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	0	0	0	None
225	0	0	0	0	0	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	0	0	0	None
228	0	0	0	0	0	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	0	0	0	None
231	9.0399999999999991	0	0	0	0	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	2	0	0	None
80	99	19.050000000000001	19	17.68	0.28999999999999998	Any branch less than or equal to 2" Nominal OD	Piping tee weldolets	Between 200 and 237	0	0	Average	Experience	0	PRV chatter	0	0.20000000000000001	6 to 10	Broken gussets or gussets welded directly to pipe	None	Moderate	0	2 to 13 weeks	0	\N	\N	\N	\N
298	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	\N	\N	0	0	\N	\N	0	\N	0	0	\N	\N	\N	\N	0	\N	0	\N	0	0	\N
312	99	19.5	18	17.68	0.25	Any branch less than or equal to 2" Nominal OD	Saddle in fittings	Between 200 and 237	0	0	Average	Experience	0	None	0	0.20000000000000001	6 to 10	Broken gussets or gussets welded directly to pipe	None	Moderate	0	Less than 2 weeks	0	\N	0	0	\N
291	99	17.079999999999998	16	14	0.29999999999999999	\N	\N	Below 200	0	0	Below average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	1.2	0	0	None
247	7	11	13	0	0.28999999999999998	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	\N	0	0	None
306	0	0	0	0	0	\N	\N	\N	0	0	\N	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	0	0	0	\N
142	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
99	99	19.050000000000001	18	17.68	0.25	Any branch less than or equal to 2" Nominal OD	Saddle in fittings	Between 200 and 237	0	0	Average	Experience	0	PRV chatter	0	0.20000000000000001	6 to 10	Broken gussets or gussets welded directly to pipe	None	Moderate	0	Less than 2 weeks	0	\N	\N	\N	\N
146	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
148	0	0	0	0	0	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	Engineering Analysis	0	None	0	0	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Minor	0	13 to 52 weeks	0	\N	0	0	\N
149	70	20	18.09	17	0.29999999999999999	Any branch less than or equal to 2" Nominal OD	Sweepolets	Below 200	0	0	Average	Engineering Analysis	0	PRV chatter	1	2.7000000000000002	Up to 5	Missing or damage supports, improper support	None	Minor	1	13 to 52 weeks	0	\N	0	0	\N
261	19	19.09	17.07	16	0.28999999999999998	Any branch less than or equal to 2" Nominal OD	\N	\N	0	0	\N	\N	0	\N	0	0	\N	\N	\N	\N	0	\N	0	\N	0	0	\N
76	99	19.050000000000001	18.5	17.68	0.29999999999999999	Any branch less than or equal to 2" Nominal OD	Piping tee weldolets	Between 200 and 237	0	0	Average	None	0	PRV chatter	1	0.20000000000000001	6 to 10	Broken gussets or gussets welded directly to pipe	None	Minor	0	Less than 2 weeks	0	\N	\N	\N	\N
347	5	29	29	28	0.5	All branches greater than 2" Nominal OD	Saddle in fittings	Between 200 and 237	0	0	Above average	Engineering Analysis	0	None	1	0.5	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Moderate	0	13 to 52 weeks	1	\N	0	0	\N
177	11.99	0	0	0	0	\N	\N	Below 200	0	0	Above average	\N	0	\N	0	\N	\N	\N	\N	\N	0	\N	0	\N	0	0	None
346	5	29	29	20	0.5	All branches greater than 2" Nominal OD	None	Below 200	0	0	Below average	Engineering Analysis	0	None	1	0.5	More than 10	Good condition	None	Moderate	0	Less than 2 weeks	1	\N	0	0	\N
348	20	18	17	16	200	\N	\N	Between 200 and 237	0	0	Above average	\N	1	\N	1	3	\N	\N	\N	\N	0	\N	1	12	1	1	Low
349	20	18	17	16	200	\N	\N	Between 200 and 237	0	0	Above average	\N	1	\N	1	3	\N	\N	\N	\N	0	\N	1	12	1	1	Low
350	20	18	17	16	200	\N	\N	Between 200 and 237	0	0	Above average	\N	1	\N	1	3	\N	\N	\N	\N	0	\N	1	12	1	1	Low
68	97.620000000000005	19.050000000000001	19.050000000000001	16.68	0.28999999999999998	Any branch less than or equal to 2" Nominal OD	None	Below 200	0	0	Above average	None	0	Valve with high pressure drop	0	0.5	More than 10	Broken gussets or gussets welded directly to pipe	Greater than one	Moderate	1	13 to 52 weeks	0	\N	\N	\N	\N
\.


--
-- Data for Name: rw_damage_mechanism; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_damage_mechanism ("ID_DM", "DMItemID", "IsActive", "Notes", "ExpectedTypeID", "IsEL", "ELValue", "IsDF", "IsUserDisabled", "DF1", "DF2", "DF3", "DFBase", "RLI", "HighestInspectionEffectiveness", "SecondInspectionEffectiveness", "NumberOfInspections", "LastInspDate", "InspDueDate", "ID") FROM stdin;
157	8	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	1990-01-04 00:00:00	2032-01-31 00:00:00	1
157	32	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	1990-01-04 00:00:00	2032-01-31 00:00:00	2
158	8	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	1990-01-04 00:00:00	2032-01-31 00:00:00	3
158	32	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	1990-01-04 00:00:00	2032-01-31 00:00:00	4
181	8	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	2000-05-04 00:00:00	2025-01-27 00:00:00	9
181	32	1	\N	0	0	0	1	0	1900	1900	1900	\N	0	E	E	0	2000-05-04 00:00:00	2025-01-27 00:00:00	10
220	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2033-01-02 00:00:00	13
220	34	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2033-01-02 00:00:00	14
220	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2033-01-02 00:00:00	15
222	8	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	16
222	32	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	17
225	8	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	18
225	32	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	19
228	8	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	21
228	32	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-03-05 00:00:00	2019-03-05 00:00:00	22
231	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	2018-03-08 00:00:00	2019-03-08 00:00:00	23
231	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	2018-03-08 00:00:00	2019-03-08 00:00:00	24
306	8	1	\N	0	0	0	1	0	5700	5700	5700	0	0	E	E	0	2018-04-12 00:00:00	2019-04-12 00:00:00	92
306	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	2018-04-12 00:00:00	2019-04-12 00:00:00	93
247	8	1	\N	0	0	0	1	0	4	4	4	0	0	E	E	0	2018-03-22 00:00:00	2033-03-22 00:00:00	27
247	32	1	\N	0	0	0	1	0	4	4	4	0	0	E	E	0	2018-03-22 00:00:00	2033-03-22 00:00:00	28
142	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-28 00:00:00	169
142	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-28 00:00:00	170
146	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	171
146	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	172
148	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	173
148	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	174
177	8	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-05-03 00:00:00	2019-05-03 00:00:00	355
177	32	1	\N	0	0	0	1	0	1390	1390	1390	0	0	E	E	0	2018-05-03 00:00:00	2019-05-03 00:00:00	356
149	8	1	\N	0	0	0	1	0	135	157.5	180	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	187
149	9	1	\N	0	0	0	1	0	1190	1190	1190	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	188
149	72	1	\N	0	0	0	1	0	39.134141431592944	43.763685041777563	48.438256936892238	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	189
149	68	1	\N	0	0	0	1	0	2000	2000	2000	0	0	E	E	0	1990-01-04 00:00:00	2019-01-11 00:00:00	190
80	8	1	\N	0	0	0	1	0	315	360	405	0	0	E	E	0	1990-01-04 00:00:00	2029-01-31 00:00:00	201
99	8	1	\N	0	0	0	1	0	525	525	600	0	0	E	E	0	1990-01-04 00:00:00	2021-01-31 00:00:00	205
99	72	1	\N	0	0	0	1	0	37.678179044906983	42.292602108548643	46.953334905223848	0	0	E	E	0	1990-01-04 00:00:00	2021-01-31 00:00:00	206
99	32	1	\N	0	0	0	1	0	20	20	20	0	0	E	E	0	1990-01-04 00:00:00	2021-01-31 00:00:00	207
298	8	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-10 00:00:00	210
291	8	1	\N	0	0	0	1	0	4.5	4.5	4.5	0	0	E	E	0	2018-04-12 00:00:00	2033-04-12 00:00:00	90
291	9	1	\N	0	0	0	1	0	9	146	1978	0	0	E	E	0	2018-04-12 00:00:00	2033-04-12 00:00:00	91
298	9	1	\N	0	0	0	1	0	612	612	612	0	0	E	E	0	1990-01-04 00:00:00	2019-01-10 00:00:00	211
298	72	1	\N	0	0	0	1	0	39.134141431592944	43.763685041777563	48.438256936892238	0	0	E	E	0	1990-01-04 00:00:00	2019-01-10 00:00:00	212
298	32	1	\N	0	0	0	1	0	1900	1900	1900	0	0	E	E	0	1990-01-04 00:00:00	2019-01-10 00:00:00	213
312	8	1	\N	0	0	0	1	0	525	525	600	0	0	E	E	0	1990-01-04 00:00:00	2022-01-19 00:00:00	228
312	72	1	\N	0	0	0	1	0	39.164846916946644	43.794704116616515	48.469563427863648	0	0	E	E	0	1990-01-04 00:00:00	2022-01-19 00:00:00	229
312	32	1	\N	0	0	0	1	0	20	20	20	0	0	E	E	0	1990-01-04 00:00:00	2022-01-19 00:00:00	230
76	8	1	\N	0	0	0	1	0	180	202.5	225	0	0	E	E	0	1990-01-04 00:00:00	2025-12-31 00:00:00	308
76	9	1	\N	0	0	0	1	0	30000	30000	30000	0	0	E	E	0	1990-01-04 00:00:00	2025-12-31 00:00:00	309
76	32	1	\N	0	0	0	1	0	6	6	6	0	0	E	E	0	1990-01-04 00:00:00	2025-12-31 00:00:00	310
348	8	1	\N	0	0	0	1	0	750	1900	1900	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	396
348	34	1	\N	0	0	0	1	0	900	900	900	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	397
348	32	1	\N	0	0	0	1	0	900	900	900	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	398
348	66	1	\N	0	0	0	1	0	862.47745123783193	862.47745123783193	862.47745123783193	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	399
348	18	1	\N	0	0	0	1	0	1.1000000000000001	1.1000000000000001	1.1000000000000001	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	400
348	1	1	\N	0	0	0	1	0	1022	1022	1022	0	0	E	E	0	2018-05-03 00:00:00	2020-05-03 00:00:00	401
68	8	1	\N	0	0	0	1	0	315	360	405	0	0	E	E	0	1990-01-04 00:00:00	2030-12-31 00:00:00	410
68	9	1	\N	0	0	0	1	0	1190	1190	1190	0	0	E	E	0	1990-01-04 00:00:00	2030-12-31 00:00:00	411
68	72	1	\N	0	0	0	1	0	39.08808731033124	43.717160177233005	48.391300649502398	0	0	E	E	0	1990-01-04 00:00:00	2030-12-31 00:00:00	412
68	32	1	\N	0	0	0	1	0	90	90	90	0	0	E	E	0	1990-01-04 00:00:00	2030-12-31 00:00:00	413
\.


--
-- Data for Name: rw_data_chart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_data_chart ("ID", risk_target, risk_age_1, risk_age_2, risk_age_3, risk_age_4, risk_age_5, risk_age_6, risk_age_7, risk_age_8, risk_age_9, risk_age_10, risk_age_11, risk_age_12, risk_age_13, risk_age_14, risk_age_15) FROM stdin;
80	30000	20523.061249276445	20523.061249276445	20523.061249276445	20523.061249276445	23088.443905435997	23088.443905435997	23088.443905435997	25653.82656159555	25653.82656159555	25653.82656159555	25653.82656159555	32494.846978021033	32494.846978021033	32494.846978021033	32494.846978021033
99	30000	27632.229123298301	27707.562346629715	27783.15503027396	31532.124376987958	31608.213128451775	31684.539396805445	31761.096710158417	35511.003937134934	35588.005340496733	35665.220425129919	35742.643997720385	39493.396103552375	39571.222090774885	39649.242467670716	39727.452970457118
298	30000	1247718.471995414	1248710.1543574042	1249705.1440078462	1250703.3448639291	1251704.6665524642	1252709.0239076468	1253716.3365264926	1254726.5283738605	1255739.5274303081	1256755.2653770975	1257773.6773135616	1258794.7015027537	1259818.2791419209	1260844.3541548231	1261872.8730033559
348	30000	17330.975852477928	31646.76908030831	46729.657938753524	62333.343633799086	78336.094922204953	94664.223667530881	111267.99852292505	119226.3167298051	119226.3167298051	119226.3167298051	119226.3167298051	119226.3167298051	119226.3167298051	119226.3167298051	119226.3167298051
261	30000	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	12.625878281806159	18.938817422709239	37.877634845418477
312	30000	27705.298534655856	27780.883550133905	27856.720475700742	31605.926976740866	31682.246215640589	31758.796688279464	31835.572273780163	35585.692162700558	35662.900913806647	35740.318304792396	35817.939394335794	35895.759481866451	39646.899069220242	39725.103928393073	39803.49496188543
76	30000	23612.351053573664	23612.351053573664	23612.351053573664	23612.351053573664	26235.945615081851	26235.945615081851	26235.945615081851	33232.197779103677	33232.197779103677	33232.197779103677	33232.197779103677	33232.197779103677	33232.197779103677	33232.197779103677	33232.197779103677
291	120000	431.22484276218353	919.95214004226716	1434.8673382188886	1967.5620353260265	2513.8804447749512	3071.3069250506646	3638.1436962013213	4213.1630050371432	4795.4332810922278	5384.2221517219323	5978.9379013713269	6579.0919694709719	7203.5058077520744	7867.2148999870833	8750.6980089342305
306	1000000	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009	5700000.0000000009
177	1000000	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269	2583357.4225191269
142	10000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000
146	10000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000
148	10000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000	3990000
149	10000	30735.523528668949	31075.180135866336	31097.053975342627	31118.99840992178	31458.866927948009	31480.946706922932	31503.091454375615	31843.154973857741	31865.424731880379	31887.754701632508	32227.99893144592	32250.445113881975	33120.562031614812	33143.119251293327	33165.730196222401
68	30000	19948.675751223604	22552.16832281914	22638.772014071714	22725.655478916979	22812.810836271037	25417.407693009111	25505.084971406333	25593.013075216568	28198.362758623833	28286.773998441498	28375.4181700115	28464.289891273696	35265.856125302336	35355.167805585363	35444.692354462204
\.


--
-- Data for Name: rw_equipment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_equipment ("ID", "CommissionDate", "AdminUpsetManagement", "ContainsDeadlegs", "CyclicOperation", "HighlyDeadlegInsp", "DowntimeProtectionUsed", "ExternalEnvironment", "HeatTraced", "InterfaceSoilWater", "LinerOnlineMonitoring", "MaterialExposedToClExt", "MinReqTemperaturePressurisation", "OnlineMonitoring", "PresenceSulphidesO2", "PresenceSulphidesO2Shutdown", "PressurisationControlled", "PWHT", "SteamOutWaterFlush", "ManagementFactor", "ThermalHistory", "YearLowestExpTemp", "Volume", "TypeOfSoil", "EnvironmentSensitivity", "DistanceToGroundWater", "AdjustmentSettle", "ComponentIsWelded", "TankIsMaintained") FROM stdin;
157	1990-01-04 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	None	0	0	\N	\N	\N	\N	0	0
158	1990-01-04 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	None	0	0	\N	\N	\N	\N	0	0
181	2000-05-04 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	\N	\N	\N	\N	0	0
220	1990-01-04 00:00:00	0	0	1	0	0	Arid/dry	0	0	0	1	0.029999999999999999	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	None	0	0	\N	\N	\N	\N	0	0
222	2017-10-01 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	High	0	Recorded settlement exceeds API 653 criteria	0	0
225	2017-10-01 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	High	0	Recorded settlement exceeds API 653 criteria	0	0
228	2017-10-01 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	High	0	Recorded settlement exceeds API 653 criteria	0	0
231	2010-02-25 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	High	0	Recorded settlement exceeds API 653 criteria	0	0
76	2017-12-31 00:00:00	1	0	1	1	0	Arid/dry	0	0	0	0	30	Amine low velocity corrosion - Key process variable	0	0	0	0	0	0.20999999999999999	None	0	100	\N	\N	\N	\N	\N	\N
142	1990-01-04 00:00:00	0	0	0	0	0	None	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	\N	0	0	\N	\N	\N	\N	0	0
146	1990-01-04 00:00:00	0	0	0	0	0	None	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	\N	0	0	\N	\N	\N	\N	0	0
306	2000-05-04 16:26:56	1	0	1	1	0	\N	0	0	0	0	0	\N	0	0	0	0	0	0.10000000000000001	\N	0	0	Coarse Sand	\N	\N	\N	0	0
124	1990-01-04 00:00:00	1	1	1	1	1	Marine	1	1	0	1	80	HCL corrosion - Corrosion coupons	0	0	0	1	1	0.20999999999999999	Solution Annealed	1	1000	\N	\N	\N	\N	0	0
123	2017-12-31 00:00:00	1	1	1	1	1	Temperate	1	1	1	1	90	HCL corrosion - Corrosion coupons	1	1	1	1	1	0.10000000000000001	Solution Annealed	1	100	\N	\N	\N	\N	\N	\N
348	1995-09-09 00:00:00	1	0	1	0	1	Arid/dry	1	1	1	1	340	HCI corrosion - Corrosion coupons	1	1	1	1	1	0.20999999999999999	Solution Annealed	1	800	Coarse Sand	High	5	Recorded settlement meets API 653 criteria	1	1
148	1990-01-04 00:00:00	0	0	0	0	0	None	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	\N	0	0	\N	\N	\N	\N	0	0
349	1995-09-09 00:00:00	1	0	1	0	1	Arid/dry	1	1	1	1	340	HCI corrosion - Corrosion coupons	1	1	1	1	1	0.20999999999999999	Solution Annealed	1	800	Coarse Sand	High	5	Recorded settlement meets API 653 criteria	1	1
177	2000-05-04 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	Low	0	Recorded settlement exceeds API 653 criteria	0	0
312	1990-01-04 16:25:33	0	0	1	0	0	None	0	0	0	0	30	Amine low velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	\N	0	100	\N	\N	\N	\N	0	0
149	1990-01-04 00:00:00	1	0	0	1	1	None	0	0	0	0	80	Amine low velocity corrosion - Key process variable	0	0	0	0	1	0.20999999999999999	\N	0	1000	\N	\N	\N	\N	0	0
350	1995-09-09 00:00:00	1	0	1	0	1	Arid/dry	1	1	1	1	340	HCI corrosion - Corrosion coupons	1	1	1	1	1	0.20999999999999999	Solution Annealed	1	800	Coarse Sand	High	5	Recorded settlement meets API 653 criteria	1	1
80	2017-12-31 00:00:00	1	0	1	1	0	None	0	0	0	0	30	Sour water high velocity corrosion - Key process variable	0	0	0	0	0	0.20999999999999999	\N	0	100	\N	\N	\N	\N	\N	\N
99	2017-12-31 00:00:00	0	0	1	0	0	None	0	0	0	0	30	Amine low velocity corrosion - Corrosion coupons	0	0	0	0	0	0.20999999999999999	\N	0	100	\N	\N	\N	\N	\N	\N
298	1990-01-04 16:25:33	0	0	0	0	0	\N	0	0	0	0	0	\N	0	0	0	0	0	0.20999999999999999	\N	0	0	\N	\N	\N	\N	0	0
247	2017-10-01 00:00:00	0	0	0	0	0	Arid/dry	0	0	0	0	0	Amine high velocity corrosion - Corrosion coupons	0	0	0	0	0	0.10000000000000001	None	0	0	Coarse Sand	High	0	Recorded settlement exceeds API 653 criteria	0	0
346	1995-12-12 00:00:00	0	1	1	1	1	Arid/dry	1	0	0	1	18	Amine low velocity corrosion - Key process variable	1	1	0	1	0	0.20999999999999999	None	0	2000	\N	\N	\N	\N	0	0
347	1995-12-12 00:00:00	0	1	1	1	1	Marine	1	0	0	1	18	Amine low velocity corrosion - Key process variable	1	1	0	1	0	0.20999999999999999	Solution Annealed	0	2000	\N	\N	\N	\N	0	0
291	2010-02-25 00:00:00	1	0	1	1	1	Arid/dry	1	1	0	1	1	\N	1	0	0	1	1	0.10000000000000001	None	0	1000	Clay	High	\N	Settlement never evaluated	1	1
261	1990-01-04 16:25:33	1	0	1	1	0	None	0	0	0	0	12	Amine low velocity corrosion - Key process variable	0	0	0	0	0	0.20999999999999999	\N	0	1000	\N	\N	\N	\N	0	0
68	2017-12-31 00:00:00	1	0	1	1	0	Arid/dry	0	0	0	0	45	Sour water low velocity corrosion - Electrical resistance probes	0	0	0	0	0	0.20999999999999999	Solution Annealed	0	100	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: rw_extcor_temperature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_extcor_temperature ("ID", "Minus12ToMinus8", "Minus8ToPlus6", "Plus6ToPlus32", "Plus32ToPlus71", "Plus71ToPlus107", "Plus107ToPlus121", "Plus121ToPlus135", "Plus135ToPlus162", "Plus162ToPlus176", "MoreThanPlus176") FROM stdin;
123	0	0	0	0	0	0	0	80	9	8.9800000000000004
124	0	0	0	0	100	0	0	0	0	0
157	0	0	0	0	0	0	0	0	0	0
158	0	0	0	0	0	0	0	0	0	0
181	0	0	0	0	0	0	0	0	0	0
220	0	0	0	0	0	0	0	0	0	0
222	0	0	0	0	0	0	0	0	0	0
225	0	0	0	0	0	0	0	0	0	0
228	0	0	0	0	0	0	0	0	0	0
231	0	0	0	0	0	0	0	0	0	0
261	0	0	0	0	100	0	0	0	0	0
346	10	30	40	50	60	10	80	90	20	10
247	0	0	0	0	0	0	0	0	0	0
347	10	30	40	50	60	10	80	90	20	10
312	2	2	0	0	90	0	0	0	0	0
348	10	23	5	14	12	5	4	4	9	14
291	0	0	0	0	100	0	0	0	0	0
306	0	0	0	0	0	0	0	0	0	0
349	10	23	5	14	12	5	4	4	9	14
350	10	23	5	14	12	5	4	4	9	14
142	0	0	0	0	0	0	0	0	0	0
146	0	0	0	0	0	0	0	0	0	0
148	0	0	0	0	0	0	0	0	0	0
177	0	0	0	0	0	0	0	0	0	0
149	0	0	0	0	100	0	0	0	0	0
80	2	2	2	2	90	12	12	12	12	2
99	2	2	2	2	90	12	12	12	12	2
298	0	0	0	0	0	0	0	0	0	0
76	2	2	2	2	90	12	12	12	12	2
68	0	0	0	0	0	0	100	0	0	0
\.


--
-- Data for Name: rw_full_fcof; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_full_fcof ("ID", "FCoFValue", "FCoFCategory", "AIL", envcost, equipcost, prodcost, popdens, injcost) FROM stdin;
123	154458568.84451801	E	\N	0	1200	50000	0.01	5000000
124	204339.86928104601	C	\N	0	1200	50000	0.001	5000000
157	100000000	E	\N	0	0	0	0	0
158	100000000	E	\N	0	0	0	0	0
181	100000000	E	\N	0	0	0	0	0
220	100000000	E	\N	0	0	0	0	0
222	100000000	E	\N	\N	\N	0	\N	\N
225	100000000	E	\N	\N	\N	0	\N	\N
228	100000000	E	\N	\N	\N	0	\N	\N
231	72.041176712607395	A	\N	\N	\N	0	\N	\N
247	100000000	E	\N	\N	\N	0	\N	\N
142	100000000	E	\N	0	0	0	0	0
146	100000000	E	\N	0	0	0	0	0
148	100000000	E	\N	0	0	0	0	0
149	672710.00022690627	C	\N	0	10000	200000	0.001	500000
76	18145689.812277798	E	\N	0	5000	50000	0.01	5000000
80	8871538.0439172648	D	\N	0	2000	50000	0.01	5000000
99	7621381.8427478774	D	\N	0	2000	50000	0.002	500000
298	100000000	E	\N	0	0	0	0	0
261	1964811.4350772114	D	\N	0	1500	50000	0.0001	100000
291	85475.687366141414	B	\N	\N	\N	20000	\N	\N
306	100000000	E	\N	\N	\N	0	\N	\N
177	25741419.941799626	E	\N	\N	\N	10000	\N	\N
312	7621381.8427478774	D	\N	0	2000	50000	0.002	500000
348	119226.3167298051	C	\N	\N	\N	\N	\N	\N
68	8704834.6420106236	D	\N	0	2000	50000	0.0050000000000000001	5000000
\.


--
-- Data for Name: rw_full_pof; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_full_pof ("ID", "ThinningAP1", "ThinningAP2", "ThinningAP3", "SCCAP1", "SCCAP2", "SCCAP3", "ExternalAP1", "ExternalAP2", "ExternalAP3", "BrittleAP1", "BrittleAP2", "BrittleAP3", "HTHA_AP1", "HTHA_AP2", "HTHA_AP3", "FatigueAP1", "FatigueAP2", "FatigueAP3", "FMS", "ThinningType", "GFFTotal", "ThinningLocalAP1", "ThinningLocalAP2", "ThinningLocalAP3", "ThinningGeneralAP1", "ThinningGeneralAP2", "ThinningGeneralAP3", "TotalDFAP1", "TotalDFAP2", "TotalDFAP3", "PoFAP1", "PoFAP2", "PoFAP3", "PoFAP1Category", "PoFAP2Category", "PoFAP3Category") FROM stdin;
123	0.90000000000000002	5.2999999999999998	23	29882.717408335699	49787.750118721502	70463.423662146801	\N	\N	\N	0	0	0	2000	2000	2000	0	0	0	0.10000000000000001	Local	3.0599999999999998e-005	1	5.2999999999999998	23	1.8999999999999999	6.2999999999999998	24	31883.717408335699	51793.050118721498	72486.423662146801	0.097564175269507294	0.158486733363288	0.221808456406169	5	5	5
124	90	495	675	29882.717408335699	49787.750118721502	70463.423662146801	\N	\N	\N	0	0	0	1	1	1	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	90	495	675	110	515	695	29973.717408335699	50283.750118721502	71139.423662146801	0.19261110806596499	0.32312337826290399	0.45714193645295598	5	5	5
157	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.0122094	0.0122094	0.0122094	5	5	5
158	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.0122094	0.0122094	0.0122094	5	5	5
181	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	3.0599999999999998e-005	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.0058139999999999997	0.0058139999999999997	0.0058139999999999997	5	5	5
220	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.012209399999999999	0.012209399999999999	0.012209399999999999	5	5	5
222	1390	1390	1390	0	0	0	1390	1390	1390	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.00072199999999999999	1390	1390	1390	2780	2780	2780	1390	1390	1390	0.100358	0.100358	0.100358	5	5	5
225	1390	1390	1390	0	0	0	1390	1390	1390	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.00072199999999999999	1390	1390	1390	2780	2780	2780	1390	1390	1390	0.100358	0.100358	0.100358	5	5	5
228	1390	1390	1390	0	0	0	1390	1390	1390	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.00072199999999999999	1390	1390	1390	2780	2780	2780	1390	1390	1390	0.100358	0.100358	0.100358	5	5	5
231	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.0001	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.019	0.019	0.019	5	5	5
247	4	4	4	0	0	0	4	4	4	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.00072199999999999999	4	4	4	8	8	8	4	4	4	0.00028880000000000003	0.00028880000000000003	0.00028880000000000003	2	2	2
142	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	0.0001	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.039900000000000005	0.039900000000000005	0.039900000000000005	5	5	5
177	1390	1390	1390	0	0	0	1390	1390	1390	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.00072199999999999999	1390	1390	1390	2780	2780	2780	1390	1390	1390	0.100358	0.100358	0.100358	5	5	5
80	315	360	405	0	0	0	1	1	1	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	315	360	405	316	361	406	315	360	405	0.0020241899999999995	0.0023133599999999995	0.0026025299999999996	4	4	4
261	0.14999999999999999	0.14999999999999999	0.14999999999999999	0	0	0	1	1	1	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	1	1	1	1.1499999999999999	1.1499999999999999	1.1499999999999999	1	1	1	6.4259999999999991e-006	6.4259999999999991e-006	6.4259999999999991e-006	1	1	1
76	180	202.5	225	0	0	0	6	6	6	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	180	202.5	225	186	208.5	231	180	202.5	225	0.0011566799999999998	0.0013012649999999998	0.0014458499999999998	4	4	4
146	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	0.0001	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.039900000000000005	0.039900000000000005	0.039900000000000005	5	5	5
148	1900	1900	1900	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	0.0001	1900	1900	1900	3800	3800	3800	1900	1900	1900	0.039900000000000005	0.039900000000000005	0.039900000000000005	5	5	5
149	135	157.5	180	39.134141431592944	43.763685041777563	48.438256936892238	1	1	1	0	0	0	2000	2000	2000	0	0	0	0.20999999999999999	Local	0.0001	135	157.5	180	136	158.5	181	2174.134141431593	2201.2636850417775	2228.4382569368922	0.045656816970063449	0.046226537385877328	0.046797203395674739	5	5	5
99	525	525	600	37.678179044906983	42.292602108548643	46.953334905223848	20	20	20	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	525	525	600	545	545	620	562.67817904490698	567.29260210854864	646.95333490522387	0.0036157699785425716	0.0036454222611495331	0.0041573221301009679	4	4	4
291	4.5	4.5	4.5	0	1674.1847610508569	3588.6935965539469	1	1	1	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.0001	4.5	4.5	4.5	5.5	5.5	5.5	4.5	1678.6847610508569	3593.1935965539469	4.5000000000000003e-005	0.016786847610508571	0.035931935965539473	2	5	5
306	5700	5700	5700	0	0	0	1900	1900	1900	0	0	0	0	0	0	0	0	0	0.10000000000000001	Local	0.0001	5700	5700	5700	7600	7600	7600	5700	5700	5700	0.057000000000000002	0.057000000000000002	0.057000000000000002	5	5	5
298	612	612	612	39.134141431592944	43.763685041777563	48.438256936892238	1900	1900	1900	0	0	0	1	1	1	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	1900	1900	1900	2512	2512	2512	1940.134141431593	1944.7636850417775	1949.4382569368922	0.012467301992839415	0.012497051440078462	0.012527090239076468	5	5	5
312	525	525	600	39.164846916946644	43.794704116616515	48.469563427863648	20	20	20	0	0	0	0	0	0	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	525	525	600	545	545	620	564.16484691694666	568.79470411661646	648.4695634278637	0.0036253233062882987	0.003655074768653377	0.0041670654145874522	4	4	4
348	0.10000000000000001	0.40000000000000002	3.2000000000000002	0	16741.847610508568	35886.935965539466	900	900	900	1022	1022	1022	0	0	0	0	0	0	0.20999999999999999	Local	0.0001	900	900	900	900.10000000000002	900.39999999999998	903.20000000000005	1922	18663.847610508568	37808.935965539466	0.040362000000000002	0.39194079982067992	0.79398765527632875	5	5	5
68	315	360	405	39.08808731033124	43.717160177233005	48.391300649502398	90	90	90	0	0	0	1	1	1	0	0	0	0.20999999999999999	Local	3.0599999999999998e-005	315	360	405	405	450	495	355.08808731033122	404.71716017723298	454.3913006495024	0.0022817960490561879	0.002600712471298899	0.0029199184979737023	4	4	4
\.


--
-- Data for Name: rw_input_ca_level1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_input_ca_level1 ("ID", "API_FLUID", "SYSTEM", "Release_Duration", "Detection_Type", "Isulation_Type", "Mitigation_System", "Equipment_Cost", "Injure_Cost", "Evironment_Cost", "Toxic_Percent", "Personal_Density", "Material_Cost", "Production_Cost", "Mass_Inventory", "Mass_Component", "Stored_Pressure", "Stored_Temp") FROM stdin;
123	Steam	Vapor	\N	C	C	Fire water monitors only	0	5000000	0	0	0.01	1.2	50000	12135	24123	2758	20
124	AlCl3	Liquid	All	C	C	Fire water deluge system and monitors	0	5000000	0	10	0.001	1.2	50000	12458	24121	303.38	27
157	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
158	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
181	C1-C2	Vapor	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
220	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
80	C1-C2	Vapor	\N	C	C	Inventory blowdown, couple with isolation system classification B or higher	2000	5000000	0	0	0.01	1	50000	12468	24154	1379	27
99	C1-C2	Vapor	\N	C	C	Inventory blowdown, couple with isolation system classification B or higher	2000	500000	0	0	0.002	1	50000	12468	24154	1379	27
298	Acid	Liquid	\N	\N	\N	\N	0	0	0	0	0	0	0	0	0	0	0
142	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
146	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
148	Acid	Liquid	\N	A	A	Fire water deluge system and monitors	0	0	0	0	0	0	0	0	0	0	0
149	Acid	Liquid	\N	A	A	Foam spray system	10000	500000	0	0	0.001	1.5	200000	1200	1500	1379	40
261	C1-C2	Vapor	\N	C	C	Foam spray system	1500	100000	0	0	0.0001	1	50000	1200	2000	1379	20
312	C1-C2	Vapor	\N	C	C	Inventory blowdown, couple with isolation system classification B or higher	2000	500000	0	0	0.002	1	50000	12468	24154	1379	27
76	C1-C2	Vapor	\N	C	C	Inventory blowdown, couple with isolation system classification B or higher	5000	5000000	0	0	0.01	1	50000	12468	24154	1379	27
346	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
347	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
68	C1-C2	Vapor	\N	C	C	Fire water deluge system and monitors	2000	5000000	0	0	0.0050000000000000001	1	50000	12400	24000	1379	20
\.


--
-- Data for Name: rw_input_ca_tank; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_input_ca_tank ("ID", "FLUID_HEIGHT", "SHELL_COURSE_HEIGHT", "TANK_DIAMETTER", "Prevention_Barrier", "Environ_Sensitivity", "P_lvdike", "P_onsite", "P_offsite", "Soil_Type", "TANK_FLUID", "API_FLUID", "SW", "ProductionCost") FROM stdin;
222	0	0	99	0	High	0	0	0	Coarse Sand	Gasoline	C6-C8	0	0
225	0	0	0	0	High	0	0	0	Coarse Sand	Gasoline	C6-C8	0	0
228	0	0	0	0	High	0	0	0	Coarse Sand	Gasoline	C6-C8	0	0
231	0	2	9.0399999999999991	0	High	0	0	0	Coarse Sand	Gasoline	C6-C8	0	0
247	0	\N	7	0	High	0	0	0	Coarse Sand	Gasoline	C6-C8	0	0
291	12	1.2	99	0	High	3	2	2	Clay	Gasoline	C6-C8	\N	20000
306	0	0	0	0	\N	0	0	0	Coarse Sand	\N	C25+	\N	0
177	12	\N	11.99	0	Low	12	10	2	Coarse Sand	Light Diesel Oil	C9-C12	0	10000
348	45	12	20	1	High	10	20	30	Coarse Sand	Light Diesel Oil	C9-C12	5	\N
349	45	12	20	1	High	10	20	30	Coarse Sand	Light Diesel Oil	C9-C12	5	\N
350	45	12	20	1	High	10	20	30	Coarse Sand	Light Diesel Oil	C9-C12	5	\N
\.


--
-- Data for Name: rw_inspection_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_inspection_history ("ID", "InspectionPlanName", "InspectionCoverageName", "EquipmentNumber", "ComponentNumber", "DM", "InspectionType", "InspectionDate", "InspectionEffective") FROM stdin;
\.


--
-- Data for Name: rw_material; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_material ("ID", "MaterialName", "DesignPressure", "DesignTemperature", "MinDesignTemperature", "BrittleFractureThickness", "CorrosionAllowance", "SigmaPhase", "SulfurContent", "HeatTreatment", "ReferenceTemperature", "PTAMaterialCode", "HTHAMaterialCode", "IsPTA", "IsHTHA", "Austenitic", "Temper", "CarbonLowAlloy", "NickelBased", "ChromeMoreEqual12", "AllowableStress", "CostFactor") FROM stdin;
123	vuna material	1500	140	-28	2	2.7000000000000002	10	Low 0.002 - 0.01%	None	2.5	347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay	1Cr-0.5Mo	1	1	1	1	1	1	1	1200	1.2
124	vuna material	200	200	0	0.29999999999999999	2.8999999999999999	1	Low 0.002 - 0.01%	Normalised Temper	2.7000000000000002	321 Stainless Stee	1.25Cr-0.5Mo	1	1	1	1	1	1	1	132	1.2
157	material demo	0	0	0	0	0	0	High > 0.01%	Annealed	0	321 Stainless Stee	1.25Cr-0.5Mo	0	0	0	0	0	0	0	0	0
158	material demo	0	0	0	0	0	0	High > 0.01%	Annealed	0	321 Stainless Stee	1.25Cr-0.5Mo	0	0	0	0	0	0	0	0	0
181	vuna material	0	0	0	0	0	0	High > 0.01%	Annealed	0	321 Stainless Stee	1.25Cr-0.5Mo	0	0	0	0	0	0	0	0	0
220	material demo	0	0	0	0	0	0	High > 0.01%	Annealed	0	321 Stainless Stee	1.25Cr-0.5Mo	0	0	0	0	0	0	0	0	0
222	vuna shell material	0	0	0	0	0	\N	High > 0.01%	Annealed	0	321 Stainless Stee	\N	0	0	0	0	0	0	0	0	0
225	vuna shell material	0	0	0	0	0	\N	High > 0.01%	Annealed	0	321 Stainless Stee	\N	0	0	0	0	0	0	0	0	0
228	vuna shell material	0	0	0	0	0	\N	High > 0.01%	Annealed	0	321 Stainless Stee	\N	0	0	0	0	0	0	0	0	0
231	vuna shell material	0	0	0	0	0	\N	High > 0.01%	Annealed	0	321 Stainless Stee	\N	0	0	0	0	0	0	0	0	0
346	Inox	100.90000000000001	400.19999999999999	100.5	30.199999999999999	11.6	2.1000000000000001	Ultra Low < 0.002%	None	160.19999999999999	Not Applicable	1.25Cr-0.5Mo	0	0	0	0	0	0	1	300.5	2.2000000000000002
347	Inox	100	200	100	60	11	60	Ultra Low < 0.002%	Sub Critical PWHT	160	L Grade 300 series Stainless Steels	C-0.5Mo (Annealed)	0	0	0	0	1	1	1	500	1
348	silver	23	1120	5	11	12	\N	Low 0.002 - 0.01%	Normalised Temper	53	Regular 300 series Stainless Steels and Alloys 600 and 800	\N	1	0	1	0	1	1	1	500	12
349	silver	23	1120	5	11	12	\N	Low 0.002 - 0.01%	Normalised Temper	53	Regular 300 series Stainless Steels and Alloys 600 and 800	\N	1	0	1	0	1	1	1	500	12
350	silver	23	1120	5	11	12	\N	Low 0.002 - 0.01%	Normalised Temper	53	Regular 300 series Stainless Steels and Alloys 600 and 800	\N	1	0	1	0	1	1	1	500	12
177	abc	0	0	0	0	0	\N	High > 0.01%	Annealed	0	\N	\N	0	0	0	0	0	0	0	0	1
261	MTA	0	0	0	0	0	0	\N	\N	0	\N	\N	0	0	0	0	0	0	0	0	1
149	adsad	2000	1000	-20	3.5	0.17000000000000001	10	Low 0.002 - 0.01%	None	2.7000000000000002	321 Stainless Stee	1Cr-0.5Mo	1	1	1	0	0	0	1	400	1.5
247	demo	0	0	0	0	0	\N	High > 0.01%	Annealed	0	\N	\N	0	0	0	0	0	0	0	0	0
80	vuna material	1300	120	-1	2.2999999999999998	3.1699999999999999	10	Low 0.002 - 0.01%	None	2	\N	\N	0	0	0	0	0	0	0	600	1
291	VuNA material	1000	350	-20	1.7	0	\N	Ultra Low < 0.002%	None	2.7000000000000002	\N	\N	1	0	1	0	1	0	0	1.7	1.2
306	aaa	0	0	0	0	0	\N	\N	\N	0	\N	\N	0	0	0	0	0	0	0	0	0
76	vuna material	1300	120	-1	2.2999999999999998	3.1699999999999999	10	High > 0.01%	None	2	\N	\N	0	0	0	0	0	0	0	600	1
99	vuna material	1300	120	-1	2.2999999999999998	3.1699999999999999	10	Low 0.002 - 0.01%	None	2	\N	\N	0	0	0	0	0	1	0	600	1
312	hoang	1300	120	-1	2.2999999999999998	3.1699999999999999	10	Low 0.002 - 0.01%	None	2	\N	\N	0	0	0	0	0	1	0	600	1
142	adsad	0	0	0	0	0	0	High > 0.01%	Annealed	0	\N	\N	0	0	0	0	0	0	0	0	0
146	adsad	0	0	0	0	0	0	High > 0.01%	Annealed	0	\N	\N	0	0	0	0	0	0	0	0	0
148	adsad	0	0	0	0	0	0	Ultra Low < 0.002%	Annealed	0	\N	\N	0	0	0	0	0	0	0	0	0
298	1	0	0	0	0	0	0	\N	\N	0	347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay	1Cr-0.5Mo	1	1	0	0	0	0	0	0	0
68	adsad	12000	1000	17	1	3.1699999999999999	1	High > 0.01%	Normalised Temper	21	321 Stainless Stee	1Cr-0.5Mo	1	1	0	0	0	0	0	240	1
\.


--
-- Data for Name: rw_stream; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rw_stream ("ID", "AmineSolution", "AqueousOperation", "AqueousShutdown", "ToxicConstituent", "Caustic", "Chloride", "CO3Concentration", "Cyanide", "ExposedToGasAmine", "ExposedToSulphur", "ExposureToAmine", "H2S", "H2SInWater", "Hydrogen", "H2SPartialPressure", "Hydrofluoric", "MaterialExposedToClInt", "MaxOperatingPressure", "MaxOperatingTemperature", "MinOperatingPressure", "MinOperatingTemperature", "CriticalExposureTemperature", "NaOHConcentration", "ReleaseFluidPercentToxic", "WaterpH", "TankFluidName", "FluidHeight", "FluidLeaveDikePercent", "FluidLeaveDikeRemainOnSitePercent", "FluidGoOffSitePercent") FROM stdin;
123	Diglycolamine DGA	1	1	1	1	0	0	1	1	1	Low Lean Amine	1	0	1	1200	1	1	1000	127	400	20	135	10	1	9	\N	\N	\N	\N	\N
124	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	102	120	44	27	150	0	0	7	\N	\N	\N	\N	\N
157	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
158	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
181	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
220	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
222	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	Gasoline	0	0	0	0
225	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	Gasoline	0	0	0	0
228	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	Gasoline	0	0	0	0
231	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	Gasoline	0	0	0	0
177	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	12	0	0	0	0	0	0	0	0	0	7	Light Diesel Oil	12	12	10	2
306	\N	0	0	0	0	0	0	0	0	0	\N	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	0	0	0	0
99	Diglycolamine DGA	1	1	1	1	1000	0	0	1	1	Low Lean Amine	1	100	1	1000	1	1	500	100	200	27	800	2	10	5	\N	\N	\N	\N	\N
346	Diethanolamine DEA	0	0	1	0	100	300	0	0	0	None	0	400	0	300	1	0	500	200	200	-2	100	10	20	10	\N	\N	\N	\N	\N
142	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
146	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
148	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
347	Sulfinol	1	1	1	1	100	300	0	0	1	Low Lean Amine	0	400	0	2000	1	1	900	150	200	-2	100	10	20	10	\N	\N	\N	\N	\N
149	Sulfinol	1	1	0	0	0	0	0	1	0	None	0	0	1	500	1	0	600	70	200	40	120	0	0	7	\N	\N	\N	\N	\N
312	Diglycolamine DGA	1	1	1	1	1000	0	0	1	1	Low Lean Amine	1	100	1	1000	1	1	500	100	200	27	800	2	10	5	\N	\N	\N	\N	\N
80	Diglycolamine DGA	0	0	1	0	1000	0	0	0	0	Low Lean Amine	0	100	0	1000	0	0	500	100	200	27	800	2	10	5	\N	\N	\N	\N	\N
76	Diglycolamine DGA	0	0	1	0	1000	0	0	0	0	Low Lean Amine	1	100	0	1000	0	1	500	100	200	27	800	2	10	5	\N	\N	\N	\N	\N
247	Diethanolamine DEA	0	0	0	0	0	0	0	0	0	High Rich Amine	0	0	0	0	0	0	0	0	0	0	0	0	0	7	Gasoline	0	0	0	0
291	Monoethanolamine MEA	0	0	0	0	0	0	0	1	0	Low Lean Amine	0	0	0	500	0	0	600	120	200	20	200	0	0	7	Gasoline	12	3	2	2
348	Diglycolamine DGA	1	1	1	1	200	300	1	1	1	Low Lean Amine	1	112	1	1000	1	1	900	500	40	10	565	45	12	9	Light Diesel Oil	45	10	20	30
349	Diglycolamine DGA	1	1	1	1	200	300	1	1	1	Low Lean Amine	1	112	1	1000	1	1	900	500	40	10	565	45	12	9	Light Diesel Oil	45	10	20	30
350	Diglycolamine DGA	1	1	1	1	200	300	1	1	1	Low Lean Amine	1	112	1	1000	1	1	900	500	40	10	565	45	12	9	Light Diesel Oil	45	10	20	30
298	\N	0	0	0	0	0	0	0	0	0	\N	0	0	0	0	0	0	0	0	0	0	0	0	0	7	\N	\N	\N	\N	\N
261	Sulfinol	0	0	0	0	0	0	0	0	0	None	0	0	0	1100	0	0	500	80	200	20	70	10	0	9	\N	\N	\N	\N	\N
68	Diglycolamine DGA	0	0	1	0	1000	0	0	0	0	Low Lean Amine	0	1000	0	10000	0	0	1000	100	200	20	80	12	1	5	\N	\N	\N	\N	\N
\.


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sites ("SiteID", "SiteName", "Create") FROM stdin;
3	SITE	2018-03-15 11:54:09.612152
4	VUNA2	2018-03-15 11:54:09.612152
8	SITE1	2018-03-15 11:54:09.612152
9	VUNATEST	2018-03-15 11:54:09.612152
11	POSTGRES demo	2018-03-15 11:54:09.612152
\.


--
-- Data for Name: tbl_204_dm_htha; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_204_dm_htha ("ID", "Susceptibility", "No Inspection", "1D", "1C", "1B", "2D", "2C", "2B") FROM stdin;
1	Damage	0	2000	2000	2000	2000	2000	2000
2	High	2000	1800	1200	800	1600	800	400
3	Low	20	18	12	8	16	8	4
4	Medium	200	180	120	80	160	80	40
5	Not	1	1	1	1	1	1	1
\.


--
-- Data for Name: tbl_213_dm_impact_exemption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_213_dm_impact_exemption ("ID", "ComponentThickness", "CurveA", "CurveB", "CurveC", "CurveD") FROM stdin;
1	0.25	18	-20	-55	-55
2	0.3125	18	-20	-55	-55
3	0.375	18	-20	-55	-55
4	0.4375	24.199999999999999	-14	-40.5	-55
5	0.5	31.600000000000001	-6.9000000000000004	-32.200000000000003	-55
6	0.5625	38.200000000000003	-0.59999999999999998	-27.199999999999999	-51
7	0.625	44	5.2000000000000002	-22.800000000000001	-47.5
8	0.6875	49.200000000000003	10.4	-18.699999999999999	-44.200000000000003
9	0.75	53.899999999999999	15.1	-15	-41.100000000000001
10	0.8125	58.200000000000003	19.5	-11.6	-38.100000000000001
11	0.875	62.100000000000001	23.5	-8.5999999999999996	-35.299999999999997
12	0.9375	65.599999999999994	27.199999999999999	-5.7000000000000002	-32.700000000000003
13	1	68.900000000000006	30.600000000000001	-3.1000000000000001	-30.100000000000001
14	1.0625	71.900000000000006	33.799999999999997	-0.69999999999999996	-27.800000000000001
15	1.125	74.599999999999994	36.700000000000003	1.6000000000000001	-25.5
16	1.1875	77.200000000000003	39.399999999999999	3.7000000000000002	-23.399999999999999
17	1.25	79.599999999999994	42	5.7999999999999998	-21.399999999999999
18	1.3125	81.799999999999997	44.399999999999999	7.7000000000000002	-19.5
19	1.375	83.799999999999997	46.600000000000001	9.5999999999999996	-17.600000000000001
20	1.4375	85.799999999999997	48.700000000000003	11.4	-15.9
21	1.5	87.599999999999994	50.700000000000003	13.1	-14.300000000000001
22	1.5625	89.200000000000003	52.5	14.800000000000001	-12.699999999999999
23	1.625	90.799999999999997	54.299999999999997	16.399999999999999	-11.199999999999999
24	1.6875	92.299999999999997	55.899999999999999	17.899999999999999	-9.8000000000000007
25	1.75	93.700000000000003	57.5	19.399999999999999	-8.5
26	1.8125	95.099999999999994	58.899999999999999	20.899999999999999	-7.2000000000000002
27	1.875	96.299999999999997	60.299999999999997	22.300000000000001	-5.9000000000000004
28	1.9375	97.5	61.700000000000003	23.699999999999999	-4.7000000000000002
29	2	98.599999999999994	63	25	-3.6000000000000001
30	2.0625	99.700000000000003	64.200000000000003	26.300000000000001	-2.5
31	2.125	100.7	65.299999999999997	27.5	-1.3999999999999999
32	2.1875	101.7	66.400000000000006	28.699999999999999	-0.40000000000000002
33	2.25	102.59999999999999	67.5	29.899999999999999	0.59999999999999998
34	2.3125	103.5	68.5	31	1.6000000000000001
35	2.375	104.3	69.5	32.100000000000001	2.5
36	2.4375	105.09999999999999	70.5	33.200000000000003	3.3999999999999999
37	2.5	105.8	71.400000000000006	34.299999999999997	4.2999999999999998
38	2.5625	106.5	72.299999999999997	35.299999999999997	5.2000000000000002
39	2.625	107.2	73.200000000000003	36.299999999999997	6
40	2.6875	107.90000000000001	74	37.200000000000003	6.9000000000000004
41	2.75	108.5	74.799999999999997	38.200000000000003	7.7000000000000002
42	2.8125	109.09999999999999	75.599999999999994	39.100000000000001	8.5
43	2.875	109.7	76.400000000000006	39.899999999999999	9.3000000000000007
44	2.9375	110.2	77.200000000000003	40.799999999999997	10.1
45	3	110.8	77.900000000000006	41.700000000000003	10.9
46	3.0625	111.3	78.700000000000003	42.5	11.699999999999999
47	3.125	111.7	79.400000000000006	43.299999999999997	12.4
48	3.1875	112.2	80.099999999999994	44	13.199999999999999
49	3.25	112.59999999999999	80.799999999999997	44.799999999999997	13.9
50	3.3125	113.09999999999999	81.5	45.5	14.699999999999999
51	3.375	113.5	82.099999999999994	46.299999999999997	15.4
52	3.4375	113.90000000000001	82.799999999999997	47	16.199999999999999
53	3.5	114.2	83.5	47.700000000000003	16.899999999999999
54	3.5625	114.59999999999999	84.099999999999994	48.299999999999997	17.600000000000001
55	3.625	114.90000000000001	84.799999999999997	49	18.300000000000001
56	3.6875	115.3	85.400000000000006	49.600000000000001	19.100000000000001
57	3.75	115.59999999999999	86	50.200000000000003	19.800000000000001
58	3.8125	115.90000000000001	86.700000000000003	50.899999999999999	20.5
59	3.875	116.2	87.299999999999997	51.399999999999999	21.199999999999999
60	3.9375	116.40000000000001	87.900000000000006	52	21.899999999999999
61	4	116.7	88.5	52.600000000000001	22.5
\.


--
-- Data for Name: tbl_214_dm_not_pwht; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_214_dm_not_pwht ("ID", "Tmin-Tref", "6.4", "12.7", "25.4", "38.1", "50.8", "63.5", "76.2", "88.9", "101.6") FROM stdin;
1	-73	4	61	579	1436	2336	3160	3883	4509	5000
2	-62	3	46	474	1239	2080	2873	3581	4203	4746
3	-51	2	30	350	988	1740	2479	3160	3769	4310
4	-40	2	16	220	697	1317	1969	2596	3176	3703
5	-29	1.2	7	109	405	850	1366	1897	2415	2903
6	-18	0.90000000000000002	3	39	175	424	759	1142	1545	1950
7	-7	0.10000000000000001	1.3	10	49	143	296	500	741	1008
8	4	0	0.69999999999999996	2	9	29	69	133	224	338
9	16	0	0	1	2	4	9	19	36	60
10	27	0	0	0	0.80000000000000004	1.1000000000000001	2	2	4	6
11	38	0	0	0	0	0	0	0.90000000000000002	1.1000000000000001	1.2
\.


--
-- Data for Name: tbl_215_dm_pwht; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_215_dm_pwht ("ID", "Tmin-Tref", "6.4", "12.7", "25.4", "38.1", "50.8", "63.5", "76.2", "88.9", "101.6") FROM stdin;
1	-73	0	1.3	9	46	133	277	472	704	962
2	-62	0	1.2	7	34	102	219	382	582	810
3	-51	0	1.1000000000000001	5	22	68	153	277	436	623
4	-40	0	0.90000000000000002	3	12	38	90	171	281	416
5	-29	0	0.40000000000000002	2	5	17	41	83	144	224
6	-18	0	0	1.1000000000000001	2	6	14	29	53	88
7	-7	0	0	0.59999999999999998	1.2	2	4	7	13	23
8	4	0	0	0	0.5	1.1000000000000001	1.3	2	3	4
9	16	0	0	0	0	0	0.5	0.90000000000000002	1.1000000000000001	1.3
10	27	0	0	0	0	0	0	0	0	0.20000000000000001
11	38	0	0	0	0	0	0	0	0	0
\.


--
-- Data for Name: tbl_3b21_si_conversion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_3b21_si_conversion ("conversionFactory", "SIUnits", "USUnits") FROM stdin;
1	31623	12
2	1000	1
3	4536	10000
4	2.2050000000000001	1
5	25.199999999999999	55.600000000000001
6	55.600000000000001	100
7	1	10.763
8	0.092899999999999996	1
9	0.123	0.59999999999999998
10	9.7439999999999998	63.32
11	0.14499999999999999	1
12	1.8	1
13	6.29	0.17799999999999999
14	1	3600
15	4.6849999999999996	1
16	30.890000000000001	70
17	0.0014809999999999999	0.0072300000000000003
18	0.0050000000000000001	0.016400000000000001
19	1.085	1.0149999999999999
20	1.0129999999999999	0.14699999999999999
21	5328	9590
22	5.7999999999999998	14.619999999999999
23	0.45000000000000001	0.34599999999999997
24	2.6000000000000001	2.2789999999999999
25	0.029600000000000001	0.043799999999999999
26	100	14.5
27	1	0.3967
28	1000	6895
29	0.00042999999999999999	0.000185
30	9.76e-008	6.4300000000000003e-007
31	864	7200
32	0.54300000000000004	107
33	0.081500000000000003	16.030000000000001
34	86.400000000000006	183000
35	2.3820000000000001	0.025899999999999999
36	30.5	100
\.


--
-- Data for Name: tbl_511_dfb_thin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_511_dfb_thin ("ID", art, "E", insp, "D", "C", "B", "A") FROM stdin;
1	0.02	1	1	1	1	1	1
2	0.02	1	2	1	1	1	1
3	0.02	1	3	1	1	1	1
4	0.02	1	4	1	1	1	1
5	0.02	1	5	1	1	1	1
6	0.02	1	6	1	1	1	1
7	0.040000000000000001	1	1	1	1	1	1
8	0.040000000000000001	1	2	1	1	1	1
9	0.040000000000000001	1	3	1	1	1	1
10	0.040000000000000001	1	4	1	1	1	1
11	0.040000000000000001	1	5	1	1	1	1
12	0.040000000000000001	1	6	1	1	1	1
13	0.059999999999999998	1	1	1	1	1	1
14	0.059999999999999998	1	2	1	1	1	1
15	0.059999999999999998	1	3	1	1	1	1
16	0.059999999999999998	1	4	1	1	1	1
17	0.059999999999999998	1	5	1	1	1	1
18	0.059999999999999998	1	6	1	1	1	1
19	0.080000000000000002	1	1	1	1	1	1
20	0.080000000000000002	1	2	1	1	1	1
21	0.080000000000000002	1	3	1	1	1	1
22	0.080000000000000002	1	4	1	1	1	1
23	0.080000000000000002	1	5	1	1	1	1
24	0.080000000000000002	1	6	1	1	1	1
25	0.10000000000000001	2	1	2	1	1	1
26	0.10000000000000001	2	2	1	1	1	1
27	0.10000000000000001	2	3	1	1	1	1
28	0.10000000000000001	2	4	1	1	1	1
29	0.10000000000000001	2	5	1	1	1	1
30	0.10000000000000001	2	6	1	1	1	1
31	0.12	6	1	5	3	2	1
32	0.12	6	2	4	2	1	1
33	0.12	6	3	3	1	1	1
34	0.12	6	4	2	1	1	1
35	0.12	6	5	2	1	1	1
36	0.12	6	6	1	1	1	1
37	0.14000000000000001	20	1	17	10	6	1
38	0.14000000000000001	20	2	13	6	1	1
39	0.14000000000000001	20	3	10	3	1	1
40	0.14000000000000001	20	4	7	2	1	1
41	0.14000000000000001	20	5	5	1	1	1
42	0.14000000000000001	20	6	4	1	1	1
43	0.16	90	1	70	50	20	3
44	0.16	90	2	50	20	4	1
45	0.16	90	3	40	10	1	1
46	0.16	90	4	30	5	1	1
47	0.16	90	5	20	2	1	1
48	0.16	90	6	14	1	1	1
49	0.17999999999999999	250	1	200	130	70	7
50	0.17999999999999999	250	2	170	70	10	1
51	0.17999999999999999	250	3	130	35	3	1
52	0.17999999999999999	250	4	100	15	1	1
53	0.17999999999999999	250	5	70	7	1	1
54	0.17999999999999999	250	6	50	3	1	1
55	0.20000000000000001	400	1	300	210	110	15
56	0.20000000000000001	400	2	290	120	20	1
57	0.20000000000000001	400	3	260	60	5	1
58	0.20000000000000001	400	4	180	20	2	1
59	0.20000000000000001	400	5	120	10	1	1
60	0.20000000000000001	400	6	100	6	1	1
61	0.25	520	1	450	290	150	20
62	0.25	520	2	350	170	30	2
63	0.25	520	3	240	80	6	1
64	0.25	520	4	200	30	2	1
65	0.25	520	5	150	15	2	1
66	0.25	520	6	120	7	1	1
67	0.29999999999999999	650	1	550	400	200	30
68	0.29999999999999999	650	2	400	200	40	4
69	0.29999999999999999	650	3	320	110	9	2
70	0.29999999999999999	650	4	240	50	4	2
71	0.29999999999999999	650	5	180	25	3	2
72	0.29999999999999999	650	6	150	10	2	2
73	0.34999999999999998	750	1	650	550	300	80
74	0.34999999999999998	750	2	600	300	80	10
75	0.34999999999999998	750	3	540	150	20	5
76	0.34999999999999998	750	4	440	90	10	4
77	0.34999999999999998	750	5	350	70	6	4
78	0.34999999999999998	750	6	280	40	5	4
79	0.40000000000000002	900	1	800	700	400	130
80	0.40000000000000002	900	2	700	400	120	30
81	0.40000000000000002	900	3	600	200	50	10
82	0.40000000000000002	900	4	500	140	20	8
83	0.40000000000000002	900	5	400	110	10	8
84	0.40000000000000002	900	6	350	90	9	8
85	0.45000000000000001	1050	1	900	810	500	200
86	0.45000000000000001	1050	2	800	500	160	40
87	0.45000000000000001	1050	3	700	270	60	20
88	0.45000000000000001	1050	4	600	200	30	15
89	0.45000000000000001	1050	5	500	160	20	15
90	0.45000000000000001	1050	6	400	130	20	15
91	0.5	1200	1	1100	970	600	270
92	0.5	1200	2	1000	600	200	60
93	0.5	1200	3	900	380	80	40
94	0.5	1200	4	800	270	50	40
95	0.5	1200	5	700	210	40	40
96	0.5	1200	6	600	180	40	40
97	0.55000000000000004	1350	1	1200	1130	700	350
98	0.55000000000000004	1350	2	1100	750	300	100
99	0.55000000000000004	1350	3	1000	500	130	90
100	0.55000000000000004	1350	4	900	350	100	90
101	0.55000000000000004	1350	5	800	260	90	90
102	0.55000000000000004	1350	6	700	240	90	90
103	0.59999999999999998	1500	1	1400	1250	850	500
104	0.59999999999999998	1500	2	1300	900	400	230
105	0.59999999999999998	1500	3	1200	620	250	210
106	0.59999999999999998	1500	4	1000	450	220	210
107	0.59999999999999998	1500	5	900	360	210	210
108	0.59999999999999998	1500	6	800	300	210	210
109	0.65000000000000002	1900	1	1700	1400	1000	700
110	0.65000000000000002	1900	2	1600	1105	670	530
111	0.65000000000000002	1900	3	1300	880	550	500
112	0.65000000000000002	1900	4	1200	700	530	500
113	0.65000000000000002	1900	5	1100	840	500	500
114	0.65000000000000002	1900	6	1000	600	500	500
\.


--
-- Data for Name: tbl_512_dfb_thin_tank_bottom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_512_dfb_thin_tank_bottom ("ID", art, "E", insp, "D", "C", "B", "A") FROM stdin;
1	0.050000000000000003	4	1	1	1	1	1
2	0.10000000000000001	14	1	3	1	1	1
3	0.14999999999999999	32	1	8	2	1	1
4	0.20000000000000001	56	1	18	6	2	1
5	0.25	87	1	32	11	4	3
6	0.29999999999999999	125	1	53	21	9	6
7	0.34999999999999998	170	1	80	36	16	12
8	0.40000000000000002	222	1	115	57	29	21
9	0.45000000000000001	281	1	158	86	47	36
10	0.5	347	1	211	124	73	58
11	0.55000000000000004	420	1	273	173	109	89
12	0.59999999999999998	500	1	346	234	158	133
13	0.65000000000000002	587	1	430	309	222	192
14	0.69999999999999996	681	1	527	401	305	270
15	0.75	782	1	635	510	409	370
16	0.80000000000000004	890	1	757	638	538	498
17	0.84999999999999998	1005	1	893	789	696	658
18	0.90000000000000002	1126	1	1044	963	888	856
19	0.94999999999999996	1255	1	1209	1163	1118	1098
20	1	1390	1	1390	1390	1390	1390
\.


--
-- Data for Name: tbl_52_ca_properties_level_1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_52_ca_properties_level_1 ("ID", "Fluid", "MW", "Density", "NBP", "Ambient", ideal, "A", "B", "C", "D", "E", "Auto") FROM stdin;
1	Acid	18	62.299999999999997	212	Liquid	3	276000	-2090	8.125	-0.0141	9.3700000000000001e-006	0
2	AlCl3	133.5	152	382	Powder	1	43400	39700	417	24000	0	1036
3	C1-C2	23	15.638999999999999	-193	Gas	1	12.300000000000001	0.115	-2.87e-005	-1.3000000000000001e-009	0	1036
4	C13-C16	205	47.728000000000002	502	Liquid	1	-11.699999999999999	1.3899999999999999	-0.00077200000000000001	1.67e-007	0	396
5	C17-C25	280	48.383000000000003	651	Liquid	1	-22.399999999999999	1.9399999999999999	-0.0011199999999999999	-2.53e-007	0	396
6	C25+	422	56.186999999999998	981	Liquid	1	-22.399999999999999	1.9399999999999999	-0.0011199999999999999	-2.53e-007	0	396
7	C3-C4	51	33.609999999999999	-6.2999999999999998	Gas	1	2.6320000000000001	0.31879999999999997	-13470	1.466e-008	0	696
8	C5	72	39.030000000000001	97	Liquid	1	-3.6259999999999999	0.48730000000000001	-0.00025999999999999998	5.2999999999999998e-008	0	544
9	C6-C8	100	42.701999999999998	210	Liquid	1	-5.1459999999999999	0.67620000000000002	-0.00036499999999999998	7.6580000000000001e-008	0	433
10	C9-C12	149	45.823	364	Liquid	1	-8.5	1.01	-0.00055599999999999996	1.18e-007	0	406
11	CO	28	50	-312	Gas	2	29100	8770	3090	8460	1540	1128
12	DEE	74	45	95	Liquid	2	86200	255000	1540	144000	-689	320
13	EE	90	58	275	Liquid	2	32500	300000	1170	208000	473	455
14	EEA	132	61	313	Liquid	2	106000	240000	659	150000	1970	715
15	EG	62	69	387	Liquid	2	63000	146000	1670	97300	774	745
16	EO	44	55	51	Gas	2	33500	121000	1610	82400	737	804
17	H2	2	4.4329999999999998	-423	Gas	1	27.100000000000001	0.0092700000000000005	-1.38e-005	7.6500000000000007e-009	0	752
18	H2S	34	61.993000000000002	-75	Gas	1	31.899999999999999	0.0014400000000000001	2.4300000000000001e-005	-1.18e-008	0	500
19	HCl	36	74	-121	Gas	0	0	0	0	0	0	0
20	HF	20	60.369999999999997	68	Gas	1	29.100000000000001	0.00066100000000000002	-2.03e-006	2.5000000000000001e-009	0	32000
21	Methanol	32	50	149	Liquid	2	39300	87900	1920	53700	897	867
22	Nitric Acid	63	95	250	Liquid	0	0	0	0	0	0	0
23	NO2	90	58	275	Liquid	0	0	0	0	0	0	0
24	Phosgene	99	86	181	Liquid	0	0	0	0	0	0	0
25	PO	58	52	93	Liquid	2	49500	174000	1560	115000	702	840
26	Pyrophoric	149	45.823	364	Liquid	1	-8.5	1.01	-0.00055599999999999996	1.18e-007	0	0
27	Steam	18	62.299999999999997	212	Gas	3	33400	26800	2610	8900	1170	0
28	Styrene	104	42.700000000000003	293	Liquid	2	89300	215000	772	99900	2440	914
29	TDI	174	76	484	Liquid	0	0	0	0	0	0	1148
30	Water	18	62.299999999999997	212	Liquid	3	276000	-2090	8.125	-0.0141	9.3700000000000001e-006	0
\.


--
-- Data for Name: tbl_58_ca_component_dm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_58_ca_component_dm ("ID", "Fluid", "CAINL_gas_a", "CAINL_gas_b", "CAINL_liquid_a", "CAINL_liquid_b", "CAIL_gas_a", "CAIL_gas_b", "CAIL_liquid_a", "CAIL_liquid_b", "IAINL_gas_a", "IAINL_gas_b", "IAINL_liquid_a", "IAINL_liquid_b", "IAIL_gas_a", "IAIL_gas_b", "IAIL_liquid_a", "IAIL_liquid_b") FROM stdin;
1	Aromatics	64.140000000000001	0.96299999999999997	353.5	0.88300000000000001	1344	0.93700000000000006	487.69999999999999	0.26800000000000002	18.079999999999998	0.68600000000000005	0.14000000000000001	0.93500000000000005	512.60000000000002	0.71299999999999997	1.4039999999999999	0.93500000000000005
2	C1-C2	8.6690000000000005	0.97999999999999998	0	0	55.130000000000003	0.94999999999999996	0	0	6.4690000000000003	0.67000000000000004	0	0	163.69999999999999	0.62	0	0
3	C13-C16	0	0	12.109999999999999	0.90000000000000002	0	0	196.69999999999999	0.92000000000000004	0	0	0.085999999999999993	0.88	0	0	1.714	0.88
4	C17-C25	0	0	3.7850000000000001	0.90000000000000002	0	0	165.5	0.92000000000000004	0	0	0.021000000000000001	0.91000000000000003	0	0	1.0680000000000001	0.91000000000000003
5	C25+	0	0	2.0979999999999999	0.91000000000000003	0	0	103	0.90000000000000002	0	0	0.0060000000000000001	0.98999999999999999	0	0	0.28399999999999997	0.98999999999999999
6	C3-C4	10.130000000000001	1	0	0	64.230000000000004	1	0	0	4.5899999999999999	0.71999999999999997	0	0	79.939999999999998	0.63	0	0
7	C5	5.1150000000000002	0.98999999999999999	100.59999999999999	0.89000000000000001	62.409999999999997	1	0	0	2.214	0.72999999999999998	0.27100000000000002	0.84999999999999998	41.380000000000003	0.60999999999999999	0	0
8	C6-C8	5.8460000000000001	0.97999999999999998	34.170000000000002	0.89000000000000001	63.979999999999997	1	103.40000000000001	0.94999999999999996	2.1880000000000002	0.66000000000000003	0.749	0.78000000000000003	41.490000000000002	0.60999999999999999	8.1799999999999997	0.55000000000000004
9	C9-C12	2.419	0.97999999999999998	24.600000000000001	0.90000000000000002	76.980000000000004	0.94999999999999996	110.3	0.94999999999999996	1.111	0.66000000000000003	0.55900000000000005	0.76000000000000001	42.280000000000001	0.60999999999999999	0.84799999999999998	0.53000000000000003
10	CO	0.040000000000000001	1.752	0	0	0	0	0	0	10.970000000000001	0.66700000000000004	0	0	0	0	0	0
11	DEE	9.0719999999999992	1.1339999999999999	164.19999999999999	1.1060000000000001	67.420000000000002	1.0329999999999999	976	0.64900000000000002	24.510000000000002	0.66700000000000004	0.98099999999999998	0.91900000000000004	0	0	1.0900000000000001	0.91900000000000004
12	EE	2.5950000000000002	1.0049999999999999	35.450000000000003	1	0	0	0	0	6.1189999999999998	0.66700000000000004	14.789999999999999	1	0	0	0	0
13	EEA	0	1.0349999999999999	23.960000000000001	1	0	0	0	0	1.2609999999999999	0.66700000000000004	14.130000000000001	1	0	0	0	0
14	EG	1.548	0.97299999999999998	22.120000000000001	1	0	0	0	0	1.0269999999999999	0.66700000000000004	14.130000000000001	1	0	0	0	0
15	EO	6.7119999999999997	1.069	0	0	0	0	0	0	21.460000000000001	0.66700000000000004	0	0	0	0	0	0
16	H2	13.130000000000001	0.99199999999999999	0	0	86.019999999999996	1	0	0	9.6050000000000004	0.65700000000000003	0	0	216.5	0.61799999999999999	0	0
17	H2S	6.5540000000000003	1	0	0	38.109999999999999	0.89000000000000001	0	0	22.629999999999999	0.63	0	0	53.719999999999999	0.60999999999999999	0	0
18	HF	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
19	Methanol	0.0050000000000000001	0.90900000000000003	340.39999999999998	0.93400000000000005	0	0	0	0	4.4249999999999998	0.66700000000000004	0.36299999999999999	0.90000000000000002	0	0	0	0
20	PO	3.2770000000000001	1.1140000000000001	257	0.95999999999999996	0	0	0	0	10.32	0.66700000000000004	0.629	0.86899999999999999	0	0	0	0
21	Pyrophoric	2.419	0.97999999999999998	24.600000000000001	0.90000000000000002	76.980000000000004	0.94999999999999996	110.3	0.94999999999999996	1.111	0.66000000000000003	0.55900000000000005	0.76000000000000001	42.280000000000001	0.60999999999999999	0.84799999999999998	0.53000000000000003
22	Styrene	3.952	1.097	21.100000000000001	1	80.109999999999999	1.0549999999999999	0	0	1.804	0.66700000000000004	14.359999999999999	1	83.680000000000007	0.71299999999999997	143.59999999999999	1
\.


--
-- Data for Name: tbl_59_component_damage_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_59_component_damage_person ("ID", "Fluid", "CAINL_gas_a", "CAINL_gas_b", "CAINL_liquid_a", "CAINL_liquid_b", "CALL_gas_a", "CALL_gas_b", "CALL_liquid_a", "CALL_liquid_b", "IAINL_gas_a", "IAINL_gas_b", "IAINL_liquid_a", "IAINL_liquid_b", "IAIL_gas_a", "IAIL_gas_b", "IAIL_liquid_a", "IAIL_liquid_b") FROM stdin;
1	Aromatics	12.76	0.96299999999999997	66.010000000000005	0.88300000000000001	261.89999999999998	0.93700000000000006	56	0.26800000000000002	2.8889999999999998	0.68600000000000005	0.027	0.93500000000000005	83.680000000000007	0.71299999999999997	0.27300000000000002	0.93500000000000005
2	C1-C2	21.829999999999998	0.95999999999999996	0	0	143.19999999999999	0.92000000000000004	0	0	12.460000000000001	0.67000000000000004	0	0	473.89999999999998	0.63	0	0
3	C13-C16	0	0	34.359999999999999	0.89000000000000001	0	0	539.39999999999998	0.90000000000000002	0	0	0.24199999999999999	0.88	0	0	4.843	0.88
4	C17-C25	0	0	10.699999999999999	0.89000000000000001	0	0	458	0.90000000000000002	0	0	0.060999999999999999	0.91000000000000003	0	0	3.052	0.90000000000000002
5	C25+	0	0	6.1959999999999997	0.89000000000000001	0	0	303.60000000000002	0.90000000000000002	0	0	0.016	0.98999999999999999	0	0	0.83299999999999996	0.98999999999999999
6	C3-C4	25.640000000000001	1	0	0	171.40000000000001	1	0	0	9.702	0.75	0	0	270.39999999999998	0.63	0	0
7	C5	12.710000000000001	1	290.10000000000002	0.89000000000000001	166.09999999999999	1	0	0	4.8200000000000003	0.76000000000000001	0.79000000000000004	0.84999999999999998	146.69999999999999	0.63	0	0
8	C6-C8	3.4900000000000002	0.95999999999999996	96.879999999999995	0.89000000000000001	169.69999999999999	1	252.80000000000001	0.92000000000000004	4.2160000000000002	0.67000000000000004	2.1859999999999999	0.78000000000000003	147.19999999999999	0.63	31.890000000000001	0.54000000000000004
9	C9-C12	5.7549999999999999	0.95999999999999996	70.030000000000001	0.89000000000000001	188.59999999999999	0.92000000000000004	269.39999999999998	0.92000000000000004	2.0350000000000001	0.66000000000000003	1.609	0.76000000000000001	151	0.63	2.847	0.54000000000000004
10	CO  	5.4909999999999997	0.99099999999999999	0	0	0	0	0	0	16.91	0.69199999999999995	0	0	0	0	0	0
11	DEE	26.760000000000002	1.0249999999999999	236.69999999999999	1.2190000000000001	241.5	0.997	488.89999999999998	0.86399999999999999	31.710000000000001	0.68200000000000005	8.3330000000000002	0.81399999999999995	128.30000000000001	0.65700000000000003	9.2579999999999991	0.81399999999999995
12	EE	7.1070000000000002	0.96899999999999997	8.1419999999999995	0.80000000000000004	0	0	0	0	25.359999999999999	0.66000000000000003	0.029000000000000001	0.92700000000000005	0	0	0	0
13	EEA	0	0.94599999999999995	79.659999999999997	0.83499999999999996	0	0	0	0	1.825	0.68700000000000006	0.029999999999999999	0.92400000000000004	0	0	0	0
14	EG	5.0419999999999998	0.94699999999999995	59.960000000000001	0.86899999999999999	0	0	0	0	1.4350000000000001	0.68700000000000006	0.027	0.92200000000000004	0	0	0	0
15	EO	11	1.105	0	0	0	0	0	0	34.700000000000003	0.66500000000000004	0	0	0	0	0	0
16	H2	32.049999999999997	0.93300000000000005	0	0	228.80000000000001	1	0	0	18.43	0.65200000000000002	0	0	636.5	0.621	0	0
17	H2S	10.65	1	0	0	73.25	0.93999999999999995	0	0	41.43	0.63	0	0	191.5	0.63	0	0
18	HF	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
19	Methanol	0	1.008	849.89999999999998	0.90200000000000002	0	0	0	0	6.0350000000000001	6.8799999999999999	1.157	0.871	0	0	0	0
20	PO	8.2390000000000008	1.0469999999999999	352.80000000000001	0.83999999999999997	0	0	0	0	13.33	0.68200000000000005	2.7320000000000002	0.82999999999999996	0	0	0	0
21	Pyrophoric	5.7549999999999999	0.95999999999999996	70.030000000000001	0.89000000000000001	188.59999999999999	0.92000000000000004	269.39999999999998	0.92000000000000004	2.0350000000000001	0.66000000000000003	1.609	0.76000000000000001	151	0.63	2.847	0.54000000000000004
22	Styrene	12.76	0.96299999999999997	66.010000000000005	0.88300000000000001	261.89999999999998	0.93700000000000006	56	0.26800000000000002	2.8889999999999998	0.68600000000000005	0.027	0.93500000000000005	83.680000000000007	0.71299999999999997	0.27300000000000002	0.93500000000000005
\.


--
-- Data for Name: tbl_64_dm_linning_inorganic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_64_dm_linning_inorganic ("ID", "YearsSinceLastInspection", "Strip lined alloy", "Castable refractory", "Castable refractory severe condition", "Glass lined", "Acid Brick", "Fibreglass") FROM stdin;
1	1	0.29999999999999999	0.5	9	3	0	1
2	2	0.5	1	40	4	0	1
3	3	0.69999999999999996	2	146	6	0	1
4	4	1	4	428	7	0	1
5	5	1	9	1017	9	1	1
6	6	2	16	1978	11	1	1
7	7	3	30	3000	13	1	2
8	8	4	53	3000	16	1	3
9	9	6	89	3000	20	2	7
10	10	9	146	3000	25	3	13
11	11	12	230	3000	30	4	26
12	12	16	351	3000	36	5	47
13	13	22	518	3000	44	7	82
14	14	30	738	3000	53	9	139
15	15	40	1017	3000	63	11	228
16	16	53	1358	3000	75	15	359
17	17	69	1758	3000	89	19	548
18	18	89	2209	3000	105	25	808
19	19	115	2697	3000	124	31	1151
20	20	146	3000	3000	146	40	1587
21	21	184	3000	3000	170	50	2119
22	22	230	3000	3000	199	63	2743
23	23	286	3000	3000	230	78	3000
24	24	351	3000	3000	266	97	3000
25	25	428	3000	3000	306	119	3000
\.


--
-- Data for Name: tbl_65_dm_linning_organic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_65_dm_linning_organic ("ID", "YearInService", "MoreThan6Years", "WithinLast6Years", "WithinLast3Years") FROM stdin;
1	1	30	1	0
2	2	89	4	0
3	3	230	16	0
4	4	518	53	0
5	5	1017	146	0.20000000000000001
6	6	1758	351	1
7	7	2697	738	4
8	8	3000	1358	16
9	9	3000	2209	53
10	10	3000	3000	146
11	11	3000	3000	351
12	12	3000	3000	738
13	13	3000	3000	1358
14	14	3000	3000	2209
15	15	3000	3000	3000
16	16	3000	3000	3000
17	17	3000	3000	3000
18	18	3000	3000	3000
19	19	3000	3000	3000
20	20	3000	3000	3000
21	21	3000	3000	3000
22	22	3000	3000	3000
23	23	3000	3000	3000
24	24	3000	3000	3000
25	25	3000	3000	3000
\.


--
-- Data for Name: tbl_71_properties_storage_tank; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_71_properties_storage_tank ("ID", "Fluid", "Level 1 Consequence Analysis Representative Fluid", "Molecular Weight", "Liquid Density", "Liquid Density Viscosity") FROM stdin;
1	Crude Oil	C17-C25	280	775.01900000000001	0.036900000000000002
2	Fuel Oil	C17-C25	280	775.01900000000001	0.036900000000000002
3	Gasonline	C6-C8	100	684.01800000000003	0.0040099999999999997
4	Heavy Crude Oil	C25+	422	900.02599999999995	0.045999999999999999
5	Heavy Diesel Oil	C13-C16	205	764.52700000000004	0.0024599999999999999
6	Heavy Fuel Oil	C25+	422	900.02599999999995	0.045999999999999999
7	Light Diesel Oil	C9-C12	149	734.01099999999997	0.0010399999999999999
\.


--
-- Data for Name: tbl_74_scc_dm_pwht; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_74_scc_dm_pwht ("ID", "SVI", "E", "1D", "1C", "1B", "1A", "2D", "2C", "2B", "2A", "3D", "3C", "3B", "3A", "4D", "4C", "4B", "4A", "5D", "5C", "5B", "5A", "6D", "6C", "6B", "6A") FROM stdin;
1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1
2	10	10	8	3	1	1	6	2	1	1	4	1	1	1	2	1	1	1	1	1	1	1	1	1	1	1
3	50	50	40	17	5	3	30	10	2	1	20	5	1	1	10	2	1	1	5	1	1	1	1	1	1	1
4	100	100	80	33	10	5	60	20	4	1	40	10	2	1	20	5	1	1	10	2	1	1	5	1	1	1
5	500	500	400	170	50	25	300	100	20	5	200	50	8	1	100	25	2	1	50	10	1	1	25	5	1	1
6	1000	1000	800	330	100	50	600	200	40	10	400	100	16	2	200	50	5	1	100	25	2	1	50	10	1	1
7	5000	5000	4000	1670	250	250	3000	1000	250	50	2000	500	80	10	1000	250	25	2	500	125	5	1	250	50	2	1
\.


--
-- Name: componentmaster_ComponentID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."componentmaster_ComponentID_seq"', 47, true);


--
-- Name: designcode_DesignCodeID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."designcode_DesignCodeID_seq"', 9, true);


--
-- Name: equipmentmaster_EquipmentID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."equipmentmaster_EquipmentID_seq"', 28, true);


--
-- Name: facility_FacilityID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."facility_FacilityID_seq"', 23, true);


--
-- Name: manufacturer_ManufacturerID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."manufacturer_ManufacturerID_seq"', 11, true);


--
-- Name: rw_assessment_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."rw_assessment_ID_seq"', 350, true);


--
-- Name: rw_damagemachinsm_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."rw_damagemachinsm_ID_seq"', 413, true);


--
-- Name: rw_inspection_history_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."rw_inspection_history_ID_seq"', 35, true);


--
-- Name: sites_SiteID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."sites_SiteID_seq"', 13, true);


--
-- Name: tbl_204_dm_htha_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_204_dm_htha_ID_seq"', 5, true);


--
-- Name: tbl_213_dm_impact_exemption_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_213_dm_impact_exemption_ID_seq"', 61, true);


--
-- Name: tbl_214_dm_not_pwht_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_214_dm_not_pwht_ID_seq"', 11, true);


--
-- Name: tbl_215_dm_pwht_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_215_dm_pwht_ID_seq"', 11, true);


--
-- Name: tbl_3b21_si_conversion_conversionFactory_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_3b21_si_conversion_conversionFactory_seq"', 36, true);


--
-- Name: tbl_511_dfb_thin_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_511_dfb_thin_ID_seq"', 114, true);


--
-- Name: tbl_512_dfb_thin_tank_bottom_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_512_dfb_thin_tank_bottom_ID_seq"', 20, true);


--
-- Name: tbl_52_ca_properties_level_1_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_52_ca_properties_level_1_ID_seq"', 30, true);


--
-- Name: tbl_58_ca_component_dm_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_58_ca_component_dm_ID_seq"', 22, true);


--
-- Name: tbl_59_component_damage_person_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_59_component_damage_person_ID_seq"', 22, true);


--
-- Name: tbl_64_dm_linning_inorganic_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_64_dm_linning_inorganic_ID_seq"', 25, true);


--
-- Name: tbl_65_dm_linning_organic_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_65_dm_linning_organic_ID_seq"', 25, true);


--
-- Name: tbl_71_properties_storage_tank_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_71_properties_storage_tank_ID_seq"', 7, true);


--
-- Name: tbl_74_scc_dm_pwht_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."tbl_74_scc_dm_pwht_ID_seq"', 7, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_content_type django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: facility facility_FacilityID_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facility
    ADD CONSTRAINT "facility_FacilityID_key" UNIQUE ("FacilityID");


--
-- Name: rw_data_chart id_rw_chart; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_data_chart
    ADD CONSTRAINT id_rw_chart PRIMARY KEY ("ID");


--
-- Name: manufacturer manufacturer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturer
    ADD CONSTRAINT manufacturer_pkey PRIMARY KEY ("ManufacturerID");


--
-- Name: api_component_type pk_api_component_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_component_type
    ADD CONSTRAINT pk_api_component_type PRIMARY KEY ("APIComponentTypeID");


--
-- Name: auth_group pk_auth_group; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT pk_auth_group PRIMARY KEY (id);


--
-- Name: auth_group_permissions pk_auth_group_permissions; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT pk_auth_group_permissions PRIMARY KEY (id);


--
-- Name: auth_permission pk_auth_permission; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT pk_auth_permission PRIMARY KEY (id);


--
-- Name: auth_user pk_auth_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT pk_auth_user PRIMARY KEY (id);


--
-- Name: auth_user_groups pk_auth_user_groups; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT pk_auth_user_groups PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions pk_auth_user_user_permissions; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT pk_auth_user_user_permissions PRIMARY KEY (id);


--
-- Name: component_master pk_component_master; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.component_master
    ADD CONSTRAINT pk_component_master PRIMARY KEY ("ComponentID");


--
-- Name: component_type pk_component_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.component_type
    ADD CONSTRAINT pk_component_type PRIMARY KEY ("ComponentTypeID");


--
-- Name: design_code pk_design_code; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.design_code
    ADD CONSTRAINT pk_design_code PRIMARY KEY ("DesignCodeID");


--
-- Name: django_admin_log pk_django_admin_log; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT pk_django_admin_log PRIMARY KEY (id);


--
-- Name: django_content_type pk_django_content_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT pk_django_content_type PRIMARY KEY (id);


--
-- Name: django_migrations pk_django_migrations; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT pk_django_migrations PRIMARY KEY (id);


--
-- Name: django_session pk_django_session; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT pk_django_session PRIMARY KEY (session_key);


--
-- Name: dm_category pk_dm_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dm_category
    ADD CONSTRAINT pk_dm_category PRIMARY KEY ("DMCategoryID");


--
-- Name: dm_items pk_dm_items; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dm_items
    ADD CONSTRAINT pk_dm_items PRIMARY KEY ("DMItemID");


--
-- Name: equipment_master pk_equipment_master; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment_master
    ADD CONSTRAINT pk_equipment_master PRIMARY KEY ("EquipmentID");


--
-- Name: equipment_type pk_equipment_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment_type
    ADD CONSTRAINT pk_equipment_type PRIMARY KEY ("EquipmentTypeID");


--
-- Name: facility pk_facility; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facility
    ADD CONSTRAINT pk_facility PRIMARY KEY ("FacilityID");


--
-- Name: facility_risk_target pk_facility_risk_target; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facility_risk_target
    ADD CONSTRAINT pk_facility_risk_target PRIMARY KEY ("FacilityID");


--
-- Name: rw_assessment rw_assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_assessment
    ADD CONSTRAINT rw_assessment_pkey PRIMARY KEY ("ID");


--
-- Name: rw_ca_level1 rw_ca_level1_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_ca_level1
    ADD CONSTRAINT rw_ca_level1_pkey PRIMARY KEY ("ID");


--
-- Name: rw_ca_tank rw_ca_tank_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_ca_tank
    ADD CONSTRAINT rw_ca_tank_pkey PRIMARY KEY ("ID");


--
-- Name: rw_coating rw_coating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_coating
    ADD CONSTRAINT rw_coating_pkey PRIMARY KEY ("ID");


--
-- Name: rw_component rw_component_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_component
    ADD CONSTRAINT rw_component_pkey PRIMARY KEY ("ID");


--
-- Name: rw_damage_mechanism rw_damage_mechanism_PrimaryKey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_damage_mechanism
    ADD CONSTRAINT "rw_damage_mechanism_PrimaryKey" PRIMARY KEY ("ID");


--
-- Name: rw_equipment rw_equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_equipment
    ADD CONSTRAINT rw_equipment_pkey PRIMARY KEY ("ID");


--
-- Name: rw_extcor_temperature rw_extcor_temperature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_extcor_temperature
    ADD CONSTRAINT rw_extcor_temperature_pkey PRIMARY KEY ("ID");


--
-- Name: rw_full_fcof rw_full_fcof_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_full_fcof
    ADD CONSTRAINT rw_full_fcof_pkey PRIMARY KEY ("ID");


--
-- Name: rw_full_pof rw_full_pof_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_full_pof
    ADD CONSTRAINT rw_full_pof_pkey PRIMARY KEY ("ID");


--
-- Name: rw_input_ca_level1 rw_input_ca_level1_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_input_ca_level1
    ADD CONSTRAINT rw_input_ca_level1_pkey PRIMARY KEY ("ID");


--
-- Name: rw_input_ca_tank rw_input_ca_tank_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_input_ca_tank
    ADD CONSTRAINT rw_input_ca_tank_pkey PRIMARY KEY ("ID");


--
-- Name: rw_inspection_history rw_inspection_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_inspection_history
    ADD CONSTRAINT rw_inspection_history_pkey PRIMARY KEY ("ID");


--
-- Name: rw_material rw_material_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_material
    ADD CONSTRAINT rw_material_pkey PRIMARY KEY ("ID");


--
-- Name: rw_stream rw_stream_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_stream
    ADD CONSTRAINT rw_stream_pkey PRIMARY KEY ("ID");


--
-- Name: sites sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY ("SiteID");


--
-- Name: tbl_204_dm_htha tbl_204_dm_htha_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_204_dm_htha
    ADD CONSTRAINT tbl_204_dm_htha_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_213_dm_impact_exemption tbl_213_dm_impact_exemption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_213_dm_impact_exemption
    ADD CONSTRAINT tbl_213_dm_impact_exemption_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_214_dm_not_pwht tbl_214_dm_not_pwht_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_214_dm_not_pwht
    ADD CONSTRAINT tbl_214_dm_not_pwht_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_215_dm_pwht tbl_215_dm_pwht_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_215_dm_pwht
    ADD CONSTRAINT tbl_215_dm_pwht_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_3b21_si_conversion tbl_3b21_si_conversion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_3b21_si_conversion
    ADD CONSTRAINT tbl_3b21_si_conversion_pkey PRIMARY KEY ("conversionFactory");


--
-- Name: tbl_511_dfb_thin tbl_511_dfb_thin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_511_dfb_thin
    ADD CONSTRAINT tbl_511_dfb_thin_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_512_dfb_thin_tank_bottom tbl_512_dfb_thin_tank_bottom_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_512_dfb_thin_tank_bottom
    ADD CONSTRAINT tbl_512_dfb_thin_tank_bottom_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_52_ca_properties_level_1 tbl_52_ca_properties_level_1_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_52_ca_properties_level_1
    ADD CONSTRAINT tbl_52_ca_properties_level_1_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_58_ca_component_dm tbl_58_ca_component_dm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_58_ca_component_dm
    ADD CONSTRAINT tbl_58_ca_component_dm_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_59_component_damage_person tbl_59_component_damage_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_59_component_damage_person
    ADD CONSTRAINT tbl_59_component_damage_person_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_64_dm_linning_inorganic tbl_64_dm_linning_inorganic_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_64_dm_linning_inorganic
    ADD CONSTRAINT tbl_64_dm_linning_inorganic_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_65_dm_linning_organic tbl_65_dm_linning_organic_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_65_dm_linning_organic
    ADD CONSTRAINT tbl_65_dm_linning_organic_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_71_properties_storage_tank tbl_71_properties_storage_tank_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_71_properties_storage_tank
    ADD CONSTRAINT tbl_71_properties_storage_tank_pkey PRIMARY KEY ("ID");


--
-- Name: tbl_74_scc_dm_pwht tbl_74_scc_dm_pwht_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_74_scc_dm_pwht
    ADD CONSTRAINT tbl_74_scc_dm_pwht_pkey PRIMARY KEY ("ID");


--
-- Name: auth_group_permissio_permission_id_84c5c92e_fk_auth_perm_auth_g; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissio_permission_id_84c5c92e_fk_auth_perm_auth_g ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_group_permissions_auth_group_permissio_permission_id_84c5c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_auth_group_permissio_permission_id_84c5c ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_group_permissions_group_id_permission_id_0cd325b0_uniq_aut; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX auth_group_permissions_group_id_permission_id_0cd325b0_uniq_aut ON public.auth_group_permissions USING btree (group_id, permission_id);


--
-- Name: auth_permission_content_type_id_codename_01ab375a_uniq_auth_per; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX auth_permission_content_type_id_codename_01ab375a_uniq_auth_per ON public.auth_permission USING btree (content_type_id, codename);


--
-- Name: auth_user_groups_auth_user_groups_group_id_97559544_fk_auth_gro; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_auth_user_groups_group_id_97559544_fk_auth_gro ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id_auth_user_g; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544_fk_auth_group_id_auth_user_g ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_group_id_94350c0c_uniq_auth_user_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX auth_user_groups_user_id_group_id_94350c0c_uniq_auth_user_group ON public.auth_user_groups USING btree (user_id, group_id);


--
-- Name: auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm_auth_u; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm_auth_u ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_auth_user_user_permi_permission_id_1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_auth_user_user_permi_permission_id_1 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_14a6b632_uniq_; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX auth_user_user_permissions_user_id_permission_id_14a6b632_uniq_ ON public.auth_user_user_permissions USING btree (user_id, permission_id);


--
-- Name: component_apicomponent_component_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX component_apicomponent_component_master ON public.component_master USING btree ("ComponentTypeID");


--
-- Name: component_equipment_component_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX component_equipment_component_master ON public.component_master USING btree ("EquipmentID");


--
-- Name: component_master_component_APIcomponent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "component_master_component_APIcomponent" ON public.component_master USING btree ("ComponentTypeID");


--
-- Name: component_master_component_equipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX component_master_component_equipment ON public.component_master USING btree ("EquipmentID");


--
-- Name: django_admin_log_content_type_id_c4bce8eb_fk_django_co_django_a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb_fk_django_co_django_a ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_django_admin_log_content_type_id_c4bce8eb_fk_d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_django_admin_log_content_type_id_c4bce8eb_fk_d ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_django_admin_log_user_id_c564eba6_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_django_admin_log_user_id_c564eba6_fk ON public.django_admin_log USING btree (user_id);


--
-- Name: django_admin_log_user_id_c564eba6_fk_django_admin_log; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6_fk_django_admin_log ON public.django_admin_log USING btree (user_id);


--
-- Name: django_content_type_app_label_model_76bd3d3b_uniq_django_conten; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX django_content_type_app_label_model_76bd3d3b_uniq_django_conten ON public.django_content_type USING btree (app_label, model);


--
-- Name: django_session_django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_expire_date_a5c62663_django_session; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663_django_session ON public.django_session USING btree (expire_date);


--
-- Name: dm_items_DMCategoryID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "dm_items_DMCategoryID" ON public.dm_items USING btree ("DMCategoryID");


--
-- Name: dmcategoryid_dm_items; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dmcategoryid_dm_items ON public.dm_items USING btree ("DMCategoryID");


--
-- Name: equipment_designcode_equipment_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_designcode_equipment_master ON public.equipment_master USING btree ("DesignCodeID");


--
-- Name: equipment_equipmenttype_equipment_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_equipmenttype_equipment_master ON public.equipment_master USING btree ("EquipmentTypeID");


--
-- Name: equipment_facility_equipment_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_facility_equipment_master ON public.equipment_master USING btree ("FacilityID");


--
-- Name: equipment_manufacturer_equipment_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_manufacturer_equipment_master ON public.equipment_master USING btree ("ManufacturerID");


--
-- Name: equipment_master_equipment_designcode; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_master_equipment_designcode ON public.equipment_master USING btree ("DesignCodeID");


--
-- Name: equipment_master_equipment_equipmentType; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "equipment_master_equipment_equipmentType" ON public.equipment_master USING btree ("EquipmentTypeID");


--
-- Name: equipment_master_equipment_facility; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_master_equipment_facility ON public.equipment_master USING btree ("FacilityID");


--
-- Name: equipment_master_equipment_manufacturer; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_master_equipment_manufacturer ON public.equipment_master USING btree ("ManufacturerID");


--
-- Name: equipment_master_equipment_sites; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_master_equipment_sites ON public.equipment_master USING btree ("SiteID");


--
-- Name: equipment_sites_equipment_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX equipment_sites_equipment_master ON public.equipment_master USING btree ("SiteID");


--
-- Name: name_auth_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX name_auth_group ON public.auth_group USING btree (name);


--
-- Name: rw_assessment_assesment_component; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rw_assessment_assesment_component ON public.rw_assessment USING btree ("ComponentID");


--
-- Name: rw_assessment_assesment_equipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rw_assessment_assesment_equipment ON public.rw_assessment USING btree ("EquipmentID");


--
-- Name: sites_facility; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sites_facility ON public.facility USING btree ("SiteID");


--
-- Name: username_auth_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX username_auth_user ON public.auth_user USING btree (username);


--
-- Name: rw_assessment assesment_component; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_assessment
    ADD CONSTRAINT assesment_component FOREIGN KEY ("ComponentID") REFERENCES public.component_master("ComponentID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_assessment assesment_equipment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_assessment
    ADD CONSTRAINT assesment_equipment FOREIGN KEY ("EquipmentID") REFERENCES public.equipment_master("EquipmentID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_ca_level1 calevel1_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_ca_level1
    ADD CONSTRAINT calevel1_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_ca_tank catank_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_ca_tank
    ADD CONSTRAINT catank_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_coating coating_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_coating
    ADD CONSTRAINT coating_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: component_master component_APIcomponent; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.component_master
    ADD CONSTRAINT "component_APIcomponent" FOREIGN KEY ("ComponentTypeID") REFERENCES public.api_component_type("APIComponentTypeID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: component_master component_componentType; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.component_master
    ADD CONSTRAINT "component_componentType" FOREIGN KEY ("ComponentTypeID") REFERENCES public.component_type("ComponentTypeID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: component_master component_equipment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.component_master
    ADD CONSTRAINT component_equipment FOREIGN KEY ("EquipmentID") REFERENCES public.equipment_master("EquipmentID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: dm_items dm_items_ibfk_1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dm_items
    ADD CONSTRAINT dm_items_ibfk_1 FOREIGN KEY ("DMCategoryID") REFERENCES public.dm_category("DMCategoryID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: equipment_master equipment_designcode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment_master
    ADD CONSTRAINT equipment_designcode FOREIGN KEY ("DesignCodeID") REFERENCES public.design_code("DesignCodeID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: equipment_master equipment_equipmentType; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment_master
    ADD CONSTRAINT "equipment_equipmentType" FOREIGN KEY ("EquipmentTypeID") REFERENCES public.equipment_type("EquipmentTypeID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: equipment_master equipment_facility; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment_master
    ADD CONSTRAINT equipment_facility FOREIGN KEY ("FacilityID") REFERENCES public.facility("FacilityID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_component rwcomponent_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_component
    ADD CONSTRAINT rwcomponent_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_equipment rwequipment_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_equipment
    ADD CONSTRAINT rwequipment_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_extcor_temperature rwextcor_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_extcor_temperature
    ADD CONSTRAINT rwextcor_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_full_fcof rwfcof_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_full_fcof
    ADD CONSTRAINT rwfcof_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_input_ca_level1 rwinputcalevel1_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_input_ca_level1
    ADD CONSTRAINT rwinputcalevel1_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_input_ca_tank rwinputcatank_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_input_ca_tank
    ADD CONSTRAINT rwinputcatank_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_material rwmaterial_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_material
    ADD CONSTRAINT rwmaterial_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_full_pof rwpof_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_full_pof
    ADD CONSTRAINT rwpof_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: rw_stream rwstream_assesment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rw_stream
    ADD CONSTRAINT rwstream_assesment FOREIGN KEY ("ID") REFERENCES public.rw_assessment("ID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: facility_risk_target target_facility; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facility_risk_target
    ADD CONSTRAINT target_facility FOREIGN KEY ("FacilityID") REFERENCES public.facility("FacilityID") ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: SEQUENCE "componentmaster_ComponentID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."componentmaster_ComponentID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."componentmaster_ComponentID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "designcode_DesignCodeID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."designcode_DesignCodeID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."designcode_DesignCodeID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "equipmentmaster_EquipmentID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."equipmentmaster_EquipmentID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."equipmentmaster_EquipmentID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "facility_FacilityID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."facility_FacilityID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."facility_FacilityID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "manufacturer_ManufacturerID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."manufacturer_ManufacturerID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."manufacturer_ManufacturerID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "rw_assessment_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."rw_assessment_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."rw_assessment_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "rw_damagemachinsm_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."rw_damagemachinsm_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."rw_damagemachinsm_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "rw_inspection_history_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."rw_inspection_history_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."rw_inspection_history_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "sites_SiteID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."sites_SiteID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."sites_SiteID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_204_dm_htha_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_204_dm_htha_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_204_dm_htha_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_213_dm_impact_exemption_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_213_dm_impact_exemption_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_213_dm_impact_exemption_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_214_dm_not_pwht_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_214_dm_not_pwht_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_214_dm_not_pwht_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_215_dm_pwht_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_215_dm_pwht_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_215_dm_pwht_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_3b21_si_conversion_conversionFactory_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_3b21_si_conversion_conversionFactory_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_3b21_si_conversion_conversionFactory_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_511_dfb_thin_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_511_dfb_thin_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_511_dfb_thin_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_512_dfb_thin_tank_bottom_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_512_dfb_thin_tank_bottom_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_512_dfb_thin_tank_bottom_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_52_ca_properties_level_1_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_52_ca_properties_level_1_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_52_ca_properties_level_1_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_58_ca_component_dm_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_58_ca_component_dm_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_58_ca_component_dm_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_59_component_damage_person_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_59_component_damage_person_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_59_component_damage_person_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_64_dm_linning_inorganic_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_64_dm_linning_inorganic_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_64_dm_linning_inorganic_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_65_dm_linning_organic_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_65_dm_linning_organic_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_65_dm_linning_organic_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_71_properties_storage_tank_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_71_properties_storage_tank_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_71_properties_storage_tank_ID_seq" TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE "tbl_74_scc_dm_pwht_ID_seq"; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE public."tbl_74_scc_dm_pwht_ID_seq" FROM postgres;
GRANT ALL ON SEQUENCE public."tbl_74_scc_dm_pwht_ID_seq" TO postgres WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

