"""
Module to estimate with LDA for local modeler
"""

import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


from port.api.commands import (
    CommandSystemGetParameters,
    CommandSystemPutParameters,
)


PREDEFINED_VOCAB = {
    'bol':0,
    'gwenvanpoorten':1,
    'reneedewinter':2,
    'onadventurewithdad':3,
    'mreegen':4,
    'rarri':5,
    'slowflowanimal':6,
    'peterpannekoek':7,
    'ozcanakyol':8,
    'thetorsband':9,
    'juliajohannadebruin':10,
    '_chayna':11,
    'moestuinkriebels':12,
    'mrbeltandwezol':13,
    'debbyvdzande':14,
    'jerdyschouten':15,
    'burciin':16,
    'ulzng.boy':17,
    'sabina.ducatista':18,
    'roediementair':19,
    'rosalie':20,
    'justinhubner5':21,
    'leontineborsato':22,
    'suzanenfreek':23,
    'bankzitters':24,
    'dehaarclipvanmarieclaire':25,
    'daveroelvink':26,
    'nl_soccergirl_imara_schutte':27,
    'marcushpederseen':28,
    'roslanofficial':29,
    'kybba_':30,
    'politieknederland':31,
    'femke_bol':32,
    'murielle':33,
    'gernot_trauner':34,
    'het7':35,
    'frankslotta':36,
    'ruud_zwaan':37,
    'wout.poels':38,
    'vivianhoorn':39,
    'thomhaye':40,
    'm.pherai':41,
    'marijnkuipers':42,
    'juliakoopman':43,
    'kirstenvo_':44,
    'rtlnieuws':45,
    'amsterdam':46,
    'lauradijkema':47,
    'heffelini':48,
    'stanbrowney':49,
    'mezdi':50,
    'djpartyraiser':51,
    'juliaheetman':52,
    'afcajax':53,
    'liekevandervorst':54,
    'mr.yo.is.everywhere':55,
    'beauvaned':56,
    'flemming':57,
    'amiratahriofficial':58,
    'siemdejong':59,
    'cabin_anna':60,
    'boazo_o':61,
    'qmusicnl':62,
    'nosjeugdjournaal':63,
    'nuravanvliet':64,
    'sennabellod':65,
    'saulnaftalicoltof':66,
    'jobstevens':67,
    'lunanieuwboer':68,
    'kikisolvej':69,
    'robbievdgraaf':70,
    'estavana':71,
    'luna.amiri':72,
    'jones_brad':73,
    'perr_schuurs':74,
    'emmawortelboer':75,
    'voetbalprimeur':76,
    'mel.dlgn':77,
    'passantdawoud':78,
    'fantasm_techno':79,
    'maxverstappen1':80,
    'nicolettevandam1':81,
    'noachblyden':82,
    'lisannedewitte':83,
    'lilkleine':84,
    'pienlaathaaretenzien':85,
    'semdeconinck':86,
    '101barznl':87,
    'dutchie':88,
    'pieterdejongh12_the_champ':89,
    'billionaire.nl':90,
    'rochka_noel':91,
    'indixoord':92,
    'kristelverbeke':93,
    'viceisice':94,
    'djmaddog':95,
    'casa.schilperoort':96,
    'dominatorofficial':97,
    'rijkhofman':98,
    'suzanneschulting':99,
    'oranjeleeuwinnen':100,
    'stefandevries':101,
    'saanamirzaie':102,
    'noeldekkers':103,
    'its.satiella':104,
    'joybeune':105,
    'robinromeysa':106,
    'mandyofficial_be':107,
    'noordegroot':108,
    'naaddx':109,
    'cestmocro':110,
    'rogierroeters':111,
    'goldbandnl':112,
    'jimbakkum':113,
    'meester_mark':114,
    '_sushique':115,
    'kalvijn':116,
    'mootjeyek':117,
    'moniquesmit_insta':118,
    'dj_dimitri_k':119,
    'jorisvoorn':120,
    'soundrush':121,
    'juultjetieleman':122,
    'elisehoogerdijk':123,
    'myjewellery':124,
    'levivankempen':125,
    'reindersjm':126,
    'wahhab_h':127,
    'roycedevries':128,
    'danielle_vanzeelst':129,
    'dyen_music':130,
    'lottleeuw':131,
    'prabhuvisha':132,
    'shirleycvc':133,
    'joejoestamstam':134,
    'casimirschmidt':135,
    'familielakap':136,
    'liekevanlexmond':137,
    'dekraantjes':138,
    'teskedeschepper':139,
    'missk8':140,
    'svrouwendaal':141,
    'shaynasenior':142,
    'mattiemarieke':143,
    'iamtouzani':144,
    'phuturenoize':145,
    'codymathesgakpo':146,
    'instavoetbalzone':147,
    'fc_utrecht':148,
    'redbullracing':149,
    'dylanhaegens':150,
    'abbeyhoes':151,
    'moniquenoell':152,
    'marthwatermelon':153,
    'dullesofficial':154,
    'maradonnie':155,
    'veracamilla':156,
    'vajenvandenbosch':157,
    'roxannekwant':158,
    'straatduivel':159,
    'numidiamusic':160,
    'quintymirjam':161,
    'kristandegraaf':162,
    'justinbijlow':163,
    'jorrelhato':164,
    'mishdj_':165,
    'fleur.overgaag':166,
    'balr':167,
    'myronkoops':168,
    'chrisstussydj':169,
    'koen':170,
    'sunneryjames':171,
    'mdeligt_':172,
    'jasonsphysique':173,
    'mariogotze':174,
    'warfaceofficial':175,
    'kraantjepappie':176,
    'charbonn':177,
    'robinelisedraws':178,
    'azra.niisa':179,
    'roxeannehazes':180,
    'papaghana':181,
    'pattybrard':182,
    'kellymexy':183,
    'uberquin':184,
    'lydia.js_':185,
    'touzanitv':186,
    'typetopia':187,
    'dylanhoogerwerf':188,
    'gaby.blaaser':189,
    'mcdonaldsnl':190,
    'annemiekvanvleuten':191,
    'woodworkingtechnics':192,
    'frodebolhuis':193,
    'patrickkluivert9':194,
    'diiggys':195,
    'kaydewolf':196,
    'pacodehond':197,
    'bassmit':198,
    'danila.reizen':199,
    'lisavandervalk_':200,
    'puckvandrenth':201,
    'fabiojakobsen':202,
    'teunkoopmeiners':203,
    'andriesnoppert':204,
    'boef':205,
    'betulsarkhome':206,
    'arieboomsmainstagram':207,
    'bentheliem':208,
    'ryanjiro_':209,
    'rowaneckhardt':210,
    'jillroord':211,
    's4mkroon':212,
    'shanekluivert':213,
    'mrpoodlemilo':214,
    'mickyvdven':215,
    'robbertrodenburg':216,
    'lesley_versprille':217,
    'rotterdamse.poetsqueen':218,
    'montanameiland':219,
    'tobias_camman':220,
    'jesseklaver':221,
    'nielsschlimback':222,
    'amyog3neofficial':223,
    'nyael300':224,
    'meisjedjamila':225,
    'florencevandoorne':226,
    'chantalbles':227,
    'theoffline_club':228,
    'jayetothekaye':229,
    'nos':230,
    'meauhewitt':231,
    'bij_spiertjes_thuis':232,
    'dualdamage_raw':233,
    'yolanthecabau':234,
    'dean_alshawa':235,
    'eva.vlaar':236,
    'moderosaofficial':237,
    'yuuyuuniee':238,
    'paulvisser1954':239,
    'thestreamers':240,
    'kimkotter':241,
    'drielingmoeder_tatiana':242,
    'koenweijland':243,
    'naomivanasofficial':244,
    'kerimbabo':245,
    'racheljohn':246,
    'hijabhills':247,
    'sophieousri':248,
    'itsjulianjordan':249,
    'naomivaneeren_':250,
    'ninahouston':251,
    'manlikeyssi':252,
    'utrechtalive':253,
    'dailypaper':254,
    'joanpronk':255,
    'katjaschuurman':256,
    'letsdoubledutch':257,
    'sanne':258,
    'ancientscientist':259,
    'tessiewester':260,
    'tourdetietema':261,
    'avduinn':262,
    'jadevanweel':263,
    'patricia_van_nes':264,
    'novasarrailh':265,
    'indiiamaaarleyy':266,
    'olcay':267,
    'toddler.hair':268,
    'didishanna':269,
    'its__mootje':270,
    'ezgikoroglu':271,
    'teuntjep':272,
    'rhodeekok':273,
    'we.dep':274,
    'xandewaard':275,
    'conniespower':276,
    'jeniffer_belao':277,
    'elise_is_here':278,
    'jenniferlevii':279,
    'juliahorsten':280,
    'mistermindset':281,
    'vtwonen':282,
    'parratv':283,
    'esmeevankampen':284,
    'seppvdberg_':285,
    'onskoningshuis':286,
    'theplugzeurope':287,
    'manuela_salinas73':288,
    'rayklaassens':289,
    'nummertje39':290,
    'mvg180':291,
    'boosbnnvara':292,
    'splinterchabot':293,
    'daniquescw':294,
    'theojansen_official':295,
    'mrskeizer':296,
    'rachellevank':297,
    'lisandromartinezzz':298,
    'subzeroproject':299,
    'jillruby':300,
    'traveler.map_':301,
    'dragigudelj':302,
    'joy.liana':303,
    'voor_positiviteit':304,
    'svandesanden':305,
    'robertgesink':306,
    'memphisdepay':307,
    'sylvana':308,
    'nick_skeyes':309,
    'martienmeiland':310,
    'kosso.nl':311,
    'cdkcompany':312,
    'michelle_bollen':313,
    'robertdoornbos':314,
    'fawrynotsawry':315,
    'voetbal_ultras':316,
    'sean.demmers':317,
    'jarnoopmeer':318,
    'deliaskinmaster':319,
    'ieuyar':320,
    'jeroenvholland':321,
    'juttaleerdam':322,
    'armineisajan':323,
    'brittdekker92':324,
    'xisabel.kr':325,
    'ewoutgenemans':326,
    'niekmarijnissen':327,
    'off_leash_photografie':328,
    'shellysterk':329,
    'yuki.indy':330,
    'jaimievaes':331,
    'jessiejazzvuijk':332,
    'sergiovsreis':333,
    'bellavie_photoart':334,
    'ilsevanesch':335,
    'akkabouz911':336,
    'eliterentalsdubai':337,
    'marlyvd':338,
    'markbaanders':339,
    'hunkemoller':340,
    'jansmit':341,
    'annanooshin':342,
    'jorrickwieten':343,
    'joeyjaq':344,
    'sifanhassan':345,
    'sarcasper_':346,
    'tagliafico3':347,
    'floortjedessing':348,
    'radicalredemption':349,
    'djlafuente':350,
    'andreonana.24':351,
    'melis.andreea':352,
    'johanbakayoko':353,
    'davyklaassen':354,
    'nrps.prince':355,
    'amsterdam_gram':356,
    'roxy.dekkerr':357,
    'dilleenkamille':358,
    'douglascassio':359,
    'simonkeizer':360,
    'rtlboulevard':361,
    'darumnl':362,
    'minpres':363,
    'joeyveerman6':364,
    'yvonjaspers.official':365,
    'dominiquejanssen_nl':366,
    'intentsfestival':367,
    'emmakokofficial':368,
    'helenehendriks1':369,
    'elaisaya':370,
    'froknroll':371,
    'gtst':372,
    'joelveltman':373,
    'natasjafroger':374,
    'annevedder':375,
    'liemeurs':376,
    'angelaschijfofficial':377,
    'davinamichelleofficial':378,
    'marloesdevee':379,
    'rijksmuseum':380,
    '_roseamsterdam_':381,
    'ler0yy038':382,
    'martijn.nugteren':383,
    'estellecruijffofficial':384,
    'actionnederland':385,
    'harderstyles.nl':386,
    'chantaljanzen.official':387,
    'stevecarlintv':388,
    '433nl':389,
    'jeffreyparmentier':390,
    'byzey':391,
    'rotjoch':392,
    'wildebras.official':393,
    'danieldalen':394,
    'awakenings':395,
    'alzomored.official':396,
    'jeroentjes':397,
    'rvdofficial':398,
    'luukdejong9':399,
    'akkamist':400,
    'eliseboers':401,
    'sharon_ipema':402,
    'uitdekeukenvanfatima':403,
    'arden_nl':404,
    'eredivisie':405,
    'efteling':406,
    'gio':407,
    'ravenvandorst':408,
    'astleighvanemden':409,
    'lucywoesthoff':410,
    'niekyholzken':411,
    'richard_groenendijk':412,
    'samanthacharrak':413,
    'rafaelvdvaart':414,
    'daphnevdomselaar':415,
    'floodcastpod':416,
    'chatmo':417,
    'joannvdherik':418,
    'expeditierobinson_rtl':419,
    'themermaidtale__':420,
    'samanthasteenwijk':421,
    '_demivdw':422,
    'jel_nl':423,
    'larsveldwijk':424,
    'driplist':425,
    'geuzeengorgels':426,
    'jippheldoorn':427,
    'melikeskids':428,
    '6ejou':429,
    '_jessedrent':430,
    'lutshageertruida':431,
    'maan.de.st':432,
    'brianbrobbeyy':433,
    'inez.atili':434,
    'rapnieuwshq':435,
    'dev.yne':436,
    'reinierzonneveld':437,
    'rumag':438,
    'goedhartmotoren':439,
    'badr_vds':440,
    'tisjeboyjay':441,
    'overmijnlijk':442,
    'vandaaginside':443,
    'quilindschy':444,
    'caravdrijkenvec':445,
    'romeestrijd':446,
    'florisgobel':447,
    'maytebellod':448,
    'jantinevandinther':449,
    'probadormusic':450,
    'tamaratohamy':451,
    'amenti.world':452,
    'thooootje':453,
    'linda':454,
    'autotopnl':455,
    'adnaan_altaher':456,
    'victoriaverstappen':457,
    'voedingsweetjes':458,
    'kajstypetjes':459,
    'gregoryvanderwiel':460,
    'laviesanne':461,
    'nikkietutorials':462,
    'thijsboermans':463,
    'meervoormannen':464,
    'closetvanval':465,
    'naomitraa':466,
    'nienke.fitness':467,
    'loavies':468,
    'isahoes':469,
    'gorillawear':470,
    'dvlunteren':471,
    'daniquebossers':472,
    'liekemartens':473,
    'strictly.techno':474,
    'myriamahmadi':475,
    'bastietema':476,
    'meesdix':477,
    'geertwilders':478,
    'frankyrizardo':479,
    'amsterdam.explores':480,
    'petergillisoostappen':481,
    'dumpertsport':482,
    'bestezangers':483,
    'rotterdamsememes':484,
    'angerfist_official':485,
    'melanielatooy':486,
    'jordanzirkzee':487,
    'upfront':488,
    'jadaborsato':489,
    'qpromes':490,
    'djamilacelina':491,
    'keestolofficial':492,
    'celesteplak':493,
    'berendjan_':494,
    'catharinaelisabethx':495,
    'shanikevh':496,
    'mariatailor':497,
    'dorianbindels':498,
    'nieuws':499,
    'mittchelb':500,
    'arjenlubach':501,
    'joeyakz6':502,
    'meesterjesper':503,
    'verde.whatever':504,
    'jeppehondelink':505,
    'saina_shokoofandeh':506,
    'missenvyperu':507,
    'nesimelahmadi':508,
    'leslie_keijzer':509,
    'mcsnelle':510,
    'arbi_emiev_aggressor_':511,
    'redbullned':512,
    'nathantjoeaon':513,
    'handigetips__':514,
    'drphunkmusic':515,
    'lecolook':516,
    'dennis_schouten95':517,
    'svenkramer':518,
    'bibibreijman':519,
    'kellerpaul01':520,
    'gamemeneer':521,
    'benzcollector.sneek':522,
    'martijn_krabbe':523,
    'donkaaklijn':524,
    'surfsterre':525,
    'ruudgullit':526,
    'stuktv':527,
    'longeneeslijk':528,
    'veggilaine':529,
    'nickschilder':530,
    'nienkeplas':531,
    'officialrebelion':532,
    'icemanvieze':533,
    'bibi.meijer':534,
    'nicole.jonk':535,
    'scheerenveenofficial':536,
    'glenncoldenhoff':537,
    'bokado':538,
    'blacka5324':539,
    'cjsgalleryonline':540,
    'susan_elbert_photography':541,
    'josip.sutalo':542,
    'ultras.cult':543,
    'katertje_nl':544,
    'dbstf':545,
    'vicccle':546,
    'lies_zhara':547,
    'fransbauer':548,
    'qucee':549,
    'emmaheesters':550,
    'barbieedripz':551,
    'bram.krikke':552,
    'psv':553,
    'unresolvedmedia':554,
    'richardverschoor':555,
    'tamaraelbaz':556,
    'eentetofleventsj':557,
    'meesvdam':558,
    'royouderikerink':559,
    'topnotchnl':560,
    'rutgervink':561,
    'joostklein':562,
    'loizalamers':563,
    'bizzey':564,
    'chefkeluc':565,
    'kazvanderwaard':566,
    'maudlowisbackup':567,
    'tabithamusik':568,
    'olivia.talar':569,
    'humansofamsterdam':570,
    'joost.goedhart':571,
    'noartmusic':572,
    '_tasha.x.x':573,
    'robinmartensofficial':574,
    'vanessavancartier':575,
    'kea_8':576,
    'othmannl':577,
    'officialjaraya':578,
    'tuliptoursholland':579,
    'giel':580,
    'defano.holwijn':581,
    'noa.mnk':582,
    'wowcrab_nl':583,
    'bravo':584,
    'broerspodcast':585,
    'markvandrunick':586,
    'joybosz':587,
    'esralakap':588,
    'josephklibansky':589,
    'joshastradowski':590,
    'koninklijkhuis':591,
    'actofrage':592,
    'jasperdemollin':593,
    'sjaak.swart':594,
    'sterkindekeuken':595,
    'afcajaxfanclub':596,
    'gerardekdom':597,
    'lepetitbeirut':598,
    'pauldeleeuw':599,
    'mikkykiemeney':600,
    'kaesutherland':601,
    'aaron.nga':602,
    'bertriewierenga':603,
    'moordcast':604,
    'johnvantschip':605,
    'deadlygunsofficial':606,
    'iamtimkeizer':607,
    'thedarkhorror':608,
    'superdushichef':609,
    'featherlighthorsemanship':610,
    'sisibolatini':611,
    'jeffreydelange':612,
    'sannewevers.official':613,
    'bridgetmaasland':614,
    'naci.unuvar':615,
    'louiselatooy':616,
    'disneyfeel.s':617,
    'kor_hoebe':618,
    '_antoinettedejong':619,
    'teamnlinsta':620,
    'jfaberski':621,
    'carvlogger':622,
    'mccrally':623,
    'mevrouwtjebestekla':624,
    'thunderdome':625,
    'allerhande':626,
    'kiyavanrossum':627,
    'brugklastv':628,
    'frenna':629,
    'lauraceliav':630,
    'merijn.scholten':631,
    'vertilemusic':632,
    'emmakeuven':633,
    'robinvanpersie':634,
    'paxenbelikeofficial':635,
    'edwinvandersar1':636,
    'bowilkes':637,
    'emms_bl':638,
    'cedicityboy':639,
    'rubenbijy':640,
    'jan_versteegh':641,
    'azizbekkaoui':642,
    'maurovdkerkhof':643,
    'zaargoedemans':644,
    'sterrekoning':645,
    'niekkimmann':646,
    'djkorsakoff':647,
    'maaike.r6':648,
    'bobrownn':649,
    'nicolettekluijver_':650,
    'christianchaco':651,
    'harm':652,
    'leroyderouw':653,
    'jayjayboske':654,
    'natuurmonumenten':655,
    'quintenverschure':656,
    'keuringsdienst_van_waarde':657,
    'joosjeburg':658,
    'hennabyibka':659,
    'viktor_brand':660,
    'djgelincik':661,
    'brittscholte':662,
    'bibijaneangelica':663,
    'nyckdevries':664,
    'jobjobse':665,
    'marthoogkamer':666,
    'jurrientimber':667,
    'jelkavanhouten':668,
    'williamrutten':669,
    'pietervalley':670,
    'hollybrood':671,
    'amsterdamworld':672,
    'alberto.stegeman':673,
    'orkunkokcu':674,
    'justinkluivert':675,
    'dunctromp':676,
    'irisrulkens':677,
    'quinsding':678,
    'daniellavanderwerf':679,
    'reez0609':680,
    'juulbarten':681,
    'jessehoefnagels':682,
    'rose_bertram':683,
    'ajaxlife':684,
    'paulinewing':685,
    'theblackmt':686,
    'hyundai_n_worldwide':687,
    'mariekeelsinga':688,
    'havermelkelite':689,
    'abdinageeye':690,
    'gerard_joling':691,
    'louisvanbaar':692,
    'maatsen_':693,
    'netflixnl':694,
    'thisdutchietravels':695,
    'ki.slash.ki':696,
    'wietzedej':697,
    'yasminepierards':698,
    'ballenbingo':699,
    'beautygloss':700,
    'liefsofficial':701,
    'akaluuk':702,
    'callumscreativeclub':703,
    'noavahle':704,
    'lonnekenooteboom':705,
    'daanalferink':706,
    'oranjehockey':707,
    'drift_banana':708,
    'joeprovers':709,
    'joshuamarkiet':710,
    'patta_nl':711,
    'badvibesforeverofficial':712,
    'lynnhermanussen':713,
    'sonuha':714,
    'franklammersofficial':715,
    'alexia_van_oranje':716,
    'dumpert':717,
    'viviannemiedema':718,
    'raptijd':719,
    'kriskrossamsterdam':720,
    'topg.nl':721,
    'monstertube_':722,
    'lynpfaff':723,
    'yip_andjar':724,
    'theteamgullit':725,
    'janiceblok':726,
    'sadkaya':727,
    'kennethtaylor_':728,
    'romeeeeyy':729,
    'sheida.alhoei':730,
    'pienhersman':731,
    'isajolein':732,
    'anita_life.style':733,
    'studio.drift':734,
    'lunaisabellaa':735,
    'djpaulelstak':736,
    'annekeedeligt':737,
    'ginneynoa':738,
    'monicageuze':739,
    'elodiekuijper':740,
    'mom.lifetips':741,
    'lijpe':742,
    'cash_catch':743,
    'isadeejansen':744,
    'martingarrix':745,
    'boerzoektvrouwofficial':746,
    'adfsamski':747,
    'buddyvedder':748,
    'that70s_crochet':749,
    'verstappencom':750,
    'berkantdural':751,
    'sannevanlierop':752,
    'mollymazs':753,
    'jenstoornstra':754,
    'silvanovos':755,
    'merel23':756,
    'kristina_pimenova_pp':757,
    'lotte_meulendijks':758,
    'onsoranje':759,
    'bartverbruggen1':760,
    'kakhiel':761,
    'noa_diorgina':762,
    'veramusicofficial':763,
    'fredvanleer':764,
    'telegraaf.nl':765,
    'fr12nl':766,
    'sophiemilzink':767,
    'politieke_jongeren':768,
    'nemanjagudelj':769,
    'xeniarooders':770,
    'snollebollekes':771,
    'matthy':772,
    'ikbenwela':773,
    'maaikevanhouten':774,
    'victoria_vermeer':775,
    'kevinlangeree':776,
    'domien':777,
    'chanelsoree':778,
    'defqon1':779,
    'dsturbnl':780,
    'k3.studio100':781,
    'sefameubel':782,
    'kuyt':783,
    'robingroot_':784,
    'ronald':785,
    'channahkoerten':786,
    'nathaliehelmer':787,
    'amffestival':788,
    'sunitasophia':789,
    'q_dance':790,
    'virgilvandijk':791,
    'nadecheandmootje':792,
    'queen.maxima':793,
    'ghdeado':794,
    'annickvelthuis':795,
    'kelly_weekers':796,
    's10s10xx':797,
    'armadamusic':798,
    'vita.cleo':799,
    'evelinesaalberg':800,
    'dj.latu':801,
    'stuntje':802,
    'koenpieter':803,
    'kinoluv7':804,
    'b_smichelle99':805,
    'artbymaudsch':806,
    'appiemussa':807,
    'thebarefoot_dutchman':808,
    'ekowjudge':809,
    'officialswaggie1':810,
    'jeffreyrholland':811,
    'leavecaricealone':812,
    'esther.vedder':813,
    'justinlucaci':814,
    'missmontreal_':815,
    'jackie_groenen_14':816,
    'treidinga':817,
    'hemanederland':818,
    'itsmaartenn':819,
    'myhomeofzodiac':820,
    'ewout.pahud':821,
    'jettenrob':822,
    'fresia.ca':823,
    'custom.caferacer':824,
    'latina_in_the_netherlands':825,
    'enzoknol':826,
    'felinehoi':827,
    'meeshilgerss':828,
    'boevenspotter':829,
    'fcgroningen':830,
    'lizzyvdligt':831,
    'ayleenbella':832,
    'mannenpage':833,
    'madeliefbroos':834,
    'jadeanna':835,
    'demivollering':836,
    'broederliefde':837,
    'carlosplatierluna':838,
    'sihamsanadd':839,
    'brabant_memes':840,
    'allesoldier':841,
    'harriesnijders':842,
    'florinehofstee':843,
    'iitsyasmine':844,
    'marcovanginkel':845,
    'soykroon':846,
    'maartenpaes':847,
    'annebelvisscher':848,
    'edgardavidsofficial':849,
    'kasperdolberg':850,
    'fashionista.for.youu':851,
    'kiratoussaint':852,
    'lucasandsteve':853,
    'videolandonline':854,
    'ad_nl':855,
    'ramalho92':856,
    'rapnieuwstv':857,
    'antoonpb':858,
    'rianne.meijer':859,
    'seravrij':860,
    'djrandofficial':861,
    'klm':862,
    'samhoogland':863,
    'donyellmalen':864,
    'mariskabauer':865,
    'onnedi':866,
    'heelhollandnakt':867,
    'jsc.automotive':868,
    'rifffiii':869,
    'demideboer':870,
    'chesmorelive':871,
    'raymilsamuel':872,
    'dr_peacock':873,
    'rowenaverdaasdonk':874,
    'ronnieflex':875,
    'manoujuecardoso':876,
    'nadine_visser':877,
    'kremersnicol':878,
    'dutchperformante':879,
    'soundos_el_ahmadi':880,
    'villain.nl':881,
    'duobedankt':882,
    'wanderlust.nl':883,
    'de_speld':884,
    'dilansabah':885,
    'amyrosedebruijn':886,
    'ginasingels':887,
    'nosstories':888,
    'quintentimber':889,
    'vandergunstnathan':890,
    'marcosenesi':891,
    'ninadewal':892,
    'thedailyquotesnl':893,
    'manontilstra':894,
    'drs__official':895,
    'diegoandmarloes':896,
    'puckpieterse':897,
    'harrielavreysen':898,
    'debroervanroos':899,
    'sergioherman':900,
    'nvitral':901,
    'ericameiland':902,
    'lidewijwelten':903,
    'jorendejager':904,
    'danique.hosmar':905,
    'chouffevon':906,
    'kasumovic_ella':907,
    'dejeugd':908,
    'miljuschka':909,
    'tinomartin':910,
    'samhofman':911,
    'jandinoasporaat':912,
    'ninaschotpoort':913,
    'lizasips':914,
    'lauraponticorvo':915,
    'bu.kolthoum':916,
    'kerstin_casparij':917,
    'timorworld':918,
    'maximeandsophie':919,
    'mijnkwaadbloed':920,
    'kleinstukjeversheid':921,
    'douwemacare':922,
    'aardrijkskunde_kennisclips':923,
    'donnyroelvink':924,
    'josylvio':925,
    'abdelhak_nouri':926,
    'eloisevanoranje':927,
    'dylanpeys':928,
    'voetbalinternational.nl':929,
    'mohammad.darabi_480':930,
    'russonl':931,
    'eo_blauwbloed':932,
    'danidewit_':933,
    'djcoone':934,
    'm1rautomotive':935,
    'kojavitez1981':936,
    'annekeannique':937,
    'wendyvandijk3':938,
    'luanbellinga_12':939,
    'yibbijansen':940,
    'keetoldenbeuving':941,
    'kanilure':942,
    'fsgreen':943,
    'pommelinetilliere':944,
    'action_tips':945,
    'ninawarink':946,
    'vincentvisser_':947,
    'maximemeiland':948,
    'internetgekkies':949,
    'famjelies':950,
    'kellyspronk':951,
    'fashionbyiems':952,
    'evasaccount':953,
    'daanboom':954,
    'hato.dj':955,
    'vjeze_fur':956,
    'maritbrugman':957,
    'lindahakeboom':958,
    'vonnekebonneke':959,
    'ricoverhoeven':960,
    'jillgoede_':961,
    'evajinek':962,
    'yazzierose':963,
    'mobicepp':964,
    'etenmetnicknl':965,
    'sjamadriaan':966,
    'keesvanderspek':967,
    'marijezuurveld':968,
    'irisenthoven':969,
    'raouljoshua':970,
    'matheu_hinzen':971,
    'tessavmontfoort':972,
    'authenticchica':973,
    'thebestsocialmedianl':974,
    'mastersofhardcore':975,
    'nicokeenan':976,
    'zoetauran':977,
    'dionne_stax':978,
    'industrieelchique':979,
    'andyvandermeijde7':980,
    'lieke_schreurs':981,
    'freekvonk':982,
    'gwens_illustrations':983,
    'jochemmyjer':984,
    'mestomusic':985,
    'irmaknol':986,
    'nadinehettinga_':987,
    'pamindegym':988
}


