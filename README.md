# BHOP-Discord

BHOP-Discord is BOT which can show TOP 10 of server or display best times of each maps using MySQL database.

## Installation



```bash
pip install requirments.txt
```

## Usage

```python
### DISCORD - SERVER CONFIGURATION
 
SERVER_ADDRESS = ("XXX.XX.XXX.XX", XXXXXX) # IP AND PORT
RCON_PASSWORD = "XXXXXXX" # RCON PASSWORD
SERVER_SQUARE_IMGURL = "XXX.XX/XXX.PNG"
 
### MYSQL CONFIGURATON
 
mydb = mysql.connector.connect(
  host="XXXXXXXX", # HOST
  user="XXXXXXXX", # USERNAME
  passwd="XXXXXXXX", # PASSWORD
  database="XXXXXXXX" # DATABASE
)

### BOT CONFIGURATION
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # OAuth2 TOKEN
PLAYER_COMMANDS = 596859166446977024 # COMMANDS CHANNELID
CONSOLE_COMMANDS = 597108276945092672 # CONSOLE CHANNELID
VIP_CHANNEL = 597181870236762132 # VIP AUTH CHANNELID
 
###########################################################################
 
with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    info = server.info()
    players = server.players()
 
bot = commands.Bot(command_prefix='.') #BOT PREFIX
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
