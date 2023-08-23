#-----------------MILESTONE PROJEKT 2 4. próbálkozás ----------------------
#Blackjack simplified, (only hold and get card, with banking, dealer compupter)

#Keveréshez
from random import shuffle
import os
clear = lambda: os.system('cls')

#Kártya, Pakli system

#Predefiniált kártyák, ezekből keveri a paklit
playing = True
szinek = ("Treff", "Káró", "Kör", "Pikk") 
szamok = ("Kettő", 'Három', 'Négy', 'Öt', "Hat", 'Hét', 'Nyolc', 'Kilenc', 'Tíz', 'Jumbó', 'Dáma', 'Király', 'Ász')
ertekek = {'Kettő':2, 'Három':3, 'Négy':4, 'Öt':5, "Hat":6, 'Hét':7, 'Nyolc':8, 'Kilenc':9, 'Tíz':10, 'Jumbó':10, 'Dáma':10, 'Király':10, 'Ász':11}
#---Classok---

#Létrehoz egy objectet bármilyen 2 strinngel argumentumként
#Ki is lehet printelni a kártyát, ez 1db kártya létrehozása
class Kartya_Letrehoz:
    def __init__(self,szin,szam):
        self.szin = szin #Self attributum lesz a beadott argumentumbol
        self.szam = szam
    def __str__(self):
        return self.szin +' '+ self. szam
    
    
#Pakli létrehozó, üres listához rakja hozzá a predeffelt kártyákat a 
#kártya létrehozóval, így lesz 52 lapos pakli, amit utána azonnal kever

class Pakli_Letrehoz:
    def __init__(self):
        self.pakli_kartya = []
        for i in szinek:
            for j in szamok:
                #Előző classt használva csinál 52 db objectet listába
                self.pakli_kartya.append(Kartya_Letrehoz(i,j))
    
    def kever(self):
        #Nem returnol semmit, eredetit keveri össze
        shuffle(self.pakli_kartya)
                
    #Osztás
    def osztas(self):
        return self.pakli_kartya.pop()
    
    
class Jatekos_Letrehoz:
    #Játékos kezébe mi van
    def __init__(self):
        self.kez = []
        self.ertek = 0
        self.aszok = 0
        
    def add_card(self,kartya):
        #ide kartya objectet var, akkor tud leosztani jol
        # player.add_card(huzott_kartya) 
        #huzott_kartya = test_pakli.osztas()
        self.kez.append(kartya)
        self.ertek = self.ertek + ertekek[kartya.szam]
        if kartya.szam == 'Ász':
            self.aszok += 1
    
    def adjust_for_ace(self):
        #if total value > 21 and still have ace
        # akkor change my ace to be 1 instead of 11
        while self.ertek > 21 and self.aszok: # == True
            self.ertek -= 10
            self.aszok -=1
            
#Bank system
class Szamla_Letrehoz:
    
    def __init__(self,osszeg=100): #Default 0, ha nem adunk meg argumentumot
        self.osszeg = osszeg
        self.bet = 0
    def __str__(self):
        return f'Egyenleg: {self.osszeg}$'
    
    #Összeg növelés
    def win_bet(self):
        self.osszeg += self.bet 
        
    #Összeg csökkentés
    def lose_bet(self):
        self.osszeg -= self.bet 
             
#---Functions---

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input(f"Egyenleg:{chips.osszeg} Mennyit szeretnél felrakni? "))
        except:
            print('Számot adj meg!')
        else: 
            if chips.bet > chips.osszeg:
                print(f'Ennyid nincs. :( Egyenleg: {chips.osszeg}')
            else:
                break
                
#Összerakja a jatekos_letrehoz() és pakli_letrehoz() osztását egy fv-be                
def hit(pakli,jatekos):
    single_card = pakli.osztas()
    jatekos.add_card(single_card)
    jatekos.adjust_for_ace()
    
def hit_or_stand(pakli,jatekos):
    global playing # külső while loop kontrollra
    
    while True:
        x = input('Kérsz még lapot? (y/n) ')
        if x.lower() == 'y':
            hit(pakli,jatekos)
        elif x.lower() == 'n':
            print("Nincs több lap, osztó jön.")
            playing = False
        elif x == 'kaszas':
            print('A KIBASZOTT SZEMEM FÉNYE!!!*half life crash noise*')
            continue
            
        elif x == 'kowi':
            print(' |\__/,|    ( \ ')
            print(' |_ _  |.--.) )')
            print(' ( T   )     /')
            print('(((^_(((/(((_/')
            continue
        elif x == 'nick':
            print('Haha én csináltam a sok easter egget :) De nincs több -.-" ')
            continue
        else: 
            print("Igen vagy Nem? (y/n)")
            continue #vissza az elejére, break nem fut le
        break
        