def serialize_random_state(rs: np.random.RandomState) -> str:
    """
    Serializes np.random.RandomState to a json string
    """
    state = rs.get_state()
    # tolist if item is ndarray
    serializable_state = [item.tolist() if isinstance(item, np.ndarray) else item for item in state]
    return json.dumps(serializable_state)



def deserialize_random_state(serialized_state: str) -> np.random.RandomState:
    """
    Deserializes a json string containing a random state and returns np.random.RandomState object
    """
    deserialized_state = tuple(
        np.array(item, dtype=np.uint32) if isinstance(item, list) 
        else item 
        for item in json.loads(serialized_state)
    )
    rs = np.random.RandomState()
    rs.set_state(deserialized_state) #pyright: ignore
    return rs


def save_lda_model(lda: LatentDirichletAllocation) -> str:
    model_params = {
        'components_': lda.components_.tolist(),
        'exp_dirichlet_component_': lda.exp_dirichlet_component_.tolist(),
        'doc_topic_prior_': lda.doc_topic_prior_,
        'n_components': lda.n_components,
        'learning_decay': lda.learning_decay,
        'learning_offset': lda.learning_offset,
        'max_iter': lda.max_iter,
        'random_state': lda.random_state,
        'n_batch_iter_': lda.n_batch_iter_,
        'topic_word_prior_': lda.topic_word_prior_,
    }
    model = {
        "model_params": model_params,
        "random_state": serialize_random_state(lda.random_state_)
    }
    return json.dumps(model)


