<p align="center">
    <img width="50%" height="auto" src="https://i.imgur.com/3A0RadR.png">
</p>

PYHABOT
=======

A **PYHABOT** egy *web scraping* alkalmazás Pythonban, amely a [Hardverapróra](https://hardverapro.hu) feltöltött hirdetéseket nézi át és küld értesítéseket egy új megjelenésekor, azokról amelyek megfelelnek az általunk megadott feltételeknek.
Rendelkezik több integrációval is, amelyek segítségével parancsokon keresztül hozzáadhatóak és törölhetőek a keresni kívánt termékek.

# Hogyan használd
Miután meghívtad a botot az általad használt platformon lévő szerverre/szobába, a lent listázott parancsokkal kezelheted.
Egy új hirdetésfigyelő hozzáadásához elsőnek fel kell menni a [Hardverapróra](https://hardverapro.hu) és rákeresni a termékre amit figyelni szeretnél. Érdemes a részletes keresést használni, beállítani a kategóriát, minimum és maximum árat.
Ha ez megvan akkor a kattints a KERESÉS gombra és a találatok oldalon másold ki az URL-t, ezután a botnak kell elküldeni a következő parancsot: `!add <Kimásolt URL>`
Ilyenkor felkerül a listára és láthatjuk a hirdetésfigyelő ID-jét (erre szükség lesz a többi parancs használatánál).
Alapértelmezetten az értesítéseket abba a szobába fogja küldeni, ahol a parancs be lett írva, de meg lehet változtatni, ehhez használd a `!notifyon <Hirdetésfigyelő ID> <Notification típus> [<args>]` parancsot.
Ha mindent megfelelően csináltál, akkor a bot innentől kezdve egy új hirdetés megjelenésekor értesítést küld.
Ha szeretnéd átvizsgáltatni vele az eddigi hirdetéseket (amelyek a figyelő hozzáadása előtt is léteztek), akkor használd a `!rescan <Hirdetésfigyelő ID>` parancsot.

# Telepítés
1. Repository letöltése: `git clone https://github.com/Patrick2562/PYHABOT.git`
2. Navigálás a letöltött repositoryba: `cd PYHABOT`
3. Szükséges modulok telepítése: `pip install -r requirements.txt`
4. **.env** fájl létrehozása *(**.env.example** másolata)*: `copy .env.example .env`
5. **.env** config fájl megnyitása és kitöltése, bot token megadása az egyenlőség után lévő 'False'-t lecserélve.
6. Indítás a kiválaszott integrációval: `python run.py discord`
7. Bot meghívása a szerverre/szobába, és jogot adni neki az üzenetek olvasásához/küldéséhez. (Discord esetében az indításkor megjelenő linken keresztül)
8. Hirdetésfigyelő hozzáadása: **Hogyan használd** szekcióban részletezve

# Integrációk
Jelenleg Discord és Telegram integrációval rendelkezik. A boton keresztül különböző parancsokkal szerkeszthetjük a beállításokat.

# Parancsok.
Minden parancs elé ki kell tenni a prefixet, ez alapértelmezetten: `!` *(Például: !add)*
| Parancs     | Leírás                                                                                                 |
| :---------- | :----------------------------------------------------------------------------------------------------- |
| help        | Listázza az elérhető parancsokat.                                                                      |
| settings    | Megmutatja a bot beállításait.                                                                         |
| add         | Felvenni lehet vele egy új hirdetésfigyelőt.                                                           |
| del         | Törölni lehet vele egy létező hirdetésfigyelőt.                                                        |
| list        | Listázza a felvett hirdetésfigyelőket.                                                                 |
| info        | Meglehet vele nézni egy hirdetésfigyelő adatait.                                                       |
| notifyon    | Módosítani lehet vele, hogy hová küldje az értesítéseket egy adott hirdetésfigyelő.                    |
| rescrape    | Elfelejti az eddig átvizsgált hirdetéseket, ismételten átnézi az összeset és elküldi az értesítéseket. |
| seturl      | Módosítani lehet egy hirdetésfigyelő URL-jét.                                                          |
| setprefix   | Módosítani lehet vele a parancs prefixet.                                                              |
| setinterval | Belehet vele állítani hány másodpercenként ellenőrizzen.                                               |
| getraw      | Feltölti a scrapelt hirdetések adatait Pastebin-rem json formátumban és elküldi a linket.              |

# Notification típusok
| Típus   | Leírás                                                                                                            |
| :------ | :---------------------------------------------------------------------------------------------------------------- |
| here    | Ide, arra a chatre ahol a parancs be lett írva.                                                                   |
| webhook | POST requestet küld a megadott URL-re. DISCORD WEBHOOK-ot támogatja! (Paraméterek: username, avatar_url, content) |

# Scraper RAW JSON paraméterek
| Paraméter    | Leírás                   |
| :----------- | :----------------------- |
| id           | Hirdetés ID              |
| name         | Termék neve              |
| link         | Link a hirdetés oldalára |
| price        | Termék ára               |
| city         | Város                    |
| date         | Közzététel időpont       |
| seller_name  | Eladó neve               |
| seller_url   | Link az eladó profiljára |
| seller_rates | Eladő értékelései        |
| image        | Kép link a termékről     |

# Hardverapró search paraméterek
| Paraméter    | Leírás                         |
| :----------- | :----------------------------- |
| stext        | Kulcsszavak                    |
| county       |
| stcid        | Megye  ID                      |
| settlement   | Település ID                   |
| stmid        |
| minprice     | Minimum ár                     |
| maxprice     | Maximum ár                     |
| company      |
| cmpid        | Termék márka ID                |
| user         |
| usrid        | Hirdető felhasználó ID         |
| selling      | Eladásra kinált hirdetés (0,1) |
| buying       | Venni akaró hirdetés (0,1)     |
| stext_none   | Kerülendő szavak               |
| noticed      | Jegelteket ne listázza (0,1)   |
| search_exac  | Csak pontos egyezések (0,1)    |
| search_title | Csak a címben keressen  (0,1)  |