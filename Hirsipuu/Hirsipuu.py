import random
from tkinter import *

SANALISTA = ["PUU", "OMENA", "KALLO", "KOODI"]
AAKKOSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
SIZE = 6


class Hirsipuu:
    def __init__(self):
        self.sana = []
        self.random = random.choice(SANALISTA)
        self.oikea = []
        for i in self.random:
            self.oikea.append(i)
            self.sana.append(i)
        self.sanan_pituus = len(self.sana)
        self.salaus = []
        for i in range(self.sanan_pituus):
            self.salaus.append("-")

        self.window = Tk()
        self.window.geometry("+900+300")
        self.screen = Tk()
        self.screen.geometry("+500+300")
        

        self.lopetus = ""

        self.vaihe1 = PhotoImage(file="./Assets/Vaihe1.png")
        self.vaihe2 = PhotoImage(file="./Assets/Vaihe2.png")
        self.vaihe3 = PhotoImage(file="./Assets/Vaihe3.png")
        self.vaihe4 = PhotoImage(file="./Assets/Vaihe4.png")
        self.vaihe5 = PhotoImage(file="./Assets/Vaihe5.png")
        self.vaihe6 = PhotoImage(file="./Assets/Vaihe6.png")
        self.vaihe7 = PhotoImage(file="./Assets/Vaihe7.png")
        self.vaihe8 = PhotoImage(file="./Assets/Vaihe8.png")
        self.vaihe9 = PhotoImage(file="./Assets/Vaihe9.png")
        self.vaihe10 = PhotoImage(file="./Assets/Vaihe10.png")
        self.vaihe11 = PhotoImage(file="./Assets/Vaihe11.png")

        self.photos = [self.vaihe1, self.vaihe2, self.vaihe3, self.vaihe4, self.vaihe5, self.vaihe6,
                       self.vaihe7, self.vaihe8, self.vaihe9, self.vaihe10, self.vaihe11]

        self.ratkaisu = 0
        
        self.image = self.photos[self.ratkaisu]
        self.kuva = Label(self.window, image=self.image)
        self.kuva.grid(row=0, column=0)

        self.kirjaimet = Label(self.window, text=self.salaus, font=60)
        self.kirjaimet.grid(row=3, column=0, columnspan=2, sticky=W+E)

        self.quit_button = Button(self.screen, text="Quit", width=3, height=1, background="yellow",
                                  relief=RAISED, command=self.quit)
        self.quit_button.grid(row=8, column=0, columnspan=6, sticky=W+E)

        self.arvaus_button = Button(self.screen, text="Arvaa", relief=RAISED, background="dodgerblue", command=self.oikein)
        self.arvaus_button.grid(row=7, columnspan=2, column=0)

        self.arvaus = Entry(self.screen, width=10)
        self.arvaus.grid(row=7, columnspan=4, column=1)
        

        self.buttons = []
        self.commands = []

        for i in range(SIZE):
            self.buttons.append([None]*SIZE)
            self.commands.append([None]*SIZE)

        indeksi = 0
        for y in range(SIZE):
            for x in range(5):
                def button_press(x_coord=x, y_coord=y):
                    self.guess(x_coord, y_coord)

                self.commands[y][x] = button_press
                try:
                    new_button = Button(self.screen,
                                        text=f"{AAKKOSET[indeksi]}",
                                        width=3,
                                        height=2,
                                        command=button_press)
                    self.buttons[y][x] = new_button
                    new_button.grid(row=y, column=x)

                except IndexError:
                    continue

                indeksi += 1
        
        self.screen.mainloop()
        self.window.mainloop()
        if self.uudestaan_button:
            main()
        else:
            print("Goodbye!")

    def guess(self, x, y):
        activated_button = self.buttons[y][x]
        
        if activated_button.cget("text") in self.sana:
            activated_button.configure(background="green")
            maara = self.sana.count(activated_button.cget("text"))
            for i in range(maara):
                indeksi = self.sana.index(activated_button.cget("text"))
                self.sana[indeksi] = " "
                self.salaus[indeksi] = activated_button.cget("text")

                self.kirjaimet.configure(text=self.salaus)
                if "".join(self.salaus) == "".join(self.oikea):
                    self.voitto()
                    
        else:
            self.ratkaisu += 1
            activated_button.configure(background="red")
            self.kuva.configure(image=self.photos[self.ratkaisu])
            if self.ratkaisu > 9:
                self.havio()

    def voitto(self):
        self.lopetus = Label(self.window, text="You won!", font=60, background="green")
        self.lopetus.grid(row=2, column=0, columnspan=2, sticky=W + E)
        self.uudestaan_button = Button(self.window, text="Pelaa uudestaan!", font=60, background="yellow", height=1, command=self.uudestaan)
        self.uudestaan_button.grid(row=1, column=0, columnspan=2, sticky=W +E)
        

    def havio(self):
        self.lopetus = Label(self.window, text="You lost!", font=60, background="red")
        self.lopetus.grid(row=2, column=0, columnspan=2, sticky=W+E)
        self.uudestaan_button = Button(self.window, text="Pelaa uudestaan!", font=60, background="yellow", height=1, command=self.uudestaan)
        self.uudestaan_button.grid(row=1, column=0, columnspan=2, sticky=W+E)
        

    def oikein(self):
        teksti = self.arvaus.get()
        if teksti.upper() == "".join(self.oikea):
            self.salaus = self.oikea
        if "".join(self.salaus) == "".join(self.oikea):
            self.kirjaimet.configure(text=self.salaus)
            self.voitto()
        else:
            self.ratkaisu += 1
            self.kuva.configure(image=self.photos[self.ratkaisu])
            if self.ratkaisu > 9:
                self.havio()
            
    def uudestaan(self):
        self.screen.destroy()
        self.window.destroy()
        

    def quit(self):
        self.uudestaan_button = False
        self.screen.destroy()
        self.window.destroy()


def main():

    Hirsipuu()
    

if __name__ == "__main__":
    main()