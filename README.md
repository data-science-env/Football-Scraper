# Football Scraper
En aquest projecte s'ha creat un web scraper amb finalitats acadèmiques.
Concretament pretén resoldre la PAC1-Web Scraping de l'assignatura M2.951 -
Tipologia i cicle de vida de les dades del Màster universitari de Ciència de
dades impartit per la Universitat Oberta de Catalunya (UOC).

En aquest cas s'ha escollit agafar les dades de la lliga espanyola de futbol.
L'extracció de dades s'ha realitzat sobre el web http://www.resultados-futbol.com
el qual té un històric de totes les jornades de la lliga espanyola des del seu
inici l'any 1929 fins a l'actualitat.

La motivació en aquest projecte ve donada arran de situacions quotidianes on
diem que guanyarà un equip o un altre basant-nos solament amb el nom de l'equip.
Per exemple, si es fes una enquesta on és preguntes "Qui guanyarà el partit
Barcelona-Eibar?" és molt probable que hagis respost Barcelona, solament pel
renom que té i la carrera que porta com a club. Basant-me en aquest fet,
m'agradaria generar un dataset on es recollís els partits jugats en la
lliga espanyola juntament amb el seu resultat. En aquesta assignatura no es
contempla la creació de model predictius, però la idea seria crear un model
que fes prediccions d'acord amb els noms dels equips que s'enfronten i digués quin dels dos
és més probable que guanyi.

M'agradaria agrair a l'equip de resultados-futbol per oferir totes les dades
necessàries per la realització d'aquesta pràctica. S'ha de dir que ofereixen
una API de pagament per fer consultes directes de les dades, però com bé s'ha
dit, en aquest cas es farà ús d'un web scraper per la recol·lecció de les dades.

## Preliminars
### Robots.txt
Durant la realització d'aquesta pràctica, el fitxer 
[robots.txt](https://resultados.elpais.com/robots.txt) era el següent. 

```
User-agent :  *
Disallow :  /muro
Disallow :  /perfil
Disallow :  /amigos
Disallow :  /mensajes
Disallow :  /notificaciones
Disallow :  /misgrupos
Disallow :  /misfotos
Disallow :  /misvideos
Disallow :  /misblogs
Disallow :  /misnoticias
Disallow :  /misjuegos
Disallow :  /control
Disallow :  /editor
Disallow :  /legal
Disallow :  /normas_uso
Disallow :  /video/
Disallow :  /videos/
Disallow :  /fotos/usuario/
Disallow :  /noticias/usuario/
Disallow :  /videos/usuario/
Disallow :  /ajax/load_extension.php
Disallow :  /ajax/preload_extension.php

Allow :  /

User-agent :  Mediapartners-Google
Disallow : 

User-agent :  grapeshot
Disallow : 
```

**Important** :  En utilitzacions futures, cal revisar l'arxiu 
[robots.txt](https://resultados.elpais.com/robots.txt) de  nou per comprovar 
que se segueix tenint permís per extraure les dades del web.
 
### Estructura HTML d'un partit
 
 ```
<tr class="vevent">
    <td class="fecha">10 Feb 29</td>
    <td class="equipo1">
        <a href="/Arenas-Club/1929" title="Arenas"><img width="18" src="https : //thumb.resfu.com/img_data/escudos/small/4657.jpg?size=37x&amp;5" alt="Arenas de Getxo">Arenas</a>
    </td>
    <td class="rstd">
        <span class="summary hidden" title="Arenas - Atlético">Arenas - Atlético</span>
        <span class="dtstart hidden" title="1929-02-10T00 : 00 : 00">1929-02-10T00 : 00 : 00</span>
        <span class="location hidden">Municipal de Gobela</span>
        <span class="eventType category" title="Fútbol"></span>

        <a class="url" href="/partido/Arenas-Club/Atletico-Madrid/1929">2&nbsp;-&nbsp;3</a> </td>
    <td class="equipo2">
        <a href="/Atletico-Madrid/1929" title="Atlético"><img width="18" src="https : //thumb.resfu.com/img_data/escudos/small/369.jpg?size=37x&amp;5" alt="Atlético">Atlético</a>
    </td>
    <td class="cmm"><a class="c" href="/partido/Arenas-Club/Atletico-Madrid/1929">5</a></td>
</tr>
 ```
 
## Contingut dataset
El dataset generat conte les dades dels partits de futbol de la lliga espanyola
des de la temporada 1929 fins a la temporada 2020. Cal destacar que no hi han
dades dels anys 1937, 1938, i 1938, ja que a causa de la guerra civil que va patir
Espanya no va haver-hi lliga.
 
 A continuació es mostren capçaleres del dataset juntament amb el tipus de valor que contenen.
 
* year : numeric
* jornada : numeric
* date : string
* stadium : string
* teamA : string
* teamB : string
* scoreTeamA : numeric
* scoreTeamB : numeric
* winner : string
* winnerAsNumeric : numeric
 
 