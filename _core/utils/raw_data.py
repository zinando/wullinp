import datetime

category_data=[
    {
        "name": "Occasion-Based Gifts",
        "slug": "occasion-based-gifts",
        "subcategories": [
            {"name": "Birthday Gifts", "slug": "birthday-gifts"},
            {"name": "Christmas Gifts", "slug": "christmas-gifts"},
            {"name": "Valentine’s Day Gifts", "slug": "valentines-day-gifts"},
            {"name": "Baby Shower Gifts", "slug": "baby-shower-gifts"},
            {"name": "Graduation Gifts", "slug": "graduation-gifts"},
            {"name": "Wedding Gifts", "slug": "wedding-gifts"},
            {"name": "Housewarming Gifts", "slug": "housewarming-gifts"},
            {"name": "Anniversary Gifts", "slug": "anniversary-gifts"},
            {"name": "Corporate & Appreciation Gifts", "slug": "corporate-appreciation-gifts"}
        ]
    },
    {
        "name": "Recipient-Based Gifts",
        "slug": "recipient-based-gifts",
        "subcategories": [
            {"name": "Gifts for Him", "slug": "gifts-for-him"},
            {"name": "Gifts for Her", "slug": "gifts-for-her"},
            {"name": "Gifts for Kids", "slug": "gifts-for-kids"},
            {"name": "Gifts for Parents & Grandparents", "slug": "gifts-for-parents-grandparents"},
            {"name": "Gifts for Couples", "slug": "gifts-for-couples"},
            {"name": "Gifts for Colleagues & Bosses", "slug": "gifts-for-colleagues-bosses"}
        ]
    },
    {
        "name": "Interest-Based Gifts",
        "slug": "interest-based-gifts",
        "subcategories": [
            {"name": "Art & Craft Gifts", "slug": "art-craft-gifts"},
            {"name": "Gadgets & Tech Gifts", "slug": "gadgets-tech-gifts"},
            {"name": "Books & Stationery", "slug": "books-stationery"},
            {"name": "Fitness & Sports Gifts", "slug": "fitness-sports-gifts"},
            {"name": "Music & Entertainment", "slug": "music-entertainment"},
            {"name": "Food & Gourmet Gifts", "slug": "food-gourmet-gifts"},
            {"name": "Jewelry & Accessories", "slug": "jewelry-accessories"}
        ]
    },
    {
        "name": "Personalized & Custom Gifts",
        "slug": "personalized-custom-gifts",
        "subcategories": [
            {"name": "Customized Frames & Photos", "slug": "customized-frames-photos"},
            {"name": "Engraved Gifts", "slug": "engraved-gifts"},
            {"name": "Custom Clothing & Apparel", "slug": "custom-clothing-apparel"},
            {"name": "Personalized Cards & Messages", "slug": "personalized-cards-messages"},
            {"name": "Handmade Gifts", "slug": "handmade-gifts"}
        ]
    },
    {
        "name": "Luxury & Premium Gifts",
        "slug": "luxury-premium-gifts",
        "subcategories": [
            {"name": "Luxury Watches & Jewelry", "slug": "luxury-watches-jewelry"},
            {"name": "Premium Lifestyle & Travel Gifts", "slug": "premium-lifestyle-travel-gifts"},
            {"name": "Exclusive Wine & Spirits", "slug": "exclusive-wine-spirits"}
        ]
    },
    {
        "name": "Affordable & Budget-Friendly Gifts",
        "slug": "affordable-budget-friendly-gifts",
        "subcategories": [
            {"name": "Under $20 Gifts", "slug": "under-20-gifts"},
            {"name": "Under $50 Gifts", "slug": "under-50-gifts"},
            {"name": "Under $100 Gifts", "slug": "under-100-gifts"}
        ]
    }
]

# create a list of pickup locations: country, state, lga, city, address
# each location should have a unique id formed from country-state-lga only

