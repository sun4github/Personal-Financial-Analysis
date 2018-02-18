#2018-02-09 SK: Personal Financial analysis Integrated version & Emailer

import re
import time
import datetime
import os
import sqlite3
import configparser
import importlib


from sys import platform
from pathlib import Path

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#AWS SES SDK
import boto3
from botocore.exceptions import ClientError

# custom support files for inclusion
import get_download_folders as wFolders

#Job scheduler
#https://apscheduler.readthedocs.io/en/latest/userguide.html
from apscheduler.schedulers.blocking import BlockingScheduler



def makeANoValueListFromConfigSection(config_section_as_dictionary):
	newList = []
	for key in config_section_as_dictionary.keys():
		newList.append(key)
	return newList
	
def makeAKWListFromConfigSection(config_section_as_dictionary):
	newList = []
	for key in config_section_as_dictionary.keys():
		newDict = {"KW":key,"category":config_section_as_dictionary[key]}
		newList.append(newDict)
	return newList
	
def makeADictionaryFromConfigSection(config_section_as_dictionary):
	newDict = {}
	for key in config_section_as_dictionary.keys():
		newDict[key] = config_section_as_dictionary[key]
	return newDict

main_config = configparser.ConfigParser(allow_no_value = True)

main_config.read('config.ini')

#Custom Private Information - START -- DO NOT SHARE

AWS_ACCESS_KEY = main_config['SETTINGS']['AWS_ACCESS_KEY']
AWS_ACCESS_PW = main_config['SETTINGS']['AWS_ACCESS_PW']
SENDER_EMAIL_ADDRESS = main_config['SETTINGS']['SENDER_EMAIL_ADDRESS']
RECIPIENT_EMAIL_ADDRESS_LIST = makeANoValueListFromConfigSection(main_config['RECIPIENT_EMAIL_ADDRESS_LIST'])
RUN_MODE = main_config['SETTINGS']['RUN_MODE']
SOURCE_LIST = makeANoValueListFromConfigSection(main_config['FINANCIAL SOURCES'])

#Custom Private Information - END -- DO NOT SHARE


# using binary search - not used
def findTransactionCategory(item_desc):
    start_index = 0
    boundary = len(Transaction_Categories_list)

    

    while boundary - start_index > 1:

        middle_index = int((start_index + boundary) / 2)
        print('start_index ' + str(start_index))
        print('boundary ' + str(boundary))
        print('middle_index ' + str(middle_index) + ' = ' + Transaction_Categories_list[middle_index]['KW'].lower())

        
        if(Transaction_Categories_list[middle_index]['KW'].lower() == item_desc.lower()):
            return Transaction_Categories_list[middle_index]['category'];
        elif(item_desc.lower() > Transaction_Categories_list[middle_index]['KW'].lower()):
            start_index = middle_index
        elif(item_desc.lower() < Transaction_Categories_list[middle_index]['KW'].lower()):
            boundary = middle_index

        print('new start_index ' + str(start_index))
        print('new boundary ' + str(boundary))
        print('---')

    return None
            

# own implementation of bubble sort  - not used
def sortTransactionCategoryList():
    lowest_index=0
    start_index = 0
    boundary = len(Transaction_Categories_list)
    how_many_left = boundary-1
##    print(boundary)

    for n in range(how_many_left):        
        lowest_index = start_index
        #print(str(n) + ': new start_index = ' + str(start_index))
        #print(str(n) + ': new how_many_left = ' + str(how_many_left))
        
        for i in range(start_index,boundary):
            #print('with  = ' + str(i) + ' = ' + Config.Transaction_Categories_list[i]['KW'])            
            if(Transaction_Categories_list[lowest_index]['KW'].lower() > Transaction_Categories_list[i]['KW'].lower()):
                #print('Is current lowest index element = ' + Config.Transaction_Categories_list[lowest_index]['KW'] + ' > than  current element = ' + Config.Transaction_Categories_list[i]['KW'])
                #print('yes greater. hence swapping lowest_index ' + str(lowest_index) + ' for current index ' + str(i))
                lowest_index = i
                
        #print('final lowest_index = ' + str(lowest_index))
        #print('final highest_index = ' + str(highest_index))
        #swap
        temp_KW = Transaction_Categories_list[start_index]['KW']
        temp_category = Transaction_Categories_list[start_index]['category']
        Transaction_Categories_list[start_index]['KW'] = Transaction_Categories_list[lowest_index]['KW']
        Transaction_Categories_list[start_index]['category'] = Transaction_Categories_list[lowest_index]['category']
        Transaction_Categories_list[lowest_index]['KW'] = temp_KW
        Transaction_Categories_list[lowest_index]['category'] = temp_category
        #print('List after swap:')
        #print(Config.Transaction_Categories_list)
        
        start_index = start_index + 1
        how_many_left = how_many_left - 1

    print('List Final:')
    print(Transaction_Categories_list)