#kártya megjelenítés:        
def show_some(player,dealer):
    #csak 1 osztó kártya látható
    clear()
    print('\n Osztó kártyái: ')
    print('Első kártya rejtett')
    print(dealer.kez[1])
    #értékek kiírása
    print(f"Osztó kártyáinak összege: ?")
    
    #player 2 kártyát mutat
    print('\n Játékos kártyái: ')
    for card in player.kez:
        print(card)
    #értékek kiírása
    print(f"Játékos kártyáinak összege: {player.ertek}")
        
def show_all(player,dealer):
    #minden kártya látható osztónak
    clear()
    print('\n Osztó kártyái: ')
    for card in dealer.kez:
        print(card)
    #értékek kiírása
    print(f"Osztó kártyáinak összege: {dealer.ertek}")
    #minden kártya látható playernek
    print('\n Játékos kártyái: ')
    for card in player.kez:
        print(card)
    #értékek kiírása
    print(f"Játékos kártyáinak összege: {player.ertek}")

#Nyerési kondíciók    
    
def player_bust(player,dealer,chips):
    print("Vesztettél, több mint 21.")
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print("Nyertél")
    chips.win_bet()
def dealer_bust(player,dealer,chips):
    print("Nyertél. Osztó túlment 21-en")
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print("Osztó nyert")
    chips.lose_bet()
def push(player,dealer):
    print("Döntetlen")
    
    #easter egg a menniyt akarsz feltennire kaszas: kibaszott szemem fénye

    
    
#--- Game Logic--- 
#Számla itt van mert ha bent van kör elején újratermeli a pénzt.
szamla = Szamla_Letrehoz() # No argument default: 100
#Opening Screen
while True:
    print("Üdv a FloydJack játékban")

    #Pakli létrehoz, kever és 2-2 lapot oszt mindenkinek
    pakli = Pakli_Letrehoz()
    pakli.kever()

    player_hand = Jatekos_Letrehoz()
    #Osztás: Jatekos_letrehoz() classból az add_card methoddal
    #osztunk ami egy card objectet vár argumentumnak, ez pedig a pakli.osztas
    #Pakli_Lertrehoz osztas methodja, ami a legfelső lapot leszedni 
    #és visszareturnol 1 card objectet. 2x mert 2 lap kell
    player_hand.add_card(pakli.osztas())
    player_hand.add_card(pakli.osztas())
    #Dealernek osztunk ugyanígy

    dealer_hand = Jatekos_Letrehoz()
    dealer_hand.add_card(pakli.osztas())
    dealer_hand.add_card(pakli.osztas())

  
    #Tétek megadása
    take_bet(szamla)
    #Először mutatjuk a kártyákat:
    show_some(player_hand,dealer_hand)
    
    while playing: #hit_or_stand fv-ben definiáltuk 

        #Megkérdezzük kér e még lapot
        hit_or_stand(pakli,player_hand)
        #Megmutatjuk a részleges kártyákat
        show_some(player_hand,dealer_hand)

        #Ha player túlmegy 21 -en bust, és break
        if player_hand.ertek > 21:
            player_bust(player_hand,dealer_hand,szamla)
            break

    #Ha Player nem ment túl 21-en, addig oszt magának az osztó
    #amíg 17et el nem éri
    if player_hand.ertek <= 21:
        
        while dealer_hand.ertek < player_hand.ertek: #Addig megy amíg nem lesz több
            hit(pakli,dealer_hand)

        #mindent mutat
        show_all(player_hand,dealer_hand)

        if dealer_hand.ertek > 21: #túlment az osztó
            dealer_bust(player_hand,dealer_hand,szamla)

        elif dealer_hand.ertek > player_hand.ertek: # nyer az osztó
            dealer_wins(player_hand,dealer_hand,szamla)
        elif dealer_hand.ertek < player_hand.ertek:
            player_wins(player_hand,dealer_hand,szamla)
        else:
            push(player_hand,dealer_hand)

    #Egyenleg megmutatása
    print(f'\n Egyenleg: {szamla.osszeg}')
    #Új játék?
    new_game = input('Akarsz még 1 kört játszani? (y/n)')

    if new_game == 'y':
        clear()
        playing = True
        
    else:
        print('Köszi a játékot!')
        break