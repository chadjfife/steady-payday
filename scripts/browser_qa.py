import base64, json, os, time
from pathlib import Path
from urllib.parse import quote
import requests, websocket

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa"
OUT.mkdir(exist_ok=True)
BASE = os.environ.get("QA_URL", "http://127.0.0.1:4173").rstrip("/")

class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=30)
        self.i = 0
    def call(self, method, params=None):
        self.i += 1
        ident = self.i
        self.ws.send(json.dumps({"id": ident, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == ident:
                if "error" in message: raise RuntimeError(message["error"])
                return message.get("result", {})
    def close(self): self.ws.close()

def evaluate(cdp, expression):
    result = cdp.call("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
    return result["result"].get("value")

def audit(name, width, height, mobile, path="/"):
    target = requests.put("http://127.0.0.1:9222/json/new?" + quote("about:blank", safe="")).json()
    cdp = CDP(target["webSocketDebuggerUrl"])
    cdp.call("Page.enable")
    cdp.call("Runtime.enable")
    cdp.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile})
    cdp.call("Page.navigate", {"url": BASE + path})
    deadline = time.time() + 20
    while time.time() < deadline:
        if evaluate(cdp, "document.readyState") == "complete": break
        time.sleep(.1)
    time.sleep(.8)
    evaluate(cdp, "new Promise(resolve=>{window.scrollTo(0,document.body.scrollHeight);setTimeout(resolve,1200)})")
    metrics = cdp.call("Page.getLayoutMetrics")
    content = metrics["cssContentSize"]
    data = {
        "name": name,
        "viewport": [width, height],
        "title": evaluate(cdp, "document.title"),
        "h1": evaluate(cdp, "document.querySelector('h1').innerText"),
        "scroll_width": evaluate(cdp, "document.documentElement.scrollWidth"),
        "client_width": evaluate(cdp, "document.documentElement.clientWidth"),
        "broken_images": evaluate(cdp, "Array.from(document.images).filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)"),
        "empty_links": evaluate(cdp, "Array.from(document.querySelectorAll('a')).filter(a=>!a.getAttribute('href')||a.getAttribute('href')==='#').length"),
        "download_exists": requests.get(BASE + "/downloads/free-payday-bill-map.pdf", timeout=10).status_code == 200,
        "route_exists": requests.get(BASE + path, timeout=10).status_code == 200,
        "content_height": content["height"],
    }
    shot = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True, "fromSurface": True})
    (OUT / f"{name}.png").write_bytes(base64.b64decode(shot["data"]))
    cdp.close()
    assert data["scroll_width"] == data["client_width"], data
    assert not data["broken_images"], data
    assert data["empty_links"] == 0, data
    assert data["download_exists"], data
    assert data["route_exists"] and data["title"] != "Error response", data
    print(json.dumps(data, indent=2))

for args in [("desktop-1440",1440,1000,False),("mobile-390",390,844,True),("mobile-320",320,760,True),("reset-pack-desktop",1440,1000,False,"/payday-reset-pack.html"),("reset-pack-mobile-390",390,844,True,"/payday-reset-pack.html"),("reset-pack-mobile-320",320,760,True,"/payday-reset-pack.html"),("bill-calendar-desktop",1440,1000,False,"/biweekly-paycheck-bill-calendar.html"),("bill-calendar-mobile-390",390,844,True,"/biweekly-paycheck-bill-calendar.html"),("bill-calendar-mobile-320",320,760,True,"/biweekly-paycheck-bill-calendar.html")]:
    audit(*args)
