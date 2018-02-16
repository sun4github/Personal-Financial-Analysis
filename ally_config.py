# Customize this for your bank/credit card statement

is_first_line_header = 'yes'

date_format = '%m/%d/%Y'

# in a credit card statement/csv deposits have a negative sign
# in such cases, set this to 1

deposits_have_negative_sign = 0

#header identification
# do not change the header field types from ex. date to datetime or transaction type should stay the same text
header_position = {
    "1":"date",
    "2":"time",
    "3":"amount",
    "4":"transaction type",
    "5":"description"
}

# array of dictionaries.

# Each dictionary entry is a keyword (KW) & category
# Each transaction source or description, is searched for the presence of KW,
# inorder to group it to the corresponding category.

# Add and customize this list to your preferences, expenses

Transaction_Categories_list = [
        
        {"KW":"BLUE CROSS OF LA","category":"Insurance"}
        ,{"KW":"ALLSTATE INS CO INS PREM","category":"Insurance"}
       
       
        ,{"KW":"LOSFA START","category":"Education-R"}
        ,{"KW":"SERVE","category":"Savings & Investments"}
        ,{"KW":"CAMPUS FCU Checking","category":"Savings & Investments"}
        ,{"KW":"account XXXXXX5410","category":"Savings & Investments"}
        ,{"KW":"APEX","category":"Savings & Investments"}

        ,{"KW":"ENTERGY","category":"Utilities & Fixed Costs"}
        ,{"KW":"UPP WATER SEWER","category":"Utilities & Fixed Costs"}
        ,{"KW":"GOOGLE PAYMENT","category":"Utilities & Fixed Costs"}
        ,{"KW":"STANDARD MORTGAG","category":"Utilities & Fixed Costs"}
        ,{"KW":"AMEX EPAYMENT","category":"Utilities & Fixed Costs"}
        ,{"KW":"ANEEL KANURI","category":"Utilities & Fixed Costs"}
        ,{"KW":"COX","category":"Utilities & Fixed Costs"}
        ,{"KW":"BANK OF AMERICA","category":"Utilities & Fixed Costs"}
        ,{"KW":"KEYSTONE","category":"Utilities & Fixed Costs"}
        ,{"KW":"PATHOLOGY","category":"Utilities & Fixed Costs"}
        ,{"KW":"LOUISIANA WOMEN","category":"Utilities & Fixed Costs"}
        ,{"KW":"BATON ROUGE CLIN","category":"Utilities & Fixed Costs"}

        ,{"KW":"BLUE STREAK","category":"Income"}
        
        
        ,{"KW":"WELLS FARGO","category":"Variable Costs"}
        ,{"KW":"DISCOVER","category":"Variable Costs"}
        ,{"KW":"CHASE","category":"Variable Costs"}
        ,{"KW":"Check Paid","category":"Variable Costs"}
        ,{"KW":"MACYS ONLINE","category":"Variable Costs"}
        ,{"KW":"CITI","category":"Variable Costs"}
        ,{"KW":"ATM Fee","category":"Variable Costs"}
        ,{"KW":"KOHL'S","category":"Variable Costs"}
        ,{"KW":"JCPenney","category":"Variable Costs"}
        ,{"KW":"Zelle","category":"Variable Costs"}
        ,{"KW":"Paypal","category":"Variable Costs"}
        ,{"KW":"COX","category":"Variable Costs"}
        ,{"KW":"TJ MAXX","category":"Variable Costs"}
        ,{"KW":"TARGET","category":"Variable Costs"}
        ,{"KW":"GOOGLE","category":"Variable Costs"}
        ,{"KW":"SEARS","category":"Variable Costs"}
        ,{"KW":"ROSS","category":"Variable Costs"}
        ,{"KW":"MATHERNES","category":"Variable Costs"}
]