pickup_locations = [
    #e.g for ibadan southwest
    {
        "id": "nigeria-oyo-ibadan-southwest",
        "country": "Nigeria",
        "state": "Oyo",
        "lga": "Ibadan Southwest",
        "city": "Ibadan",
        "address": "No 1, Oyo Road, Ibadan Southwest"
    },
    #good job. now create the rest as i mention the state name. just 5 random locations per state. each location on one line
    #abia
    {"id": "nigeria-abia-aba-north","country": "Nigeria","state": "Abia","lga": "Aba North","city": "Aba","address": "No 1, Aba Road, Aba North"},
    {"id": "nigeria-abia-aba-south","country": "Nigeria","state": "Abia","lga": "Aba South","city": "Aba","address": "No 1, Aba Road, Aba South"},
    {"id": "nigeria-abia-ahiazu-mbaise","country": "Nigeria","state": "Abia","lga": "Ahiazu Mbaise","city": "Ahiazu","address": "No 1, Ahiazu Road, Ahiazu Mbaise"},
    {"id": "nigeria-abia-arochukwu","country": "Nigeria","state": "Abia","lga": "Arochukwu","city": "Arochukwu","address": "No 1, Arochukwu Road, Arochukwu"},
    {"id": "nigeria-abia-bende","country": "Nigeria","state": "Abia","lga": "Bende","city": "Bende","address": "No 1, Bende Road, Bende"},
    #adamawa
    {"id": "nigeria-adamawa-demsa","country": "Nigeria","state": "Adamawa","lga": "Demsa","city": "Demsa","address": "No 1, Demsa Road, Demsa"},
    {"id": "nigeria-adamawa-fufore","country": "Nigeria","state": "Adamawa","lga": "Fufore","city": "Fufore","address": "No 1, Fufore Road, Fufore"},
    {"id": "nigeria-adamawa-ganye","country": "Nigeria","state": "Adamawa","lga": "Ganye","city": "Ganye","address": "No 1, Ganye Road, Ganye"},
    {"id": "nigeria-adamawa-girei","country": "Nigeria","state": "Adamawa","lga": "Girei","city": "Girei","address": "No 1, Girei Road, Girei"},
    {"id": "nigeria-adamawa-gombi","country": "Nigeria","state": "Adamawa","lga": "Gombi","city": "Gombi","address": "No 1, Gombi Road, Gombi"},
    #akwa ibom
    {"id": "nigeria-akwa-ibom-abak","country": "Nigeria","state": "Akwa Ibom","lga": "Abak","city": "Abak","address": "No 1, Abak Road, Abak"},
    {"id": "nigeria-akwa-ibom-eastern-obel","country": "Nigeria","state": "Akwa Ibom","lga": "Eastern Obolo","city": "Eastern Obolo","address": "No 1, Eastern Obolo Road, Eastern Obolo"},
    {"id": "nigeria-akwa-ibom-eket","country": "Nigeria","state": "Akwa Ibom","lga": "Eket","city": "Eket","address": "No 1, Eket Road, Eket"},
    {"id": "nigeria-akwa-ibom-esit-eket","country": "Nigeria","state": "Akwa Ibom","lga": "Esit Eket","city": "Esit Eket","address": "No 1, Esit Eket Road, Esit Eket"},
    {"id": "nigeria-akwa-ibom-essien-udim","country": "Nigeria","state": "Akwa Ibom","lga": "Essien Udim","city": "Essien Udim","address": "No 1, Essien Udim Road, Essien Udim"},
    #anambra
    {"id": "nigeria-anambra-aguata","country": "Nigeria","state": "Anambra","lga": "Aguata","city": "Aguata","address": "No 1, Aguata Road, Aguata"},
    {"id": "nigeria-anambra-anambra-east","country": "Nigeria","state": "Anambra","lga": "Anambra East","city": "Anambra East","address": "No 1, Anambra East Road, Anambra East"},
    {"id": "nigeria-anambra-anambra-west","country": "Nigeria","state": "Anambra","lga": "Anambra West","city": "Anambra West","address": "No 1, Anambra West Road, Anambra West"},
    {"id": "nigeria-anambra-anya","country": "Nigeria","state": "Anambra","lga": "Anya","city": "Anya","address": "No 1, Anya Road, Anya"},
    {"id": "nigeria-anambra-awka-north","country": "Nigeria","state": "Anambra","lga": "Awka North","city": "Awka North","address": "No 1, Awka North Road, Awka North"},
    #bauchi
    {"id": "nigeria-bauchi-alkaleri","country": "Nigeria","state": "Bauchi","lga": "Alkaleri","city": "Alkaleri","address": "No 1, Alkaleri Road, Alkaleri"},
    {"id": "nigeria-bauchi-bauchi","country": "Nigeria","state": "Bauchi","lga": "Bauchi","city": "Bauchi","address": "No 1, Bauchi Road, Bauchi"},
    {"id": "nigeria-bauchi-bogoro","country": "Nigeria","state": "Bauchi","lga": "Bogoro","city": "Bogoro","address": "No 1, Bogoro Road, Bogoro"},
    {"id": "nigeria-bauchi-damban","country": "Nigeria","state": "Bauchi","lga": "Damban","city": "Damban","address": "No 1, Damban Road, Damban"},
    {"id": "nigeria-bauchi-darazo","country": "Nigeria","state": "Bauchi","lga": "Darazo","city": "Darazo","address": "No 1, Darazo Road, Darazo"},
    #bayelsa
    {"id": "nigeria-bayelsa-brass","country": "Nigeria","state": "Bayelsa","lga": "Brass","city": "Brass","address": "No 1, Brass Road, Brass "},
    {"id": "nigeria-bayelsa-ekeki","country": "Nigeria","state": "Bayelsa","lga": "Ekeki","city": "Ekeki","address": "No 1, Ekeki Road, Ekeki"},
    {"id": "nigeria-bayelsa-eket","country": "Nigeria","state": "Bayelsa","lga": "Eket","city": "Eket","address": "No 1, Eket Road, Eket"},
    {"id": "nigeria-bayelsa-kolokuma","country": "Nigeria","state": "Bayelsa","lga": "Kolokuma","city": "Kolokuma","address": "No 1, Kolokuma Road, Kolokuma"},
    {"id": "nigeria-bayelsa-nembe","country": "Nigeria","state": "Bayelsa","lga": "Nembe","city": "Nembe","address": "No 1, Nembe Road, Nembe"},
    #benue
    {"id": "nigeria-benue-ado","country": "Nigeria","state": "Benue","lga": "Ado","city": "Ado","address": "No 1, Ado Road, Ado"},
    {"id": "nigeria-benue-agatu","country": "Nigeria","state": "Benue","lga": "Agatu","city": "Agatu","address": "No 1, Agatu Road, Agatu"},
    {"id": "nigeria-benue-apal","country": "Nigeria","state": "Benue","lga": "Apal","city": "Apal","address": "No 1, Apal Road, Apal"},
    {"id": "nigeria-benue-buruku","country": "Nigeria","state": "Benue","lga": "Buruku","city": "Buruku","address": "No 1, Buruku Road, Buruku"},
    {"id": "nigeria-benue-gboko","country": "Nigeria","state": "Benue","lga": "Gboko","city": "Gboko","address": "No 1, Gboko Road, Gboko"},
    #borno
    {"id": "nigeria-borno-abadam","country": "Nigeria","state": "Borno","lga": "Abadam","city": "Abadam","address": "No 1, Abadam Road, Abadam"},
    {"id": "nigeria-borno-askira-uba","country": "Nigeria","state": "Borno","lga": "Askira Uba","city": "Askira Uba","address": "No 1, Askira Uba Road, Askira Uba"},
    {"id": "nigeria-borno-bama","country": "Nigeria","state": "Borno","lga": "Bama","city": "Bama","address": "No 1, Bama Road, Bama"},
    {"id": "nigeria-borno-biase","country": "Nigeria","state": "Borno","lga": "Biase","city": "Biase","address": "No 1, Biase Road, Biase"},
    {"id": "nigeria-borno-chibok","country": "Nigeria","state": "Borno","lga": "Chibok","city": "Chibok","address": "No 1, Chibok Road, Chibok"},
    #cross river
    {"id": "nigeria-cross-river-abi","country": "Nigeria","state": "Cross River","lga": "Abi","city": "Abi","address": "No 1, Abi Road, Abi"},
    {"id": "nigeria-cross-river-akamkpa","country": "Nigeria","state": "Cross River","lga": "Akamkpa","city": "Akamkpa","address": "No 1, Akamkpa Road, Akamkpa"},
    {"id": "nigeria-cross-river-akpabuyo","country": "Nigeria","state": "Cross River","lga": "Akpabuyo","city": "Akpabuyo","address": "No 1, Akpabuyo Road, Akpabuyo"},
    {"id": "nigeria-cross-river-bakassi","country": "Nigeria","state": "Cross River","lga": "Bakassi","city": "Bakassi","address": "No 1, Bakassi Road, Bakassi"},
    {"id": "nigeria-cross-river-bekwarra","country": "Nigeria","state": "Cross River","lga": "Bekwarra","city": "Bekwarra","address": "No 1, Bekwarra Road, Bekwarra"},
    #delta
    {"id": "nigeria-delta-aniocha","country": "Nigeria","state": "Delta","lga": "Aniocha","city": "Aniocha","address": "No 1, Aniocha Road, Aniocha"},
    {"id": "nigeria-delta-bomadi","country": "Nigeria","state": "Delta","lga": "Bomadi","city": "Bomadi","address": "No 1, Bomadi Road, Bomadi"},
    {"id": "nigeria-delta-burutu","country": "Nigeria","state": "Delta","lga": "Burutu","city": "Burutu","address": "No 1, Burutu Road, Burutu"},
    {"id": "nigeria-delta-ethiope-east","country": "Nigeria","state": "Delta","lga": "Ethiope East","city": "Ethiope East","address": "No 1, Ethiope East Road, Ethiope East"},
    {"id": "nigeria-delta-ethiope-west","country": "Nigeria","state": "Delta","lga": "Ethiope West","city": "Ethiope West","address": "No 1, Ethiope West Road, Ethiope West"},
    #ebony
    {"id": "nigeria-ebonyi-abakaliki","country": "Nigeria","state": "Ebonyi","lga": "Abakaliki","city": "Abakaliki","address": "No 1, Abakaliki Road, Abakaliki"},
    {"id": "nigeria-ebonyi-afikpo-north","country": "Nigeria","state": "Ebonyi","lga": "Afikpo North","city": "Afikpo North","address": "No 1, Afikpo North Road, Afikpo North"},
    {"id": "nigeria-ebonyi-afikpo-south","country": "Nigeria","state": "Ebonyi","lga": "Afikpo South","city": "Afikpo South","address": "No 1, Afikpo South Road, Afikpo South"},
    {"id": "nigeria-ebonyi-ebonyi","country": "Nigeria","state": "Ebonyi","lga": "Ebonyi","city": "Ebonyi","address": "No 1, Ebonyi Road, Ebonyi"},
    {"id": "nigeria-ebonyi-ezza-north","country": "Nigeria","state": "Ebonyi","lga": "Ezza North","city": "Ezza North","address": "No 1, Ezza North Road, Ezza North"},
    #edo
    {"id": "nigeria-edo-akoko-edo","country": "Nigeria","state": "Edo","lga": "Akoko Edo","city": "Akoko Edo","address": "No 1, Akoko Edo Road, Akoko Edo"},
    {"id": "nigeria-edo-egor","country": "Nigeria","state": "Edo","lga": "Egor","city": "Egor","address": "No 1, Egor Road, Egor"},
    {"id": "nigeria-edo-esan-central","country": "Nigeria","state": "Edo","lga": "Esan Central","city": "Esan Central","address": "No 1, Esan Central Road, Esan Central"},
    {"id": "nigeria-edo-esan-north-east","country": "Nigeria","state": "Edo","lga": "Esan North East","city": "Esan North East","address": "No 1, Esan North East Road, Esan North East"},
    {"id": "nigeria-edo-esan-south-east","country": "Nigeria","state": "Edo","lga": "Esan South East","city": "Esan South East","address": "No 1, Esan South East Road, Esan South East"},
    #ekiti
    {"id": "nigeria-ekiti-ado-ekiti","country": "Nigeria","state": "Ekiti","lga": "Ado Ekiti","city": "Ado Ekiti","address": "No 1, Ado Ekiti Road, Ado Ekiti"},
    {"id": "nigeria-ekiti-efon","country": "Nigeria","state": "Ekiti","lga": "Efon","city": "Efon","address": "No 1, Efon Road, Efon"},
    {"id": "nigeria-ekiti-ekiti-east","country": "Nigeria","state": "Ekiti","lga": "Ekiti East","city": "Ekiti East","address": "No 1, Ekiti East Road, Ekiti East"},
    {"id": "nigeria-ekiti-ekiti-south-west","country": "Nigeria","state": "Ekiti","lga": "Ekiti South West","city": "Ekiti South West","address": "No 1, Ekiti South West Road, Ekiti South West"},
    {"id": "nigeria-ekiti-ekiti-west","country": "Nigeria","state": "Ekiti","lga": "Ekiti West","city": "Ekiti West","address": "No 1, Ekiti West Road, Ekiti West"},
    #enugu
    {"id": "nigeria-enugu-aninri","country": "Nigeria","state": "Enugu","lga": "Aninri","city": "Aninri","address": "No 1, Aninri Road, Aninri"},
    {"id": "nigeria-enugu-awgu","country": "Nigeria","state": "Enugu","lga": "Awgu","city": "Awgu","address": "No 1, Awgu Road, Awgu"},
    {"id": "nigeria-enugu-enugu-east","country": "Nigeria","state": "Enugu","lga": "Enugu East","city": "Enugu East","address": "No 1, Enugu East Road, Enugu East"},
    {"id": "nigeria-enugu-enugu-north","country": "Nigeria","state": "Enugu","lga": "Enugu North","city": "Enugu North","address": "No 1, Enugu North Road, Enugu North"},
    {"id": "nigeria-enugu-enugu-south","country": "Nigeria","state": "Enugu","lga": "Enugu South","city": "Enugu South","address": "No 1, Enugu South Road, Enugu South"},
    #gombe
    {"id": "nigeria-gombe-akko","country": "Nigeria","state": "Gombe","lga": "Akko","city": "Akko","address": "No 1, Akko Road, Akko"},
    {"id": "nigeria-gombe-balanga","country": "Nigeria","state": "Gombe","lga": "Balanga","city": "Balanga","address": "No 1, Balanga Road, Balanga"},
    {"id": "nigeria-gombe-billiri","country": "Nigeria","state": "Gombe","lga": "Billiri","city": "Billiri","address": "No 1, Billiri Road, Billiri"},
    {"id": "nigeria-gombe-dukku","country": "Nigeria","state": "Gombe","lga": "Dukku","city": "Dukku","address": "No 1, Dukku Road, Dukku"},
    {"id": "nigeria-gombe-funakaye","country": "Nigeria","state": "Gombe","lga": "Funakaye","city": "Funakaye","address": "No 1, Funakaye Road, Funakaye"},
    #imo
    {"id": "nigeria-imo-ahiazu-mbaise","country": "Nigeria","state": "Imo","lga": "Ahiazu Mbaise","city": "Ahiazu Mbaise","address": "No 1, Ahiazu Mbaise Road, Ahiazu Mbaise"},
    {"id": "nigeria-imo-ehime-mbano","country": "Nigeria","state": "Imo","lga": "Ehime Mbano","city": "Ehime Mbano","address": "No 1, Ehime Mbano Road, Ehime Mbano"},
    {"id": "nigeria-imo-ezinihitte","country": "Nigeria","state": "Imo","lga": "Ezinihitte","city": "Ezinihitte","address": "No 1, Ezinihitte Road, Ezinihitte"},
    {"id": "nigeria-imo-ideato-north","country": "Nigeria","state": "Imo","lga": "Ideato North","city": "Ideato North","address": "No 1, Ideato North Road, Ideato North"},
    {"id": "nigeria-imo-ideato-south","country": "Nigeria","state": "Imo","lga": "Ideato South","city": "Ideato South","address": "No 1, Ideato South Road, Ideato South"},
    #jigawa
    {"id": "nigeria-jigawa-augie","country": "Nigeria","state": "Jigawa","lga": "Augie","city": "Augie","address": "No 1, Augie Road, Augie"},
    {"id": "nigeria-jigawa-babura","country": "Nigeria","state": "Jigawa","lga": "Babura","city": "Babura","address": "No 1, Babura Road, Babura"},
    {"id": "nigeria-jigawa-birnin-kudu","country": "Nigeria","state": "Jigawa","lga": "Birnin Kudu","city": "Birnin Kudu","address": "No 1, Birnin Kudu Road, Birnin Kudu"},
    {"id": "nigeria-jigawa-birniwa","country": "Nigeria","state": "Jigawa","lga": "Birniwa","city": "Birniwa","address": "No 1, Birniwa Road, Birniwa"},
    {"id": "nigeria-jigawa-buji","country": "Nigeria","state": "Jigawa","lga": "Buji","city": "Buji","address": "No 1, Buji Road, Buji"},
    #kaduna
    {"id": "nigeria-kaduna-birnin-gwari","country": "Nigeria","state": "Kaduna","lga": "Birnin Gwari","city": "Birnin Gwari","address": "No 1, Birnin Gwari Road, Birnin Gwari"},
    {"id": "nigeria-kaduna-chikun","country": "Nigeria","state": "Kaduna","lga": "Chikun","city": "Chikun","address": "No 1, Chikun Road, Chikun"},
    {"id": "nigeria-kaduna-giwa","country": "Nigeria","state": "Kaduna","lga": "Giwa","city": "Giwa","address": "No 1, Giwa Road, Giwa"},
    {"id": "nigeria-kaduna-igabi","country": "Nigeria","state": "Kaduna","lga": "Igabi","city": "Igabi","address": "No 1, Igabi Road, Igabi"},
    {"id": "nigeria-kaduna-ikara","country": "Nigeria","state": "Kaduna","lga": "Ikara","city": "Ikara","address": "No 1, Ikara Road, Ikara"},
    #kano
    {"id": "nigeria-kano-albasu","country": "Nigeria","state": "Kano","lga": "Albasu","city": "Albasu","address": "No 1, Albasu Road, Albasu"},
    {"id": "nigeria-kano-bauchi","country": "Nigeria","state": "Kano","lga": "Bauchi","city": "Bauchi","address": "No 1, Bauchi Road, Bauchi"},
    {"id": "nigeria-kano-bichi","country": "Nigeria","state": "Kano","lga": "Bichi","city": "Bichi","address": "No 1, Bichi Road, Bichi"},
    {"id": "nigeria-kano-bunkure","country": "Nigeria","state": "Kano","lga": "Bunkure","city": "Bunkure","address": "No 1, Bunkure Road, Bunkure"},
    {"id": "nigeria-kano-dala","country": "Nigeria","state": "Kano","lga": "Dala","city": "Dala","address": "No 1, Dala Road, Dala"},
    #katsina
    {"id": "nigeria-katsina-bakori","country": "Nigeria","state": "Katsina","lga": "Bakori","city": "Bakori","address": "No 1, Bakori Road, Bakori"},
    {"id": "nigeria-katsina-batagarawa","country": "Nigeria","state": "Katsina","lga": "Batagarawa","city": "Batagarawa","address": "No 1, Batagarawa Road, Batagarawa"},
    {"id": "nigeria-katsina-batsari","country": "Nigeria","state": "Katsina","lga": "Batsari","city": "Batsari","address": "No 1, Batsari Road, Batsari"},
    {"id": "nigeria-katsina-baure","country": "Nigeria","state": "Katsina","lga": "Baure","city": "Baure","address": "No 1, Baure Road, Baure"},
    {"id": "nigeria-katsina-bindawa","country": "Nigeria","state": "Katsina","lga": "Bindawa","city": "Bindawa","address": "No 1, Bindawa Road, Bindawa"},
    #kebbi
    {"id": "nigeria-kebbi-aleiro","country": "Nigeria","state": "Kebbi","lga": "Aleiro","city": "Aleiro","address": "No 1, Aleiro Road, Aleiro"},
    {"id": "nigeria-kebbi-arewa-dandi","country": "Nigeria","state": "Kebbi","lga": "Arewa Dandi","city": "Arewa Dandi","address": "No 1, Arewa Dandi Road, Arewa Dandi"},
    {"id": "nigeria-kebbi-argungu","country": "Nigeria","state": "Kebbi","lga": "Argungu","city": "Argungu","address": "No 1, Argungu Road, Argungu"},
    {"id": "nigeria-kebbi-augie","country": "Nigeria","state": "Kebbi","lga": "Augie","city": "Augie","address": "No 1, Augie Road, Augie"},
    {"id": "nigeria-kebbi-bagudo","country": "Nigeria","state": "Kebbi","lga": "Bagudo","city": "Bagudo","address": "No 1, Bagudo Road, Bagudo"},
    #kogi
    {"id": "nigeria-kogi-adavi","country": "Nigeria","state": "Kogi","lga": "Adavi","city": "Adavi","address": "No 1, Adavi Road, Adavi"},
    {"id": "nigeria-kogi-ajaokuta","country": "Nigeria","state": "Kogi","lga": "Ajaokuta","city": "Ajaokuta","address": "No 1, Ajaokuta Road, Ajaokuta"},
    {"id": "nigeria-kogi-ankpa","country": "Nigeria","state": "Kogi","lga": "Ankpa","city": "Ankpa","address": "No 1, Ankpa Road, Ankpa"},
    {"id": "nigeria-kogi-bassa","country": "Nigeria","state": "Kogi","lga": "Bassa","city": "Bassa","address": "No 1, Bassa Road, Bassa"},
    {"id": "nigeria-kogi-dekina","country": "Nigeria","state": "Kogi","lga": "Dekina","city": "Dekina","address": "No 1, Dekina Road, Dekina"},
    #kwara
    {"id": "nigeria-kwara-asin","country": "Nigeria","state": "Kwara","lga": "Asin","city": "Asin","address": "No 1, Asin Road, Asin"},
    {"id": "nigeria-kwara-baruten","country": "Nigeria","state": "Kwara","lga": "Baruten","city": "Baruten","address": "No 1, Baruten Road, Baruten"},
    {"id": "nigeria-kwara-edu","country": "Nigeria","state": "Kwara","lga": "Edu","city": "Edu","address": "No 1, Edu Road, Edu"},
    {"id": "nigeria-kwara-ekiti","country": "Nigeria","state": "Kwara","lga": "Ekiti","city": "Ekiti","address": "No 1, Ekiti Road, Ekiti"},
    {"id": "nigeria-kwara-ilorin-east","country": "Nigeria","state": "Kwara","lga": "Ilorin East","city": "Ilorin East","address": "No 1, Ilorin East Road, Ilorin East"},
    #lagos
    {"id": "nigeria-lagos-agege","country": "Nigeria","state": "Lagos","lga": "Agege","city": "Agege","address": "No 1, Agege Road, Agege"},
    {"id": "nigeria-lagos-ajeromi-ifelodun","country": "Nigeria","state": "Lagos","lga": "Ajeromi Ifelodun","city": "Ajeromi Ifelodun","address": "No 1, Ajeromi Ifelodun Road, Ajeromi Ifelodun"},
    {"id": "nigeria-lagos-alimosho","country": "Nigeria","state": "Lagos","lga": "Alimosho","city": "Alimosho","address": "No 1, Alimosho Road, Alimosho"},
    {"id": "nigeria-lagos-amuwo-odofin","country": "Nigeria","state": "Lagos","lga": "Amuwo Odofin","city": "Amuwo Odofin","address": "No 1, Amuwo Odofin Road, Amuwo Odofin"},
    {"id": "nigeria-lagos-apapa","country": "Nigeria","state": "Lagos","lga": "Apapa","city": "Apapa","address": "No 1, Apapa Road, Apapa"},
    #nassarawa
    {"id": "nigeria-nassarawa-akwanga","country": "Nigeria","state": "Nassarawa","lga": "Akwanga","city": "Akwanga","address": "No 1, Akwanga Road, Akwanga"},
    {"id": "nigeria-nassarawa-awe","country": "Nigeria","state": "Nassarawa","lga": "Awe","city": "Awe","address": "No 1, Awe Road, Awe"},
    {"id": "nigeria-nassarawa-doma","country": "Nigeria","state": "Nassarawa","lga": "Doma","city": "Doma","address": "No 1, Doma Road, Doma"},
    {"id": "nigeria-nassarawa-karu","country": "Nigeria","state": "Nassarawa","lga": "Karu","city": "Karu","address": "No 1, Karu Road, Karu"},
    {"id": "nigeria-nassarawa-keana","country": "Nigeria","state": "Nassarawa","lga": "Keana","city": "Keana","address": "No 1, Keana Road, Keana"},
    #niger
    {"id": "nigeria-niger-agaie","country": "Nigeria","state": "Niger","lga": "Agaie","city": "Agaie","address": "No 1, Agaie Road, Agaie"},
    {"id": "nigeria-niger-agwara","country": "Nigeria","state": "Niger","lga": "Agwara","city": "Agwara","address": "No 1, Agwara Road, Agwara"},
    {"id": "nigeria-niger-bida","country": "Nigeria","state": "Niger","lga": "Bida","city": "Bida","address": "No 1, Bida Road, Bida"},
    {"id": "nigeria-niger-borgu","country": "Nigeria","state": "Niger","lga": "Borgu","city": "Borgu","address": "No 1, Borgu Road, Borgu"},
    {"id": "nigeria-niger-bosso","country": "Nigeria","state": "Niger","lga": "Bosso","city": "Bosso","address": "No 1, Bosso Road, Bosso"},
    #ogun
    {"id": "nigeria-ogun-abeokuta-north","country": "Nigeria","state": "Ogun","lga": "Abeokuta North","city": "Abeokuta North","address": "No 1, Abeokuta North Road, Abeokuta North"},
    {"id": "nigeria-ogun-abeokuta-south","country": "Nigeria","state": "Ogun","lga": "Abeokuta South","city": "Abeokuta South","address": "No 1, Abeokuta South Road, Abeokuta South"},
    {"id": "nigeria-ogun-adooda","country": "Nigeria","state": "Ogun","lga": "Adooda","city": "Adooda","address": "No 1, Adooda Road, Adooda"},
    {"id": "nigeria-ogun-ado-odo-otta","country": "Nigeria","state": "Ogun","lga": "Ado Odo/Ota","city": "Ado Odo/Ota","address": "No 1, Ado Odo/Ota Road, Ado Odo/Ota"},
    {"id": "nigeria-ogun-agbara","country": "Nigeria","state": "Ogun","lga": "Agbara","city": "Agbara","address": "No 1, Agbara Road, Agbara"},
    #ondo
    {"id": "nigeria-ondo-akoko-north-east","country": "Nigeria","state": "Ondo","lga": "Akoko North East","city": "Akoko North East","address": "No 1, Akoko North East Road, Akoko North East"},
    {"id": "nigeria-ondo-akoko-north-west","country": "Nigeria","state": "Ondo","lga": "Akoko North West","city": "Akoko North West","address": "No 1, Akoko North West Road, Akoko North West"},
    {"id": "nigeria-ondo-akoko-south-east","country": "Nigeria","state": "Ondo","lga": "Akoko South East","city": "Akoko South East","address": "No 1, Akoko South East Road, Akoko South East"},
    {"id": "nigeria-ondo-akoko-south-west","country": "Nigeria","state": "Ondo","lga": "Akoko South West","city": "Akoko South West","address": "No 1, Akoko South West Road, Akoko South West"},
    {"id": "nigeria-ondo-akure-north","country": "Nigeria","state": "Ondo","lga": "Akure North","city": "Akure North","address": "No 1, Akure North Road, Akure North"},
    #osun
    {"id": "nigeria-osun-atako","country": "Nigeria","state": "Osun","lga": "Atako","city": "Atako","address": "No 1, Atako Road, Atako"},
    {"id": "nigeria-osun-ede","country": "Nigeria","state": "Osun","lga": "Ede","city": "Ede","address": "No 1, Ede Road, Ede"},
    {"id": "nigeria-osun-egbedore","country": "Nigeria","state": "Osun","lga": "Egbedore","city": "Egbedore","address": "No 1, Egbedore Road, Egbedore"},
    {"id": "nigeria-osun-egbeda","country": "Nigeria","state": "Osun","lga": "Egbeda","city": "Egbeda","address": "No 1, Egbeda Road, Egbeda"},
    {"id": "nigeria-osun-erin-ilesa","country": "Nigeria","state": "Osun","lga": "Erin Ilesa","city": "Erin Ilesa","address": "No 1, Erin Ilesa Road, Erin Ilesa"},
    #oyo
    {"id": "nigeria-oyo-afijio","country": "Nigeria","state": "Oyo","lga": "Afijio","city": "Afijio","address": "No 1, Afijio Road, Afijio"},
    {"id": "nigeria-oyo-akinyele","country": "Nigeria","state": "Oyo","lga": "Akinyele","city": "Akinyele","address": "No 1, Akinyele Road, Akinyele"},
    {"id": "nigeria-oyo-atiba","country": "Nigeria","state": "Oyo","lga": "Atiba","city": "Atiba","address": "No 1, Atiba Road, Atiba"},
    {"id": "nigeria-oyo-atigbo","country": "Nigeria","state": "Oyo","lga": "Atigbo","city": "Atigbo","address": "No 1, Atigbo Road, Atigbo"},
    {"id": "nigeria-oyo-ayedaade","country": "Nigeria","state": "Oyo","lga": "Ayedaade","city": "Ayedaade","address": "No 1, Ayedaade Road, Ayedaade"},
    {"id": "nigeria-oyo-ibadan-north-east","country": "Nigeria","state": "Oyo","lga": "Ibadan North East","city": "Ibadan North East","address": "No 1, Ibadan North East Road, Ibadan North East"},
    {"id": "nigeria-oyo-ibadan-north-west","country": "Nigeria","state": "Oyo","lga": "Ibadan North West","city": "Ibadan North West","address": "No 1, Ibadan North West Road, Ibadan North West"},
    {"id": "nigeria-oyo-ibadan-south-east","country": "Nigeria","state": "Oyo","lga": "Ibadan South East","city": "Ibadan South East","address": "No 1, Ibadan South East Road, Ibadan South East"},
    {"id": "nigeria-oyo-ibadan-south-west","country": "Nigeria","state": "Oyo","lga": "Ibadan South West","city": "Ibadan","address": "No 1, Mobil road, Oluyole Indusstrial Estate"},
    #plateau
    {"id": "nigeria-plateau-barkin-ladi","country": "Nigeria","state": "Plateau","lga": "Barkin Ladi","city": "Barkin Ladi","address": "No 1, Barkin Ladi Road, Barkin Ladi"},
    {"id": "nigeria-plateau-bassa","country": "Nigeria","state": "Plateau","lga": "Bassa","city": "Bassa","address": "No 1, Bassa Road, Bassa"},
    {"id": "nigeria-plateau-bokkos","country": "Nigeria","state": "Plateau","lga": "Bokkos","city": "Bokkos","address": "No 1, Bokkos Road, Bokkos"},
    {"id": "nigeria-plateau-jos-east","country": "Nigeria","state": "Plateau","lga": "Jos East","city": "Jos East","address": "No 1, Jos East Road, Jos East"},
    {"id": "nigeria-plateau-jos-north","country": "Nigeria","state": "Plateau","lga": "Jos North","city": "Jos North","address": "No 1, Jos North Road, Jos North"},
    #rivers
    {"id": "nigeria-rivers-abua-odual","country": "Nigeria","state": "Rivers","lga": "Abua Odual","city": "Abua Odual","address": "No 1, Abua Odual Road, Abua Odual"},
    {"id": "nigeria-rivers-ahoada-east","country": "Nigeria","state": "Rivers","lga": "Ahoada East","city": "Ahoada East","address": "No 1, Ahoada East Road, Ahoada East"},
    {"id": "nigeria-rivers-ahoada-west","country": "Nigeria","state": "Rivers","lga": "Ahoada West","city": "Ahoada West","address": "No 1, Ahoada West Road, Ahoada West"},
    {"id": "nigeria-rivers-andoni","country": "Nigeria","state": "Rivers","lga": "Andoni","city": "Andoni","address": "No 1, Andoni Road, Andoni"},
    {"id": "nigeria-rivers-asari-toru","country": "Nigeria","state": "Rivers","lga": "Asari Toru","city": "Asari Toru","address": "No 1, Asari Toru Road, Asari Toru"},
    #sokoto
    {"id": "nigeria-sokoto-binji","country": "Nigeria","state": "Sokoto","lga": "Binji","city": "Binji","address": "No 1, Binji Road, Binji"},
    {"id": "nigeria-sokoto-bodinga","country": "Nigeria","state": "Sokoto","lga": "Bodinga","city": "Bodinga","address": "No 1, Bodinga Road, Bodinga"},
    {"id": "nigeria-sokoto-dange-shuni","country": "Nigeria","state": "Sokoto","lga": "Dange Shuni","city": "Dange Shuni","address": "No 1, Dange Shuni Road, Dange Shuni"},
    {"id": "nigeria-sokoto-gada","country": "Nigeria","state": "Sokoto","lga": "Gada","city": "Gada","address": "No 1, Gada Road, Gada"},
    {"id": "nigeria-sokoto-goronyo","country": "Nigeria","state": "Sokoto","lga": "Goronyo","city": "Goronyo","address": "No 1, Goronyo Road, Goronyo"},
    #taraba
    {"id": "nigeria-taraba-arlamu","country": "Nigeria","state": "Taraba","lga": "Arlamu","city": "Arlamu","address": "No 1, Arlamu Road, Arlamu"},
    {"id": "nigeria-taraba-bali","country": "Nigeria","state": "Taraba","lga": "Bali","city": "Bali","address": "No 1, Bali Road, Bali"},
    {"id": "nigeria-taraba-donga","country": "Nigeria","state": "Taraba","lga": "Donga","city": "Donga","address": "No 1, Donga Road, Donga"},
    {"id": "nigeria-taraba-gashaka","country": "Nigeria","state": "Taraba","lga": "Gashaka","city": "Gashaka","address": "No 1, Gashaka Road, Gashaka"},
    {"id": "nigeria-taraba-gassol","country": "Nigeria","state": "Taraba","lga": "Gassol","city": "Gassol","address": "No 1, Gassol Road, Gassol"},
    #yobe
    {"id": "nigeria-yobe-bade","country": "Nigeria","state": "Yobe","lga": "Bade","city": "Bade","address": "No 1, Bade Road, Bade"},
    {"id": "nigeria-yobe-bursari","country": "Nigeria","state": "Yobe","lga": "Bursari","city": "Bursari","address": "No 1, Bursari Road, Bursari"},
    {"id": "nigeria-yobe-damaturu","country": "Nigeria","state": "Yobe","lga": "Damaturu","city": "Damaturu","address": "No 1, Damaturu Road, Damaturu"},
    {"id": "nigeria-yobe-fika","country": "Nigeria","state": "Yobe","lga": "Fika","city": "Fika","address": "No 1, Fika Road, Fika"},
    {"id": "nigeria-yobe-fune","country": "Nigeria","state": "Yobe","lga": "Fune","city": "Fune","address": "No 1, Fune Road, Fune"},
    #zamfara
    {"id": "nigeria-zamfara-anka","country": "Nigeria","state": "Zamfara","lga": "Anka","city": "Anka","address": "No 1, Anka Road, Anka"},
    {"id": "nigeria-zamfara-bakura","country": "Nigeria","state": "Zamfara","lga": "Bakura","city": "Bakura","address": "No 1, Bakura Road, Bakura"},
    {"id": "nigeria-zamfara-birnin-magaji","country": "Nigeria","state": "Zamfara","lga": "Birnin Magaji","city": "Birnin Magaji","address": "No 1, Birnin Magaji Road, Birnin Magaji"},
    {"id": "nigeria-zamfara-bukkuyum","country": "Nigeria","state": "Zamfara","lga": "Bukkuyum","city": "Bukkuyum","address": "No 1, Bukkuyum Road, Bukkuyum"},
    {"id": "nigeria-zamfara-bungudu","country": "Nigeria","state": "Zamfara","lga": "Bungudu","city": "Bungudu","address": "No 1, Bungudu Road, Bungudu"},
    #fct
    {"id": "nigeria-fct-abaji","country": "Nigeria","state": "FCT","lga": "Abaji","city": "Abaji","address": "No 1, Abaji Road, Abaji"},
    {"id": "nigeria-fct-abuja-municipal","country": "Nigeria","state": "FCT","lga": "Abuja Municipal","city": "Abuja Municipal","address": "No 1, Abuja Municipal Road, Abuja Municipal"},
    {"id": "nigeria-fct-bwari","country": "Nigeria","state": "FCT","lga": "Bwari","city": "Bwari","address": "No 1, Bwari Road, Bwari"},
    {"id": "nigeria-fct-gwagwalada","country": "Nigeria","state": "FCT","lga": "Gwagwalada","city": "Gwagwalada","address": "No 1, Gwagwalada Road, Gwagwalada"},
    {"id": "nigeria-fct-kuje","country": "Nigeria","state": "FCT","lga": "Kuje","city": "Kuje","address": "No 1, Kuje Road, Kuje"}
    ]

