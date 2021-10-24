# Keskustelupalstasovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Käynnissä täällä: https://radiant-woodland-47861.herokuapp.com/

### Luodut toiminnallisuudet:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
* Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
* Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
* Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
* Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
* Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
* Syötteiden koon rajoittaminen.

### Testaaminen Herokussa:

* Käyttäjä voi luoda itselleen käyttäjätunnuksen näkymässä, joka aukeaa valitsemalla "Luo tunnus".
* Tunnusten luonnin jälkeen jatkossa käyttäjä voi kirjautua sisään valitsemalla "Kirjaudu sisään", kirjautumisen jälkeen teksti vaihtuu muotoon "Kirjaudu ulos". Tunnusten luonnin yhteydessä käyttäjä kuitenkin kirjautuu sisäään automaattisesti.
* Ilman tunnuksia keskusteluja voi tarkistella, mutta niihin ei voi osallistua.
* Admin-oikeuksilla varustettu käyttäjä voi luoda myös keskustelualueita etusivulla.
* Etusivulta voi siirtyä keskustelualueille ja keskustelualueen näkymässä yksittäisiin ketjuihin.
* Yksittäisen keskustelualueen näkymässä käyttäjä voi luoda uuden viestiketjun otsikolla ja aloitusviestillä varustettuna.
* Viestiketjunäkymässä käyttäjä voi vastata ketjuun.
* Viestihakunäkymässä käyttäjä voi hakea aloitusviestejä tai vastauksia joko koko viestillä tai sen osalla.
* Ketjun aloittaja voi muokata ketjua muokkausnäkymässä johon pääsee sekä alue- että viestiketjunäkymästä.
* Viestin kirjoittaja voi muokata viestiä muokkausnäkymässä johon pääsee viestiketjunäkymästä.
