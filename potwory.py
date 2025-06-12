


# Ten kod NAPEWNO NIE był kopiowany ze Stack Overflow !!!! :DDDDDDDD (serio)
# Nie wiem jak działa, ale działa
# Nie ruszać!!! 

# import wszystko_co_sie_da
# import palenie_glupa
# from internet import rozwiazanie
# from prosby import daj_pan_trzy

# if prezentacja_trwa:
#     print("Proszę nie pytać jak to działa")

# if prowadzacy_pyta
#   print("...")




























import random
import json
import os

def pobierz_sciezke_zapisu():
    return os.path.join(os.path.expanduser('~'), 'Desktop', 'zapis_gry.json')
zapisz_gre = pobierz_sciezke_zapisu()

dane_potworow = [
    {"nazwa": "Goblin", "hp": 30, "sila": 10},
    {"nazwa": "Wilk", "hp": 40, "sila": 12},
    {"nazwa": "Ork", "hp": 50, "sila": 15},
    {"nazwa": "Szkielet", "hp": 35, "sila": 11},
    {"nazwa": "Demon", "hp": 60, "sila": 18},
    {"nazwa": "Wykładowca", "hp": 50, "sila": 13}
]

def stworz_pasek_hp(aktualne_hp, max_hp, dlugosc_paska=20):
    if aktualne_hp < 0:
        aktualne_hp = 0


    procent = aktualne_hp / max_hp
    wypelnione_bloki = int(procent * dlugosc_paska)
    puste_bloki = dlugosc_paska - wypelnione_bloki
    
    pasek = '█' * wypelnione_bloki + '░' * puste_bloki
    
    if procent > 0.66:
        kolor = '\033[92m'  # Zielony
    elif procent > 0.33:
        kolor = '\033[93m'  # Żółty
    else:
        kolor = '\033[91m'  # Czerwony
    
    reset_koloru = '\033[0m'
    
    return f"{kolor}|{pasek}|{reset_koloru} {aktualne_hp}/{max_hp} HP"

def zapisz_stan(gracz):
    stan = {
        "imie": gracz.imie,
        "klasa": gracz.klasa,
        "poziom": gracz.poziom,
        "doswiadczenie": gracz.doswiadczenie,
        "hp": gracz.hp,
        "max_hp": gracz.max_hp,
        "mikstury": gracz.mikstury,
        "pokonane_potwory": list(gracz.pokonane_potwory)
    }
    try:
        with open(zapisz_gre, 'w', encoding='utf-8') as f:
            json.dump(stan, f, ensure_ascii=False, indent=4)
        print("💾 Stan gry zapisany.")
    except IOError:
        print("⚠️ Nie udało się zapisać stanu gry.")

def wczytaj_stan():
    try:
        with open(zapisz_gre, 'r', encoding='utf-8') as f:
            stan = json.load(f)
        gracz = Gracz(stan.get("imie"), stan.get("klasa", "Wojownik"))
        gracz.poziom = stan.get("poziom", 1)
        gracz.doswiadczenie = stan.get("doswiadczenie", 0)
        gracz.hp = stan.get("hp", gracz.hp)
        gracz.max_hp = stan.get("max_hp", 100)
        gracz.mikstury = stan.get("mikstury", gracz.mikstury)
        gracz.pokonane_potwory = set(stan.get("pokonane_potwory", []))
        print("📂 Zapis gry wczytany.")
        return gracz
    except (FileNotFoundError, json.JSONDecodeError):
        print("❗ Rozpoczynam nową grę.")
        return None

def wybierz_akcje():
    while True:
        wybor = input("1) 🗡️ Atakuj  2) 🧪 Mikstura  3)🏃 Uciekaj: ")
        if wybor in ('1', '2', '3'):
            return int(wybor)
        print("❗ Podaj 1, 2 lub 3!")

def awans(gracz):
    if gracz.doswiadczenie >= 100:
        gracz.poziom += 1
        gracz.doswiadczenie -= 100
        stare_max_hp = gracz.max_hp
        gracz.max_hp += 30
        gracz.hp += 30
        gracz.mikstury += 1
        print(f"🎉 Poziom {gracz.poziom}! Max HP: {stare_max_hp} -> {gracz.max_hp}, +1 mikstura")

class Gracz:
    def __init__(self, imie, klasa):
        self.imie = imie
        self.klasa = klasa
        self.poziom = 1
        self.doswiadczenie = 0
        self.hp = 100
        self.max_hp = 100
        self.mikstury = 3
        self.pokonane_potwory = set()

    def atak(self):
        return random.randint(10, 20)

    def wez_miksture(self):
        if self.mikstury > 0:
            self.hp = min(self.hp + 20, self.max_hp)
            self.mikstury -= 1
            print(f"💖 +20 HP, mikstur pozostało: {self.mikstury}")
            return True
        return False

