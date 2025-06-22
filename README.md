# Daily IT News Automation

Ett Docker-baserat Python-projekt som automatiskt skickar dagliga IT-nyheter och läropunkter via e-post. **Portabelt och fungerar på alla plattformar** (Windows, Mac, Linux).

## Funktioner

- Hämtar IT-nyheter och tekniska koncept från OpenAI GPT-4
- Skickar pedagogiska genomgångar via e-post dagligen kl 07:00
- Loggar alla resultat i textfiler
- **Portabelt**: Körs på vilken maskin som helst med Docker
- **Automatisk schemaläggning**: Inbyggd schemaläggare i Docker (ingen extern crontab/systemd)
- **Enkel manuell testning**: Medföljande testskript

## Snabbstart

1. **Kör startskriptet**
   ```bash
   ./start.sh
   ```
   Detta kommer att:
   - Skapa `.env`-filen från mallen om den saknas
   - Bygga och starta Docker-containrar
   - Visa användbara kommandon

2. **Konfigurera miljövariabler**
   - Redigera `.env`-filen med dina egna värden:
     - `OPENAI_API_KEY`: Din OpenAI API-nyckel
     - `EMAIL_FROM`: Din e-postadress som avsändare
     - `EMAIL_TO`: Mottagarens e-postadress
     - `SMTP_SERVER`: Din SMTP-server (t.ex. smtp.gmail.com)
     - `SMTP_PORT`: SMTP-port (vanligtvis 587 för TLS)
     - `SMTP_USER`: Din e-postadress för inloggning
     - `SMTP_PASS`: Ditt e-postlösenord (App-lösenord för Gmail)

3. **Kör startskriptet igen**
   ```bash
   ./start.sh
   ```

## Manuell installation

1. **Konfigurera miljövariabler**
   ```bash
   cp env.example .env
   # Redigera .env-filen med dina värden
   ```

2. **Bygg och starta projektet**
   ```bash
   docker-compose up -d --build
   ```

## Konfiguration av e-post

### Gmail
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=din-email@gmail.com
SMTP_PASS=ditt-app-lösenord
```
**OBS:** Du behöver använda ett "App-lösenord" från Google, inte ditt vanliga lösenord.

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Andra leverantörer
Kontrollera din e-postleverantörs SMTP-inställningar.

## Loggar

- **Applikationsloggar**: `/app/logs/app.log` (i containern)
- **Schemaläggarloggar**: `docker-compose logs scheduler`
- **Dagliga nyhetsfiler**: `/app/logs/YYYY-MM-DD.txt` (i containern)
- **Lokala loggar**: `./logs/` (mappad från containern)

## Övervakning

- Kontrollera att containrarna körs:
  ```bash
  docker-compose ps
  ```
- Visa schemaläggarloggar:
  ```bash
  docker-compose logs -f scheduler
  ```
- Visa applikationsloggar:
  ```bash
  docker-compose logs daily-it-news
  ```

## Testa manuellt

För att testa skriptet manuellt:
```bash
./test-manual.sh
```
Eller:
```bash
docker-compose exec daily-it-news python /app/app/main.py
```

## Struktur

```
daily-it-news/
├── app/
│   └── main.py               # Huvudskript
├── scheduler/
│   ├── Dockerfile            # Schemaläggningscontainer
│   └── scheduler.sh          # Schemaläggningslogik
├── requirements.txt          # Python-beroenden
├── Dockerfile                # Huvudcontainer
├── docker-compose.yml        # Docker Compose-konfiguration
├── env.example               # Exempel på miljövariabler
├── .env                      # Dina miljövariabler (skapa från env.example)
├── start.sh                  # Startskript för enkel installation
├── test-manual.sh            # Testskript för manuell körning
├── .gitignore                # Git-ignore
├── README.md                 # Dokumentation
└── logs/                     # Loggfiler (skapas automatiskt)
```

## Hur det fungerar

1. **Schemaläggningscontainer**: Körs kontinuerligt och väntar till kl 07:00
2. **Huvudcontainer**: Är alltid igång och kör skriptet direkt vid behov (snabbt)
3. **Portabilitet**: Fungerar på alla plattformar med Docker
4. **Automatisk återstart**: Containrarna startar automatiskt om de stoppas

## Felsökning

- Kontrollera att `.env`-filen finns och är korrekt konfigurerad
- Kontrollera Docker-loggarna: `docker-compose logs`
- Kontrollera schemaläggarloggarna: `docker-compose logs scheduler`
- Kontrollera att tidszonen är korrekt: `docker-compose logs scheduler | grep TZ`
- Kontrollera att din OpenAI-nyckel och SMTP-inställningar är korrekta

## Säkerhet

- Lägg aldrig till `.env`-filen i versionshantering
- Använd starka lösenord för e-post
- Begränsa API-nycklarnas behörigheter när möjligt

## Portabilitet

Detta projekt är designat för att fungera på:
- **Windows** (med Docker Desktop)
- **macOS** (med Docker Desktop)
- **Linux** (med Docker Engine)
- **Raspberry Pi** (med Docker)
- **Vilken som helst server** med Docker

Ingen extern crontab eller systemd-tjänster behövs - allt hanteras av Docker!

## Licens

MIT License 