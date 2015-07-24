import timeit
from collections import OrderedDict
import requests
from parser import XMLParser
import excep as ex
class ScrabbleSolver(object):

	def __init__(self,filename):
		'''
		filename - the file that contains the words
		scores - dictionary containing all the letters and their score '''
		self.filename = filename
		self.api_key = '9832fd27-0fe4-4bc6-961a-e2e74b2d9bb9'
		self.parser = XMLParser()
		self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
						"f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
						"l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
						"r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
						"x": 8, "z": 10}
		self.load_file()

	def load_file(self):
		''' Open the file and load all the words from the file into a list '''
		#open the word file
		word_file = open(self.filename,'r')
		#create an empty list to sort the lowered words
		self.words = []
		#traverse the file line by line and append the lowered word without the newline character([:-2]) to the list
		for word in word_file:
			self.words.append(word[:-2].lower())
		#then we close the file
		word_file.close()
    	

	def check_rack(self,rack):
		'''
			checks all the words from the list and compares them to the substrings in the rack
		'''
		#we lower the letters in the rack so AAA is equal to aaa
		rack = rack.lower()
		for letter in rack:
			if not letter.isalpha() :
				raise ex.IncorrectRack(rack)
		#create an empty list to hold the letters that we have already used
		used_letters = []
		#create a dictionary to hold the key=words ,value = score
		self.scored_words = {}
		#traverse the words list
		for word in self.words:
			#we create a sentinel value that at the end of every word will check if the whole word is in the rack
			increment = 0
			for letter in word:
				#we check to see if the letter is in the rack and if the letter is not in used letter
				#if it is in the used we check the count of the letter in the rack and in the word
				if letter in rack and (letter not in used_letters or rack.count(letter)>=word.count(letter)):
					increment += 1
					used_letters.append(letter)
			#after we have traversed the word, 
			# we check if the increment is equal to the len of the word , again to see if the whole word is in the rack
			if increment == len(word):
				#score the word
				score = self._get_score(word)
				#add the word and the score to the scored words dict
				self.scored_words[word]=score
			#we delete everything in the used letters so we can start over
			used_letters = []
		return self._bucketize(self.scored_words)

	def _bucketize(self,info_dict):
		'''
			makes the info_dict into a dictionary with buckets containing 10 results each
		'''
		#we create the bucketized dict , key = bucket number, value = dict(key=word,value=score)
		to_return = OrderedDict()
		#we get the keys
		keys = info_dict.keys()
		#we check the number of buckets we should create
		buckets = len(info_dict) / 10
		#we loop over the number of buckets
		for index in xrange(buckets):
			#if buckets is  >= 1 then we are sure that there are atleast 10 items
			for x in xrange(10):
				try:
					to_return[index][keys[x]] = info_dict[keys[x]]
				except KeyError:
					to_return[index] = OrderedDict()
					to_return[index][keys[x]] = info_dict[keys[x]]
			#on every loop we make keys 10 items shorter
			keys = keys[10:]

		#if there are still items in list, meaning that they are less than 10
		if keys:
			#we set last key to 1 if the whole result is less than 10
			if buckets == 0:
				last_key = 1
			#or to the last bucket + 1
			else:
				last_key = max(to_return.keys())+1
			to_return[last_key] = OrderedDict()
			for key in keys:
				to_return[last_key][key] = info_dict[key]
		return to_return

	def sort(self,sort_by):
		''' sorts the results by word or by score '''

		if sort_by == 'word':
			#we create a dictionary to hold key=word length, value = list of words with that len
			sorted_len_dict = OrderedDict()
			#we get the words
			keys_to_sort = self.scored_words.keys()
			#creating a set to held the different lens
			key_lens = set((len(x) for x in keys_to_sort))
			current_len = min(key_lens)
			max_len = max(key_lens)
			while current_len <= max_len:
				for key in keys_to_sort:
					if len(key) == current_len:
						try:
							sorted_len_dict[current_len].append(key)
						except KeyError:
							sorted_len_dict[current_len] = [key]
				current_len += 1

			#create an ordered dict to hold the actual sorted words and their scores
			sorted_dict = OrderedDict()
			for key,value in sorted_len_dict.items():
				for val in sorted(value):
					sorted_dict[val] = self.scored_words[val]
			return self._bucketize(sorted_dict)

		elif sort_by == 'score':
			#dict to be returned
			to_return = OrderedDict()
			#instanciate a list
			keys = self.scored_words.values()
			keys.sort()
			while keys:
				for key in self.scored_words:
					if not keys:
						break
					if self.scored_words[key] == keys[0]:
						to_return[key] = self.scored_words[key]
						keys.pop(0)
			return self._bucketize(to_return)

	def _get_score(self,word):
		score = 0
		for letter in word:
			score += self.scores[letter]
		return score

	def get_def(self,word):
		endpoint = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key={}'.format(word,self.api_key)
		result = requests.get(endpoint)
		result = result.text.encode('utf-8')
		result = self.parser.parse(result)
		return result


if __name__=='__main__':
	solver = ScrabbleSolver('sowpods.txt')
	file_to_write = file('test.txt',mode='w')
	file_to_write.write(solver.get_def('aa'))
	file_to_write.close()
	#print solver.get_def('aa').count('<entry ',65)