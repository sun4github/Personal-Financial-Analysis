# Customize this for your bank/credit card statement

is_first_line_header = 'yes'

date_format = '%m/%d/%Y'

# in a credit card statement/csv deposits have a negative sign
# in such cases, set this to 1

deposits_have_negative_sign = 1

#header identification
# do not change the header field types from ex. date to datetime or transaction type should stay the same text
header_position = {
    "1":"date",
    "2":"time",
    "3":"description",
    "4":"amount",
    "5":"transaction type"
}

# array of dictionaries.

# Each dictionary entry is a keyword (KW) & category
# Each transaction source or description, is searched for the presence of KW,
# inorder to group it to the corresponding category.

# Add and customize this list to your preferences, expenses

Transaction_Categories_list = [
        
        {"KW":"WAL-MART","category":"Stationery"}
        ,{"KW":"WALMART","category":"Stationery"}
        
        ,{"KW":"AMAZON","category":"Stationery & Electronics"}
        ,{"KW":"GREENMANGAMING","category":"Software & Entertainment"}
        
        
        ,{"KW":"B&H PHOTO","category":"Electronics"}

        ,{"KW":"SARKU JAPAN","category":"Outside Food"}
        ,{"KW":"CUISINE","category":"Outside Food"}
        ,{"KW":"DOMINO","category":"Outside Food"}
        ,{"KW":"PAPA ROCCOS","category":"Outside Food"}
        ,{"KW":"RAISING CANE","category":"Outside Food"}
        ,{"KW":"INDIA'S","category":"Outside Food"}
        ,{"KW":"ICE CREAM","category":"Outside Food"}
        ,{"KW":"NINE DRAGON","category":"Outside Food"}
        ,{"KW":"THAI KITCHEN","category":"Outside Food"}
        ,{"KW":"ORIENTAL PEARL","category":"Outside Food"}
        ,{"KW":"TACO BELL","category":"Outside Food"}
        ,{"KW":"SMOOTHIE","category":"Outside Food"}
        ,{"KW":"BURGERS","category":"Outside Food"}
        ,{"KW":"GRILL","category":"Outside Food"}
        ,{"KW":"LAVA CANTINA","category":"Outside Food"}
        ,{"KW":"CAFE","category":"Outside Food"}
        ,{"KW":"CHICK-FIL-A","category":"Outside Food"}
        
        ,{"KW":"TARGET","category":"Grocery"}
        ,{"KW":"GOPPELT","category":"Grocery"}
        ,{"KW":"FRESH MKT","category":"Grocery"}
        ,{"KW":"SOUTHSIDE","category":"Grocery"}
        ,{"KW":"WINN-DIXIE","category":"Grocery"}
        ,{"KW":"KASED BROTHERS","category":"Grocery"}        	
        ,{"KW":"ASIAN MARKET","category":"Grocery"}
	,{"KW":"ALBERTSONS","category":"Grocery"}
        ,{"KW":"MATHERNE","category":"Grocery"}
        ,{"KW":"ROUSE","category":"Grocery"}
		
        ,{"KW":"FASHION INDIA","category":"Grocery & Indian"}
	,{"KW":"INTERNATIONAL MARKET","category":"Grocery & Indian"}	        

        ,{"KW":"YUPPTV","category":"Entertainment & Tours"}
        ,{"KW":"ZOO","category":"Entertainment & Tours"}
        ,{"KW":"AUDUBON","category":"Entertainment & Tours"}
        ,{"KW":"PLANTATION","category":"Entertainment & Tours"}
        ,{"KW":"ALG","category":"Entertainment & Tours"}
        ,{"KW":"JUNGLE GARDENS","category":"Entertainment & Tours"}
        ,{"KW":"HOTELS.COM","category":"Entertainment & Tours"}
        ,{"KW":"SWAMP TOUR","category":"Entertainment & Tours"}
        ,{"KW":"MUSEUM","category":"Entertainment & Tours"}
        
        ,{"KW":"PARTY CITY","category":"Birthday"}
        ,{"KW":"PARTY TIME","category":"Birthday"}
        ,{"KW":"AMBROSIA","category":"Birthday"}
        ,{"KW":"LIL BAMBINO","category":"Birthday"}
        
        
        ,{"KW":"PSI Services","category":"Education"}		
        ,{"KW":"AUDIBLE","category":"Education"}
        ,{"KW":"UDEMY","category":"Education"}
        
		
        ,{"KW":"BEDBATH","category":"Stationery"}
        ,{"KW":"TOYS R US","category":"Stationery"}
        ,{"KW":"AMZ*S&D","category":"Stationery"}
        ,{"KW":"BED BATH","category":"Stationery"}
        ,{"KW":"USPS","category":"Stationery"}
        ,{"KW":"OFFICE DEPOT","category":"Stationery"}
        ,{"KW":"HOBBY-LOBBY","category":"Stationery"}
		
        ,{"KW":"EBAY","category":"Stationery & Electronics"}
        ,{"KW":"NEWEGG","category":"Stationery & Electronics"}
        ,{"KW":"BESTBUY","category":"Stationery & Electronics"}
	,{"KW":"TING","category":"Stationery & Electronics"}
		
        ,{"KW":"CARTERS","category":"Clothing"}
        ,{"KW":"DILLARD","category":"Clothing"}
        ,{"KW":"KOHL","category":"Clothing"}
        ,{"KW":"MACY'S","category":"Clothing"}
        ,{"KW":"GYMBOREE","category":"Clothing"}
	,{"KW":"GAP US","category":"Clothing"}
        ,{"KW":"JCPENNEY","category":"Clothing"}
		
        ,{"KW":"HOME DEPOT","category":"Hardware"}
        ,{"KW":"LOWES","category":"Hardware"}
        ,{"KW":"TERMINIX INTL","category":"Hardware"}

        ,{"KW":"WALGREENS","category":"Health & Medicine"}
        ,{"KW":"CVS","category":"Health & Medicine"}
        ,{"KW":"RITE AID","category":"Health & Medicine"}
        ,{"KW":"Lens","category":"Health & Contacts"}
        ,{"KW":"VUE EYECARE","category":"Health & Contacts"}
        ,{"KW":"CUSTOM EYES","category":"Health & Contacts"}
        ,{"KW":"FITNESS","category":"Health & Fitness"}
        ,{"KW":"CONTACTS","category":"Health & Contacts"}
        ,{"KW":"GOPPLET","category":"Health & Grooming"}
        ,{"KW":"THREADING","category":"Health & Grooming"}
        ,{"KW":"WONDER CUTS","category":"Health & Grooming"}

        ,{"KW":"BENNY","category":"Auto & Maintenance"}
        ,{"KW":"Firestone","category":"Auto & Maintenance"}
        ,{"KW":"OREILLY AUTO","category":"Auto & Maintenance"}
        ,{"KW":"EXXON","category":"Auto & Gasoline"}
        ,{"KW":"TEXACO","category":"Auto & Gasoline"}
        ,{"KW":"SHELL","category":"Auto & Gasoline"}
        ,{"KW":"BP","category":"Auto & Gasoline"}
        ,{"KW":"CHEVRON","category":"Auto & Gasoline"}
]