# own implementation of bubble sort
def sortTransactionCategorySummaryList():
    lowest_index=0
    start_index = 0
    boundary = len(summary_list)
    how_many_left = boundary-1
##    print(boundary)
    
    for n in range(how_many_left):        
        lowest_index = start_index
        #print(str(n) + ': new start_index = ' + str(start_index))
        #print(str(n) + ': new how_many_left = ' + str(how_many_left))
        
        for i in range(start_index,boundary):
            #print('with  = ' + str(i) + ' = ' + Config.Transaction_Categories_list[i]['KW'])            
            if(summary_list[lowest_index].total > summary_list[i].total):
                #print('Is current lowest index element = ' + Config.Transaction_Categories_list[lowest_index]['KW'] + ' > than  current element = ' + Config.Transaction_Categories_list[i]['KW'])
                #print('yes greater. hence swapping lowest_index ' + str(lowest_index) + ' for current index ' + str(i))
                lowest_index = i
                
        #print('final lowest_index = ' + str(lowest_index))
        #print('final highest_index = ' + str(highest_index))
        #swap
        temp_sum_obj = summary_list[start_index]
        #temp_category = summary_list[start_index]['category']
        summary_list[start_index] = summary_list[lowest_index]
        summary_list[lowest_index] = temp_sum_obj
        #print('List after swap:')
        #print(Config.Transaction_Categories_list)
        
        start_index = start_index + 1
        how_many_left = how_many_left - 1

    #print('List Final:')
    #print(summary_list)




def isLinuxOS():
    if platform == "linux" or platform == "linux2":
        return 'yes'
    else:
        return 'no'
    
def isWindowsOS():
    if platform == "win32":
        return 'yes'
    else:
        return 'no'

def clearScreen():
    if(isLinuxOS() == 'yes'):
        os.system('clear')
    elif(isWindowsOS() == 'yes'):
        os.system('cls')

class Cat_Summary:

    def __init__(self, category,total,source):
        self.category = category
        self.total = float(total)
        self.source_list = []
        self.source_list.append(source)

    def update(self, total, source):
        self.total = self.total + float(total)
        self.source_list.append(source)

    def printinfo(self):

        print(self.category + ' = $' + '{:,.2f}'.format(self.total))
        #print('Summary Category is: ' + self.category)
        #print('Summary is: ' + '{:,.2f}'.format(self.total))


    def retinfo(self):
        summy = '<b>' + self.category + '</b> = $' + '{:,.2f}'.format(self.total)
        return summy



def split_line(line_to_split):
    lst = line_to_split.split(',')
    new_lst=[]
    sq = False
    tmp = ''
    reggie = re.compile('.*".+".*')
    for item in lst:
        ls = '"' in item
        if(reggie.match(item) != None):
            closing_quotes_exist = True
        else:
            closing_quotes_exist = False
            
        #print('item:' + item)
        #print('ls:' + str(ls))
        #print('sq:' + str(sq))
        #print('closing_quotes_exist:' + str(closing_quotes_exist))
               
        if(ls == True and sq == False):
            if(closing_quotes_exist == True):
                sq = False
                new_lst.append(item)
            else:
                sq = True
                tmp = tmp + item
                
        elif(ls == False and sq == True):
            tmp = tmp + item
        elif(ls == True and sq == True):
            tmp = tmp + item
            #print('tmp:' + tmp)
            new_lst.append(tmp)
            tmp = ''
            sq = False
        else:
            new_lst.append(item)

    #print(new_lst)
    return new_lst


class final_item:
	def __init__(self, total_income, total_expenses, summary_remaining, actual_remaining, summary_list, data_source, institution_name):
		self.data_source = data_source
		self.total_income = total_income
		self.total_expenses = total_expenses
		self.summary_remaining = summary_remaining
		self.actual_remaining = actual_remaining
		self.summary_list = summary_list
		self.institution_name = institution_name

	def ret_info(self):
		summy = '''
					<h3>Data Source : ''' + self.data_source + ''' & Institution : ''' + self.institution_name + ''' </h3><br />
					<b>Total Income</b> : $''' + '{:,.2f}'.format(self.total_income) + '''<br />
					<b>Total Expenses</b> : $''' + '{:,.2f}'.format(self.total_expenses) + '''<br />
					<b>Summary</b> : $''' + '{:,.2f}'.format(self.summary_remaining) + '''<br />
					<b>Actual Remaining</b> : $''' + '{:,.2f}'.format(self.actual_remaining) + '''<br />
					<hr />'''
		for sum_obj in self.summary_list:
			summy = summy + sum_obj.retinfo() + '<br />'
		summy = summy + '<hr color = "#DC143C" width="3px" />'
		return summy


