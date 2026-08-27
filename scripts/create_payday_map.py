from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "downloads" / "free-payday-bill-map.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAPER = HexColor("#F7F2E9")
INK = HexColor("#2D342F")
FOREST = HexColor("#355746")
CLAY = HexColor("#C9795D")
OAT = HexColor("#DED2C0")
WHITE = HexColor("#FFFDF9")

pdfmetrics.registerFont(TTFont("NotoSerif", "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifBold", "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"))
pdfmetrics.registerFont(TTFont("NotoSans", "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSansBold", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"))

c = canvas.Canvas(str(OUT), pagesize=letter)
w, h = letter
c.setTitle("The 10-Minute Payday Bill Map")
c.setAuthor("Steady Payday")
c.setSubject("Free printable payday and bill planning worksheet")
c.setFillColor(PAPER)
c.rect(0, 0, w, h, stroke=0, fill=1)

# Header
c.setFillColor(FOREST)
c.roundRect(36, h-116, w-72, 78, 10, stroke=0, fill=1)
c.setFillColor(WHITE)
c.setFont("NotoSansBold", 9)
c.drawString(54, h-62, "STEADY PAYDAY  •  FREE PRINTABLE")
c.setFont("NotoSerifBold", 23)
c.drawString(54, h-92, "The 10-Minute Payday Bill Map")
c.setFont("NotoSans", 8.5)
c.drawRightString(w-54, h-93, "One check. The bills it needs to carry.")

# Payday details
c.setFillColor(INK)
c.setFont("NotoSansBold", 9)
c.drawString(44, h-145, "THIS PAYDAY")
c.setStrokeColor(OAT)
c.setLineWidth(1)
fields = [(44, "Payday date"), (224, "Take-home amount"), (414, "Next payday")]
for x, label in fields:
    c.setFillColor(CLAY)
    c.setFont("NotoSans", 7.5)
    c.drawString(x, h-164, label.upper())
    c.setStrokeColor(OAT)
    c.line(x, h-190, x+150, h-190)

# Bill table
c.setFillColor(FOREST)
c.setFont("NotoSerifBold", 15)
c.drawString(44, h-225, "Bills due before the next payday")
c.setFont("NotoSans", 8)
c.setFillColor(INK)
c.drawRightString(w-44, h-225, "Write the real due date. Future-you will appreciate it.")

top = h-245
cols = [44, 250, 346, 456, 548]
headers = ["BILL", "DUE", "AMOUNT", "PAID?", "NOTES"]
c.setFillColor(OAT)
c.rect(44, top-24, w-88, 24, stroke=0, fill=1)
c.setFillColor(FOREST)
c.setFont("NotoSansBold", 7.5)
for x, label in zip(cols, headers): c.drawString(x+4, top-16, label)
row_h = 32
c.setStrokeColor(OAT)
for r in range(8):
    y = top-24-(r+1)*row_h
    c.setFillColor(WHITE if r%2==0 else PAPER)
    c.rect(44, y, w-88, row_h, stroke=0, fill=1)
    c.setStrokeColor(OAT)
    c.line(44, y, w-44, y)
    for x in cols[1:]: c.line(x, y, x, y+row_h)

# Totals strip
base = 188
c.setFillColor(WHITE)
c.roundRect(44, base, w-88, 88, 8, stroke=0, fill=1)
summary = [(58, "TOTAL BILLS"), (226, "ROOM AFTER BILLS"), (410, "SET ASIDE")]
for x, label in summary:
    c.setFillColor(CLAY)
    c.setFont("NotoSansBold", 7.5)
    c.drawString(x, base+62, label)
    c.setStrokeColor(OAT)
    c.line(x, base+28, x+130, base+28)

# Note area
c.setFillColor(FOREST)
c.setFont("NotoSerifBold", 13)
c.drawString(44, 152, "One thing I do not want to keep in my head")
c.setStrokeColor(OAT)
for y in [130, 108, 86]: c.line(44, y, w-44, y)

c.setFillColor(INK)
c.setFont("NotoSans", 7.2)
c.drawString(44, 52, "Planning worksheet only. It does not calculate taxes, verify balances, or replace professional advice.")
c.setFillColor(CLAY)
c.setFont("NotoSansBold", 7.2)
c.drawRightString(w-44, 52, "STEADYPAYDAY")

c.showPage()
c.save()
print(OUT)
