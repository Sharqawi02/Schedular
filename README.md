-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STATIC
        CSS
    [#first-site.css
    #homepage.css
    #profilepage.css
    #login.css
    #redigera_event.css]
    'Var och en av dessa är kopplade till respektive HTML fil som finns nedan.'

        JavaScript
    [#homepage.js
    #script.js]
    'homepage.js denna filen innehåller all javascript kod för självaste kalendern som har importerats från fullcalendar.io'
    'script.js denna filen innehller kod för dark och light mode för hemsidan.'

        images
    'innehåller alla bilder och loggor.'

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# VIEWS
    #first-site.html
    'Denna filen ska vara strukturen för login sidan samt register sidan.'

    #homepage.html
    'Denna filen ska vara strukturen för homepage där användaren ska kunna skapa aktiviteter, se kalendern, se sin profilsida samt se kategorier av aktiviteterna.'

    #profilepage.html
    'Denna filen är struktren för profil sidan vars användaren ska kunna se sina uppgifter, uppdatera sin profilbild och infromation samt kunna logga ut.'

    #login.html & registrera.html
    'Dessa två sidor är nästan identiska. Jär ska användaren kunna antingen logga in eller registrera sig med hjälp av olika inputfält och en knapp.'

    #redigera-event.html
    'här ska användaren kunna redigera sina event eller radera dem. Denna sidan är strukturerad på ett sätt där användaren bemöts med ett formlär som är centrerad i mitten.'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PYTHON
    #db.py
    'innehåller en simpel funktion för att kunna koppla till databasen som vi användare - pgAdmin 4
    innehåller även en funktion som kollar om användarens token matchar cookien.'

    #program.py
    'Innehåller alla funktioner för applikationen'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATABAS
    #sqlkod.txt
    'Varje person kommer ha en koppling till Shahos databas på sin dator för att införa mer säkerhet.
    Denna filen finns för att alla ska ha liknande databaser och för att ifall det sker en ändring
    i databasen ska man kunna pusha/commita denna filen'
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Github - https://github.com/Sharqawi02/Schedular.git
fullcalendar.io - https://fullcalendar.io/ 
bottle - https://bottlepy.org/docs/dev/ 