"""
Linux FS AI Agent
pip install google-genai python-telegram-bot
"""
import os,glob,shutil,time,subprocess,difflib,requests
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,ContextTypes,filters
API_KEY=os.environ["G_API_KEY"]
TG_TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN")
MODEL="gemini-2.5-flash"
MAX_STEPS=10
client=genai.Client(api_key=API_KEY)

tool_config=types.Tool(function_declarations=[
types.FunctionDeclaration(name="memory_info",description="Show Linux memory info",parameters={"type":"object","properties":{}}),
types.FunctionDeclaration(name="system_uptime",description="Show Linux uptime",parameters={"type":"object","properties":{}}),
types.FunctionDeclaration(name="process_list",description="Show Linux processes",parameters={"type":"object","properties":{"keyword":{"type":"string"}}}),
types.FunctionDeclaration(name="list_dir",description="List directory files",parameters={"type":"object","properties":{"path":{"type":"string"}}}),
types.FunctionDeclaration(name="find_files",description="Find files by pattern",parameters={"type":"object","properties":{"directory":{"type":"string"},"pattern":{"type":"string"}}}),
types.FunctionDeclaration(name="find_large_files",description="Find large files",parameters={"type":"object","properties":{"directory":{"type":"string"},"min_mb":{"type":"integer"}}}),
types.FunctionDeclaration(name="create_backup",description="Create file backup",parameters={"type":"object","properties":{"path":{"type":"string"}}}),
types.FunctionDeclaration(name="compare_files",description="Compare two files",parameters={"type":"object","properties":{"path1":{"type":"string"},"path2":{"type":"string"}}}),
types.FunctionDeclaration(name="weather_now",description="Show current weather by city",parameters={"type":"object","properties":{"city":{"type":"string"}}}),
types.FunctionDeclaration(name="world_time",description="Show current time by city",parameters={"type":"object","properties":{"city":{"type":"string"}}})
])

def get_city(city):
    try:
        city=city.lower().strip()
        city=city.replace("время","")
        city=city.replace("погода","")
        city=city.replace("в ","")
        city=city.strip()
        aliases={
            "алмате":"алматы",
            "астане":"астана",
            "москве":"москва"
        }
        city=aliases.get(city,city)
        url="https://geocoding-api.open-meteo.com/v1/search"
        r=requests.get(
            url,
            params={
                "name":city,
                "count":1,
                "language":"ru",
                "format":"json"
            },
            timeout=10
        ).json()
        if "results" not in r:
            return {"error":"Город не найден"}
        x=r["results"][0]
        return {
            "name":x["name"],
            "country":x.get("country",""),
            "lat":x["latitude"],
            "lon":x["longitude"],
            "timezone":x["timezone"]
        }
    except Exception as e:
        return {"error":str(e)}
def weather_now(city):
    try:
        c=get_city(city)
        if "error" in c:
            return c
        url="https://api.open-meteo.com/v1/forecast"
        r=requests.get(
            url,
            params={
                "latitude":c["lat"],
                "longitude":c["lon"],
                "current":"temperature_2m,wind_speed_10m,relative_humidity_2m",
                "timezone":c["timezone"]
            },
            timeout=10
        ).json()
        cur=r["current"]
        return {
            "city":c["name"],
            "country":c["country"],
            "temperature":cur["temperature_2m"],
            "humidity":cur["relative_humidity_2m"],
            "wind_speed":cur["wind_speed_10m"]
        }
    except Exception as e:
        return {"error":str(e)}
def world_time(city):
    try:
        c=get_city(city)

        if "error" in c:
            return c

        now=datetime.now(ZoneInfo(c["timezone"]))

        return {
            "city":c["name"],
            "country":c["country"],
            "timezone":c["timezone"],
            "time":now.strftime("%H:%M:%S"),
            "date":now.strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"error":str(e)}

def find_files(directory,pattern):
    try:return {"files":glob.glob(os.path.join(directory,"**",pattern),recursive=True)[:20]}
    except Exception as e:return {"error":str(e)}

def read_file(path):
    try:
        with open(path,"r",encoding="utf-8",errors="ignore") as f:return {"content":f.read(4000),"size":os.path.getsize(path)}

    except Exception as e:return {"error":str(e)}

def file_info(path):
    try:
        st=os.stat(path)
        return {"path":path,"size":st.st_size,"modified":time.ctime(st.st_mtime),"is_dir":os.path.isdir(path)}
    except Exception as e:return {"error":str(e)}

def disk_usage(path="/"):
    try:
        t,u,f=shutil.disk_usage(path)
        g=1024**3
        return {"total_gb":round(t/g,2),"used_gb":round(u/g,2),"free_gb":round(f/g,2)}
    except Exception as e:return {"error":str(e)}

