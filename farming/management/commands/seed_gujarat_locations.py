from django.core.management.base import BaseCommand
from farming.models import District, Taluka, Village, FarmerProfile, Crop

class Command(BaseCommand):
    help = "Seeds all 33 official Gujarat districts, comprehensive talukas, and sample villages into the database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Gujarat Location Seeding (Districts -> Talukas -> Villages)..."))

        gujarat_data = {
            "Ahmedabad": {
                "region": "Central Gujarat",
                "talukas": {
                    "Ahmedabad City": ["Vastrapur", "Navrangpura", "Maninagar", "Chandkheda", "Bopal"],
                    "Daskroi": ["Bakrol", "Kuha", "Miroli", "Gatrad", "Kanbha"],
                    "Sanand": ["Sanand Rural", "Changodar", "Manipur", "Nidharad", "Telav", "Chekhla", "Moraiya"],
                    "Viramgam": ["Viramgam Rural", "Hansalpur", "Karakthal", "Dumana", "Jakhwada"],
                    "Dholka": ["Dholka Rural", "Koth", "Saroda", "Rampur", "Bavla Road"],
                    "Bavla": ["Bavla Rural", "Adroda", "Dhegam", "Kavitha", "Saljada"],
                    "Detroj-Rampura": ["Detroj", "Rampura", "Gunjala", "Kukvav", "Bhagapura"],
                    "Mandal": ["Mandal Rural", "Trent", "Nayka", "Udhroj", "Kadvasan"],
                    "Dhandhuka": ["Dhandhuka Rural", "Tagadi", "Rayka", "Aniyali", "Khadol"],
                    "Dholera": ["Dholera SIR", "Bhangadh", "Gogla", "Panchhi", "Bavliyari"]
                }
            },
            "Amreli": {
                "region": "Saurashtra",
                "talukas": {
                    "Amreli": ["Amreli Rural", "Chakkargadh", "Vedi", "Jalila", "Bhandaria"],
                    "Babra": ["Babra Rural", "Karanu", "Chamarval", "Garna", "Kotda Pitha"],
                    "Bagasara": ["Bagasara Rural", "Hadala", "Jithudi", "Munjiasar", "Pipalva"],
                    "Dhari": ["Dhari Rural", "Chalala", "Dalkhaniya", "Ambardi", "Sarasiya"],
                    "Jafrabad": ["Jafrabad Port", "Babararkot", "Nageshri", "Shiyalbet", "Mitiala"],
                    "Khambha": ["Khambha Rural", "Dedan", "Dhavadia", "Lasa", "Nonghanvadar"],
                    "Kunkavav Vadia": ["Vadia", "Kunkavav", "Devgam", "Bilkha Road", "Moti Kunkavav"],
                    "Lathi": ["Lathi Rural", "Damnagar", "Chavand", "Ansodar", "Dudhiya"],
                    "Lilia": ["Lilia Rural", "Lilia Mota", "Bhensan", "Kalyanpur", "Panchtalavda"],
                    "Rajula": ["Rajula Rural", "Dungar", "Kovaya", "Victor", "Pipavav Port"],
                    "Savarkundla": ["Savarkundla Rural", "Vijpadi", "Vanda", "Badhada", "Nesadi"]
                }
            },
            "Anand": {
                "region": "Central Gujarat",
                "talukas": {
                    "Anand": ["Anand City", "Bakrol", "Mogri", "Karamsad", "Vithal Udyognagar", "Chikhodra"],
                    "Anklav": ["Anklav Rural", "Asodar", "Bhetasi", "Joshikuva", "Navakhal"],
                    "Borsad": ["Borsad Rural", "Bhadran", "Davol", "Napa", "Vasad"],
                    "Khambhat": ["Khambhat Rural", "Kansari", "Undel", "Taran", "Metpur"],
                    "Petlad": ["Petlad Rural", "Dharmaj", "Sunav", "Bandra", "Pandoli"],
                    "Sojitra": ["Sojitra Rural", "Malataj", "Petli", "Dali", "Devataj"],
                    "Tarapur": ["Tarapur Rural", "Moraj", "Milrampura", "Vataman Road", "Padra"],
                    "Umreth": ["Umreth Rural", "Dakore Road", "Thamna", "Lingda", "Sundalpura"]
                }
            },
            "Aravalli": {
                "region": "North Gujarat",
                "talukas": {
                    "Modasa": ["Modasa Rural", "Dhansura Road", "Malpur Road", "Tintoi", "Sabalpur"],
                    "Bayad": ["Bayad Rural", "Demai", "Sathamba", "Amodra", "Vatrak"],
                    "Bhiloda": ["Bhiloda Rural", "Shamlaji", "Mankroda", "Meru", "Lilchha"],
                    "Dhansura": ["Dhansura Rural", "Bhorol", "Rahiyol", "Vakhtapur", "Sika"],
                    "Malpur": ["Malpur Rural", "Ubharan", "Helodar", "Magodi", "Vankaneda"],
                    "Meghraj": ["Meghraj Rural", "Isari", "Kumbhapur", "Vasan", "Panchal"]
                }
            },
            "Banaskantha": {
                "region": "North Gujarat",
                "talukas": {
                    "Palanpur": ["Palanpur Rural", "Gadh", "Chandisar", "Kanodar", "Malana"],
                    "Deesa": ["Deesa Rural", "Bhildi", "Jharu", "Ranpur", "Khadol", "Lorwada"],
                    "Dhanera": ["Dhanera Rural", "Nenava", "Ramsan", "Dhanera Market", "Bhadra"],
                    "Danta": ["Danta Rural", "Ambaji", "Khedbrahma Road", "Hadad", "Motasada"],
                    "Vadgam": ["Vadgam Rural", "Chhapi", "Majadar", "Mahi", "Semodra"],
                    "Tharad": ["Tharad Rural", "Vav Road", "Dodgam", "Piluda", "Rah"],
                    "Vav": ["Vav Rural", "Bhatvar", "Radhanpur Road", "Chotil", "Dhedhal"],
                    "Kankrej": ["Shihori", "Thara", "Kharia", "Nekoi", "Raner"],
                    "Bhabhar": ["Bhabhar Rural", "Mitha", "Sanva", "Kaprupur", "Kareli"],
                    "Deodar": ["Deodar Rural", "Kotda", "Salpura", "Bhadreshwar", "Lilacha"],
                    "Amirgadh": ["Amirgadh Rural", "Iqbalgadh", "Jorapura", "Khara", "Dhanari"],
                    "Dantiwada": ["Dantiwada Dam", "Nilpur", "Gangudra", "Bhadli", "Panthawada"],
                    "Suigam": ["Suigam Rural", "Koreti", "Radhanpur Boundary", "Benap", "Golgam"],
                    "Lakhani": ["Lakhani Rural", "Lavana", "Jasra", "Kuda", "Vakwada"]
                }
            },
            "Bharuch": {
                "region": "South Gujarat",
                "talukas": {
                    "Bharuch": ["Bharuch City", "Zadeshwar", "Bholav", "Dahej Road", "Tham"],
                    "Ankleshwar": ["Ankleshwar GIDC", "Sarangpur", "Piraman", "Panoli", "Bakrol"],
                    "Jambusar": ["Jambusar Rural", "Kavi", "Magnad", "Nahiyer", "Tundaj"],
                    "Jhagadia": ["Jhagadia GIDC", "Umaralla", "Avidha", "Bhalod", "Mulad"],
                    "Hansot": ["Hansot Rural", "Sunevkalla", "Ilav", "Katpor", "Ankleshwar Road"],
                    "Valia": ["Valia Rural", "Netrang Road", "Kondh", "Dodiapada", "Pithor"],
                    "Vagra": ["Vagra Rural", "Dahej Port", "Vilayat GIDC", "Aliyabet", "Khandera"],
                    "Amod": ["Amod Rural", "Achhod", "Nahier", "Machhasara", "Kerwada"],
                    "Netrang": ["Netrang Rural", "Bhilwada", "Kakrapar Road", "Dharoli", "Vataria"]
                }
            },
            "Bhavnagar": {
                "region": "Saurashtra",
                "talukas": {
                    "Bhavnagar": ["Bhavnagar City", "Vartej", "Nari", "Budhel", "Ruva", "Sidsar"],
                    "Sihor": ["Sihor Rural", "Songadh", "Navagam", "Tana", "Kajavadar"],
                    "Ghogha": ["Ghogha Port", "Kuda", "Lakhanka", "Tagadi", "Avali"],
                    "Palitana": ["Palitana Rural", "Gheti", "Gariadhar Road", "Rohishala", "Ankolali"],
                    "Mahuva": ["Mahuva Rural", "Kalgath", "Bagdana", "Otha", "Talgajarda", "Katpar"],
                    "Talaja": ["Talaja Rural", "Trapaj", "Alang Road", "Sartanpar", "Shetrunji Dam"],
                    "Gariadhar": ["Gariadhar Rural", "Parvadi", "Luvara", "Survilas", "Morba"],
                    "Vallabhipur": ["Vallabhipur Rural", "Kalyanpur", "Patan", "Chamardi", "Nava Ratanpur"],
                    "Umrala": ["Umrala Rural", "Dhola", "Rampura", "Bhojavadar", "Dadhar"],
                    "Jesar": ["Jesar", "Nava Sanala (Joliya Vadi)", "Biladi", "Chhapriyali", "Kotda", "Matida"]
                }
            },
            "Botad": {
                "region": "Saurashtra",
                "talukas": {
                    "Botad": ["Botad Rural", "Gadhada Road", "Turkha", "Lathidad", "Salangpur Road"],
                    "Gadhada": ["Gadhada Rural", "Gopinathji Mandir", "Ugmedi", "Ningala", "Dhasa"],
                    "Barwala": ["Barwala Rural", "Salangpur (Hanuman)", "Chokdi", "Rampur", "Navda"],
                    "Ranpur": ["Ranpur Rural", "Kinara", "Devgana", "Kundli", "Umrala Road"]
                }
            },
            "Chhota Udepur": {
                "region": "Central Gujarat",
                "talukas": {
                    "Chhota Udepur": ["Chhota Udepur Rural", "Tejgadh", "Zoz", "Punsiyavant", "Mithibor"],
                    "Bodeli": ["Bodeli Rural", "Alipura", "Dharmpuri", "Hadod", "Sankheda Road"],
                    "Jetpur Pavi": ["Pavi Jetpur", "Kadwal", "Sajwa", "Panvad", "Suskal"],
                    "Kavant": ["Kavant Rural", "Panvad", "Mogara", "Hamirpur", "Raypur"],
                    "Nasvadi": ["Nasvadi Rural", "Tanakhla", "Khandi", "Sindhikuva", "Amroli"],
                    "Sankheda": ["Sankheda Rural", "Bahadarpur", "Gundi", "Hareshwar", "Pipaldi"]
                }
            },
            "Dahod": {
                "region": "Eastern Gujarat",
                "talukas": {
                    "Dahod": ["Dahod City", "Raska", "Bavka", "Jekot", "Limdi Road"],
                    "Devgadh Baria": ["Devgadh Baria Rural", "Piplod", "Ranapur", "Sagtala", "Bhuvero"],
                    "Dhanpur": ["Dhanpur Rural", "Pipodra", "Kanjeta", "Gadhvel", "Pavadi"],
                    "Fatepura": ["Fatepura Rural", "Sukhsar", "Batwada", "Karadhana", "Ghoghas"],
                    "Garbada": ["Garbada Rural", "Gangardi", "Jesawada", "Nandva", "Matwa"],
                    "Limkheda": ["Limkheda Rural", "Dudhia", "Singvad Road", "Palla", "Agara"],
                    "Jhalod": ["Jhalod Rural", "Limdi", "Kadwal", "Therka", "Vagela"],
                    "Sanjeli": ["Sanjeli Rural", "Pithapur", "Mandli", "Nenki", "Bodiya"],
                    "Singvad": ["Singvad Rural", "Ratanpur", "Dabhva", "Machhai", "Chhapri"]
                }
            },
            "Dang": {
                "region": "South Gujarat",
                "talukas": {
                    "Ahwa": ["Ahwa Town", "Don Hill", "Pimpalner Road", "Chikhli", "Bhavandag"],
                    "Subir": ["Subir Rural", "Shabari Dham", "Pampa Sarovar", "Pipaldahad", "Lavchali"],
                    "Waghai": ["Waghai Botanical Garden", "Gira Falls", "Saputara Hill Station", "Dagadpada", "Borkhal"]
                }
            },
            "Devbhumi Dwarka": {
                "region": "Saurashtra",
                "talukas": {
                    "Dwarka": ["Dwarka Town", "Beyt Dwarka", "Okha Port", "Varwala", "Mithapur", "Kuranga"],
                    "Bhanvad": ["Bhanvad Rural", "Verad", "Raval Road", "Ghumli", "Kalyanpur Road"],
                    "Kalyanpur": ["Kalyanpur Rural", "Lamba", "Bhatiya", "Harshad (Miyani)", "Bankodi"],
                    "Khambhalia": ["Khambhalia Rural", "Salaya Port", "Vadinar", "Dharampur", "Zakhar"]
                }
            },
            "Gandhinagar": {
                "region": "North Gujarat",
                "talukas": {
                    "Gandhinagar": ["Sector 1-30", "Koba", "Pethapur", "Vavol", "Kudasan", "Raysan", "Chiloda"],
                    "Dehgam": ["Dehgam Rural", "Bahiyal", "Kadadra", "Sampa", "Zundal Road"],
                    "Kalol": ["Kalol GIDC", "Saij", "Chhatral", "Veda", "Adraj", "Shertha"],
                    "Mansa": ["Mansa Rural", "Charada", "Amarpura", "Itadra", "Lodra", "Vihar"]
                }
            },
            "Gir Somnath": {
                "region": "Saurashtra",
                "talukas": {
                    "Veraval": ["Veraval Port", "Somnath Temple", "Prabhas Patan", "Dari", "Bhalpara"],
                    "Kodinar": ["Kodinar Rural", "Mul Dwarka", "Chhara Port", "Harmadiya", "Devli"],
                    "Sutrapada": ["Sutrapada Rural", "Prasnavada", "Lodva", "Moradiya", "Vavdi"],
                    "Talala": ["Talala (Gir Kesar)", "Sasan Gir", "Ankolwadi", "Bhojde", "Surva", "Lushala"],
                    "Una": ["Una Rural", "Nawabandar", "Delvada", "Ahmedpur Mandvi", "Tad"],
                    "Gir Gadhada": ["Gir Gadhada Rural", "Dron", "Jardhar", "Harmadiya", "Jamwala"]
                }
            },
            "Jamnagar": {
                "region": "Saurashtra",
                "talukas": {
                    "Jamnagar": ["Jamnagar City", "Bedeshwar", "Sikka", "Motikhavdi", "Dared", "Aliabada"],
                    "Dhrol": ["Dhrol Rural", "Jaliya", "Bhadra", "Latipur", "Manekpar"],
                    "Jamjodhpur": ["Jamjodhpur Rural", "Gingani", "Shethvadala", "Vansjalia", "Parbadi"],
                    "Jodiya": ["Jodiya Port", "Balachadi", "Khadba", "Amran", "Kunad"],
                    "Kalavad": ["Kalavad Rural", "Khandhera", "Mota Vadala", "Ranuja", "Bhagat Khijadiya"],
                    "Lalpur": ["Lalpur Rural", "Padana", "Khavdi", "Kanalus", "Pipar"]
                }
            },
            "Junagadh": {
                "region": "Saurashtra",
                "talukas": {
                    "Junagadh City": ["Junagadh Town", "Girnar Foothills", "Majevadi", "Dolatpara", "Zanzarda"],
                    "Junagadh Rural": ["Choki", "Vadal", "Bilkha", "Makhiyala", "Ivnagar"],
                    "Bhesan": ["Bhesan Rural", "Chhapretha", "Ranpur", "Pasvala", "Mendpara"],
                    "Keshod": ["Keshod Rural", "Agatrai", "Mevasa", "Koyalana", "Sil"],
                    "Malia Hatina": ["Malia Rural", "Bhanduri", "Kukaswada", "Aambalval", "Gadu"],
                    "Manavadar": ["Manavadar Rural", "Bantwa", "Mitana", "Koyilana", "Sardargadh"],
                    "Mangrol": ["Mangrol Port", "Lathodra", "Sherbaug", "Khorasa", "Mekhdi"],
                    "Mendarda": ["Mendarda Rural", "Amrapur", "Barwala", "Nataliya", "Rajsar"],
                    "Vanthali": ["Vanthali Rural", "Shapur", "Kajleshwar", "Lushala", "Sendarda"],
                    "Visavadar": ["Visavadar Rural", "Kalsari", "Moti Monpari", "Dhari Road", "Prempara"]
                }
            },
            "Kheda": {
                "region": "Central Gujarat",
                "talukas": {
                    "Nadiad": ["Nadiad City", "Uttarsanda", "Piplag", "Salun", "Dabhan", "Gutal"],
                    "Kheda": ["Kheda Rural", "Rasikpura", "Vataman Road", "Pithai", "Samadra"],
                    "Kapadvanj": ["Kapadvanj Rural", "Torna", "Ladvel", "Kathana", "Antroli"],
                    "Kathlal": ["Kathlal Rural", "Abhvel", "Pithai", "Chhipial", "Ladol"],
                    "Mahudha": ["Mahudha Rural", "Alina", "Undra", "Chunel", "Finav"],
                    "Matar": ["Matar Rural", "Limbasi", "Shetranj", "Traj", "Sayla Road"],
                    "Mehmedabad": ["Mehmedabad Rural", "Siddhivinayak Temple", "Khatraj", "Raska", "Mankwa"],
                    "Thasra": ["Thasra Rural", "Dakor", "Sevaliya", "Menpura", "Vanoda"],
                    "Galteshwar": ["Galteshwar Temple", "Timba", "Sevaliya Road", "Ambav", "Rozva"],
                    "Vaso": ["Vaso Rural", "Palana", "Pij", "Mitel", "Kalsar"]
                }
            },
            "Kutch": {
                "region": "Kutch",
                "talukas": {
                    "Bhuj": ["Bhuj City", "Madhapar", "Mirzapar", "Kukma", "Khavda (Rann)", "Dordo"],
                    "Abdasa": ["Naliya", "Kothara", "Jakhau Port", "Vanku", "Bada"],
                    "Anjar": ["Anjar City", "Varshamedi", "Ratnal", "Dudhala", "Megalpur"],
                    "Bhachau": ["Bhachau Rural", "Samakhiali", "Chobari", "Adhoi", "Katariya"],
                    "Gandhidham": ["Gandhidham City", "Kandla Port", "Adipur", "Shinay", "Padana"],
                    "Lakhpat": ["Lakhpat Fort", "Dayapar", "Narayan Sarovar", "Koteshwar", "Ghaduli"],
                    "Mandvi": ["Mandvi Beach", "Koday", "Maska", "Layja", "Gadhsisa", "Bada"],
                    "Mundra": ["Mundra Port", "Baroi", "Zarpara", "Samagoga", "Dhrub"],
                    "Nakhatrana": ["Nakhatrana Rural", "Deshalpar", "Vithon", "Netra", "Ravapar"],
                    "Rapar": ["Rapar Rural", "Adesar", "Bhimasar", "Fatehgad", "Gedi"]
                }
            },
            "Mahisagar": {
                "region": "Central Gujarat",
                "talukas": {
                    "Lunawada": ["Lunawada Rural", "Kothamba", "Khanpur Road", "Madhwas", "Viraniya"],
                    "Balasinor": ["Balasinor Fossil Park", "Raiya", "Gadhvada", "Janod", "Pandva"],
                    "Kadana": ["Kadana Dam", "Dithwas", "Sarsan", "Rathda", "Kelamul"],
                    "Khanpur": ["Khanpur Rural", "Bakor", "Pandharwada", "Limbodra", "Mor"],
                    "Santrampur": ["Santrampur Rural", "Gothib", "Batavada", "Narsingpur", "Babra"],
                    "Virpur": ["Virpur (Mahisagar)", "Debhari", "Khatnal", "Saliya", "Vardhari"]
                }
            },
            "Mehsana": {
                "region": "North Gujarat",
                "talukas": {
                    "Mehsana": ["Mehsana City", "Naglapur", "Modhera Road", "Palavasna", "Panchot"],
                    "Becharaji": ["Becharaji Temple", "Sankhalpur", "Modhera Sun Temple", "Dedana", "Rantej"],
                    "Kadi": ["Kadi GIDC", "Nani Kadi", "Kundal", "Jhulasan", "Karannagar"],
                    "Kheralu": ["Kheralu Rural", "Chada", "Dhabha", "Malekpur", "Gorad"],
                    "Satlasana": ["Satlasana Rural", "Dharoi Dam", "Vav", "Kothasana", "Bhalusana"],
                    "Unjha": ["Unjha APMC (Jeera Hub)", "Upera", "Aithor", "Makhu", "Brahmanwada"],
                    "Vadnagar": ["Vadnagar Town", "Molipur", "Chhabaliya", "Sipor", "Kahoda"],
                    "Vijapur": ["Vijapur Rural", "Ladol", "Pilvai", "Kukrawada", "Sundarpur"],
                    "Visnagar": ["Visnagar Rural", "Kansa", "Tarabh", "Valam", "Kada"],
                    "Jotana": ["Jotana Rural", "Suraj", "Kasva", "Santhal", "Ganeshpura"]
                }
            },
            "Morbi": {
                "region": "Saurashtra",
                "talukas": {
                    "Morbi": ["Morbi City (Ceramic)", "Trajpar", "Mahendranagar", "Lakhdhirpur", "Pipali"],
                    "Halvad": ["Halvad Rural", "Sara", "Tikkar", "Mayurnagar", "Dharangadhra Road"],
                    "Maliya": ["Maliya Miyana", "Vavaniya", "Bhavpar", "Janjasar", "Bodki"],
                    "Tankara": ["Tankara Rural", "Dayanand Saraswati Ashram", "Lajai", "Neknam", "Kalyanpar"],
                    "Wankaner": ["Wankaner Royal Palace", "Sindhavadar", "Matel (Khodiyar)", "Garida", "Kotharia"]
                }
            },
            "Narmada": {
                "region": "South Gujarat",
                "talukas": {
                    "Rajpipla": ["Rajpipla Town", "Poicha Nilkanthdham", "Nandod", "Vavdi", "Bhinar"],
                    "Dediapada": ["Dediapada Rural", "Ninvat", "Mosda", "Gartal", "Dumkhal"],
                    "Garudeshwar": ["Statue of Unity (Kevadia)", "Garudeshwar Temple", "Gora", "Ekta Nagar", "Vaghadia"],
                    "Sagbara": ["Sagbara Rural", "Patvali", "Selamba", "Dhavlibhar", "Nana Suka"],
                    "Tilakwada": ["Tilakwada Rural", "Utavali", "Vengani", "Devlia", "Gametha"]
                }
            },
            "Navsari": {
                "region": "South Gujarat",
                "talukas": {
                    "Navsari": ["Navsari City", "Mahuva Road", "Kabilpore", "Jalalpore Road", "Chapra"],
                    "Chikhli": ["Chikhli Rural", "Alipore", "Samroli", "Majigam", "Vankal"],
                    "Gandevi": ["Gandevi Rural", "Amalsad (Chikoo)", "Bilimora Port", "Devsar", "Dhamdacha"],
                    "Jalalpore": ["Jalalpore Rural", "Dandi (Salt March Beach)", "Ubhrat Beach", "Maroil", "Vansi"],
                    "Khergam": ["Khergam Rural", "Panikhadak", "Bhairav", "Naranpore", "Vad"],
                    "Vansda": ["Vansda National Park", "Unai (Hot Springs)", "Kandolpada", "Vaghasi", "Kurelia"]
                }
            },
            "Panchmahal": {
                "region": "Central Gujarat",
                "talukas": {
                    "Godhra": ["Godhra City", "Vavdi", "Bhamaiya", "Tuwa Hot Springs", "Chhabanpur"],
                    "Ghoghamba": ["Ghoghamba Rural", "Rajgadh", "Goya Sundal", "Kantibhari", "Damavav"],
                    "Halol": ["Halol GIDC", "Pavagadh Foothills", "Champaner Heritage", "Tajpura", "Baska"],
                    "Jambughoda": ["Jambughoda Wildlife Sanctuary", "Narukot", "Kevdi", "Dunkra", "Vav"],
                    "Kalol": ["Kalol (Panchmahal)", "Derol Station", "Vejalpur", "Bakrol", "Pingli"],
                    "Morwa Hadaf": ["Morwa Rural", "Hadaf Dam", "Rasulpur", "Metral", "Sagwada"],
                    "Shehra": ["Shehra Rural", "Matariya", "Aniyad", "Morva Road", "Khairee"]
                }
            },
            "Patan": {
                "region": "North Gujarat",
                "talukas": {
                    "Patan": ["Patan City (Rani ki Vav)", "Balap", "Sander", "Dharpur", "Vagdod"],
                    "Chanasma": ["Chanasma Rural", "Dhinoj", "Rupawali", "Lanva", "Jhulasan"],
                    "Harij": ["Harij Rural", "Kukas", "Sankheshwar Road", "Tamboliya", "Katosan"],
                    "Radhanpur": ["Radhanpur Rural", "Santalpur Road", "Chhaniyana", "Memdapur", "Kamalpur"],
                    "Sami": ["Sami Rural", "Loliya", "Mota Joravarpura", "Varana", "Kukrana"],
                    "Sankheshwar": ["Sankheshwar Jain Tirth", "Panchasar", "Ranol", "Bhadresar", "Dhanora"],
                    "Santalpur": ["Santalpur Rural", "Charanka (Solar Park)", "Varahi", "Bakutra", "Piprala"],
                    "Saraswati": ["Saraswati Rural", "Vagdod", "Bhilvan", "Odha", "Koita"],
                    "Sidhpur": ["Sidhpur (Matru Gaya)", "Bindu Sarovar", "Kakoshi", "Metrana", "Nedra"]
                }
            },
            "Porbandar": {
                "region": "Saurashtra",
                "talukas": {
                    "Porbandar": ["Porbandar Town", "Chhaya", "Bokhira", "Rokadiya", "Degam", "Madhavpur (Ghed)"],
                    "Kutiyana": ["Kutiyana Rural", "Gokran", "Paswali", "Mahira", "Kotda"],
                    "Ranavav": ["Ranavav Rural", "Bileshwar", "Ashapura", "Adityana", "Barda Hills"]
                }
            },
            "Rajkot": {
                "region": "Saurashtra",
                "talukas": {
                    "Rajkot": ["Rajkot City", "Kuvadva GIDC", "Metoda GIDC", "Kasturbadham", "Bedipara", "Hadala"],
                    "Dhoraji": ["Dhoraji Rural", "Jamnavad", "Toraniya", "Fareni", "Zanzmer"],
                    "Gondal": ["Gondal Town", "Bhojpara", "Gomta", "Kolithad", "Bandhiya", "Moti Marad", "Dharwala"],
                    "Jamkandorna": ["Jamkandorna Rural", "Dholidhar", "Chitravad", "Boriya", "Roghad"],
                    "Jasdan": ["Jasdan Rural", "Atkot", "Kamlapur", "Ghela Somnath", "Bhadla"],
                    "Jetpur": ["Jetpur (Dyeing & Printing)", "Navagadh", "Dhebar", "Pithadiya", "Kagvad (Khodaldham)"],
                    "Kotda Sangani": ["Kotda Sangani Rural", "Solsumba", "Navagam", "Rajgadh", "Ramod"],
                    "Lodhika": ["Lodhika Rural", "Metoda Village", "Dholra", "Vajdi", "Und Khijadiya"],
                    "Paddhari": ["Paddhari Rural", "Targhadi", "Nyari Dam", "Khirsara", "Mota Khijadiya"],
                    "Upleta": ["Upleta Rural", "Bhayavadar", "Dumiyani", "Paneli Moti", "Kolki"],
                    "Vinchhiya": ["Vinchhiya Rural", "Sompipaliya", "Pipardi", "Ovanpur", "Kalasar"]
                }
            },
            "Sabarkantha": {
                "region": "North Gujarat",
                "talukas": {
                    "Himatnagar": ["Himatnagar City", "Mahavirnagar", "Gambhoi", "Hapa", "Berol"],
                    "Idar": ["Idar Fort (Idario Gadh)", "Kadiyadra", "Lalpur", "Badoli", "Sherpur"],
                    "Khedbrahma": ["Khedbrahma (Ambaji Chhatri)", "Radhiwad", "Galoada", "Dhingawada", "Kheroj"],
                    "Poshina": ["Poshina Rural", "Lambadiya", "Kotda", "Gota", "Gunbhakhari"],
                    "Prantij": ["Prantij Rural", "Salal", "Sonasan", "Pogalu", "Rasulpur"],
                    "Talod": ["Talod Rural", "Harsol", "Anior", "Ranasan", "Ujeshwar"],
                    "Vadali": ["Vadali Rural", "Hathoj", "Dholvani", "Khadat", "Bhadresar"],
                    "Vijaynagar": ["Polo Forest", "Vijaynagar Rural", "Chithoda", "Antarsuba", "Kherwara Road"]
                }
            },
            "Surat": {
                "region": "South Gujarat",
                "talukas": {
                    "Surat City": ["Adajan", "Vesu", "Katargam", "Varachha", "Dindoli", "Udhna", "Sachin"],
                    "Bardoli": ["Bardoli (Sardar Ashram)", "Sarbhon", "Baben", "Ten", "Madhi (Sugar Factory)"],
                    "Choryasi": ["Hazira Port", "Dumas Beach", "Ichhapore", "Mora", "Damka"],
                    "Kamrej": ["Kamrej Rural", "Kholvad", "Navagam", "Valak", "Antroli"],
                    "Mahuva": ["Mahuva (Surat)", "Anawal", "Karchelia", "Bhamaiya", "Nihali"],
                    "Mandvi": ["Mandvi (Surat)", "Areth", "Gadat", "Tadkeshwar", "Pipalwada"],
                    "Mangrol": ["Mangrol (Surat)", "Kosamba", "Kim GIDC", "Mosali", "Hathuran"],
                    "Olpad": ["Olpad Rural", "Sayan (Sugar Factory)", "Karanj", "Masma", "Saras"],
                    "Palsana": ["Palsana Rural", "Kadodara", "Bagumara", "Baleshwar", "Gangadhara"],
                    "Umarpada": ["Umarpada Rural", "Chavda", "Gardi", "Zarda", "Vadpada"]
                }
            },
            "Surendranagar": {
                "region": "Saurashtra",
                "talukas": {
                    "Wadhwan": ["Surendranagar City", "Wadhwan Fort", "Dudhrej", "Kherali", "Muli Road"],
                    "Chotila": ["Chotila Chamunda Hill", "Aanandpur", "Bamanbore", "Than Road", "Nava"],
                    "Chuda": ["Chuda Rural", "Bhadreshwar", "Morvad", "Karmad", "Bala"],
                    "Dasada": ["Patdi", "Dasada (Little Rann Wild Ass)", "Zinzuwada", "Adariyana", "Bajana"],
                    "Dhrangadhra": ["Dhrangadhra Rural", "Kuda (Salt Works)", "Soldi", "Rajsitapur", "Jasmatpur"],
                    "Lakhtar": ["Lakhtar Rural", "Talsana", "Dhanki", "Vana", "Bajarangpura"],
                    "Limbdi": ["Limbdi Rural", "Raska", "Panshina", "Ralol", "Bhoika"],
                    "Muli": ["Muli Rural", "Gautameshwar", "Sara", "Digsar", "Chanpa"],
                    "Sayla": ["Sayla Rural", "Dhandhalpur", "Sudamada", "Thoriyali", "Sejakpar"],
                    "Thangadh": ["Thangadh (Tarnetar Fair)", "Sarvali", "Jamwali", "Songadh", "Amrapur"]
                }
            },
            "Tapi": {
                "region": "South Gujarat",
                "talukas": {
                    "Vyara": ["Vyara Town", "Kapadbandh", "Magra", "Chunawadi", "Maypur"],
                    "Dolvan": ["Dolvan Rural", "Panchol", "Padamdungari", "Gadhvi", "Kakadva"],
                    "Kukarmunda": ["Kukarmunda Rural", "Narmada Par", "Sadarmat", "Mataji Faliya", "Chhotedhar"],
                    "Nizar": ["Nizar Rural", "Vanka", "Nandurbar Road", "Raygadh", "Kevdi"],
                    "Songadh": ["Songadh Fort", "Ukai Dam (Tapi)", "Doswada Dam", "Gunkhadi", "Singpur"],
                    "Ucchhal": ["Ucchhal Rural", "Navapur Road", "Vadpada", "Mogran", "Chhaktala"],
                    "Valod": ["Valod (Lijjat Papad Birthplace)", "Buhari", "Titwa", "Kalamkui", "Bedkuva"]
                }
            },
            "Vadodara": {
                "region": "Central Gujarat",
                "talukas": {
                    "Vadodara": ["Vadodara City", "Alkapuri", "Manjalpur", "Gotri", "Koyali (Refinery)", "Vaghodia Road"],
                    "Dabhoi": ["Dabhoi Heritage Gate", "Kayavarohan (Lakulesh)", "Ten Talav", "Chanod (Triveni Sangam)", "Karnali"],
                    "Desar": ["Desar Rural", "Vejpur", "Vankaner", "Limda", "Piparwada"],
                    "Karjan": ["Karjan Rural", "Miyagam Karjan", "Kandari", "Valan", "Sampa"],
                    "Padra": ["Padra Rural", "Muval", "Dabhasa", "Lakhigam", "Chokari"],
                    "Savli": ["Savli Rural", "Manjusar GIDC", "Tundav", "Lamdapura", "Moxi"],
                    "Shinor": ["Shinor Rural", "Malsar (Narmada Ghat)", "Anandi", "Sadhli", "Segva"],
                    "Waghodia": ["Waghodia Rural", "Parul University / Limda", "Jarod", "Goraj", "Ganeshpura"]
                }
            },
            "Valsad": {
                "region": "South Gujarat",
                "talukas": {
                    "Valsad": ["Valsad Town", "Tithal Beach (Swaminarayan)", "Atul Chemical Hub", "Dharampur Road", "Segvi"],
                    "Dharampur": ["Dharampur (Lady Wilson Museum)", "Barumal (Shiva Temple)", "Bilpudi Falls", "Karanjveri", "Pindval"],
                    "Kaprada": ["Kaprada (Dixit)", "Nana Pondha", "Mandva", "Sutharpada", "Ambabari"],
                    "Pardi": ["Pardi Rural", "Killa Pardi", "Udvada (Parsi Atash Behram)", "Dumlav", "Bhadeli"],
                    "Umbergaon": ["Umbergaon (Film City)", "Sanjan (Parsi Heritage)", "Maroli", "Bhilad", "Sarigam GIDC"],
                    "Vapi": ["Vapi Industrial Hub", "Chala", "Chanod GIDC", "Morai", "Salvav"]
                }
            }
        }

        districts_created = 0
        talukas_created = 0
        villages_created = 0

        for dist_name, dist_info in gujarat_data.items():
            district_obj, created = District.objects.get_or_create(
                name=dist_name,
                defaults={"region": dist_info.get("region", "Gujarat")}
            )
            if created:
                districts_created += 1

            for taluka_name, village_list in dist_info.get("talukas", {}).items():
                taluka_obj, t_created = Taluka.objects.get_or_create(
                    district=district_obj,
                    name=taluka_name
                )
                if t_created:
                    talukas_created += 1

                for v_name in village_list:
                    village_obj, v_created = Village.objects.get_or_create(
                        taluka=taluka_obj,
                        name=v_name
                    )
                    if v_created:
                        villages_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded Gujarat Location System:\n"
            f"  - Districts: {District.objects.count()} (New: {districts_created})\n"
            f"  - Talukas:   {Taluka.objects.count()} (New: {talukas_created})\n"
            f"  - Villages:  {Village.objects.count()} (New: {villages_created})"
        ))

        # Backfill existing FarmerProfiles and Crops with Foreign Key references where matching
        self.stdout.write(self.style.NOTICE("Backfilling existing Farmer Profiles and Crops references..."))
        for profile in FarmerProfile.objects.all():
            if profile.district and not profile.district_ref:
                matched_dist = District.objects.filter(name__iexact=profile.district.strip()).first()
                if matched_dist:
                    profile.district_ref = matched_dist
            if profile.taluka and not profile.taluka_ref:
                matched_taluka = Taluka.objects.filter(name__iexact=profile.taluka.strip(), district=profile.district_ref).first()
                if not matched_taluka:
                    matched_taluka = Taluka.objects.filter(name__iexact=profile.taluka.strip()).first()
                if matched_taluka:
                    profile.taluka_ref = matched_taluka
            profile.save()

        for crop in Crop.objects.all():
            farmer_profile = getattr(crop.farmer, 'farmer_profile', None)
            if farmer_profile:
                if not crop.district and farmer_profile.district:
                    crop.district = farmer_profile.district
                    crop.district_ref = farmer_profile.district_ref
                if not crop.taluka and farmer_profile.taluka:
                    crop.taluka = farmer_profile.taluka
                    crop.taluka_ref = farmer_profile.taluka_ref
                if not crop.village and farmer_profile.farm_location:
                    crop.village = farmer_profile.farm_location
                    crop.village_ref = farmer_profile.village_ref
                crop.save()

        self.stdout.write(self.style.SUCCESS("Gujarat Locations successfully seeded and existing records synchronized!"))
