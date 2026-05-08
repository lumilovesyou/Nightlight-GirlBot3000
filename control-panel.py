from dotenv import load_dotenv
from scripts.database import downtime
from string import Template
from pathlib import Path
import cherrypy
import os

load_dotenv()
    
def colouredByPercent(value):
    try:
        value = int(value)
        if value > 99:
            return "green"
        if value > 90:
            return "yellow"
        elif value > 50:
            return "orange"
        else:
            return "red"
    except Exception as e:
        print(e)
        return "white"

PATH = "./assets/panel/"
DOWNTIME = downtime.uptimeDatabase(int(os.getenv("COOLDOWN")))
INDEX = Template(Path(PATH, "index.html").read_text())

def template(html):
    return html.safe_substitute(
        INDEX,
        uptime=DOWNTIME.getWeeklyUptimePercent(),
        colouredUptime=colouredByPercent(
            DOWNTIME.getWeeklyUptimePercent()
        ),
        name=os.getenv("USERNAME")
    )
    

class controlPanel(object):
    @cherrypy.expose
    def index(self):
        return template(INDEX)
    
if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 7889
    })
    
    config = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './assets/panel'
        }
    }
    cherrypy.quickstart(controlPanel(), "/", config)