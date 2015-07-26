import Tkinter as tk
import tkMessageBox as mb
import tkFileDialog as fd
from srabble import ScrabbleSolver
import excep as ex

class Gui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):

		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.cheater = ScrabbleSolver()

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		self.main_display = tk.Frame(self)
		self.button_display = tk.Frame(self.main_display)
		self.results_display = tk.Frame(self.main_display)
		self.ref_display = tk.Frame(self.main_display)

		self.ref_check = False

		self.entry_var = tk.StringVar()

		self.main()

	def main(self):
		self.main_display.pack()
		self.main_display.config()
		self.button_display.pack(anchor='n')
		tk.Entry(self.button_display, textvariable=self.entry_var ).grid(row=0,column=0)
		tk.Button(self.button_display,text='Check',command=lambda : self.packer(self.results_display,self.check_results)).grid(row=0,column=1)
		tk.Button(self.button_display,text='Quit',command=self.quit).grid(row=0,column=2)

	def quit(self):
		self.master.quit()

	def packer(self,to_unpack,to_pack,optional=None):
		if optional:
			for child in optional.winfo_children():
				child.destroy()
			optional.pack_forget()
		for child in to_unpack.winfo_children():
			child.destroy()
		to_unpack.pack_forget()
		to_pack()

	def check_results(self):
		if self.ref_check:
			for child in self.ref_display.winfo_children():
				child.destroy()
			self.ref_display.pack_forget()
			self.ref_check = False
		try:
			self.results = self.cheater.check_rack(self.entry_var.get())
			self.current_bucket = min(self.results.keys())
			self.packer(self.results_display,self.update_sumary)
		except ex.IncorrectRack as e:
			mb.showwarning('Incorrect Rack', 'The rack you provided contains digits or is empty: \n\n%s' % e.rack)

		

	def update_sumary(self):
		self.results_display.pack()
		self.results_display.config(relief='sunken',bd=2)
		tk.Button(self.results_display,text='>',command = lambda : self.go_right('bucket')).grid(row=12,column=6)
		tk.Button(self.results_display,text='<',command = lambda : self.go_left('bucket')).grid(row=12,column=5)

		tk.Button(self.results_display,text='Word',width=15,command = lambda : self.sort('word')).grid(row=0,column=1)
		tk.Button(self.results_display,text='Score',width=8,command = lambda : self.sort('score')).grid(row=0,column=2)
		tk.Label(self.results_display,text='',width=8).grid(row=0,column=3)
		tk.Label(self.results_display,text='').grid(row=1,column=1)
		tk.Button(self.results_display,text='Word',width=15,command = lambda : self.sort('word')).grid(row=0,column=4)
		tk.Button(self.results_display,text='Score',width=8,command = lambda : self.sort('score')).grid(row=0,column=5)
		tk.Label(self.results_display,text='',width=8).grid(row=0,column=6)


		bucket = self.results[self.current_bucket]
		keys = bucket.keys()
		if self.current_bucket+1 in self.results.keys():
			bucket2 = self.results[self.current_bucket+1]
		else:
			bucket2 = None
		
		if bucket2:
			keys2 = bucket2.keys()
		for i in xrange(len(keys)):
			row = i + 2
			tk.Label(self.results_display,text=keys[i]).grid(row=row,column=1)
			tk.Label(self.results_display,text=bucket[keys[i]]).grid(row=row,column=2)
			tk.Button(self.results_display,text = 'Ref',command=lambda word = keys[i] : self.display_ref(word)).grid(row=row,column=3)
			if bucket2:
				try:
					tk.Label(self.results_display,text=keys2[i]).grid(row=row,column=4)
					tk.Label(self.results_display,text=bucket2[keys2[i]]).grid(row=row,column=5)
					tk.Button(self.results_display,text = 'Ref',command = lambda word = keys2[i] : self.display_ref(word)).grid(row=row,column=6)
				except IndexError:
					pass
		

	def go_right(self,option):
		if option == 'bucket':
			if self.current_bucket + 1 >= max(self.results.keys()):
				return
			else:
				self.current_bucket += 1
				self.packer(self.results_display,self.update_sumary)
		elif option == 'key':
			if self.current_key != self.ordered_keys[-1]:
				self.current_key = self.ordered_keys[self.ordered_keys.index(self.current_key) + 1]
				self.packer(self.ref_display,self.update_ref)
			else:
				return

	def go_left(self,option):
		if option == 'bucket':
			if self.current_bucket - 1 < min(self.results.keys()):
				return
			else:
				self.current_bucket -= 1
				self.packer(self.results_display,self.update_sumary)
		elif option == 'key':
			if self.current_key != self.ordered_keys[0]:
				self.current_key = self.ordered_keys[self.ordered_keys.index(self.current_key) - 1]
				self.packer(self.ref_display,self.update_ref)
			else:
				return

	def sort(self,sort_by):
		self.results = self.cheater.sort(sort_by)
		self.current_bucket = min(self.results.keys())	
		self.packer(self.results_display,self.update_sumary)

	def display_ref(self,word):
		self.ref_check = True
		try:
			self.ref_dict = self.cheater.get_def(word)
			print self.ref_dict
			self.ordered_keys = self.ref_dict.keys()
			self.current_key = self.ordered_keys[0]
			self.packer(self.ref_display,self.update_ref,self.results_display)
		except ex.NoFreeLunch:
			mb.showwarning('Error','Sorry, the word exists but the free online dictionary has limits, so we couldn\'t fetch the definition')
		

	def update_ref(self):
		self.ref_display.pack()
		self.ref_display.config(relief = 'sunken',bd=2)
		self.change_button_frame = tk.Frame(self.ref_display)
		self.change_button_frame.grid(row=3,column=1)
		tk.Label(self.ref_display, text='Word',width=20).grid(row=0,column=0)
		tk.Label(self.ref_display,text ='Sentence part',width=20).grid(row=1,column=0)
		tk.Label(self.ref_display,text= 'Meaning',width=20).grid(row=2,column=0)
		tk.Label(self.ref_display,text= self.ref_dict[self.current_key]['ew'],width=50).grid(row=0,column=1)
		tk.Label(self.ref_display,text= self.ref_dict[self.current_key]['sentence_part'],width=50).grid(row=1,column=1)
		tk.Button(self.change_button_frame,text='<',command = lambda : self.go_left('key')).grid(row=0,column=0)
		tk.Button(self.change_button_frame,text='>',command = lambda : self.go_right('key')).grid(row=0,column=1)
		tk.Button(self.ref_display,text='Back',command = self.back_ref).grid(row=3,column=0)
		meaning = tk.Text(self.ref_display)
		meaning.config(width=50,relief='raised',height=17,wrap='word')
		meaning.insert('end',self.ref_dict[self.current_key]['sn'])
		meaning.config(state='disabled')
		meaning.grid(row=2,column=1)

	def back_ref(self):
		self.packer(self.ref_display,self.update_sumary)

if __name__=='__main__':
	p = Gui()
	p.mainloop()