discounts = [
    {
        "code": "WULLINP40",
        "type": "percentage",
        "value": 40,
        "minPurchase": 0,
        "expiration": datetime.datetime.now() + datetime.timedelta(days=30),
        "usageLimit": 100,
        "usageCount": 0,
        "applicableProducts": [],
        "applicableCategories": [],
        "used_by": [],
    },
    {
        "code": "WULLINP2000",
        "type": "fixed",
        "value": 2000,
        "minPurchase": 0,
        "expiration": datetime.datetime.now() + datetime.timedelta(days=60),
        "usageLimit": 100,
        "usageCount": 0,
        "applicableProducts": [],
        "applicableCategories": [],
        "used_by": [],
    },
    {
        "code": "WULLINP3000",
        "type": "fixed",
        "value": 2000,
        "minPurchase": 0,
        "expiration": datetime.datetime.now() - datetime.timedelta(days=30),
        "usageLimit": 100,
        "usageCount": 57,
        "applicableProducts": [],
        "applicableCategories": [],
        "used_by": [],
    },
    {
        "code": "WULLINP35000",
        "type": "fixed",
        "value": 2000,
        "minPurchase": 100000,
        "expiration": datetime.datetime.now() + datetime.timedelta(days=60),
        "usageLimit": 100,
        "usageCount": 0,
        "applicableProducts": [],
        "applicableCategories": [],
        "used_by": [],
    },
    {
        "code": "WULLINP70",
        "type": "percentage",
        "value": 70,
        "minPurchase": 0,
        "expiration": datetime.datetime.now() + datetime.timedelta(days=30),
        "usageLimit": 100,
        "usageCount": 0,
        "applicableProducts": [14,17,18,20,23,24,26,27,28,30],
        "applicableCategories": [],
        "used_by": [],
    },
    {
        "code": "WULLINP10000",
        "type": "fixed",
        "value": 10000,
        "minPurchase": 0,
        "expiration": datetime.datetime.now() + datetime.timedelta(days=30),
        "usageLimit": 100,
        "usageCount": 100,
        "applicableProducts": [],
        "applicableCategories": [],
        "used_by": [],
    }

]