class Transaction:

    def __init__(self, line):
        
        if(len(line) > 0):
            #print(line)
            sublist = split_line(line)
            #print(sublist)
            field_position = 1
            for field in sublist:
                #determine what current field position , is actually from config
                field_type = header_position[str(field_position)]
                #print(str(field_position) + ' : ' + field_type);
                if(field_type == "date"):
                    try:
                        self.date = datetime.datetime.strptime(field,'%Y-%m-%d')
                    except ValueError:
                        try:
                            self.date = datetime.datetime.strptime(field,'%Y/%m/%d')
                        except ValueError:
                            try:
                                self.date = datetime.datetime.strptime(field,'%m/%d/%Y')
                            except:
                                print('Unknown date format')
                                break
                   
                    field_position = field_position+1
                elif(field_type == "time"):
                    self.time = field
                    field_position = field_position+1
                elif(field_type == "amount"):
                    self.amount = float(field)
                    field_position = field_position+1
                elif(field_type == "transaction type"):
                    self.t_type = field
                    field_position = field_position + 1
                elif(field_type == "description"):
                    self.source = field
                    field_position = field_position + 1
            #self.printinfo()

    

    def printinfo(self):
        print('Date is: ' + str(self.date))
        print('Amount is: ' + '{:,.2f}'.format(self.amount))
        print('Transaction type is: ' + self.t_type)
        if(len(self.source) > 0):
            print('Source is: ' + self.source)


def findCategorySummaryObject(category_name):
    retObj = None
    for category_obj in summary_list:
        #print('searching for ' + category_name + ' in ' + category_obj.category)
        m = re.match('^' + category_name + '$',category_obj.category, flags=re.IGNORECASE)
        if(m != None):
            retObj = category_obj
            return retObj
    return retObj


        


def categorize_transaction(tran_obj):
    tran_cat = None
    #print(' categorizing source: ' + tran_obj.source)
    if((tran_obj.amount > 0 and deposits_have_negative_sign == 0 ) or (tran_obj.amount < 0 and deposits_have_negative_sign == 1)):
        tran_cat='Income'
        #print(' matched to ' + tran_cat)
    elif((tran_obj.amount < 0 and deposits_have_negative_sign == 0 ) or (tran_obj.amount > 0 and deposits_have_negative_sign == 1 )):
        for cat_obj in Transaction_Categories_list:
            #print(cat_obj['KW'])
            reggi = re.compile(cat_obj['KW'], re.IGNORECASE)
            #if(reggi.search(tran_obj.source) != None):
            if(re.search(cat_obj['KW'],tran_obj.source,flags=re.IGNORECASE) != None):
                tran_cat=cat_obj['category']
                break
    
    if(tran_cat != None):
        cat_sum_obj = findCategorySummaryObject(tran_cat)
        
        if(cat_sum_obj != None):
            cat_sum_obj.update(tran_obj.amount,tran_obj.source + ' = ' + '{:,.2f}'.format(tran_obj.amount))
            return
        else:
            cat_sum_obj = Cat_Summary(tran_cat,tran_obj.amount,tran_obj.source + ' = ' + '{:,.2f}'.format(tran_obj.amount))
            summary_list.append(cat_sum_obj)
            return
    else: 
        #print(' updating other for: ' + tran_obj.source)
        other_obj.update(tran_obj.amount,tran_obj.source + ' = ' + '{:,.2f}'.format(tran_obj.amount))
        #print(cat_obj['KW'])
        