def create_file(path,content):
    try:
        p=os.path.join(os.getcwd(),os.path.basename(path))
        with open(p,"w",encoding="utf-8") as f:f.write(content)
        return {"created":p}
    except Exception as e:return {"error":str(e)}

def list_dir(path="."):
    try:return {"items":[{"name":x,"is_dir":os.path.isdir(os.path.join(path,x))} for x in os.listdir(path)[:40]]}
    except Exception as e:return {"error":str(e)}

def search_in_file(path,keyword):
    try:
        r=[]
        with open(path,"r",encoding="utf-8",errors="ignore") as f:
            for n,l in enumerate(f,1):
                if keyword.lower() in l.lower():r.append({"line":n,"text":l.strip()})
        return {"matches":r[:20]}
    except Exception as e:return {"error":str(e)}

def process_list(keyword=""):
    try:
        r=subprocess.run(["ps","aux"],capture_output=True,text=True).stdout.splitlines()
        if keyword:r=[x for x in r if keyword.lower() in x.lower()]
        return {"processes":r[:25]}
    except Exception as e:return {"error":str(e)}

def memory_info():
    try:return {"memory":subprocess.run(["free","-h"],capture_output=True,text=True).stdout}
    except Exception as e:return {"error":str(e)}

def system_uptime():
    try:return {"uptime":subprocess.run(["uptime"],capture_output=True,text=True).stdout}
    except Exception as e:return {"error":str(e)}

def find_large_files(directory=".",min_mb=10):
    try:
        r=[];limit=min_mb*1024*1024
        for root,dirs,files in os.walk(directory):
            for n in files:
                p=os.path.join(root,n)
                try:
                    s=os.path.getsize(p)
                    if s>=limit:r.append({"path":p,"size_mb":round(s/1048576,2)})
                except:pass
        return {"files":sorted(r,key=lambda x:x["size_mb"],reverse=True)[:20]}
    except Exception as e:return {"error":str(e)}

def create_backup(path):
    try:
        b=path+".backup"
        shutil.copy2(path,b)
        return {"backup":b}
    except Exception as e:return {"error":str(e)}

def compare_files(path1,path2):
    try:
        with open(path1,"r",encoding="utf-8",errors="ignore") as f:a=f.readlines()
        with open(path2,"r",encoding="utf-8",errors="ignore") as f:b=f.readlines()
        d=list(difflib.unified_diff(a,b,fromfile=path1,tofile=path2,lineterm=""))
        return {"different":bool(d),"diff":d[:50]}
    except Exception as e:return {"error":str(e)}

TOOLS={
"find_files":find_files,
"read_file":read_file,
"file_info":file_info,
"disk_usage":disk_usage,
"create_file":create_file,
"list_dir":list_dir,
"search_in_file":search_in_file,
"process_list":process_list,
"memory_info":memory_info,
"system_uptime":system_uptime,
"find_large_files":find_large_files,
"create_backup":create_backup,
"compare_files":compare_files,
"weather_now":weather_now,
"world_time":world_time
}

def call_model(history,config):
    for a in range(3):
        try:return client.models.generate_content(model=MODEL,contents=history,config=config)
        except Exception as e:
            if a<2 and ("429" in str(e) or "503" in str(e)):time.sleep(5*(a+1))
            else:raise

def agent_answer(user_input,history=None):
    history=history or []
    config=types.GenerateContentConfig(
        tools=[tool_config],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        system_instruction="You are a Linux filesystem assistant. Use tools before answering."
    )
    history.append(types.Content(role="user",parts=[types.Part.from_text(text=user_input)]))
    for step in range(MAX_STEPS):
        response=call_model(history,config)
        content=response.candidates[0].content
        history.append(content)
        calls=[p.function_call for p in content.parts if p.function_call]
        if not calls:return response.text or "Нет ответа."
        parts=[]
        for c in calls:
            fn=TOOLS.get(c.name)
            try:result=fn(**c.args) if fn else {"error":"Unknown tool"}
            except Exception as e:result={"error":str(e)}
            parts.append(types.Part.from_function_response(name=c.name,response={"result":result}))
        history.append(types.Content(role="user",parts=parts))
    return "Достигнут лимит шагов."

def run_cli():
    h=[]
    while True:
        t=input("You: ").strip()
        if not t or t.lower() in ("exit","quit","выход"):break
        print(agent_answer(t,h))

async def telegram_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        a=agent_answer(update.message.text)
        await update.message.reply_text(a[:4000])
    except Exception as e:
        await update.message.reply_text(str(e))

def run_telegram():
    if not TG_TOKEN:return run_cli()
    app=ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,telegram_handler))
    app.run_polling()

if __name__=="__main__":
    run_telegram()
