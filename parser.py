class XMLParser(object):

	def __init__(self):
		self.def_dict = {}

	def parse(self,string):
		string = string[69:]
		while string:
			start_index = string.find('<entry ')
			end_index = string.find('</entry>')+8
			entry = string[start_index:end_index]
			self.handle_entry(entry)
			string = string[end_index:]
		return self.def_dict


	def handle_entry(self,string):
		id_start = string.find('id="')+4
		id_end = string.find('"',id_start)
		current_entry = string[id_start:id_end]
		if current_entry:
			self.def_dict[current_entry] = {}

			#<ew>
			ew_start = string.find('<ew>')
			ew_end = string.find('</ew>')
			if ew_start != -1:
				self.def_dict[current_entry]['ew'] = string[ew_start+4:ew_end]
			
			#<pr>
			pron_start = string.find('<pr>')
			pron_end = string.find('</pr>')
			if pron_start != -1:
				self.def_dict[current_entry]['pron'] = string[pron_start+4:pron_end]

			#<fl>
			sentance_part_start = string.find('<fl>')
			sentance_part_end = string.find('</fl>')
			if sentance_part_start != -1:
				self.def_dict[current_entry]['sentance_part'] = string[sentance_part_start+4:sentance_part_end]

			#<def>
			def_start = string.find('<def>')
			def_end = string.find('</def>')
			def_str = string[def_start+5:def_end]
			self.handle_def(def_str,current_entry)
		return

	def handle_def(self,def_tag,current_entry):
		while def_tag:
			sn_start = def_tag.find('<sn>')
			sn_end = def_tag.find('</sn>')
			if sn_start != -1:
				sn = def_tag[sn_start+4:sn_end]
				if len(sn) > 1:
					self.parent = sn[0]
				if sn.isdigit():
					self.handle_sn(def_tag[sn_start:def_tag.find('</dt>')+5],current_entry)
				else:
					self.handle_sn(def_tag[sn_start:def_tag.find('</dt>')+5],current_entry,self.parent)
				sn_end = def_tag.find('</sn>',sn_end)
				if sn_end != -1:
					def_tag = def_tag[def_tag.find('</dt>') + 5:]
				else:
					def_tag = ''
			else:
				self.def_dict[current_entry]['sn0'] = def_tag[def_tag.find('<dt>')+4:def_tag.find('</dt>')]
				def_tag = ''

	def handle_sn(self,sn,current_entry,parent=None):
		key = sn[sn.find('<sn>')+4:sn.find('</sn>')]
		if len(key) > 1:
			key = key[-1]
		if parent:
			try:
				self.def_dict[current_entry]['sn{}'.format(parent)].append((key,sn[sn.find('<dt>')+4:sn.find('</dt>')]))
			except KeyError:
				self.def_dict[current_entry]['sn{}'.format(parent)] = [(key,sn[sn.find('<dt>')+4:sn.find('</dt>')])]
		else:
			self.def_dict[current_entry]['sn{}'.format(key)] = sn[sn.find('<dt>')+4:sn.find('</dt>')]




if __name__ =='__main__':
	parser = XMLParser()
	file_to_read = open('test.txt')
	parser.parse(file_to_read.read())
	for item in  parser.def_dict.items():
		print item
		print
	file_to_read.close()