def load_lda_model(serialized_model: str | None, n_components: int) -> LatentDirichletAllocation:
    if serialized_model == None:
        lda = LatentDirichletAllocation(n_components=n_components, learning_method='online', max_iter=1)
        return lda

    model: dict = json.loads(serialized_model)
    model_params = model['model_params']
    random_state = model['random_state']
    
    lda = LatentDirichletAllocation(
        learning_method='online',
        n_components=model_params['n_components'],
        learning_decay=model_params['learning_decay'],
        learning_offset=model_params['learning_offset'],
        max_iter=model_params['max_iter'],
        random_state=model_params['random_state']
    )

    lda.components_ = np.array(model_params['components_'])
    lda.exp_dirichlet_component_ = np.array(model_params['exp_dirichlet_component_'])
    lda.doc_topic_prior_ = model_params['doc_topic_prior_']
    lda.n_batch_iter_ = model_params['n_batch_iter_'] 
    lda.topic_word_prior_ = model_params['topic_word_prior_'] 

    lda.random_state_ = deserialize_random_state(random_state)
    return lda


#def learn_params(data, vocabulary, model: str, n_components) -> str:
def learn_params(data, model: str, n_components) -> str:
    lda = load_lda_model(model, n_components)
    vectorizer = CountVectorizer(vocabulary=PREDEFINED_VOCAB)

    # data should be list of a list of strings
    batch_term_matrix = vectorizer.fit_transform(data)
    lda.partial_fit(batch_term_matrix)
    new_model = save_lda_model(lda)

    return new_model


STUDY_ID="test"

def getParameters(study_id=STUDY_ID):
    return CommandSystemGetParameters(study_id=study_id)


def putParameters(run_json: str, data):
    run = json.loads(run_json)
    new_model = learn_params(data, run["model"], n_components=3)

    return CommandSystemPutParameters(
        id=run["id"],
        model=new_model,
        check_value=run["check_value"],
        study_id=STUDY_ID,
    )



