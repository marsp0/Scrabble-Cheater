import Tkinter as tk
import tkMessageBox as mb
import tkFileDialog as fd
from srabble import ScrabbleSolver

class Gui(tk.Frame):

	def __init__(self,filename,parent=None,*args,**kwargs):

		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.cheater = ScrabbleSolver(filename)

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		self.main_display = tk.Frame(self)
		self.button_display = tk.Frame(self.main_display)
		self.results_display = tk.Frame(self.main_display)

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

	def packer(self,to_unpack,to_pack):
		for child in to_unpack.winfo_children():
			child.destroy()
		to_pack()

	def check_results(self):
		self.results = self.cheater.check_rack(self.entry_var.get())
		self.current_bucket = min(self.results.keys())
		self.packer(self.results_display,self.update_sumary)

	def update_sumary(self):
		self.results_display.pack()
		self.results_display.config(relief='sunken',bd=2)
		tk.Button(self.results_display,text='>',command = self.go_right).grid(row=12,column=6)
		tk.Button(self.results_display,text='<',command = self.go_left).grid(row=12,column=5)

		tk.Button(self.results_display,text='Word',width=15,command = lambda : self.sort('word')).grid(row=0,column=1)
		tk.Button(self.results_display,text='Score',width=8,command = lambda : self.sort('score')).grid(row=0,column=2)
		tk.Label(self.results_display,text='',width=8).grid(row=0,column=3)
		tk.Label(self.results_display,text='').grid(row=1,column=1)
		tk.Button(self.results_display,text='Word',width=15,command = lambda : self.sort('word')).grid(row=0,column=4)
		tk.Button(self.results_display,text='Score',width=8,command = lambda : self.sort('score')).grid(row=0,column=5)
		tk.Label(self.results_display,text='',width=8).grid(row=0,column=6)


		try:
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
				tk.Button(self.results_display,text = 'Ref',command=lambda word = keys[i] : self.get_ref(word)).grid(row=row,column=3)
				if bucket2:
					try:
						tk.Label(self.results_display,text=keys2[i]).grid(row=row,column=4)
						tk.Label(self.results_display,text=bucket2[keys2[i]]).grid(row=row,column=5)
						tk.Button(self.results_display,text = 'Ref',command = lambda word = keys2[i] : self.get_ref(word)).grid(row=row,column=6)
					except IndexError:
						pass
		except KeyError:
			mb.showwarning('No more words','No more words to be shown.')
			self.current_bucket = min(self.results.keys())
			self.packer(self.results_display,self.update_sumary)
		

	def go_right(self):
		if self.current_bucket + 1 >= max(self.results.keys()):
			return
		else:
			self.current_bucket += 1
			self.packer(self.results_display,self.update_sumary)

	def go_left(self):
		if self.current_bucket - 1 < min(self.results.keys()):
			return
		else:
			self.current_bucket -= 1
			self.packer(self.results_display,self.update_sumary)

	def sort(self,sort_by):
		self.results = self.cheater.sort(sort_by)
		self.current_bucket = min(self.results.keys())	
		self.packer(self.results_display,self.update_sumary)

	def get_ref(self, word):
		print self.cheater.get_def(word)
		

if __name__=='__main__':
	p = Gui('sowpods.txt')
	p.mainloop()