def process_file(localFinFile, data_source, is_current_account_the_salary_account, salary_amount, institution_name):
        
	if(localFinFile != None and len(localFinFile) != 0):
		try:
			with open(localFinFile ) as infile_object :
				lines = infile_object.read().splitlines() # strips the newline at end of line
				infile_object.close()
		except Exception:
				#continue if file not found
				print('File not found.')
				exit()

	#earliest_date = datetime.datetime.today()
	earliest_date = None
	#latest_date = datetime.datetime.today()
	latest_date = None

	line_cnt = 1 

	#first line is header. Dso do not load it
	if is_first_line_header =='yes':
		header_line = 1
	else:
		header_line = 0


	for line in lines:
		if(line_cnt > header_line):
			tsc = Transaction(line)
			#print(line)
			
			if(earliest_date == None):
				earliest_date = tsc.date
			elif(tsc.date <= earliest_date):
				earliest_date = tsc.date

			if(latest_date == None):
				latest_date = tsc.date
			if(tsc.date >= latest_date):
				latest_date = tsc.date
			
			transaction_list.append(tsc)
				#tsc.printinfo()
				#categorize_transaction(tsc)
				#print('-------------------')
		line_cnt = line_cnt+1

	#clearScreen()
	print('Earliest date in dataset is ' + earliest_date.strftime('%Y-%m-%d'))
	print('Latest date in dataset is ' + latest_date.strftime('%Y-%m-%d'))
	print('')

	start_date = earliest_date

	end_date = latest_date

	total_expenses = 0
	total_income = 0

	summary_list.append(other_obj)

	# categorize each transaction
	for trans_obj in transaction_list:
		#trans_obj.printinfo()
		if((trans_obj.date >= start_date  ) and  (trans_obj.date <= end_date )):
			categorize_transaction(trans_obj)

			if((trans_obj.amount > 0 and deposits_have_negative_sign == 0 ) or (trans_obj.amount < 0 and deposits_have_negative_sign == 1)):
				total_income = total_income + trans_obj.amount
			elif((trans_obj.amount < 0 and deposits_have_negative_sign == 0 ) or (trans_obj.amount > 0 and deposits_have_negative_sign == 1)):
				total_expenses =  total_expenses + trans_obj.amount
		   

	print('')
	
	print('Total income is ' + '{:,.2f}'.format(total_income))
	# special case for earlier part of the month when that months salary is deposted on the last days of the
	# previous month, as salary is often deposted on 30th or 31st of prev month, manually add the salary.
	# uncomment it out if this does not suite your case
	#print('salary_amount =' + str(salary_amount))
	#print('data_source =' + str(data_source))
	#print('is_current_account_the_salary_account =' + str(is_current_account_the_salary_account))
	if(total_income < salary_amount and data_source=="bank" and is_current_account_the_salary_account == "yes"):
		total_income = salary_amount + total_income
		print('Adjusted "Total income" amount using provided salary = $' + '{:,.2f}'.format(total_income))
	
	summary_remaining = total_income + total_expenses
	print('Total expenses is ' + '{:,.2f}'.format(total_expenses))
	print('Summary is ' + '{:,.2f}'.format(summary_remaining))
	print('')

	sortTransactionCategorySummaryList()

	actual_remaining = 0
	if(data_source == "bank"):
		#display each transaction summary
		for sum_obj in summary_list:
			sum_obj.printinfo()
			if(sum_obj.category == 'Savings & Investments'):
				actual_remaining = (total_income + total_expenses) +  (-1 * sum_obj.total)
		
		print('Actual Remaining ("Total income" - "Total expenses") + All Savings & Investments is $' + '{:,.2f}'.format(actual_remaining))
	
	print('')



	nf = final_item(total_income, total_expenses, summary_remaining , actual_remaining, summary_list, data_source, institution_name)
	final_list.append(nf)

	if(RUN_MODE == 'Interactive'):
		# Exclusive for interactive version 
		print('Specify any category to research further (enter to skip & exit))')
		category_to_research = input()

		while(len(category_to_research) > 0):
			#category_to_research = "Utilities & Fixed Costs"
			# analysis of other category transactions
			print('')
			for category_obj in summary_list:
				#print('searching for ' + category_to_research+ ' in ' + category_obj.category )
				m = re.match('^' + category_to_research + '$',category_obj.category, flags=re.IGNORECASE)
				if(m != None):
					for other_source in category_obj.source_list:
					   print(other_source)
					   print('')
			print('Specify any category to research further (enter to skip & exit)')
			category_to_research = input()


