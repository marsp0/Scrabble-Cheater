import re
import excep as ex

class XMLParser(object):

	def parse(self,string):
		self.def_dict = {}
		string = string[69:]
		if string.startswith('<suggestion>'):
			raise ex.NoFreeLunch()
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
				self.def_dict[current_entry]['sentence_part'] = string[sentance_part_start+4:sentance_part_end]
			else:
				self.def_dict[current_entry]['sentence_part'] = 'None'

			#<def>
			def_start = string.find('<def>')
			def_end = string.find('</def>')
			def_str = string[def_start+5:def_end]
			if def_start != -1:
				self.handle_def(def_str,current_entry)
			else:
				self.def_dict[current_entry]['sn'] = string[string.find('<dx>')+4:string.find('<dxt>')]+'"'+string[string.find('<dxt>')+5:string.find('</dxt>')]+'"'
			for key,value in self.def_dict[current_entry].items():
				if key == 'sn':
					self.handle_tags(current_entry,value)
		return

	def handle_def(self,def_tag,current_entry):
		self.def_dict[current_entry]['sn'] = ''
		while def_tag:
			sn_start = def_tag.find('<sn>')
			sn_end = def_tag.find('</sn>')
			if sn_start != -1:
				sn = def_tag[sn_start+4:sn_end]
				self.parent = None if len(sn) == 1 else sn[0]
				if sn.isdigit():
					self.handle_sn(def_tag[sn_start:def_tag.find('</dt>')+5],current_entry)
				elif sn.isalpha():
					if self.parent:
						self.def_dict[current_entry]['sn'] += '{} '.format(self.parent)
					self.handle_sn(def_tag[sn_start:def_tag.find('</dt>')+5],current_entry,self.parent)
				sn_end = def_tag.find('</sn>',sn_end)
				if sn_end != -1:
					def_tag = def_tag[def_tag.find('</dt>') + 5:]
				else:
					def_tag = ''
			else:
				to_add = def_tag[def_tag.find('<dt>')+4:def_tag.find('</dt>')]
				if to_add.startswith(':'):
					to_add = to_add[1:]
				self.def_dict[current_entry]['sn'] += '1: ' + to_add
				def_tag = ''

	def handle_sn(self,sn,current_entry,parent=None):
		key = sn[sn.find('<sn>')+4:sn.find('</sn>')]
		if len(key) > 1:
			key = key[-1]
		if parent:
			self.def_dict[current_entry]['sn'] += '{key}){value}\n'.format(key=key,value=sn[sn.find('<dt>')+4:sn.find('</dt>')])
		else:
			to_add = sn[sn.find('<dt>')+4:sn.find('</dt>')]
			if to_add.startswith(':'):
				to_add = to_add[1:]
			self.def_dict[current_entry]['sn'] += '{key}: {value}\n'.format(key=key,value=to_add)

	def handle_tags(self,current_entry,string):
		to_remove = re.findall('</?[a-z]*>',string)
		while to_remove:
			string = string[:string.find(to_remove[0])]+string[string.find(to_remove[0])+len(to_remove[0]):]
			to_remove.pop(0)
		self.def_dict[current_entry]['sn'] = string