class Potwor:
    def __init__(self, nazwa, hp, sila):
        self.nazwa = nazwa
        self.hp = hp
        self.max_hp = hp
        self.sila = sila

    def atak(self):
        return random.randint(5, self.sila)

def stworz_potwora():
    wyb = random.choice(dane_potworow)
    return Potwor(wyb["nazwa"], wyb["hp"], wyb["sila"])

def walka(gracz, potwor):
    print(f"\n⚔️  {potwor.nazwa} nadchodzi!")
    
    while potwor.hp > 0 and gracz.hp > 0:
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 50)
        print(f"⚔️  WALKA Z {potwor.nazwa.upper()}")
        print("=" * 50)
        
        print(f"\n👤 {gracz.imie} ({gracz.klasa}):")
        print(stworz_pasek_hp(gracz.hp, gracz.max_hp))
        
        print(f"\n👹 {potwor.nazwa}:")
        print(stworz_pasek_hp(potwor.hp, potwor.max_hp))
        
        print(f"\n🧪 Mikstury: {gracz.mikstury}")
        print(f"⭐ Poziom: {gracz.poziom} | XP: {gracz.doswiadczenie}/100")
        print("-" * 30)
        
        akcja = wybierz_akcje()
        
        if akcja == 1:
            dmg = gracz.atak()
            potwor.hp -= dmg
            print(f"\n🗡️ Zadajesz {dmg} obrażeń {potwor.nazwa}!")
            if potwor.hp < 0:
                potwor.hp = 0
        elif akcja == 2:
            if not gracz.wez_miksture():
                print("❗ Brak mikstur.")
                input("Naciśnij Enter, aby kontynuować...")
                continue
        else:
            print("🏃‍♂️ Uciekasz z walki!")
            return True
        
        if potwor.hp <= 0:
            break
            
        dmg = potwor.atak()
        gracz.hp -= dmg
        print(f"💥 {potwor.nazwa} zadaje Ci {dmg} obrażeń!")
        if gracz.hp < 0:
            gracz.hp = 0
        
        input("\nNaciśnij Enter, aby kontynuować...")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if gracz.hp <= 0:
        print("💀 Zginąłeś.")
        return False
    
    print(f"✅ Pokonujesz {potwor.nazwa}!")
    gracz.pokonane_potwory.add(potwor.nazwa)
    gracz.doswiadczenie += 20
    print("✨ +20 XP")
    awans(gracz)
    return True

def utworz_gracza():
    imie = input("Podaj imię postaci: ").strip()
    while not imie:
        print("❗ Imię nie może być puste.")
        imie = input("Podaj imię postaci: ").strip()
    print("Wybierz klasę: 1) Wojownik  2) Mag  3) Łucznik")
    while True:
        wybor = input("Klasa (1-3): ")
        if wybor in ('1', '2', '3'):
            break
        print("❗ Podaj 1, 2 lub 3.")
    klasy = {"1": "Wojownik", "2": "Mag", "3": "Łucznik"}
    gracz = Gracz(imie, klasy[wybor])
    print(f"👤 Witaj, {gracz.imie} ({gracz.klasa})!")
    print(stworz_pasek_hp(gracz.hp, gracz.max_hp))
    return gracz

def menu_glowne():
    print("=== MENU GŁÓWNE ===")
    print("1) Nowa gra\n2) Wczytaj grę\n3) Wyjdź")
    while True:
        wybor = input("Opcja (1-3): ")
        if wybor in ('1', '2', '3'):
            return int(wybor)
        print("❗ Podaj 1, 2 lub 3.")

def glowna():
    opcja = menu_glowne()
    if opcja == 3:
        print("🔚 Do zobaczenia!")
        return
    if opcja == 2:
        gracz = wczytaj_stan() or utworz_gracza()
    else:
        gracz = utworz_gracza()
    while gracz.hp > 0:
        potwor = stworz_potwora()
        if not walka(gracz, potwor):
            break
        zapisz_stan(gracz)
        print(f"🏆 Pokonane: {list(gracz.pokonane_potwory)}")
        kontynuuj = input("Kontynuować? (t/n): ").lower()
        while kontynuuj not in ('t', 'n'):
            print("❗ Podaj 't' lub 'n'.")
            kontynuuj = input("Kontynuować? (t/n): ").lower()
        if kontynuuj != 't':
            print("🛑 Dzięki za grę!")
            break
    print("=== Koniec gry ===")

if __name__ == '__main__':
    glowna()
