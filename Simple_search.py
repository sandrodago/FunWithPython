'''

Alex D'Agostino 26316417
Comp 479 - Project 2
November 15, 2015

'''

import nltk
import re
import csv
import collections
import glob
import os.path
import sys
csv.field_size_limit(sys.maxsize)

## Global Variables
MAX_MEMORY = 100000
curr_mem = 0
TOTAL_TOKENS = 0
docID = 1							# start docID's at 1

def doSpimi(token_stream):
	global docID
	TOTAL_TOKENS = len(token_stream)# get the size of the tokenized list.
	index = 0						# start at the first token.
	blocks = 0						# dictionary number.
	while(index < TOTAL_TOKENS):	# while we have memory to spare.
		t = csv.writer(open("dictionary_" + str(blocks) +".csv", 'w'))
		curr_mem=0
		blocks+=1
		dictionary = collections.OrderedDict() # New blank ordered dictionary.
		while(True):
			if index < TOTAL_TOKENS:# if we're still in the bounds of the token list.
				word = token_stream[index-1]# get the i'th token.
				if word == "/reuters":	# if we get to a new ID Block, increment.
					docID += 1
				if word not in dictionary:# if the word is not in the dictionary.
					dictionary[word] = [docID]	 # add it to the dictionary.
				else:
					# otherwise, add the posting ID, IF it doesn't exist.
					if docID not in dictionary[word]:
						postings_list = dictionary[word]
						postings_list.append(docID)
						dictionary[word] = postings_list
			curr_mem+=1#len(word)					# increase memory by one(word)
			index+=1								# go to next word.
			# IF we're done all the tokens, or have reached maximum memory 
			if index >= TOTAL_TOKENS or curr_mem>MAX_MEMORY:
				break
		# sort the dictionary		
		dictionary = sorted(dictionary.items(), key = lambda t: t[0])
		# write the dictionary to file
		for key, val in dictionary:
			t.writerow([key, val])


def main():
	num = 0
	while(num <= 21):
			# accessing the document
		if(num == 0):
			_file_ = open('reuters21578/reut2-000.sgm', 'r')
		elif(num == 1):
			_file_ = open('reuters21578/reut2-001.sgm', 'r')	
		elif(num == 2):
			_file_ = open('reuters21578/reut2-002.sgm', 'r')	
		elif(num == 3):
			_file_ = open('reuters21578/reut2-003.sgm', 'r')	
		elif(num == 4):
			_file_ = open('reuters21578/reut2-004.sgm', 'r')	
		elif(num == 5):
			_file_ = open('reuters21578/reut2-005.sgm', 'r')	
		elif(num == 6):
			_file_ = open('reuters21578/reut2-006.sgm', 'r')	
		elif(num == 7):
			_file_ = open('reuters21578/reut2-007.sgm', 'r')	
		elif(num == 8):
			_file_ = open('reuters21578/reut2-008.sgm', 'r')	
		elif(num == 9):
			_file_ = open('reuters21578/reut2-009.sgm', 'r')	
		elif(num == 10):
			_file_ = open('reuters21578/reut2-010.sgm', 'r')	
		elif(num == 11):
			_file_ = open('reuters21578/reut2-011.sgm', 'r')	
		elif(num == 12):
			_file_ = open('reuters21578/reut2-012.sgm', 'r')	
		elif(num == 13):
			_file_ = open('reuters21578/reut2-013.sgm', 'r')	
		elif(num == 14):
			_file_ = open('reuters21578/reut2-014.sgm', 'r')	
		elif(num == 15):
			_file_ = open('reuters21578/reut2-015.sgm', 'r')	
		elif(num == 16):
			_file_ = open('reuters21578/reut2-016.sgm', 'r')	
		elif(num == 17):
			_file_ = open('reuters21578/reut2-017.sgm', 'r')	
		elif(num == 18):
			_file_ = open('reuters21578/reut2-018.sgm', 'r')	
		elif(num == 19):
			_file_ = open('reuters21578/reut2-019.sgm', 'r')	
		elif(num == 20):
			_file_ = open('reuters21578/reut2-020.sgm', 'r')
		elif(num == 21):
			_file_ = open('reuters21578/reut2-021.sgm', 'r')

		newDoc = _file_.read()				# puts document into memory
		newDoc = newDoc.lower()				# normalizes all tokens
		tokens = nltk.word_tokenize(newDoc)	# tokenize the document

		doSpimi(tokens) #send a tokenized document to spimi
		num += 1