def send_email(html_body,first_day_of_month, date_until):
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = SENDER_EMAIL_ADDRESS

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT_LIST = RECIPIENT_EMAIL_ADDRESS_LIST

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = """ Financial Summary from """ + first_day_of_month + """ till """ + date_until

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Financial Summary from """ + first_day_of_month + """ till """ + date_until + """ </h1> 
      <p> """ + html_body + """ </p>
    </body>
    </html>
    """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    #client = boto3.client('ses',region_name=AWS_REGION)
    client = boto3.client('ses',region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_ACCESS_PW)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT_LIST
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])

		

# MAIN program area

localDirectory = wFolders.get_download_path()
#localDirectory = localDirectory + '\\'

#final lists - used for email
final_list = []
todays_date = datetime.datetime.today()
#date_today_formatted = todays_date.strftime('%Y%m%d')

is_first_line_header = 'no'
deposits_have_negative_sign = 0

other_obj = Cat_Summary('Other',0,'')
header_position = {}
Transaction_Categories_list = []
# declare a list to hold events
transaction_list = []

#clear the summary list
summary_list = []


print('Running in Mode: ' + RUN_MODE)
	
def lead_the_analysis():
	print('called main ' + localDirectory)
	
	for source_config_file in SOURCE_LIST:
		try:
			
			dConfig = configparser.ConfigParser(allow_no_value=True)
			dConfig.read(source_config_file)
			
			institution_name = dConfig['SETTINGS']['institution_name']
			print(' ----------- Processing financial institution : ' + institution_name + ' --------------- ')

			# run the automated downloader if setup
			if(dConfig['SETTINGS']['auto_driver_exists'] == 'yes'):
				module_name = importlib.import_module(dConfig['SETTINGS']['driver_module'])
				module_path = dConfig['SETTINGS']['driver_module_file_path']	
				auto_downloader_method = dConfig['SETTINGS']['driver_trigger_method']
				#import_a_module_dynamically(auto_download_method,module_path)
				get_data_method = getattr(module_name, auto_downloader_method)
				get_data_method()

			#get the latest downloaded file that matches the prefix, ending with a .csv
			download_csv_prefix = dConfig['SETTINGS']['download_csv_prefix']
			last_modified_time = 0	
			last_file = ''
			for file in os.listdir(localDirectory):
				if file.startswith(download_csv_prefix) and file.endswith('.csv'):
					#print(os.path.join(localDirectory,file))
					stat_result = os.lstat(os.path.join(localDirectory,file))
					#print(stat_result)
					if(stat_result.st_mtime > last_modified_time):
						last_modified_time = stat_result.st_mtime
						last_file = file

	
			file_name = last_file
			localFinFile = os.path.join(localDirectory,file_name)

			if(len(last_file) > 0):
				print('Selected latest file: ' + localFinFile)
			else:
				raise ValueError('Source download failed')

			# declare a list to hold events
			global transaction_list
			transaction_list = []

			#clear the summary list
			global summary_list
			summary_list = []
			
			global is_first_line_header
			is_first_line_header = dConfig['SETTINGS']['is_first_line_header']
			
			global deposits_have_negative_sign
			deposits_have_negative_sign = int(dConfig['SETTINGS']['deposits_have_negative_sign'])

			#header identification
			# do not change the header field types from ex. date to datetime or transaction type should stay the same text

			global header_position
			header_position = makeADictionaryFromConfigSection(dConfig['HEADER POSITION'])

			#print(header_position)
			

			# array of dictionaries. Each dictionary entry is a keyword & category
			# prev: Transaction_Categories_list = dConfig.Transaction_Categories_list
			global Transaction_Categories_list
			Transaction_Categories_list = makeAKWListFromConfigSection(dConfig['TRANSACTION CATEGORY LIST'])

			#call the main method to parse discover statement
			process_file(localFinFile,dConfig['SETTINGS']['source_type'],dConfig['SETTINGS']['salary_bank'],float(dConfig['SETTINGS']['salary_amount']),institution_name)
			
			os.remove(localFinFile)
		except Exception as ex:
			print('Something went wrong')
			print('Exception: ' + str(ex))
			
	if(RUN_MODE == 'Interactive'):
		print('Would you like to receive the analysis in e-mail (yes/no) ?')
		email_requested = input()
		

	if(RUN_MODE == 'Emailer' or email_requested == 'yes'):
		#finally send a email
		htmlB = ''
		for fin_obj in final_list:
			htmlB = htmlB + fin_obj.ret_info() + '<br />'

		todays_date = datetime.datetime.today()

		first_day_of_month = todays_date.strftime('%m') + '/01/' + todays_date.strftime('%Y')
		date_until = todays_date.strftime('%m/%d/%Y')

		#send email using AWS SES SDK
		send_email(htmlB, first_day_of_month, date_until)
	
	print('')
	print('********* Financial Analysis Complete **********')

def tick():
    print('Tick! The time is: %s' % datetime.datetime.now())

# To run code directly	
#tick()
lead_the_analysis()
	
# To Schedule it as a task
#if __name__ == '__main__':
	#scheduler = BlockingScheduler()   
	
	##run the job every 3 days starting from monday, at 9 am, 5 minutes
	#scheduler.add_job(tick, 'cron',day_of_week='*/3',hour=9,minute=5)
	#scheduler.add_job(lead_the_analysis, 'cron',day_of_week='*/3',hour=9,minute=5)
	#print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

	#try:
	#	scheduler.start()
	#except (KeyboardInterrupt, SystemExit):
	#	pass
