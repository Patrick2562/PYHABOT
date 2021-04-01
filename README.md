PYHABOT
=======

A **PYHABOT** egy *web scraping* alkalmazás, amely a [Hardverapróra](https://hardverapro.hu) feltöltött hirdetéseket nézi át és küld értesítéseket egy új megjelenésekor, amelyek megfelelnek az általunk megadott feltételeknek.
Az alkalmazás rendelkezik több integrációval is, amelyek segítségével parancsokon keresztül hozzáadhatóak és törölhetőek a keresni kívánt termékek.

# Hogyan használd
Miután meghívtad a botot az általad használt platformon lévő szerverre/szobába, a lent listázott parancsokkal kezelheted.
Egy új hirdetésfigyelő hozzáadásához elsőnek fel kell menni a [Hardverapróra](https://hardverapro.hu) és rákeresni a termékre amit figyelni szeretnél. Érdemes a részletes keresést használni, beállítani a kategóriát, minimum és maximum árat.
Ha ez megvan, akkor a kattints a KERESÉS gombra és a találatok oldalon másold ki az URL-t, ezután a botnak kell elküldeni a következő parancsot: `!add <Kimásolt URL>`
Ilyenkor felkerül a listára és láthatjuk a hirdetésfigyelő ID-jét (erre szükség lesz a többi parancs használatánál), de még be kell állítani hova szeretnéd kapni az értesítéseket mielőtt működésbe lépne. Ehhez használd a `!notifyon <Hirdetésfigyelő ID> <Típus>` parancsot.
Ha mindent megfelelően csináltál, akkor a bot innentől kezdve egy új hirdetés megjelenésekor értesítést küld. Ha szeretnéd átvizsgáltatni vele az eddigi hirdetéseket (amelyek a figyelő hozzáadása előtt is léteztek), akkor használd a `!rescan <Hirdetésfigyelő ID>` parancsot.

# Integrációk
Jelenleg Discord és Telegram integrációval rendelkezik. A boton keresztül különböző parancsokkal szerkeszthetjük a beállításokat.

# Parancsok.
Minden parancs elé ki kell tenni a prefixet, ez alapértelmezetten: `!` *(Például: !reload)*
| Parancs      | Leírás                                                                                                 |
| :----------- | :----------------------------------------------------------------------------------------------------- |
| add          | Felvenni lehet vele egy új hirdetésfigyelőt.                                                           |
| del          | Törölni lehet vele egy létező hirdetésfigyelőt.                                                        |
| list         | Listázza az eddig felvett hirdetésfigyelőket.                                                          |
| rescan       | Elfelejti az eddig átvizsgált hirdetéseket, ismételten átnézi az összeset és elküldi az értesítéseket. |
| url          | Módosítani lehet egy hirdetésfigyelő URL-jét.                                                          |
| prefix       | Módosítani lehet vele a parancs prefixet.                                                              |
| raw          | Elküldi a scrapelt hirdetések adatait json formátumban.                                                |
| scaninterval | Belehet vele állítani hány másodpercenként ellenőrizzen.                                               |

# Notification típusok
| Típus           | Leírás                                                           |
| :-------------- | :--------------------------------------------------------------- |
| here            | Ide, arra a chatra ahol a parancs be lett írva.                  |
| private         | Privát üzenetben, azon a platformon ahol a parancs be lett írva. |
| discordwebhook  | Discord szobába, webhookon keresztül.                            |
| telegramwebhook | Telegram szobába, webhookon keresztül.                           |

# Hardverapró paraméterek
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