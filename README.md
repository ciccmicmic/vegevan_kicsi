# Vége van kicsi Játék - README

**Verzió:** 1.0
**Dátum:** 2025. május 13.

---

## Rövid Leírás

A **"Vége van kicsi"** egy oldalra gördülő (side-scrolling) ügyességi játék, ahol a főhős, ViktorSaurus bőrébe bújva kell minél tovább túlélned az egyre gyorsuló pályán. Kerüld ki az akadályokat, gyűjtsd a Penzeket a magasabb pontszámért, és döntsd meg a legjobb eredményeket! A játékban hallhatsz háttérzenét és különböző hanghatásokat is.

---

## Hogyan Kell Játszani / Irányítás

A játék irányítása egyszerű:

* **FEL Nyíl:** Ugrás (ViktorSaurus ugrik, hogy kikerülje az alacsony akadályokat vagy elérje a Penzeket)
* **LE Nyíl:** Guggolás (ViktorSaurus leguggol, hogy kikerülje a magasabban érkező akadályokat)

A játék automatikusan indul a neved megadása után a kezdőképernyőn.

---

## Cél

A játék célja, hogy minél tovább életben maradj a pályán, elkerülve az ütközést a különböző akadályokkal (KisAvokado, NagyAvokado, Helikopter). Minden sikeresen átugrott vagy kikerült akadály után pontokat kapsz. Gyűjtsd össze a Penzeket további extra pontokért! A játék végén a pontszámodat elmentheted a legjobb eredmények listájába.

---

## Jellemzők

* Végtelenített játékmenet, egyre növekvő sebességgel.
* Különböző típusú akadályok: KisAvokado, NagyAvokado, Heli.
* Gyűjthető Penzek az extra pontokért.
* Kezdőképernyő névbevitellel.
* Helyben tárolt legjobb eredmények listája (Top 5), a `high_scores.txt` fájlban.
* Hanghatások (ugrás, guggolás, ütközés, pénzgyűjtés, játék vége).
* Folyamatos háttérzene.

---

## Követelmények

A játék futtatásához a következőkre van szükség:

* **Python 3.x** verzió telepítve.
* **Pygame** könyvtár telepítve.
  * Telepítés (ha még nincs telepítve): Nyiss egy parancssort vagy terminált, és add ki a következő parancsot:

        ```bash
        pip install pygame
        ```

---

## A Játék Futtatása

1. Győződj meg róla, hogy a Python és a Pygame könyvtár telepítve van a számítógépeden.
2. Töltsd le a játék fájljait. A játék fő Python fájljának (pl. `main.py` vagy `jatek.py`) és az `Assets` mappának a teljes tartalmával együtt kell lennie.
3. Az `Assets` mappának (és annak al-mappáinak: `Avocado`, `Heli`, `Other`, `Sounds`, `Viktor`) ugyanabban a könyvtárban kell lennie, mint a játék fő Python fájljának.
4. Nyiss egy parancssort vagy terminált, és navigálj abba a könyvtárba, ahová a játékot mentetted.
5. Indítsd el a játékot a következő paranccsal (feltételezve, hogy a fő fájl neve `main.py`):

    ```bash
    python main.py
    ```

6. A játék elindul, és a kezdőképernyőn megadhatod a neved.

---

## Fájlstruktúra (Assets)

A játék megfelelő működéséhez elengedhetetlen az `Assets` mappa és annak pontos tartalma. Ez a mappa tartalmazza a játékhoz szükséges összes grafikai elemet (képeket) és hangfájlt. A várt struktúra:
