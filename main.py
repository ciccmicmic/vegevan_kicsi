import pygame
import os
import random

# Pygame es a mixer inicializalasa
pygame.init()
pygame.mixer.init()  # Hangmixer inicializalasa

# --- Eszkozbetoltes (Hangok) ---
try:
    ugras_hang = pygame.mixer.Sound("Assets/Sounds/jump.wav")
    guggolas_hang = pygame.mixer.Sound("Assets/Sounds/duck.wav")
    utkozes_hang = pygame.mixer.Sound("Assets/Sounds/collision.wav")
    penz_hang = pygame.mixer.Sound("Assets/Sounds/coin.wav") # Penz (korabban felho) hangja
    jatek_vege_hang = pygame.mixer.Sound("Assets/Sounds/game_over.wav")
    pygame.mixer.music.load("Assets/Sounds/background_music.mp3")
    pygame.mixer.music.play(-1)  # Hatterzene lejatszasa vegtelenitve
except pygame.error as hiba_hangbetoltes:
    print(f"Hiba a hangfajlok betoltesekor: {hiba_hangbetoltes}")
    raise SystemExit("Hianyzo hangfajlok. Kerlek ellenorizd az 'Assets/Sounds' konyvtarat.")
except FileNotFoundError as hiba_fajlnemtalalhato_hang:
    print(f"Hiba a hangfajl megnyitasakor: {hiba_fajlnemtalalhato_hang}")
    raise SystemExit("Hianyzo hangfajl. Kerlek ellenorizd az 'Assets/Sounds' konyvtarat.")

# --- Globalis Konstansok ---
KEPERNYO_MAGASSAG = 600
KEPERNYO_SZELESSEG = 1100
KEPERNYO = pygame.display.set_mode((KEPERNYO_SZELESSEG, KEPERNYO_MAGASSAG))
pygame.display.set_caption("Vége van kicsi")  # Ablak cimenek beallitasa

# --- Eszkoztarolas (Kepek) ---
FUTO_KEPEK = []
UGRO_KEP = None
GUGGOLO_KEPEK = []
KIS_AVOKADO_KEPEK = []
NAGY_AVOKADO_KEPEK = []
HELI_KEPEK = []
PENZ_KEP = None
HATTER_KEP = None
KEZDOOLDAL_KEP = None

# --- Eszkozbetoltes (Kepek) ---
try:
    FUTO_KEPEK = [
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorRun1.png")),
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorRun2.png")),
    ]
    UGRO_KEP = pygame.image.load(os.path.join("Assets/Viktor", "ViktorJump.png"))
    GUGGOLO_KEPEK = [
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorDuck1.png")),
        pygame.image.load(os.path.join("Assets/Viktor", "ViktorDuck2.png")),
    ]
    KIS_AVOKADO_KEPEK = [
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado1.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado2.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "SmallAvocado3.png")),
    ]
    NAGY_AVOKADO_KEPEK = [
        pygame.image.load(os.path.join("Assets/Avocado", "LargeAvocado1.png")),
        pygame.image.load(os.path.join("Assets/Avocado", "LargeAvocado2.png")),
    ]
    HELI_KEPEK = [
        pygame.image.load(os.path.join("Assets/Heli", "Heli1.png")),
        pygame.image.load(os.path.join("Assets/Heli", "Heli2.png")),
    ]
    PENZ_KEP = pygame.image.load(os.path.join("Assets/Other", "Cloud.png")) # Az eredeti kepfajl neve "Cloud.png" marad
    HATTER_KEP = pygame.image.load(os.path.join("Assets/Other", "background.png"))
    KEZDOOLDAL_KEP = pygame.image.load(os.path.join("Assets/Other", "landingpage.png"))
except pygame.error as hiba_kepbetoltes:
    print(f"Hiba a kepfajlok betoltesekor: {hiba_kepbetoltes}")
    raise SystemExit("Hianyzo kepfajlok. Kerlek ellenorizd az 'Assets' konyvtarat.")
except FileNotFoundError as hiba_fajlnemtalalhato_kep:
    print(f"Hiba a kepfajl megnyitasakor: {hiba_fajlnemtalalhato_kep}")
    raise SystemExit("Hianyzo kepfajl. Kerlek ellenorizd az 'Assets' konyvtarat.")


