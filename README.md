<p align="center">
    <img width="50%" height="auto" src="https://github.com/Patrick2562/PYHABOT/blob/master/assets/logo.png">
</p>

# PYHABOT

A **PYHABOT** egy _web scraping_ alkalmazás Pythonban, amely a [Hardverapróra](https://hardverapro.hu) feltöltött hirdetéseket nézi át és küld értesítéseket egy új megjelenésekor, azokról amelyek megfelelnek az általunk megadott feltételeknek.
Rendelkezik több integrációval is, amelyek segítségével parancsokon keresztül hozzáadhatóak és törölhetőek a keresni kívánt termékek.

# Hogyan használd

Miután meghívtad a botot az általad használt platformon lévő szerverre/szobába, a lent listázott parancsokkal kezelheted.
Egy új hirdetésfigyelő hozzáadásához elsőnek fel kell menni a [Hardverapróra](https://hardverapro.hu) és rákeresni a termékre amit figyelni szeretnél. Érdemes a részletes keresést használni, beállítani a kategóriát, minimum és maximum árat.
Ha ez megvan akkor a kattints a KERESÉS gombra és a találatok oldalon másold ki az URL-t, ezután a botnak kell elküldeni a következő parancsot: `!add <Kimásolt URL>`
Ilyenkor felkerül a listára és láthatjuk a hirdetésfigyelő ID-jét (erre szükség lesz a többi parancs használatánál).
Alapértelmezetten az értesítéseket abba a szobába fogja küldeni, ahol a parancs be lett írva, de meg lehet változtatni, ehhez használd a `!notifyon <Hirdetésfigyelő ID> <Notification típus> [<args>]` parancsot.
Ha mindent megfelelően csináltál, akkor a bot innentől kezdve egy új hirdetés megjelenésekor értesítést küld.
Ha szeretnéd átvizsgáltatni vele az eddigi hirdetéseket (amelyek a figyelő hozzáadása előtt is léteztek), akkor használd a `!rescrape <Hirdetésfigyelő ID>` parancsot.

# Használat (Windows)

0. Python telepítése. [(letöltés)](https://www.python.org/downloads/)
1. Repository letöltése és kicsomagolása. [(letöltés)](https://github.com/Patrick2562/PYHABOT/archive/refs/heads/master.zip)
2. Parancssor megnyitása és navigálás a letöltött repositoryba: `cd PYHABOT`
3. Szükséges modulok telepítése: `pip install -r requirements.txt`
4. **.env** fájl létrehozása _(**.env.example** másolata)_: `copy .env.example .env`
5. **.env** config fájl megnyitása és kitöltése
6. Indítás a `python run.py` paranccsal
7. Bot meghívása a szerverre/szobába, és jogot adni neki az üzenetek olvasásához/küldéséhez. (Discord esetében az indításkor megjelenő linken keresztül)
8. Hirdetésfigyelő hozzáadása: **Hogyan használd** szekcióban részletezve

# Használat (Docker)

0. Feltételezzük, hogy a Docker telepítve van és minimális ismeretekkel rendelkezel.
1. **.env** fájl létrehozása _(**.env.example** másolata)_: `copy .env.example .env`
2. **.env** config fájl megnyitása és kitöltése
3. Indítás a `docker compose up -d` paranccsal
4. Bot meghívása a szerverre/szobába, és jogot adni neki az üzenetek olvasásához/küldéséhez. (Discord esetében az indításkor megjelenő linken keresztül)
5. Hirdetésfigyelő hozzáadása: **Hogyan használd** szekcióban részletezve

# Integrációk

| Azonosító | Leírás       |
| :----     | :-----       |
| discord   | Discord bot  |
| telegram  | Telegram bot |

# Parancsok

Minden parancs elé ki kell tenni a prefixet, ez alapértelmezetten: `!` _(Például: !add)_
| Parancs | Leírás |
| :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| help | Listázza az elérhető parancsokat. |
| settings | Megmutatja a bot beállításait. |
| add | Felvenni lehet vele egy új hirdetésfigyelőt. |
| del | Törölni lehet vele egy létező hirdetésfigyelőt. |
| list | Listázza a felvett hirdetésfigyelőket. |
| info | Meglehet vele nézni egy hirdetésfigyelő adatait. |
| notifyon | Módosítani lehet vele, hogy hová küldje az értesítéseket egy adott hirdetésfigyelő. |
| rescrape | Elfelejti az eddig átvizsgált hirdetéseket, ismételten átnézi az összeset és elküldi az értesítéseket. (Ha van megadva Hirdetésfigyelő ID akkor csak azt, egyébként mindegyiket átnézi.) |
| seturl | Módosítani lehet egy hirdetésfigyelő URL-jét. |
| setprefix | Módosítani lehet vele a parancs prefixet. |
| setinterval | Belehet vele állítani hány másodpercenként ellenőrizzen. |

# Notification típusok

| Típus   | Leírás                                                                                                            |
| :------ | :---------------------------------------------------------------------------------------------------------------- |
| here    | Ide..., abba a szobába ahol a parancs be lett írva.                                                               |
| webhook | POST requestet küld a megadott URL-re. DISCORD WEBHOOK-ot támogatja! (Paraméterek: username, avatar_url, content) |
