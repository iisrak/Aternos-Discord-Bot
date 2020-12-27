import requests
from bs4 import BeautifulSoup

class AternosAPI():
    def __init__(self, headers, TOKEN):
        self.headers = {}
        self.TOKEN = TOKEN
        self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        self.headers['Cookie'] = headers
        self.SEC = self.getSEC()
        self.JavaSoftwares = ['Vanilla', 'Spigot', 'Forge', 'Magma','Snapshot', 'Bukkit', 'Paper', 'Modpacks', 'Glowstone']
        self.BedrockSoftwares = ['Bedrock', 'Pocketmine-MP']

    def getSEC(self):
        headers = self.headers['Cookie'].split(";")
        for sec in headers:
            if sec[:12] == "ATERNOS_SEC_":
                sec = sec.split("_")
                if len(sec) == 3:
                    sec = ":".join(sec[2].split("="))
                    return sec

        print("Invaild SEC")
        exit(1)

    def GetStatus(self):
        webserver = requests.get(url='https://aternos.org/server/', headers=self.headers)
        webdata = BeautifulSoup(webserver.content, 'html.parser')
        status = webdata.find('span', class_='statuslabel-label').get_text()
        status = status.strip()
        return status

    def StartServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Online":
            return "Server is currently online!"
        else:
            parameters = {}
            parameters['headstart'] = 0
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            startserver = requests.get(url=f"https://aternos.org/panel/ajax/start.php", params=parameters, headers=self.headers)
            return "Server is being started..."

    def StopServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Offline":
            return "Server is already offline!"
        else:
            parameters = {}
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            stopserver = requests.get(url=f"https://aternos.org/panel/ajax/stop.php", params=parameters, headers=self.headers)
            return "Server is being stopped..."

    def GetServerInfo(self):
        ServerInfo = requests.get(url='https://aternos.org/server/', headers=self.headers)
        ServerInfo = BeautifulSoup(ServerInfo.content, 'html.parser')
        
        Players = ServerInfo.find('div', class_='server-info-box-value').get_text()
        Players = Players.strip()
        
        Software = ServerInfo.find('span', id='software').get_text()
        Software = Software.strip()

        Version = ServerInfo.find('span', id='version').get_text()
        Version = Version.strip()

        if (Software in self.JavaSoftwares):
            IP = ServerInfo.find('div', class_='server-ip mobile-full-width').get_text()
            IP = IP.strip()

            IP = IP.split(" ")
            IP = IP[0].strip()

            Port = "25565 (Optional)"

            return f"IP: {IP}\nPort: {Port}\nSoftware: {Software}\nPlayers: {Players}\nVersion: {Version}"
        else:
            return "Bedrock not supported. Sorry not sorry."


