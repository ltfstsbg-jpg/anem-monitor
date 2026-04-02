import requests,time
requests.packages.urllib3.disable_warnings()
CAR="400298014600"
NIN="109980090014600005"
TOKEN="8673770315:AAHEeYs2xBq95rXnReIrz-_z6W9H49GRxYo"
CHAT="5492379451"
def tg(m):
 try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",data={"chat_id":CHAT,"text":m},timeout=10)
 except: pass
def check():
 s=requests.Session()
 s.headers.update({"User-Agent":"Mozilla/5.0","Content-Type":"application/json","Origin":"https://minha.anem.dz","Referer":"https://minha.anem.dz/pre_inscription"})
 try:
  r=s.post("https://minha.anem.dz/api/pre-inscription/login",json={"numeroWassit":CAR,"numeroPieceIdentite":NIN},timeout=30,verify=False)
  print("Login:",r.status_code,r.text[:100])
  r2=s.get("https://minha.anem.dz/api/pre-inscription/rendez-vous",timeout=30,verify=False)
  print("RDV:",r2.status_code,r2.text[:100])
  if "aucun" in r2.text.lower():
   print("no appointment")
   return False
  return True
 except Exception as e:
  print("error:",e)
  return False
print("started")
tg("started monitoring")
while True:
 if check(): tg("APPOINTMENT FOUND!\nhttps://minha.anem.dz/pre_inscription")
 time.sleep(1800)
