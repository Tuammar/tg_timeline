from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from funcs import Huinya as h
from json import load

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
file = load(open('result.json'))
z = h(file)
contacts = z.get_frequent_contacts()
all_contacts = z.get_all_contacts()
for i in range(len(all_contacts)):
    all_contacts[i]['name'] = all_contacts[i]['first_name'] + ' ' + all_contacts[i]['last_name']


@app.get("/timeline", response_class=HTMLResponse)
async def read_timeline(request: Request, id: int):
    chat = z.get_chat_by_id(id)
    timeline = z.analyse_messages(z.get_chat_timeline(chat))
    data = {date.isoformat(): metrics for date, metrics in timeline.items()}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/contacts", response_class=HTMLResponse)
async def read_contacts(request: Request):
    return templates.TemplateResponse("contacts.html",
                                      {"request": request, "contacts": contacts, "all_contacts": all_contacts})


@app.get("/search", response_class=HTMLResponse)
async def search_contacts(request: Request, query: str):
    filtered_contacts = [contact for contact in contacts if
                         query.lower() in contact["name"].lower() or str(contact["id"]) == query]
    filtered_all_contacts = [contact for contact in all_contacts if
                             query.lower() in contact["name"].lower() or query.lower() in contact.get("first_name",
                                                                                                      "").lower() or query.lower() in contact.get(
                                 "last_name", "").lower() or query.lower() in contact.get("phone_number", "").lower()]
    return templates.TemplateResponse("contacts.html", {"request": request, "contacts": filtered_contacts,
                                                        "all_contacts": filtered_all_contacts, "query": query})
