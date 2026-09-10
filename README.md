# Speeddate-app

Een lokale webapp voor speeddate-avonden. De app toont alle vragen eenmaal in een willekeurige volgorde en schudt ze daarna opnieuw.

## Installeren en starten

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open daarna [http://127.0.0.1:5000](http://127.0.0.1:5000) in de browser.

## Publiceren via Git, Portainer en Nginx Proxy Manager

De productiecontainer gebruikt intern poort `8000` en is op de Docker-host bereikbaar via poort `8050`.

### 1. Git-repository maken

Maak een lege repository aan bij bijvoorbeeld GitHub of GitLab. Een private repository is prima. Voer daarna in deze projectmap uit, waarbij je de voorbeeld-URL vervangt door de URL van jouw repository:

```bash
git init
git add .
git commit -m "Add speeddate application"
git branch -M main
git remote add origin https://github.com/GEBRUIKERSNAAM/speeddate.git
git push -u origin main
```

De map `.venv` wordt door `.gitignore` uitgesloten en hoort niet in de repository.

### 2. Oude applicatie stoppen

Open in Portainer **Containers** en stop de oude applicatie op hostpoort `8050`. Verwijder daarna de oude container of stack. Er kan maar één container tegelijk aan poort `8050` gekoppeld zijn.

### 3. Stack vanuit Git deployen

Open in Portainer **Stacks**, kies **Add stack** en vervolgens **Repository**:

- Name: `speeddate`
- Repository URL: de HTTPS- of SSH-URL van jouw repository
- Repository reference: `refs/heads/main`
- Compose path: `compose.yaml`

Vul voor een private repository onder **Authentication** een gebruikersnaam en access token in. Gebruik geen normaal GitHub-wachtwoord. Kies daarna **Deploy the stack**.

Portainer kloont de repository, bouwt het image en start de container als `speeddate`. Controleer onder **Containers** dat de status `healthy` wordt en dat de port mapping `8050:8000` zichtbaar is.

Controleer vanaf de Docker-host of de app reageert:

```bash
curl http://127.0.0.1:8050/health
```

Dit moet `ok` teruggeven. De container draait onder een gebruiker zonder rootrechten, heeft een read-only bestandssysteem en wordt na een herstart automatisch opnieuw gestart.

### 4. Nginx Proxy Manager instellen

Maak een nieuwe **Proxy Host** met deze waarden:

- Domain Names: `speeddate.nerc.me`
- Scheme: `http`
- Forward Hostname / IP: het LAN-adres van de Docker-host, bijvoorbeeld `192.168.1.10`
- Forward Port: `8050`
- Cache Assets: uitgeschakeld
- Block Common Exploits: ingeschakeld
- Websockets Support: niet nodig

Gebruik niet `127.0.0.1` als Nginx Proxy Manager zelf in een container draait: dat adres wijst dan naar de proxycontainer. Gebruik in dat geval het LAN-adres van de Docker-host, bijvoorbeeld `192.168.1.10`.

### 5. Cloudflare DNS instellen

Open de DNS-zone van `nerc.me` in Cloudflare en maak één record:

- Type: `A`
- Name: `speeddate`
- IPv4 address: het publieke IP-adres van jouw internetverbinding/server
- Proxy status: **Proxied**, herkenbaar aan de oranje wolk
- TTL: `Auto`

Als `nerc.me` al met een correct `A`-record naar dezelfde server wijst, mag je in plaats daarvan een proxied `CNAME` voor `speeddate` naar `nerc.me` maken.

### 6. Cloudflare Origin Certificate koppelen

Als je al een Cloudflare Origin Certificate hebt waar `*.nerc.me` of `speeddate.nerc.me` in staat, kun je dat hergebruiken. Anders:

1. Open in Cloudflare **SSL/TLS**, **Origin Server** en kies **Create Certificate**.
2. Voeg `speeddate.nerc.me` toe als hostname. Een wildcard `*.nerc.me` is ook geldig.
3. Laat het sleuteltype op RSA en kies de gewenste geldigheidsduur.
4. Kopieer zowel het Origin Certificate als de Private Key meteen naar een veilige locatie.
5. Open in Nginx Proxy Manager **SSL Certificates**, kies **Add SSL Certificate** en **Custom**.
6. Geef het certificaat een naam en plak het Cloudflare-certificaat en de private key in de juiste velden.
7. Open daarna de Proxy Host voor `speeddate.nerc.me`, ga naar **SSL** en selecteer dit certificaat.
8. Schakel **Force SSL**, **HTTP/2 Support** en eventueel **HSTS Enabled** in.

Open in Cloudflare **SSL/TLS**, **Overview** en stel de encryptiemodus in op **Full (strict)**. Gebruik niet **Flexible**.

### 7. Netwerk en eindcontrole

Zorg dat de router/firewall publiek verkeer voor poorten `80` en `443` naar Nginx Proxy Manager stuurt. Poort `8050` hoeft niet vanaf het internet bereikbaar te zijn; alleen Nginx Proxy Manager moet die poort via het lokale netwerk kunnen bereiken.

Na DNS-propagatie is de app beschikbaar op [https://speeddate.nerc.me](https://speeddate.nerc.me).

Controleer bij problemen in deze volgorde:

```text
http://IP-VAN-DOCKER-HOST:8050/health
http://IP-VAN-NGINX-PROXY-MANAGER
https://speeddate.nerc.me
```

Een Cloudflare-fout `502` betekent meestal dat Nginx Proxy Manager poort `8050` niet kan bereiken. Een fout `525` of `526` wijst meestal op het Origin Certificate of een verkeerde SSL/TLS-modus.

### Updates publiceren

Wijzig lokaal de applicatie en push de wijziging naar `main`. Open daarna in Portainer de stack `speeddate`, kies **Pull and redeploy** en schakel **Re-pull image and redeploy** in. Omdat deze stack lokaal een image bouwt, moet Portainer bij iedere codewijziging opnieuw builden.

## Vragen aanpassen

Open `app.py` en pas de teksten in de lijst `QUESTIONS` aan:

```python
QUESTIONS = [
    "Eerste vraag?",
    "Tweede vraag?",
]
```

Herstart de app na een wijziging. Iedere vraag moet tussen aanhalingstekens staan en regels worden door een komma gescheiden.

Bij een Docker-installatie bouw je na gewijzigde vragen de container opnieuw:

```bash
docker compose up -d --build
```

## Bediening

- Stel op het beginscherm de tijd per vraag in en kies **Start de speeddate**.
- Kies **Volgende vraag** om meteen een nieuwe vraag met een nieuwe timer te starten.
- Gebruik eventueel de spatiebalk of pijl naar rechts als sneltoets.
- Kies rechtsboven de knop met vier hoeken voor volledig scherm.
- Na het piepsignaal blijft de huidige vraag staan totdat je doorgaat.
