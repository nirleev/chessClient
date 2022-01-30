# chessClient

## Wymagania wstępne
* Zainstalowane JDK w wersji co najmniej 8
* Wartość zmiennej środowiskowej `JAVA_HOME` odpowiada lokalizacji pakietu JDK

## Budowanie aplikacji uciServer i chessServer
Aplikację można zbudować za pomocą jednego z poniższych poleceń:
* `./gradlew build` - aplikacja zostanie zbudowana, zostanie utworzony plik jar o nazwie `uciServer.jar` lub `chessServer.jar` w katalogu `./build/libs`
* `./gradlew bootRun` - aplikacja zostanie zbudowana, a następnie uruchomiona na domyślnym porcie 8080

## Przygotowanie aplikacji chessClient
Żeby silnik działał z wybranym GUI szachowym należy:
* doinstalować brakujące biblioteki
* zmodyfikować plik config.json umieszczając w nim adresy chessServerów i uciServera
* uruchomić serwery, a następnie main.py

Żeby silnik był plikiem wykonywalnym należy:
* doinstalować brakujące biblioteki
* zmodyfikować plik config.json umieszczając w nim adresy chessServerów i uciServera
* przekonwerować projekt przy użyciu narzędzia auto-py-to-exe do pliku .exe 
https://python.plainenglish.io/convert-a-python-project-to-an-executable-exe-file-175080da4485
(konwertować sam plik main.py, załączyć chessClient.py, configuration.py i config.json)

## Uruchamianie aplikacji serwerowych
* java -jar .\uciServer.jar
* java -jar .\chessServer.jar
### Dodatkowe parametry
* --server.port=8080 - uruchomienie aplikacji na wybranym porcie
* --config.MAX_USER_INACTIVE=30000 - maksymalny czas nieaktywności użytkownika (ms)

## Uwagi
* baza danych zawiera domyślnego użytkownika test:test, po pierwszym zalogowaniu (wykorzystując np. Swagger UI dostępnego przez IP:port uciServera) należy dodać nowego użytkownika i usunąć z bazy danych użytkownika domyślnego
* plik w katalogu ./src/main/resources/application.properties zawiera parametr config.JWT_SECRET_KEY, którego wartość należy zmienić dla uruchamianych aplikacji uciServer i chessServer (wartość wspólna dla wszystkich serwerów) w celu zachowania bezpieczeństwa komunikacji (wartość powinna być nietrywialna i odpowiednio długa)