class ViktorSaurus: # Korabban Viktosaur
    """
    A jatekos karakteret, ViktorSaurus-t reprezentalja.
    Kezeli a mozgasat (futas, ugras, guggolas) es animaciojat.
    """
    X_POZ = 80
    Y_POZ = 310
    Y_POZ_GUGGOLAS = 340
    UGRAS_ALAP_SEBESSEG = 8.5 # Konstans ugrasi sebesseg
    TALAJ_SZINT = 380

    def __init__(self):
        """Inicializalja a ViktorSaurus karaktert."""
        self.guggolo_kep_lista = GUGGOLO_KEPEK
        self.futo_kep_lista = FUTO_KEPEK
        self.ugro_alap_kep = UGRO_KEP # egyetlen kep az ugrashoz

        self.guggol_allapot = False
        self.fut_allapot = True
        self.ugrik_allapot = False

        self.lepes_index = 0
        self.aktualis_ugras_sebesseg = self.UGRAS_ALAP_SEBESSEG
        self.kep = self.futo_kep_lista[0] # Aktualisan megjelenitendo kep
        self.terulet = self.kep.get_rect() # A karakter terulete (pozicio es meret)
        self.terulet.x = self.X_POZ
        self.terulet.y = self.Y_POZ
        self.maszk = pygame.mask.from_surface(self.kep) # Pixel-pontos utkozeshez

    def frissites(self, felhasznaloi_bevitel):
        """Frissiti ViktorSaurus allapotat a felhasznaloi bevitel alapjan."""
        if self.guggol_allapot:
            self.guggol()
        elif self.fut_allapot:
            self.fut()
        elif self.ugrik_allapot:
            self.ugras()

        if self.lepes_index >= 10:
            self.lepes_index = 0

        if felhasznaloi_bevitel[pygame.K_UP] and not self.ugrik_allapot:
            self.guggol_allapot = False
            self.fut_allapot = False
            self.ugrik_allapot = True
            ugras_hang.play()
        elif felhasznaloi_bevitel[pygame.K_DOWN] and not self.ugrik_allapot:
            self.guggol_allapot = True
            self.fut_allapot = False
            self.ugrik_allapot = False
            guggolas_hang.play()
        elif not (self.ugrik_allapot or felhasznaloi_bevitel[pygame.K_DOWN]):
            self.guggol_allapot = False
            self.fut_allapot = True
            self.ugrik_allapot = False

    def guggol(self):
        """Kezeli a guggolas animaciojat es allapotat."""
        self.kep = self.guggolo_kep_lista[self.lepes_index // 5]
        self.terulet = self.kep.get_rect()
        self.terulet.x = self.X_POZ
        self.terulet.y = self.Y_POZ_GUGGOLAS
        self.lepes_index += 1
        self.maszk = pygame.mask.from_surface(self.kep)

    def fut(self):
        """Kezeli a futas animaciojat es allapotat."""
        self.kep = self.futo_kep_lista[self.lepes_index // 5]
        self.terulet = self.kep.get_rect()
        self.terulet.x = self.X_POZ
        self.terulet.y = self.Y_POZ
        self.lepes_index += 1
        self.maszk = pygame.mask.from_surface(self.kep)

    def ugras(self):
        """Kezeli az ugrasi muveletet es fizikat."""
        self.kep = self.ugro_alap_kep
        if self.ugrik_allapot:
            self.terulet.y -= self.aktualis_ugras_sebesseg * 4
            self.aktualis_ugras_sebesseg -= 0.8
            if self.terulet.y >= self.TALAJ_SZINT - self.kep.get_height():
                self.terulet.y = self.TALAJ_SZINT - self.kep.get_height()
                self.ugrik_allapot = False
                self.aktualis_ugras_sebesseg = self.UGRAS_ALAP_SEBESSEG
        elif not self.ugrik_allapot:
             self.terulet.y = self.TALAJ_SZINT - self.kep.get_height()
        self.maszk = pygame.mask.from_surface(self.kep)

    def rajzol(self, rajzfelulet):
        """Kirajzolja ViktorSaurus-t a megadott feluletre."""
        rajzfelulet.blit(self.kep, (self.terulet.x, self.terulet.y))


class Penz: # Korabban Cloud
    """Egy penz objektumot reprezental, amelyet pontokert lehet osszegyujteni."""
    def __init__(self):
        """Inicializal egy penz objektumot."""
        self.kep = PENZ_KEP
        self.szelesseg = self.kep.get_width()
        self.x_poz = KEPERNYO_SZELESSEG + random.randint(800, 1000)
        self.y_poz = random.randint(100, 150)
        self.terulet = self.kep.get_rect(topleft=(self.x_poz, self.y_poz))
        self.maszk = pygame.mask.from_surface(self.kep)
        self.lathato = True

    def frissites(self, aktualis_jatek_sebesseg):
        """Frissiti a penz poziciojat."""
        if self.lathato:
            self.x_poz -= aktualis_jatek_sebesseg * 0.5
        
        if self.x_poz < -self.szelesseg:
            if not self.lathato :
                self.x_poz = KEPERNYO_SZELESSEG + random.randint(2500, 3000)
                self.y_poz = random.randint(50, 100)
                self.lathato = True
            elif self.lathato:
                 self.x_poz = KEPERNYO_SZELESSEG + random.randint(2500, 3000)
                 self.y_poz = random.randint(50, 100)

        self.terulet.x = int(self.x_poz)
        self.terulet.y = int(self.y_poz)

    def rajzol(self, rajzfelulet):
        """Kirajzolja a penzt, ha lathato."""
        if self.lathato:
            rajzfelulet.blit(self.kep, (self.x_poz, self.y_poz))


class Akadaly: # Korabban Obstacle
    """Alap osztaly a jatekban talalhato osszes akadaly szamara."""
    def __init__(self, kep_lista, akadaly_tipus_index):
        self.kep_lista = kep_lista
        self.akadaly_tipus_index = akadaly_tipus_index
        self.kep = self.kep_lista[self.akadaly_tipus_index]
        self.terulet = self.kep.get_rect()
        self.terulet.x = KEPERNYO_SZELESSEG
        self.terulet.y = 370
        self.maszk = pygame.mask.from_surface(self.kep)

    def frissites(self, aktualis_jatek_sebesseg, akadalyok_lista_ref):
        """Frissiti az akadaly poziciojat es eltavolitja, ha szukseges."""
        self.terulet.x -= aktualis_jatek_sebesseg
        if self.terulet.x < -self.terulet.width:
            if self in akadalyok_lista_ref:
                akadalyok_lista_ref.pop(akadalyok_lista_ref.index(self))

    def rajzol(self, rajzfelulet):
        """Kirajzolja az akadaly."""
        rajzfelulet.blit(self.kep, self.terulet)


class KisAvokado(Akadaly): # Korabban SmallAvocado
    """Kis avokado akadaly."""
    def __init__(self, kep_lista):
        valasztott_tipus_index = random.randint(0, len(kep_lista) - 1)
        super().__init__(kep_lista, valasztott_tipus_index)


class NagyAvokado(Akadaly): # Korabban LargeAvocado
    """Nagy avokado akadaly."""
    def __init__(self, kep_lista):
        valasztott_tipus_index = random.randint(0, len(kep_lista) - 1)
        super().__init__(kep_lista, valasztott_tipus_index)


class Heli(Akadaly): # Nev marad Heli
    """Helikopter akadaly."""
    def __init__(self, kep_lista):
        self.animacio_index = 0
        super().__init__(kep_lista, 0)
        self.terulet.y = 300

    def rajzol(self, rajzfelulet):
        """Kirajzolja a helikoptert, animalva azt."""
        aktualis_kepkocka = self.kep_lista[self.animacio_index // 5]
        rajzfelulet.blit(aktualis_kepkocka, self.terulet)
        
        self.animacio_index += 1
        if self.animacio_index >= len(self.kep_lista) * 5:
            self.animacio_index = 0
        # A maszk frissitese itt is elmarad az egyszeruseg kedveert


# Modul szintu valtozok a jatekallapot megosztasahoz
jatek_akadalyok_global = []
jatek_penz_global = None
jatekos_nev_global = ""


def _pontszam_kijelzes_jatekon_belul(aktualis_pontok_ertek, aktualis_jatek_sebesseg_ertek, betutipus_obj):
    """
    Kiszamolja es megjeleniti az aktualis pontszamot a jatek kozben.
    Visszaadja a frissitett pontszamot es jateksebesseget.
    """
    aktualis_pontok_ertek += 1
    if aktualis_pontok_ertek > 0 and aktualis_pontok_ertek % 100 == 0:
        aktualis_jatek_sebesseg_ertek += 1

    pontszam_szoveg_felulet = betutipus_obj.render("Pontok: " + str(aktualis_pontok_ertek), True, (0, 0, 0))
    pontszam_szoveg_terulet = pontszam_szoveg_felulet.get_rect()
    pontszam_szoveg_terulet.center = (KEPERNYO_SZELESSEG - 150, 40)
    KEPERNYO.blit(pontszam_szoveg_felulet, pontszam_szoveg_terulet)
    return aktualis_pontok_ertek, aktualis_jatek_sebesseg_ertek

def _hatter_rajzolas_jatekon_belul(x_palya_poz, x_hatter_poz, y_palya_poz_ertek, aktualis_jatek_sebesseg_ertek):
    """
    Kirajzolja es gorgeti a jatek hatteret es palyajat.
    Visszaadja a palya es a hatter frissitett X pozicioit.
    """
    hatterkep_szelesseg = HATTER_KEP.get_width()
    KEPERNYO.blit(HATTER_KEP, (x_hatter_poz, 0))
    KEPERNYO.blit(HATTER_KEP, (hatterkep_szelesseg + x_hatter_poz, 0))
    x_hatter_poz -= aktualis_jatek_sebesseg_ertek * 0.25
    if x_hatter_poz <= -hatterkep_szelesseg:
        x_hatter_poz = 0

    x_palya_poz -= aktualis_jatek_sebesseg_ertek

    return x_palya_poz, x_hatter_poz

def jatek_ciklus():
    """A fo jatekciklus."""
    global jatek_akadalyok_global, jatek_penz_global # Hozzaferes a modul szintu valtozokhoz

    jatek_fut = True
    jatek_ora = pygame.time.Clock()
    jatekos_karakter = ViktorSaurus()
    
    # Helyi valtozok a jatek_ciklus szamara
    aktualis_jatek_sebesseg = 20
    x_pozicio_palya = 0
    y_pozicio_palya = 380
    x_pozicio_tavoli_hatter = 0
    aktualis_pontok = 0
    jatekon_beluli_betutipus = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    
    jatek_akadalyok_global.clear() 
    jatek_penz_global = Penz() # Penz osztaly peldanyositasa

    while jatek_fut:
        for esemeny in pygame.event.get():
            if esemeny.type == pygame.QUIT:
                jatek_fut = False
                pygame.quit()
                exit()

        KEPERNYO.fill((255, 255, 255))

        x_pozicio_palya, x_pozicio_tavoli_hatter = _hatter_rajzolas_jatekon_belul(
            x_pozicio_palya, x_pozicio_tavoli_hatter, y_pozicio_palya, aktualis_jatek_sebesseg
        )

        if jatek_penz_global:
            jatek_penz_global.rajzol(KEPERNYO)
            jatek_penz_global.frissites(aktualis_jatek_sebesseg)

        jatekos_karakter.rajzol(KEPERNYO)
        lenyomott_gombok = pygame.key.get_pressed()
        jatekos_karakter.frissites(lenyomott_gombok)

        if not jatek_akadalyok_global:
            akadaly_valasztas_random = random.randint(0, 2)
            if akadaly_valasztas_random == 0:
                jatek_akadalyok_global.append(KisAvokado(KIS_AVOKADO_KEPEK))
            elif akadaly_valasztas_random == 1:
                jatek_akadalyok_global.append(NagyAvokado(NAGY_AVOKADO_KEPEK))
            elif akadaly_valasztas_random == 2:
                jatek_akadalyok_global.append(Heli(HELI_KEPEK))

        for akadaly_elem in list(jatek_akadalyok_global):
            akadaly_elem.rajzol(KEPERNYO)
            akadaly_elem.frissites(aktualis_jatek_sebesseg, jatek_akadalyok_global)

            eltolas_utkozes_x = akadaly_elem.terulet.x - jatekos_karakter.terulet.x
            eltolas_utkozes_y = akadaly_elem.terulet.y - jatekos_karakter.terulet.y
            if jatekos_karakter.maszk.overlap(akadaly_elem.maszk, (eltolas_utkozes_x, eltolas_utkozes_y)):
                utkozes_hang.play()
                pygame.mixer.music.stop()
                jatek_vege_hang.play()
                pygame.time.delay(2000)
                menu_megjelenites(aktualis_pontok)
                return

        if jatek_penz_global and jatek_penz_global.lathato:
            eltolas_penz_x = jatek_penz_global.terulet.x - jatekos_karakter.terulet.x
            eltolas_penz_y = jatek_penz_global.terulet.y - jatekos_karakter.terulet.y
            if jatekos_karakter.maszk.overlap(jatek_penz_global.maszk, (eltolas_penz_x, eltolas_penz_y)):
                penz_hang.play()
                aktualis_pontok += 100
                jatek_penz_global.lathato = False

        aktualis_pontok, aktualis_jatek_sebesseg = _pontszam_kijelzes_jatekon_belul(
            aktualis_pontok, aktualis_jatek_sebesseg, jatekon_beluli_betutipus
        )

        pygame.display.update()
        jatek_ora.tick(30)


def menu_megjelenites(elert_pontszam_ertek=0): # Korabban show_menu
    """Megjeleniti a jatekmenut, kezeli a nevbevitelt es a magas pontszamokat."""
    global jatekos_nev_global # Hozzaferes a modul szintu jatekosnevhez

    menu_aktiv_allapot = True
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Assets/Sounds/background_music.mp3")
        pygame.mixer.music.play(-1)
    if jatek_vege_hang.get_num_channels() > 0:
        jatek_vege_hang.stop()

    menu_cim_betutipus = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    menu_bevitel_betutipus = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    menu_pontszam_betutipus = pygame.font.Font("PressStart2P-Regular.ttf", 16)

    nev_beviteli_mezo_terulet = pygame.Rect(KEPERNYO_SZELESSEG // 2 - 150, KEPERNYO_MAGASSAG // 2 - 25, 300, 50)
    szin_bevitel_inaktiv = pygame.Color("lightskyblue3")
    szin_bevitel_aktiv = pygame.Color("dodgerblue2")
    beviteli_mezo_aktualis_szin = szin_bevitel_inaktiv
    nev_bevitel_aktiv = False
    nev_bevitel_puffer = jatekos_nev_global if jatekos_nev_global else "" 

    betoltott_legjobb_pontok = legjobb_pontok_betoltese()

    while menu_aktiv_allapot:
        KEPERNYO.blit(KEZDOOLDAL_KEP, (0, 0))

        for esemeny in pygame.event.get():
            if esemeny.type == pygame.QUIT:
                pygame.quit()
                exit()
            if esemeny.type == pygame.MOUSEBUTTONDOWN:
                if nev_beviteli_mezo_terulet.collidepoint(esemeny.pos):
                    nev_bevitel_aktiv = not nev_bevitel_aktiv
                else:
                    nev_bevitel_aktiv = False
                beviteli_mezo_aktualis_szin = szin_bevitel_aktiv if nev_bevitel_aktiv else szin_bevitel_inaktiv
            if esemeny.type == pygame.KEYDOWN:
                if nev_bevitel_aktiv:
                    if esemeny.key == pygame.K_RETURN:
                        jatekos_nev_global = nev_bevitel_puffer
                        if jatekos_nev_global:
                            betoltott_legjobb_pontok.append((jatekos_nev_global, elert_pontszam_ertek))
                            legjobb_pontok_mentese(betoltott_legjobb_pontok)
                        
                        jatek_ciklus() 
                        return
                    elif esemeny.key == pygame.K_BACKSPACE:
                        nev_bevitel_puffer = nev_bevitel_puffer[:-1]
                    else:
                        if len(nev_bevitel_puffer) < 15 :
                            nev_bevitel_puffer += esemeny.unicode

        felszolito_szoveg_felulet = menu_cim_betutipus.render("Írd be a neved:", True, (0, 0, 0))
        felszolito_szoveg_terulet = felszolito_szoveg_felulet.get_rect(center=(KEPERNYO_SZELESSEG // 2, KEPERNYO_MAGASSAG // 2 - 100))
        KEPERNYO.blit(felszolito_szoveg_felulet, felszolito_szoveg_terulet)

        pygame.draw.rect(KEPERNYO, beviteli_mezo_aktualis_szin, nev_beviteli_mezo_terulet, 2)
        nev_szoveg_felulet = menu_bevitel_betutipus.render(nev_bevitel_puffer, True, (0,0,0))
        KEPERNYO.blit(nev_szoveg_felulet, (nev_beviteli_mezo_terulet.x + (nev_beviteli_mezo_terulet.w - nev_szoveg_felulet.get_width()) // 2 ,
                                      nev_beviteli_mezo_terulet.y + (nev_beviteli_mezo_terulet.h - nev_szoveg_felulet.get_height()) // 2))

        legjobbpont_cim_felulet = menu_cim_betutipus.render("Legjobb Eredmények", True, (0, 0, 0))
        legjobbpont_cim_terulet = legjobbpont_cim_felulet.get_rect(center=(KEPERNYO_SZELESSEG // 2, KEPERNYO_MAGASSAG // 2 + 100))
        KEPERNYO.blit(legjobbpont_cim_felulet, legjobbpont_cim_terulet)

        rendezett_pontok_lista = sorted(betoltott_legjobb_pontok, key=lambda pont_elem: pont_elem[1], reverse=True)[:5]
        for i, (nev_lp, pont_lp) in enumerate(rendezett_pontok_lista): # lp = legjobb pont
            bejegyzett_pont_felulet = menu_pontszam_betutipus.render(f"{i + 1}. {nev_lp}: {pont_lp}", True, (0,0,0))
            bejegyzett_pont_terulet = bejegyzett_pont_felulet.get_rect(center=(KEPERNYO_SZELESSEG // 2, KEPERNYO_MAGASSAG // 2 + 150 + i * 30))
            KEPERNYO.blit(bejegyzett_pont_felulet, bejegyzett_pont_terulet)

        pygame.display.update()


def legjobb_pontok_betoltese():
    """Betolti a legjobb pontszamokat a 'high_scores.txt' fajlbol."""
    try:
        with open("high_scores.txt", "r", encoding="utf-8") as fajl_obj:
            pontok_adat = []
            for sor_adat in fajl_obj:
                sor_adat = sor_adat.strip()
                if ":" in sor_adat:
                    nev_resz, pont_resz_str = sor_adat.split(":", 1)
                    try:
                        pontok_adat.append((nev_resz, int(pont_resz_str)))
                    except ValueError:
                        print(f"Figyelmeztetes: Nem sikerult feldolgozni a pontszamot '{nev_resz}'-hez a sorbol: '{sor_adat}'")
                elif sor_adat:
                    print(f"Figyelmeztetes: Hibasan formazott sor kihagyasa a high_scores.txt-ben: '{sor_adat}'")
            return pontok_adat
    except FileNotFoundError:
        return []
    except Exception as hiba_pontbetoltes:
        print(f"Hiba a legjobb pontok betoltesekor: {hiba_pontbetoltes}")
        return []


def legjobb_pontok_mentese(mentendo_pontok_lista):
    """Elmenti a legjobb pontszamok listajat a 'high_scores.txt' fajlba."""
    try:
        with open("high_scores.txt", "w", encoding="utf-8") as fajl_obj:
            for nev_mentes, pont_mentes in mentendo_pontok_lista:
                fajl_obj.write(f"{nev_mentes}:{pont_mentes}\n")
    except Exception as hiba_pontmentes:
        print(f"Hiba a legjobb pontok mentésekor: {hiba_pontmentes}")


# --- Jatek Inditasa ---
if __name__ == "__main__":
    # jatekos_nev_global mar modul szinten inicializalva van ("")
    menu_megjelenites(elert_pontszam_ertek=0)