def query(query):
	print "searching for: \"" + query + "\""
	iterator=1				# count through the dictionary files
	query = query.lower() 	# normalizes the search term
	newdictionary = {}		# create new blank dictionary
	MAX_ITERATOR = len(glob.glob1(".","dictionary_*.csv"))
	postings_list_new = []	# create new blank postings list
	while (iterator < MAX_ITERATOR): # while there are files left
		filename = "dictionary_" + str(iterator) + ".csv" 	# get the new filename
		# for every row in the file, grab by key, and value
		for key, val in csv.reader(open(filename)):			
				tempVal = re.sub('[\[\],]*', '', val) 		#removes all non integer values
				tempVal = tempVal.split()					# recreate the postings list as a list
				newdictionary[key] = tempVal		  		# put the postings list in the dictionary
		for word in newdictionary:
			#print filename
		 	if query in newdictionary:						# if the query is in the dicionary
		 		postings_list_temp = newdictionary[query]	# put the list into a new blank list
				for ID in postings_list_temp:				# check if there are duplicates and only
		 			if ID not in postings_list_new:			# add the new document ID's.
		 				postings_list_new.append(ID)
		iterator+=1
	if postings_list_new == []:
		return "none"
	else:
		return postings_list_new							# return the complete list.

def merge():
	print "merging"
	dirLength = len(glob.glob1("","*.csv")) # gives the quantity of files the loop has to iterate over    
	a= 0
	iterator = 0
	mergeDictionary = collections.OrderedDict()
	while (a < dirLength):
	    for key, val in csv.reader(open("dictionary_" + str(iterator) +".csv")):
	        
	        tempVal = re.sub('[\[\],]*', '', val) #removes all non integer values
	        tempVal = tempVal.split()
	        tempVal = map(int, tempVal)

	        if key not in mergeDictionary:
	                mergeDictionary[key] = tempVal  #Adds new token with related docID
	        else:
	            mergeList = []    
	            mergeList = mergeDictionary[key]
	            for doc in tempVal:
	                mergeList.append(doc)#append new docID to preexisting token postings list
	            mergeDictionary[key] = mergeList    
	    iterator += 1        
	    a+= 1

	mergeFile = csv.writer(open("mergeFile.csv", "w")) #creates new file
	dictionary = sorted(mergeDictionary.items(), key = lambda t: t[0])
	for key, val in dictionary: #write current dicionary
	    mergeFile.writerow([key, val])


def Jquery(queryTerm):
	originalTerm = queryTerm
	queryTerm = queryTerm.lower()
	queryTerm = queryTerm.split()
	queryQty = len(queryTerm)
	results = []
	print queryQty
	
	global dirLength
	i = 0
	j = 0
	while(j < queryQty): #loops through the indexes for each query term if there is a space in the term
		
		for key, val in csv.reader(open("mergeFile.csv")):
			tempVal = re.sub('[\[\],]*', '', val) #removes all non integer values
			tempVal = tempVal.split()
			if(key == queryTerm[j]): #if the current query term is found in the index then add it to the list
				for doc in tempVal:
					results.append(doc) 
			elif(key > queryTerm[j]):
				break
		j += 1
		i = 0
		iterator = 0
	results = map(int, results) #converts the list back to integer form
	results = sorted(results)
	completeResults = [] #only used if the query involves more than one word
	completeResultsUnique = [] #will store the unique values of intersecting query term docIDs
	if(queryQty > 1):	
		for index, result in enumerate(results):
			if(results.count(result) == queryQty): #checks to see if the same ID is found for the qty of terms searched
					completeResults.append(result)
		for index, docID in enumerate(completeResults): #removes the duplicate values
			if(index+1 < len(completeResults)):
				if(docID == completeResults[index+1]):
					completeResultsUnique.append(docID)			
		print "\"" + originalTerm + "\"" + " found in the following documents "
		print completeResultsUnique
	else:
		print "\"" + originalTerm + "\"" + " found in the following documents "
		print results # if the query is only one word this one is used
	print "search ended"

#main()
#merge()
#print query("Carter")
print Jquery("george bush")
