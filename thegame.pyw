from Tkinter import *
import tkMessageBox
from random import randint

counter = 0

class GU1:

	
	def __init__(self, master):
		self.master=master
		master.title("THE GAME")
		self.buttons()
		
			
	def buttons(self):
		a = randint(0, 5)
		b = randint(0, 5)
		tuple_random = (a, b)
		for x in range (0, 6):
			for y in range (0, 6):
				column = x
				row = y
				self.button=Button(text="", command = lambda x = x, y = y: self.choice(x, y, tuple_random))
				self.button.grid(column=x, row=y, sticky = "NSEW" , pady=2, padx=2)
				self.button.config(height = 0, width=2)
		self.new_game=Button(text="NEW GAME", command = lambda: self.buttons())
		self.new_game.grid(column=6, row = 0, sticky ="NSEW", pady =2, padx = 2)
		self.EXIT = Button(text="EXIT", command = lambda: self.master.destroy())
		self.EXIT.grid(column = 6, row = 1, sticky = "NSEW", pady = 2, padx = 2)
		
	
	def choice(self, x, y, tuple_random):
		global counter
		counter += 1
		tuple_choice = (x, y)
		if tuple_choice != tuple_random and counter < 7:
			self.button=Button(text="", relief="sunken")
			self.button.grid(column=x, row = y, sticky = "NSEW" , pady=2, padx=2)
		elif tuple_choice == tuple_random and counter < 7:
			self.button=Button(text="", bg= "red")
			self.button.grid(column=x, row = y, sticky = "NSEW" , pady=2, padx=2)
			self.victory = tkMessageBox.showinfo("VICTORY", "YOU HAVE WON!!!")
			counter = 0
			self.buttons()
		elif counter == 7:
			self.lost = tkMessageBox.showinfo("YOU LOST", "YOU LOST, LOSER!")
			counter = 0
			self.buttons()
	

root = Tk()
app = GU1(root)
root.mainloop()