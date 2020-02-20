--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

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
-- Name: trails; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.trails (
    trail_id integer NOT NULL,
    trail_name character varying(200) NOT NULL,
    length double precision NOT NULL,
    difficulty character varying(50),
    img_thumb_url character varying(200),
    img_lg_url character varying(200),
    long double precision NOT NULL,
    lat double precision NOT NULL,
    city character varying(50),
    state character varying(50),
    description character varying(200)
);


ALTER TABLE public.trails OWNER TO vagrant;

--
-- Name: trails_trail_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.trails_trail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trails_trail_id_seq OWNER TO vagrant;

--
-- Name: trails_trail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.trails_trail_id_seq OWNED BY public.trails.trail_id;


--
-- Name: user_trails; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.user_trails (
    ut_id integer NOT NULL,
    user_id integer NOT NULL,
    trail_id integer NOT NULL,
    is_completed boolean,
    date_added timestamp without time zone NOT NULL
);


ALTER TABLE public.user_trails OWNER TO vagrant;

--
-- Name: user_trails_ut_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.user_trails_ut_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_trails_ut_id_seq OWNER TO vagrant;

--
-- Name: user_trails_ut_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.user_trails_ut_id_seq OWNED BY public.user_trails.ut_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(200) NOT NULL,
    password character varying(200) NOT NULL,
    fname character varying(50),
    lname character varying(50),
    cell character varying(15),
    city character varying(50),
    state character varying(2),
    zipcode character varying(5)
);


ALTER TABLE public.users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: trails trail_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.trails ALTER COLUMN trail_id SET DEFAULT nextval('public.trails_trail_id_seq'::regclass);


