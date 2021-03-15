import qrcode
from PIL import Image, ImageDraw, ImageFont
from pymongo import MongoClient
import os
import config
cluster = MongoClient(config.MongoURI)
db = cluster["sportcomdb"]
collection = db["sportcomdbs"]

font = ImageFont.truetype("font.otf", 22, encoding='UTF-8')
TicketDirName = "Tickets"
NumberOfTickets = 10
id_req = 0 #Запрашиваемый id с которого начинается перебор
Path = os.path.abspath(os.curdir) #Устанавливаем расположение корневой папки

qr = qrcode.QRCode(
    version=1,
    box_size=6,
    border=0
)

while id_req < NumberOfTickets:
    results = collection.find({"UserID": id_req})
    for result in results:
        data = result['_id']
    qr.add_data(config.QRAddress + str(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    fon = Image.open("TicketBlank.png")
    draw = ImageDraw.Draw(fon)
    id_text = str(id_req)
    if(id_req < 10): #Генерирую числа в формате 001 010 100
        id_text = str(0) + id_text
    if(id_req < 100):
        id_text = str(0) + id_text
    draw.text((364, 655), str(id_text), font=font) #Для повышения жирности цифр накладывается слегка смещенный повтор цифры
    draw.text((363, 655), str(id_text), font=font)
    fon.paste(img, (fon.width-346, 370))
    if(os.path.exists(TicketDirName) == False): #Проверка на существование папки с билетами
        os.mkdir(TicketDirName)
    os.chdir(TicketDirName)
    fon.save(str(id_req)+'.png')
    os.chdir(Path)
    id_req = id_req + 1
    qr.clear()

TicketsPath = Path + "/" + TicketDirName
os.startfile(TicketsPath)
print("Done")

