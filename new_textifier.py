"""Extracts the title, content and date from the blogs and saves it in a file that is organized into sentences. The name of the file will be the date followed by the article title.
Argument passed should be the absolute path to the folder containing the website data. When giving path, start from the "/" folder"""
__author__ = 'kidus'

import os
import glob
import sys
import html2text
from datetime import datetime
import selenium
from selenium.webdriver.firefox import webdriver
import re,nltk
import unicodedata
import codecs


def address_split(location):
	return location[len_path+1:]


def clear_date(the_date):
	"""returns properly formatted date"""
	for element in days:
		if the_date.startswith(element):
			day=element
			break

 							
	the_date=the_date[len(day)+2:]


	for value in months.keys():
		if the_date.startswith(value):
			val_month= months[value]
			the_date= the_date[len(value)+1:]
			break
	buff= ''
	for element in the_date:
		if element != ',':
			buff += element
		else:
			the_date= the_date[len(buff)+2:]
			val_day= buff
			break
	if len(buff)!=2:
		val_day = "0"+val_day
	return_date= the_date[0:4]+"-"+val_month+"-"+val_day
	return return_date

def get_text(link):
	"""uses html2Text library to tidy up and return content of an html code string."""
	h= html2text.HTML2Text()
	h.ignore_links = True
	h.ignore_images= True
	h.ignore_emphasis = True
	return h.handle(link)



def htmltotext(the_file):
	"""Opens a webpage using selenium, extracts the content and writes it onto a file organized into sentences."""

	link= "file://" + the_file
	wd.get(link)
	try:
		element = wd.find_element_by_class_name("articletitle")
	except selenium.common.exceptions.NoSuchElementException: 
		print "didn't load " + the_file
		return

	header_name= get_text(element.get_attribute('innerHTML'))
	header_name= header_name.rstrip()

	try:
		element = wd.find_element_by_class_name('postmetadata-date')
		date_of_post= element.get_attribute('innerHTML')
		date_of_post= clear_date(date_of_post)
		#dprint date_of_post
	except selenium.common.exceptions.NoSuchElementException: 
		print "couldn't load date for article " + the_file
		date_of_post = "unknown"

	try:
		element = wd.find_element_by_class_name('post-content')
		data= element.get_attribute('innerHTML')
		data= get_text(data)
		#print data
	except selenium.common.exceptions.NoSuchElementException:
		print "article loading failed" + the_file

	data= data.replace('\n',' ')
	date= data.replace('#','')
	data=data.replace("*",'')
	if data.find("### Related Posts") != -1:
		data= data[0:data.find("### Related Posts")]
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	data =  '\n-----\n'.join(tokenizer.tokenize(data))

	#unicodedata.normalize('NFKD', data).encode('ascii','ignore')	
	#data= re.sub(u"(\u2018|\u2019|\u201c|\u201d)", "'", data)
	#data= re.sub(u"(\u201c'))
	file = codecs.open(date_of_post + '_' + header_name + '.txt', "w", "utf-8")
	#file = open(date_of_post + '_' + header_name + '.txt','w')

	file.write(header_name + '\n\n')
	file.write(data)
	file.close()

	#print header_name

	#wd.get(os.path.join("file://",the_file))
# def htmltotext(the_file):
# 	data = open(the_file, 'rb').readlines()
# 	is_here= False
# 	for index in range(len(data)):
# 		if data[index].startswith("##"):
# 			header= data[index][3:]
# 			is_here= True
# 			index= index + 2
# 			date= data[index]
# 			is_valid_date=False
# 			for element in days:
# 				if date.startswith(element):
# 					is_valid_date= True
# 					date= clear_date(date,element)
# 					print date
# 					break		
# 			if not is_valid_date:
# 				date="unknown"
# 			new_text=list()
# 			my_file= open(date+'_' + header +'.txt','w')

# 			while not data[index].startswith("### Related Posts") and index < len(data)-1:
# 				my_file.write(data[index])
# 				new_text.append(data[index])
# 				index += 1
# 			my_file.close


# 			break
# 	if not is_here:
# 		print the_file, " is not here"


def main(current_folder):
	"""recursively goes into the folders passed as an argument and sends html files to be read."""

	current_folder = glob.glob(os.path.join(current_folder ,'*'))
	for element in current_folder:
		if element.endswith('.html'):
			#print element
			htmltotext(element)
		elif os.path.isdir(element):
			#print element
			main(element)
		

if __name__=='__main__':
	if len(sys.argv)==2:
		global cwd , the_dir, len_path,wd,days,months
		days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		months={'January':'01', 'February':'02','March':'03' ,'April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
		wd= webdriver.WebDriver()		
		len_path= len(sys.argv[1])
		(lash,the_dir)= os.path.split(sys.argv[1])
		cwd = os.getcwd()
		new_folder= os.path.join(cwd ,the_dir)
		count = 1
		while os.path.isdir(new_folder):
			new_folder= os.path.join(cwd,the_dir + '_' + str(count))
			count +=1 
		#print new_folder
		os.makedirs(new_folder)
		os.chdir(new_folder)
		main(sys.argv[1])
		#htmltotext('/media/kidus/DATA/Downloads/iCog/web3/index.html')
		#htmltotext('/home/kidus/Desktop/extracted/deep-panic.html')
		#print address_split('/media/kidus/DATA/Downloads/iCog/web3/index.html')
	else:
		print "Enter absolute path to folder with webfiles in it as an argument."
	#htmltotext(sys.argv[1])