--
-- Name: user_trails ut_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_trails ALTER COLUMN ut_id SET DEFAULT nextval('public.user_trails_ut_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: trails; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.trails (trail_id, trail_name, length, difficulty, img_thumb_url, img_lg_url, long, lat, city, state, description) FROM stdin;
1234	Sample trail	7	\N	\N	\N	123.123000000000005	123.123000000000005	\N	\N	\N
12345	Sample trail 2	3	\N	\N	\N	321.12299999999999	321.12299999999999	\N	\N	\N
7005207	Half Dome	14.5	black	https://cdn-files.apstatic.com/hike/7003987_small_1554236134.jpg	https://cdn-files.apstatic.com/hike/7003987_smallMed_1554236134.jpg	-119.558300000000003	37.7325000000000017	Yosemite Valley	California	THE premier route in Yosemite. Hike to the top of the most iconic granite dome in the USA.
7004777	Vernal and Nevada Falls Loop	6.20000000000000018	blueBlack	https://cdn-files.apstatic.com/hike/7003987_small_1554236134.jpg	https://cdn-files.apstatic.com/hike/7003987_smallMed_1554236134.jpg	-119.558300000000003	37.7325999999999979	Yosemite Valley	California	A splendid loop past two of Yosemite's most powerful cascades.
7004501	Lower Yosemite Fall Trail	1	green	https://cdn-files.apstatic.com/hike/7003948_small_1554236020.jpg	https://cdn-files.apstatic.com/hike/7003948_smallMed_1554236020.jpg	-119.596199999999996	37.7464000000000013	Yosemite Valley	California	Revel in stunning views of Yosemite Falls in its entirety and walk to the base of the Lower Fall.
7018036	Clouds Rest Viewpoint Trail	12.4000000000000004	blueBlack	https://cdn-files.apstatic.com/hike/7018146_small_1554830392.jpg	https://cdn-files.apstatic.com/hike/7018146_smallMed_1554830392.jpg	-119.469999999999999	37.8256999999999977	Yosemite Valley	California	Incredibly stupendous side-on views of Half Dome are the highlight of this hike.
7009377	Sentinel Dome	2.10000000000000009	greenBlue	https://cdn-files.apstatic.com/hike/7004023_small_1554236250.jpg	https://cdn-files.apstatic.com/hike/7004023_smallMed_1554236250.jpg	-119.586699999999993	37.7128999999999976	Yosemite Valley	California	An easy trail with some great westward sunset views on top of the dome.
7004770	Mirror Lake Loop	4.70000000000000018	greenBlue	https://cdn-files.apstatic.com/hike/7003961_small_1554236057.jpg	https://cdn-files.apstatic.com/hike/7003961_smallMed_1554236057.jpg	-119.560299999999998	37.7393000000000001	Yosemite Valley	California	A beautiful loop through Tenaya Canyon.
7004499	Bridalveil Falls Trail	0.400000000000000022	green	https://cdn-files.apstatic.com/hike/7003576_small_1554234562.jpg	https://cdn-files.apstatic.com/hike/7003576_smallMed_1554234562.jpg	-119.650899999999993	37.7167999999999992	Yosemite Valley	California	A short jaunt to one of Yosemite's most accessible marvels, the 600' Bridalveil Falls.
7045115	Upper Yosemite Falls and Yosemite Point Hike	8	blueBlack	https://cdn-files.apstatic.com/hike/7004881_small_1554310989.jpg	https://cdn-files.apstatic.com/hike/7004881_smallMed_1554310989.jpg	-119.602199999999996	37.7424000000000035	Yosemite Valley	California	Hike to the top of Yosemite Falls, and then to Yosemite Point for amazing views of the valley and surrounding mountains.
7009786	Taft Point	2.29999999999999982	greenBlue	https://cdn-files.apstatic.com/hike/7053805_small_1555704172.jpg	https://cdn-files.apstatic.com/hike/7053805_smallMed_1555704172.jpg	-119.586399999999998	37.7126000000000019	Yosemite Valley	California	A short trail from the Glacier Point Road to an excellent perch to view the valley and the sunset.
7004500	Glacier Point	0.5	green	https://cdn-files.apstatic.com/hike/7017719_small_1554829715.jpg	https://cdn-files.apstatic.com/hike/7017719_smallMed_1554829715.jpg	-119.574399999999997	37.7276000000000025	Yosemite Valley	California	Come for the sunrise or stay for the sunset - the view from Glacier Point is spectacular.
7005880	Redwood Regional Loop	7.29999999999999982	blue	https://cdn-files.apstatic.com/hike/7044815_small_1555531106.jpg	https://cdn-files.apstatic.com/hike/7044815_smallMed_1555531106.jpg	-122.176900000000003	37.803600000000003	Piedmont	California	A mostly shady hike through Serpentine Prairie, oak forest, and the East Bay's largest redwood forest.
7042934	Mount Diablo Falls Loop	5.40000000000000036	blueBlack	https://cdn-files.apstatic.com/hike/7063558_small_1570208963.jpg	https://cdn-files.apstatic.com/hike/7063558_smallMed_1570208963.jpg	-121.927099999999996	37.9221000000000004	Clayton	California	This rugged and scenic hike explores the waterfalls around the headwaters of Donner Creek.
7030162	Peace Circle: Wildcat Peak from Little Farm	4	blue	https://cdn-files.apstatic.com/hike/7048665_small_1555539720.jpg	https://cdn-files.apstatic.com/hike/7048665_smallMed_1555539720.jpg	-122.264600000000002	37.9087999999999994	Kensington	California	Several Tilden Nature Area trails can be stitched together into one ideal loop with great views and local history!
7041523	Mount Diablo Four Peaks Loop	15.4000000000000004	blueBlack	https://cdn-files.apstatic.com/hike/7011282_small_1554400324.jpg	https://cdn-files.apstatic.com/hike/7011282_smallMed_1554400324.jpg	-121.927000000000007	37.9221000000000004	Clayton	California	This long, challenging hike visits Mount Diablo and three other summits.
7030209	Mt. Diablo Summit Loop - South	16	blueBlack	https://cdn-files.apstatic.com/hike/7011282_small_1554400324.jpg	https://cdn-files.apstatic.com/hike/7011282_smallMed_1554400324.jpg	-121.978800000000007	37.8626999999999967	Diablo	California	A long loop hike through Mt. Diablo Foothills and to the summit of Mt. Diablo.
7056138	Eagle Peak Out and Back	4.20000000000000018	black	https://cdn-files.apstatic.com/hike/7052184_small_1555694830.jpg	https://cdn-files.apstatic.com/hike/7052184_smallMed_1555694830.jpg	-122.025899999999993	37.8340000000000032	Alamo	California	Excellent workout with great views of Mt. Diablo.
7051489	Educational Loop	4.29999999999999982	blue	https://cdn-files.apstatic.com/hike/7048197_small_1555538705.jpg	https://cdn-files.apstatic.com/hike/7048197_smallMed_1555538705.jpg	-122.198599999999999	37.8477999999999994	Orinda	California	A great hike to explore volcanoes in Oakland.
7051316	Richmond Marina Bay Trail	8.09999999999999964	green	https://cdn-files.apstatic.com/hike/7047983_small_1555538268.jpg	https://cdn-files.apstatic.com/hike/7047983_smallMed_1555538268.jpg	-122.316699999999997	37.9001000000000019	El Cerrito	California	Hike along the San Francisco Bay Trail (Richmond Segment) with stunning views of San Francisco.
7052665	Wildcat Canyon Loop	9.40000000000000036	blue	https://cdn-files.apstatic.com/hike/7058853_small_1558289055.jpg	https://cdn-files.apstatic.com/hike/7058853_smallMed_1558289055.jpg	-122.314400000000006	37.9525000000000006	East Richmond Heights	California	Uses trails less traveled in Wildcat Canyon.
7084337	Berkeley Hills	3.5	black	https://cdn-files.apstatic.com/hike/7060639_small_1563345465.jpg	https://cdn-files.apstatic.com/hike/7060639_smallMed_1563345465.jpg	-122.244	37.8626000000000005	Berkeley	California	One of several ways to hike the beautiful trails on the Berkeley hills. Great combination of uphill and flat trails.
7000175	Great Falls Park - South Loop	3.29999999999999982	blue	https://cdn-files.apstatic.com/hike/7000291_small_1554159203.jpg	https://cdn-files.apstatic.com/hike/7000291_smallMed_1554159203.jpg	-77.254099999999994	38.9932999999999979	Great Falls	Virginia	A tour of some great trails in the south end of GFNP culminating with dramatic views of the falls.
7005547	Berma Road to Billy Goat Trail Section A	3.5	blueBlack	https://cdn-files.apstatic.com/hike/7005757_small_1554312819.jpg	https://cdn-files.apstatic.com/hike/7005757_smallMed_1554312819.jpg	-77.227099999999993	38.9819000000000031	Potomac	Maryland	A nice morning hike, the Billy Goat Trail Section A has a few tricky spots.
7004459	Burke Lake Trail	4.40000000000000036	greenBlue	https://cdn-files.apstatic.com/hike/7003554_small_1554234503.jpg	https://cdn-files.apstatic.com/hike/7003554_smallMed_1554234503.jpg	-77.2933000000000021	38.7545000000000002	Burke	Virginia	One of the best hikes in Northern Virginia.
7000312	Rock Creek Park Loop: Western Ridge to Valley Trails	8.80000000000000071	blue	https://cdn-files.apstatic.com/hike/7000482_small_1554159385.jpg	https://cdn-files.apstatic.com/hike/7000482_smallMed_1554159385.jpg	-77.0504999999999995	38.9436999999999998	Washington	Washington	A beautiful loop through Rock Creek Park, a D.C. Metro Area oasis.
7040272	Chesapeake and Ohio Canal Loop	1.60000000000000009	green	https://cdn-files.apstatic.com/hike/7019881_small_1554837315.jpg	https://cdn-files.apstatic.com/hike/7019881_smallMed_1554837315.jpg	-77.2468999999999966	39.0024999999999977	Potomac	Maryland	A beautiful family-friendly loop that mixes history with breathtaking scenery.
7004588	First Battle of Manassas	5.20000000000000018	greenBlue	https://cdn-files.apstatic.com/hike/7003156_small_1554233150.jpg	https://cdn-files.apstatic.com/hike/7003156_smallMed_1554233150.jpg	-77.5207999999999942	38.8130000000000024	Bull Run	Virginia	Leisurely trail around one half of Manassas National Battlefield. Lots of woods, grass and history!
7004036	Lake Shore Trail	3.29999999999999982	greenBlue	https://cdn-files.apstatic.com/hike/7004863_small_1554310944.jpg	https://cdn-files.apstatic.com/hike/7004863_smallMed_1554310944.jpg	-77.2412000000000063	39.1432000000000002	Gaithersburg	Maryland	Follow the shore of Clopper Lake for a fast and fun three miles.
7087444	Riverbend—Great Falls Loop	7.70000000000000018	black	https://cdn-files.apstatic.com/hike/7000288_small_1554159194.jpg	https://cdn-files.apstatic.com/hike/7000288_smallMed_1554159194.jpg	-77.2460999999999984	39.0176999999999978	Great Falls	Virginia	This is the best way to see Riverbend and Great Falls Parks.
7013356	Bull Run-Occoquan Trail	17.8999999999999986	blue	https://cdn-files.apstatic.com/hike/7010696_small_1554399044.jpg	https://cdn-files.apstatic.com/hike/7010696_smallMed_1554399044.jpg	-77.4758999999999958	38.8031000000000006	Loch Lomond	Virginia	A nicely maintained long distance trail between Bull Run Regional Park and Fountainhead Regional Park.
7003909	Second Battle of Manassas Trail	6.70000000000000018	greenBlue	https://cdn-files.apstatic.com/hike/7003156_small_1554233150.jpg	https://cdn-files.apstatic.com/hike/7003156_smallMed_1554233150.jpg	-77.5220999999999947	38.8126000000000033	Bull Run	Virginia	A great route on well maintained trails in the Manassas Battlefield National Park.
7005428	Old Rag Loop	8.90000000000000036	black	https://cdn-files.apstatic.com/hike/7004757_small_1554310721.jpg	https://cdn-files.apstatic.com/hike/7004757_smallMed_1554310721.jpg	-78.2869000000000028	38.5707000000000022	Stanley	Virginia	An extremely popular hike, and for good reason, with awesome scrambling and stunning views.
7013220	Whiteoak Canyon to Cedar Run Loop	8.19999999999999929	blueBlack	https://cdn-files.apstatic.com/hike/7017404_small_1554829347.jpg	https://cdn-files.apstatic.com/hike/7017404_smallMed_1554829347.jpg	-78.3492999999999995	38.5396000000000001	Stanley	Virginia	Among the best hikes --if not the best hike-- in Shenandoah. Enjoy waterfalls for 9 miles.
7015928	Rose River Loop	3.79999999999999982	blue	https://cdn-files.apstatic.com/hike/7052871_small_1555697331.jpg	https://cdn-files.apstatic.com/hike/7052871_smallMed_1555697331.jpg	-78.4209000000000032	38.5334999999999965	Stanley	Virginia	For most of this loop hike, you'll be in one of SNP's federally designated wilderness areas.
7005865	Humpback Rocks	1.80000000000000004	blueBlack	https://cdn-files.apstatic.com/hike/7005207_small_1554311672.jpg	https://cdn-files.apstatic.com/hike/7005207_smallMed_1554311672.jpg	-78.8966000000000065	37.9684000000000026	Nellysford	Virginia	A steady climb from wide gravel path to narrow forest singletrack. Stunning 360 views from the top!
7027298	Hawksbill Mountain Loop	2.70000000000000018	blue	https://cdn-files.apstatic.com/hike/7013554_small_1554822773.jpg	https://cdn-files.apstatic.com/hike/7013554_smallMed_1554822773.jpg	-78.3867999999999938	38.5563000000000002	Stanley	Virginia	This 2.7-mile loop takes you directly to the peak and then takes a less aggressive way back down.
7011923	Bearfence Loop Trail	1.10000000000000009	blueBlack	https://cdn-files.apstatic.com/hike/7018088_small_1554830294.jpg	https://cdn-files.apstatic.com/hike/7018088_smallMed_1554830294.jpg	-78.4669999999999987	38.4523999999999972	Stanley	Virginia	A short trail with moderately hard rock scrambles, but great views!
7016844	Dark Hollow Falls	1.69999999999999996	blue	https://cdn-files.apstatic.com/hike/7037946_small_1555087128.jpg	https://cdn-files.apstatic.com/hike/7037946_smallMed_1555087128.jpg	-78.4308999999999941	38.519599999999997	Stanley	Virginia	A short, out-and-back hike to the tumbling, 70-foot Dark Hollow Falls.
7027258	Double Falls Loop	6.90000000000000036	blue	https://cdn-files.apstatic.com/hike/7047588_small_1555537398.jpg	https://cdn-files.apstatic.com/hike/7047588_smallMed_1555537398.jpg	-78.7261000000000024	38.2299000000000007	Grottoes	Virginia	This combination of four trails creates a loop that provides views of the water falls on the Doyle River & Jones Run.
7012060	Upper Hawksbill Ascent	2.20000000000000018	greenBlue	https://cdn-files.apstatic.com/hike/7013554_small_1554822773.jpg	https://cdn-files.apstatic.com/hike/7013554_smallMed_1554822773.jpg	-78.3931999999999931	38.5437000000000012	Stanley	Virginia	A fairly easy trail to a fire road which leads to great views at the highest point in Shenandoah.
7016820	Whiteoak Canyon to Upper Falls	4.70000000000000018	blue	https://cdn-files.apstatic.com/hike/7010288_small_1554398199.jpg	https://cdn-files.apstatic.com/hike/7010288_smallMed_1554398199.jpg	-78.3829000000000065	38.5859000000000023	Stanley	Virginia	A must-do hike in Shenandoah National Park with views of the upper waterfalls of Whiteoak Run.
7017501	Mystic Falls Loop	3.5	blue	https://cdn-files.apstatic.com/hike/7013037_small_1554822121.jpg	https://cdn-files.apstatic.com/hike/7013037_smallMed_1554822121.jpg	-110.852400000000003	44.4849999999999994	Yellowstone	Wyoming	Great trail to a beautiful 70-foot cascade and up to an amazing lookout over the Upper Geyser Basin.
7017503	Fairy Falls-Imperial Geyser	6.59999999999999964	greenBlue	https://cdn-files.apstatic.com/hike/7009131_small_1554395897.jpg	https://cdn-files.apstatic.com/hike/7009131_smallMed_1554395897.jpg	-110.832499999999996	44.515500000000003	Old Faithful Village	Wyoming	A popular hike to impressive hot springs and geysers, and one of Yellowstone’s highest falls.
7017582	Bechler Canyon	31.6000000000000014	blue	https://cdn-files.apstatic.com/hike/7061159_small_1563993489.jpg	https://cdn-files.apstatic.com/hike/7061159_smallMed_1563993489.jpg	-110.804500000000004	44.4444000000000017	Old Faithful Village	Wyoming	A classic Yellowstone backpacking trip -- if waterfalls are your thing, this one is for you!
7017586	Observation Point-Geyser Hill	2.29999999999999982	greenBlue	https://cdn-files.apstatic.com/hike/7017674_small_1554829656.jpg	https://cdn-files.apstatic.com/hike/7017674_smallMed_1554829656.jpg	-110.829099999999997	44.4588999999999999	Old Faithful Village	Wyoming	Get a birds-eye view of Old Faithful and the entire Upper Geyser Basin!
7008982	Storm Point	2.39999999999999991	green	https://img.youtube.com/vi/_5o_9p7zDbA/hqdefault.jpg	https://img.youtube.com/vi/_5o_9p7zDbA/hqdefault.jpg	-110.327699999999993	44.5593999999999966	Lake Village	Wyoming	Dazzling views of Yellowstone Lake and opportunities to observe buffalo, marmots, & waterfowl.
7017580	Shoshone Lake & Geyser Basin	21.1999999999999993	blue	https://cdn-files.apstatic.com/hike/7013164_small_1554822310.jpg	https://cdn-files.apstatic.com/hike/7013164_smallMed_1554822310.jpg	-110.701599999999999	44.4468000000000032	Old Faithful Village	Wyoming	Beautiful route highlighted by a tour of Shoshone Geyser Basin tour, best backcountry basin in YNP!
7017584	Union Falls	16.6000000000000014	blue	https://cdn-files.apstatic.com/hike/7014263_small_1554824059.jpg	https://cdn-files.apstatic.com/hike/7014263_smallMed_1554824059.jpg	-110.820599999999999	44.1315000000000026	Yellowstone South Entrance	Wyoming	Spectacular 250-foot Union Falls is one of the most beautiful falls on the planet!
7017688	Grand Canyon South Rim	2.60000000000000009	greenBlue	https://cdn-files.apstatic.com/hike/7017721_small_1554829718.jpg	https://cdn-files.apstatic.com/hike/7017721_smallMed_1554829718.jpg	-110.496200000000002	44.7152000000000029	Canyon Village	Wyoming	A must-do trail with iconic views of the Upper and Lower Falls and the Yellowstone Grand Canyon!
7017579	Heart Lake/Mt. Sheridan	23.6999999999999993	blueBlack	https://cdn-files.apstatic.com/hike/7011101_small_1554399940.jpg	https://cdn-files.apstatic.com/hike/7011101_smallMed_1554399940.jpg	-110.598200000000006	44.3173999999999992	Grant Village	Wyoming	One of Yellowstone's best - hot springs, geysers, park's 4th largest lake, and an awesome summit!
7008812	Monument Geyser Basin	2.70000000000000018	blue	https://cdn-files.apstatic.com/hike/7056478_small_1555711538.jpg	https://cdn-files.apstatic.com/hike/7056478_smallMed_1555711538.jpg	-110.744600000000005	44.683799999999998	Norris Junction	Wyoming	This trail leads to unusual geyserite forms named Thermos Bottle Geyser, Sunning Seal, & Dog's Head.
7002763	Bizz Johnson National Recreation Trail	26.3000000000000007	green	https://cdn-files.apstatic.com/hike/7001789_small_1554219508.jpg	https://cdn-files.apstatic.com/hike/7001789_smallMed_1554219508.jpg	-120.998999999999995	40.3620000000000019	Westwood	California	The most scenic rail trail anywhere with parallel singletrack on the South Side Trail.
7002803	Eagle Lake South Shore	9.19999999999999929	green	https://cdn-files.apstatic.com/hike/7001761_small_1554219419.jpg	https://cdn-files.apstatic.com/hike/7001761_smallMed_1554219419.jpg	-120.768199999999993	40.5563000000000002	Susanville	California	A relaxing pathway along one of America's most beautiful natural lakes.
7002799	Modoc Line Rail Trail - Snowstorm Canyon Segment	17	green	https://cdn-files.apstatic.com/hike/7001785_small_1554219497.jpg	https://cdn-files.apstatic.com/hike/7001785_smallMed_1554219497.jpg	-120.322999999999993	40.5615999999999985	Johnstonville	California	An adventure in the great wide open.
7002798	Lassen Creek Conservation Area Trail	1.80000000000000004	greenBlue	https://cdn-files.apstatic.com/hike/7001778_small_1554219475.jpg	https://cdn-files.apstatic.com/hike/7001778_smallMed_1554219475.jpg	-120.628399999999999	40.3733999999999966	Johnstonville	California	Great for an efficient workout with amazing views of the Diamond Mountains.
7002762	South Side Trail	14.6999999999999993	blue	https://cdn-files.apstatic.com/hike/7001754_small_1554219398.jpg	https://cdn-files.apstatic.com/hike/7001754_smallMed_1554219398.jpg	-120.674000000000007	40.4192999999999998	Susanville	California	Spectacular singletrack in the Susan River Canyon.
7002770	Heart Attack Hill	1.5	blueBlack			-120.663600000000002	40.4421999999999997	Susanville	California	A popular trail with challenging climbs and great views.
7032444	Modoc Line Rail Trail	84.7000000000000028	green	https://cdn-files.apstatic.com/hike/7001785_small_1554219497.jpg	https://cdn-files.apstatic.com/hike/7001785_smallMed_1554219497.jpg	-120.530100000000004	41.2588000000000008	Alturas	California	85 miles of fresh air and wide open spaces. Get free from the congestion of other trails.
7002809	Helipad Trail	0.5	blueBlack	https://cdn-files.apstatic.com/hike/7001770_small_1554219453.jpg	https://cdn-files.apstatic.com/hike/7001770_smallMed_1554219453.jpg	-120.669300000000007	40.4301999999999992	Susanville	California	A quick way to get a great view.
7002810	Paiute Creek Trail	0.5	blue	https://cdn-files.apstatic.com/hike/7001764_small_1554219427.jpg	https://cdn-files.apstatic.com/hike/7001764_smallMed_1554219427.jpg	-120.662999999999997	40.4251000000000005	Susanville	California	This is an amazing way to enter the trail network. Right along Paiute Creek.
7002823	Osprey Overlook Trail - one of the best views of Eagle Lake and a great chance of seeing Golden & Bald Eagles and Osprey	0.5	blue	https://cdn-files.apstatic.com/hike/7001768_small_1554219438.jpg	https://cdn-files.apstatic.com/hike/7001768_smallMed_1554219438.jpg	-120.759900000000002	40.559899999999999	Susanville	California	
7015182	Ohlone Wilderness Trail / Hidden Valley Trail	6.5	blueBlack	https://cdn-files.apstatic.com/hike/7039499_small_1555092057.jpg	https://cdn-files.apstatic.com/hike/7039499_smallMed_1555092057.jpg	-121.909800000000004	37.5041999999999973	Milpitas	California	A steep climb up Mission Peak with great views of the southern half of the bay.
7002434	San Gorgonio Peak	16.3000000000000007	blueBlack	https://cdn-files.apstatic.com/hike/7002957_small_1554232101.jpg	https://cdn-files.apstatic.com/hike/7002957_smallMed_1554232101.jpg	-116.891300000000001	34.0818000000000012	Banning	California	The shortest and steepest route to the summit of Mt. San Gorgonio.
7042030	Aspen Glen - Skyline Loop	12.5	blue	https://cdn-files.apstatic.com/hike/7063043_small_1568650448.jpg	https://cdn-files.apstatic.com/hike/7063043_smallMed_1568650448.jpg	-116.927300000000002	34.2349999999999994	Big Bear Lake	California	Everything from views of Big Bear Lake to stunning vistas from the Skyline Trail.
7019185	Keller Peak via Exploration Trail	12.5999999999999996	blueBlack	https://cdn-files.apstatic.com/hike/7019744_small_1554837144.jpg	https://cdn-files.apstatic.com/hike/7019744_smallMed_1554837144.jpg	-117.086799999999997	34.202300000000001	Running Springs	California	Hike up to, and enjoy the views from, the oldest fire lookout in the San Bernardino Mountains.
7052894	South Fork of the Santa Ana River via Dollar Lake	19.6999999999999993	blueBlack	https://cdn-files.apstatic.com/hike/7022152_small_1554840871.jpg	https://cdn-files.apstatic.com/hike/7022152_smallMed_1554840871.jpg	-116.871499999999997	34.1608000000000018	Big Bear Lake	California	Hike a moderately graded route to the highest point in Southern California.
7087534	San Bernadino Peak via Angelus Oak	16.3000000000000007	blueBlack	https://cdn-files.apstatic.com/hike/7004823_small_1554310861.jpg	https://cdn-files.apstatic.com/hike/7004823_smallMed_1554310861.jpg	-116.978399999999993	34.1462000000000003	Big Bear Lake	California	Incredible views out towards and back from San Bernardino Peak.
7044633	Heaps Peak Arboretum Sequoia Loop	0.699999999999999956	green	https://cdn-files.apstatic.com/hike/7042270_small_1555105979.jpg	https://cdn-files.apstatic.com/hike/7042270_smallMed_1555105979.jpg	-117.160700000000006	34.2338999999999984	Running Springs	California	A short, easy loop trail featuring a sequoia grove, picnic area, and educational info.
7055830	Terri Peak Loop	4.59999999999999964	blueBlack	https://cdn-files.apstatic.com/hike/7051764_small_1555693562.jpg	https://cdn-files.apstatic.com/hike/7051764_smallMed_1555693562.jpg	-117.180099999999996	33.8781000000000034	March Air Force Base	California	A great loop and an alternative to the Terri Peak Summit out-and-back.
7085464	Big Bear - Champion Lodgepole Pine & Bluff Lake	0.5	blue	https://cdn-files.apstatic.com/hike/7062033_small_1566151866.jpg	https://cdn-files.apstatic.com/hike/7062033_smallMed_1566151866.jpg	-116.974100000000007	34.2152999999999992	Big Bear Lake	California	A short, easy hike with splendid views.
7026740	Zanja Peak Out-and-Back	4.79999999999999982	blueBlack	https://cdn-files.apstatic.com/hike/7029033_small_1554919777.jpg	https://cdn-files.apstatic.com/hike/7029033_smallMed_1554919777.jpg	-117.058499999999995	34.0431000000000026	Yucaipa	California	An intense, out-and-back climb to Zanja Peak.
7055702	Terri Peak Summit	4	blueBlack	https://cdn-files.apstatic.com/hike/7051764_small_1555693562.jpg	https://cdn-files.apstatic.com/hike/7051764_smallMed_1555693562.jpg	-117.1755	33.8791000000000011	March Air Force Base	California	This trail winds up the hill at a moderate pace giving way to expansive views of the Inland Empire.
7027132	Steep Ravine - Matt Davis Loop	7.09999999999999964	blueBlack	https://cdn-files.apstatic.com/hike/7055144_small_1555708413.jpg	https://cdn-files.apstatic.com/hike/7055144_smallMed_1555708413.jpg	-122.635900000000007	37.8965999999999994	Bolinas	California	This awesome loop takes you up a redwood canyon and then down sunny slopes overlooking the Pacific.
7007647	Coastal Trail: Lands End	2.89999999999999991	greenBlue	https://cdn-files.apstatic.com/hike/7013808_small_1554823419.jpg	https://cdn-files.apstatic.com/hike/7013808_smallMed_1554823419.jpg	-122.511700000000005	37.7807000000000031	San Francisco	California	A mega-popular hike hitting many Bay Area attractions in one fell swoop.
7002042	Palomarin to Alamere Falls Out and Back	8.30000000000000071	blue	https://cdn-files.apstatic.com/hike/7001026_small_1554217463.jpg	https://cdn-files.apstatic.com/hike/7001026_smallMed_1554217463.jpg	-122.746200000000002	37.9339000000000013	Bolinas	California	This is a wonderful outing to a waterfall that lands on the beach.
7017752	Hillside Loop	2.5	greenBlue	https://cdn-files.apstatic.com/hike/7017221_small_1554829027.jpg	https://cdn-files.apstatic.com/hike/7017221_smallMed_1554829027.jpg	-122.569400000000002	37.8913000000000011	Tamalpais Valley	California	Enjoy a loop around the world’s most visited redwood park under towering old growth Coastal Redwoods
7016771	Muir Beach Loop	5.79999999999999982	blue	https://cdn-files.apstatic.com/hike/7011872_small_1554560154.jpg	https://cdn-files.apstatic.com/hike/7011872_smallMed_1554560154.jpg	-122.575400000000002	37.8611000000000004	Tamalpais Valley	California	If you want to experience rugged California coast, this loop is perfect for you!
7024570	Mount Tamalpais from Muir Woods	8.69999999999999929	blueBlack	https://cdn-files.apstatic.com/hike/7017221_small_1554829027.jpg	https://cdn-files.apstatic.com/hike/7017221_smallMed_1554829027.jpg	-122.569199999999995	37.8913000000000011	Tamalpais Valley	California	Head from old-growth redwoods to the top of one of the Bay Area's most iconic peaks.
7017753	Panoramic Loop	4.5	greenBlue	https://cdn-files.apstatic.com/hike/7017221_small_1554829027.jpg	https://cdn-files.apstatic.com/hike/7017221_smallMed_1554829027.jpg	-122.569400000000002	37.8913000000000011	Tamalpais Valley	California	Take on this route to see how world the renowned Muir Woods fits into the heart of Mount Tamalpais.
7002041	Mount Wittenberg and Bear Valley Loop	13.8000000000000007	blue	https://cdn-files.apstatic.com/hike/7001804_small_1554219545.jpg	https://cdn-files.apstatic.com/hike/7001804_smallMed_1554219545.jpg	-122.799700000000001	38.0397000000000034	Inverness	California	This long but rewarding excursion hits many Point Reyes highlights.
7024571	Montara Mountain from Gray Whale Cove	9.90000000000000036	blue	https://cdn-files.apstatic.com/hike/7008241_small_1554324445.jpg	https://cdn-files.apstatic.com/hike/7008241_smallMed_1554324445.jpg	-122.512600000000006	37.5628999999999991	Montara	California	A sea-to-summit hike of Montara Mountain.
7001511	Tomales Point Trail	9.80000000000000071	greenBlue	https://cdn-files.apstatic.com/hike/7057504_small_1555947224.jpg	https://cdn-files.apstatic.com/hike/7057504_smallMed_1555947224.jpg	-122.954300000000003	38.1891000000000034	Inverness	California	A trail with spectacular coastal views and probable elk sightings.
7013286	Mt. Livermore Summit - North Ridge Trail	4.29999999999999982	blue	https://cdn-files.apstatic.com/hike/7010442_small_1554398504.jpg	https://cdn-files.apstatic.com/hike/7010442_smallMed_1554398504.jpg	-122.434600000000003	37.8686000000000007	Tiburon	California	Get rewarded with the 360-degree views of the entire SF Bay from the summit of Mt. Livermore on Angel Island!
7007410	Jordan Pond Path	3.39999999999999991	greenBlue	https://cdn-files.apstatic.com/hike/7067070_small_1581547606.jpg	https://cdn-files.apstatic.com/hike/7067070_smallMed_1581547606.jpg	-68.2530000000000001	44.3222999999999985	Bar Harbor	Maine	A nice hike around one of the most beautiful ponds in Acadia.
7007506	Great Head Trail	1.5	blue	https://cdn-files.apstatic.com/hike/7014036_small_1554823699.jpg	https://cdn-files.apstatic.com/hike/7014036_smallMed_1554823699.jpg	-68.180499999999995	44.3297000000000025	Bar Harbor	Maine	A great trail to escape the crowds at Sand Beach and explore the rocky coastline.
7019235	Gorham Mountain Loop	3.60000000000000009	blueBlack	https://cdn-files.apstatic.com/hike/7006727_small_1554321346.jpg	https://cdn-files.apstatic.com/hike/7006727_smallMed_1554321346.jpg	-68.1846000000000032	44.3305000000000007	Bar Harbor	Maine	A short but challenging tour that passes a number of the must-see gems and views in the park.
7019230	Acadia Mountain	2.5	blueBlack	https://cdn-files.apstatic.com/hike/7013955_small_1554823581.jpg	https://cdn-files.apstatic.com/hike/7013955_smallMed_1554823581.jpg	-68.3323000000000036	44.3228999999999971	Tremont	Maine	This forested loop up Acadia Mountain is one of the most popular hikes in the park with great views.
7019232	Precipice Loop	2.29999999999999982	black	https://cdn-files.apstatic.com/hike/7017558_small_1554829595.jpg	https://cdn-files.apstatic.com/hike/7017558_smallMed_1554829595.jpg	-68.1880000000000024	44.349499999999999	Bar Harbor	Maine	An adventurous loop with brilliant views using one of the most exhilarating trails in the park.
7019362	Penobscot Mountain Loop	5.20000000000000018	blueBlack	https://cdn-files.apstatic.com/hike/7067070_small_1581547606.jpg	https://cdn-files.apstatic.com/hike/7067070_smallMed_1581547606.jpg	-68.2541999999999973	44.3205000000000027	Bar Harbor	Maine	Earn your Jordan Pond House popovers on this loop hike up to the summit of Penobscot Mountain.
7005465	Wonderland Trail	1.30000000000000004	green	https://cdn-files.apstatic.com/hike/7004846_small_1554310910.jpg	https://cdn-files.apstatic.com/hike/7004846_smallMed_1554310910.jpg	-68.3199000000000041	44.2338000000000022	Tremont	Maine	This is a very easy trail that is flat and extremely well-marked to an awesome ocean view.
7007397	Bubble Rock	1.19999999999999996	blue	https://cdn-files.apstatic.com/hike/7014368_small_1554824202.jpg	https://cdn-files.apstatic.com/hike/7014368_smallMed_1554824202.jpg	-68.2505000000000024	44.3410999999999973	Bar Harbor	Maine	A short path that splits Acadia’s iconic “Bubbles” and has the easiest access to famed Bubble Rock.
7007422	Beech Mountain Trail	1.19999999999999996	blue	https://cdn-files.apstatic.com/hike/7013881_small_1554823526.jpg	https://cdn-files.apstatic.com/hike/7013881_smallMed_1554823526.jpg	-68.3438000000000017	44.3153000000000006	Tremont	Maine	This short loop hike offers great views of western Mount Desert Island with minimal hiking.
7019354	Dorr Mountain Ladder Trail Loop	3.39999999999999991	black	https://cdn-files.apstatic.com/hike/7018336_small_1554830699.jpg	https://cdn-files.apstatic.com/hike/7018336_smallMed_1554830699.jpg	-68.2045999999999992	44.3519000000000005	Bar Harbor	Maine	An exciting loop up the  Dorr Mountain Ladder Trail, down the ridge, returning up through The Gorge.
7019500	Berry Creek Falls Loop	9.69999999999999929	blue	https://cdn-files.apstatic.com/hike/7027026_small_1554915336.jpg	https://cdn-files.apstatic.com/hike/7027026_smallMed_1554915336.jpg	-122.222399999999993	37.1721000000000004	Boulder Creek	California	Great hike for waterfalls, redwoods, enjoying the little creatures and plants around you, and not needing much sunscreen!
7012643	Castle Rock Loop	3.39999999999999991	blue	https://cdn-files.apstatic.com/hike/7010612_small_1554398875.jpg	https://cdn-files.apstatic.com/hike/7010612_smallMed_1554398875.jpg	-122.095799999999997	37.2306999999999988	Monte Sereno	California	A beautiful wooded loop with openings for views of the Santa Cruz Mountains.
7017526	Hamms Gulch-Spring Ridge Trail Loop	7.70000000000000018	blue	https://cdn-files.apstatic.com/hike/7016516_small_1554827877.jpg	https://cdn-files.apstatic.com/hike/7016516_smallMed_1554827877.jpg	-122.223600000000005	37.3751999999999995	Portola Valley	California	A long climb to great views of the Bay Area and Santa Cruz Mountains.
7038340	Mount Umunhum Summit and Back	8.30000000000000071	blue	https://cdn-files.apstatic.com/hike/7037850_small_1555086910.jpg	https://cdn-files.apstatic.com/hike/7037850_smallMed_1555086910.jpg	-121.875299999999996	37.1595999999999975	Almaden Valley	California	Combine nature, amazing scenery, and interesting history while hiking to one of the highest peaks in the Santa Cruz Mts.
7025610	Skyline to the Sea Trail	25.3999999999999986	blue	https://cdn-files.apstatic.com/hike/7027026_small_1554915336.jpg	https://cdn-files.apstatic.com/hike/7027026_smallMed_1554915336.jpg	-122.122900000000001	37.2578999999999994	Saratoga	California	An amazing hike from the crest of the Santa Cruz Mountains to the Pacific Ocean.
7021695	Henry Cowell Park	8.40000000000000036	blue	https://cdn-files.apstatic.com/hike/7046060_small_1555533870.jpg	https://cdn-files.apstatic.com/hike/7046060_smallMed_1555533870.jpg	-122.083200000000005	37.0497999999999976	Felton	California	This is a delightful redwood forest and creek hike on several of the trails at Henry Cowell Park.
7024835	Quicksilver History Loop	8	blue	https://cdn-files.apstatic.com/hike/7026215_small_1554913719.jpg	https://cdn-files.apstatic.com/hike/7026215_smallMed_1554913719.jpg	-121.825100000000006	37.1739999999999995	Almaden Valley	California	A scenic hike that visits several of the old cinnabar (mercury ore) mining historical sites.
7014512	Fremont Older to Steven's Creek Reservoir Loop	7.70000000000000018	blue	https://cdn-files.apstatic.com/hike/7004564_small_1554245636.jpg	https://cdn-files.apstatic.com/hike/7004564_smallMed_1554245636.jpg	-122.055099999999996	37.2860000000000014	Saratoga	California	Wide open bay views descend into lush singletrack and steep climbs.
7010486	Quicksilver - McAbee Loop CCW	4.5	greenBlue	https://cdn-files.apstatic.com/hike/7025704_small_1554912738.jpg	https://cdn-files.apstatic.com/hike/7025704_smallMed_1554912738.jpg	-121.884699999999995	37.2135000000000034	Almaden Valley	California	A fairly easy, broad, well-maintained trail through beautiful hills with views of the San Francisco South Bay Area.
7062162	Hostel/Grapevine/Creek Trail Loop	2.39999999999999991	blueBlack	https://cdn-files.apstatic.com/hike/7053630_small_1555703824.jpg	https://cdn-files.apstatic.com/hike/7053630_smallMed_1555703824.jpg	-122.160499999999999	37.3504000000000005	Los Altos Hills	California	Climb the side of Elephant Mountain for beautiful views. Return along Adobe Creek with its rushing water.
7075842	Pedro Point Headlands Loop	2.29999999999999982	black	https://cdn-files.apstatic.com/hike/7031857_small_1554931901.jpg	https://cdn-files.apstatic.com/hike/7031857_smallMed_1554931901.jpg	-122.507900000000006	37.5850000000000009	Pacifica	California	Park has 246 acres of wilderness with spectacular views, a wide variety of birds and plants, and 3 miles of trails.
7026481	Redbird Creek Trail	1.89999999999999991	blue	https://cdn-files.apstatic.com/hike/7034999_small_1555018367.jpg	https://cdn-files.apstatic.com/hike/7034999_smallMed_1555018367.jpg	-81.1997999999999962	31.8887999999999998	Montgomery	Georgia	A great winding and level hike through the forest with views of the surrounding salt marsh.
7015632	Tupelo Trail	3.70000000000000018	greenBlue	https://cdn-files.apstatic.com/hike/7012826_small_1554821703.jpg	https://cdn-files.apstatic.com/hike/7012826_smallMed_1554821703.jpg	-81.0970999999999975	32.1732000000000014	Hardeeville	South Carolina	A mixed trail winding through the dike system of an old rice plantation.
7015580	Kingfisher Pond Loop	0.900000000000000022	blue	https://cdn-files.apstatic.com/hike/7012790_small_1554821669.jpg	https://cdn-files.apstatic.com/hike/7012790_smallMed_1554821669.jpg	-81.0785999999999945	32.1893000000000029	Hardeeville	South Carolina	A wooded loop around a "borrow pit" pond.
7015673	Recess Plantation Trail	3.29999999999999982	greenBlue	https://cdn-files.apstatic.com/hike/7013060_small_1554822152.jpg	https://cdn-files.apstatic.com/hike/7013060_smallMed_1554822152.jpg	-81.1141999999999967	32.1619000000000028	Hardeeville	South Carolina	A nice 5k trail around an old rice plantation irrigation canal.
7070046	Priests Landing Trail	6	green			-81.0144999999999982	31.9636999999999993	Skidaway Island	Georgia	Cruise through the Palmetto's of coastal Savannah.
7015649	Little Back River Trail	4	green	https://cdn-files.apstatic.com/hike/7022344_small_1554841165.jpg	https://cdn-files.apstatic.com/hike/7022344_smallMed_1554841165.jpg	-81.107600000000005	32.1691999999999965	Hardeeville	South Carolina	A lollipop trail that follows the Little Back River to the diversion canal and then circles back.
7062418	Beech Hill Trail	0.299999999999999989	green			-81.0762	32.1726000000000028	Hardeeville	South Carolina	Needs Summary
7062398	Duck Point Pond Access Trail	0.400000000000000022	green			-80.7586000000000013	32.2590000000000003	Hilton Head Island	South Carolina	Needs Summary
7062364	Clubhouse Access 2 Trail	0.200000000000000011	green			-80.7583999999999946	32.261099999999999	Hilton Head Island	South Carolina	Needs Summary
7015548	Lighthouse Overlook Trail	0.699999999999999956	greenBlue	https://cdn-files.apstatic.com/hike/7012725_small_1554821599.jpg	https://cdn-files.apstatic.com/hike/7012725_smallMed_1554821599.jpg	-80.8897999999999939	32.0287999999999968	Tybee Island	Georgia	A National Park trail leading to the Cockspur Lighthouse.
\.


--
-- Data for Name: user_trails; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.user_trails (ut_id, user_id, trail_id, is_completed, date_added) FROM stdin;
1	1	1234	t	2020-02-13 20:43:49.504482
2	2	1234	f	2020-02-13 20:43:49.504543
3	2	12345	f	2020-02-13 20:43:49.504653
4	1	12345	t	2020-02-13 20:43:49.504678
6	4	7019500	f	2020-02-19 20:30:24.43285
7	4	7019500	f	2020-02-19 20:41:44.721156
8	4	7019500	f	2020-02-19 20:45:03.322738
9	4	7019500	f	2020-02-19 20:45:39.784584
10	4	7019500	f	2020-02-19 20:45:42.697251
11	4	7019500	f	2020-02-19 20:58:26.703574
12	4	7025610	t	2020-02-20 00:14:08.216885
13	4	7012643	t	2020-02-20 00:17:05.754991
14	4	7012643	f	2020-02-20 00:30:10.007169
15	4	7012643	f	2020-02-20 00:30:32.47338
16	4	7025610	f	2020-02-20 00:58:41.294899
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.users (user_id, username, email, password, fname, lname, cell, city, state, zipcode) FROM stdin;
1	hello	hello@hello.com	hello	hel	lo	1234567890	\N	\N	\N
2	dude	dude@hello.com	hello	du	de	1234567891	\N	\N	\N
4	brobro	bro@bro.com	dude	Bro	Dude	\N	\N	\N	\N
\.


--
-- Name: trails_trail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.trails_trail_id_seq', 1, false);


--
-- Name: user_trails_ut_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.user_trails_ut_id_seq', 18, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- Name: trails trails_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.trails
    ADD CONSTRAINT trails_pkey PRIMARY KEY (trail_id);


--
-- Name: user_trails user_trails_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_trails
    ADD CONSTRAINT user_trails_pkey PRIMARY KEY (ut_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: user_trails user_trails_trail_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_trails
    ADD CONSTRAINT user_trails_trail_id_fkey FOREIGN KEY (trail_id) REFERENCES public.trails(trail_id);


--
-- Name: user_trails user_trails_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_trails
    ADD CONSTRAINT user_trails_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

