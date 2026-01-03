# pip install -U langchain langchain-core langchain-community langchain-google-genai panel wikipedia requests

import os
import param
import requests
import wikipedia
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

import panel as pn
from langchain.tools import tool

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# Session-based memory store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# Tools
@tool
def get_current_temperature(latitude: float, longitude: float) -> str:
    """
    Get current temperature (°C) using Open-Meteo API.
    """
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return "Weather API failed."

    data = response.json()
    now = datetime.now(timezone.utc)

    times = [
        datetime.fromisoformat(t.replace("Z", "+00:00"))
        for t in data["hourly"]["time"]
    ]
    temps = data["hourly"]["temperature_2m"]

    index = min(range(len(times)), key=lambda i: abs(times[i] - now))
    return f"The current temperature is {temps[index]}°C"


@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia and return summaries.
    """
    titles = wikipedia.search(query)
    summaries = []

    for title in titles[:3]:
        try:
            page = wikipedia.page(title, auto_suggest=False)
            summaries.append(f"**{title}**\n{page.summary}")
        except Exception:
            pass

    return "\n\n".join(summaries) if summaries else "No results found."


@tool
def reverse_data(query: str) -> str:
    """
    Reverse input text.
    """
    return f"Reverse of '{query}' is '{query[::-1]}'"


tools = [get_current_temperature, search_wikipedia, reverse_data]


# Model configuration
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"


# Panel App
pn.extension()

class ConversationalBot(param.Parameterized):

    def __init__(self, tools, **params):
        super().__init__(**params)
        self.panels = []

        # Gemini LLM
        model = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=0,
            project=PROJECT_ID,
            location=LOCATION,
        )

        llm_with_tools = model.bind_tools(tools)

        # Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful but sassy assistant."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # Base runnable
        base_runnable = (prompt | llm_with_tools | StrOutputParser())

        # Add memory
        self.agent = RunnableWithMessageHistory(
            base_runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def interact(self, query):
        if not query:
            return

        result = self.agent.invoke(
            {"input": query},
            config={"configurable": {"session_id": "panel-session"}}
        )

        self.panels.extend([
            pn.Row("User:", pn.pane.Markdown(query, width=500)),
            pn.Row(
                "ChatBot:",
                pn.pane.Markdown(
                    result,
                    width=500,
                    styles={"background-color": "#f0f0f0"}
                )
            )
        ])

        return pn.WidgetBox(*self.panels, scroll=True)


# UI layout
# cb = ConversationalBot(tools)

# user_input = pn.widgets.TextInput(placeholder="Ask me anything...")
# conversation = pn.bind(cb.interact, user_input)

# dashboard = pn.Column(
#     pn.pane.Markdown("# 🤖 Conversational Agent Bot"),
#     user_input,
#     pn.layout.Divider(),
#     pn.panel(conversation, loading_indicator=True, height=400),
# )

# dashboard.servable()
cb = ConversationalBot(tools)

user_input = pn.widgets.TextInput(
    placeholder="Ask me anything...",
    sizing_mode="stretch_width"
)

send_btn = pn.widgets.Button(
    name="Send",
    button_type="primary",
    width=80
)

chat_area = pn.Column(
    sizing_mode="stretch_width",
    height=420,
    scroll=True
)

def on_send(event=None):
    if not user_input.value.strip():
        return
    response = cb.interact(user_input.value)
    chat_area.objects = [response]
    user_input.value = ""

send_btn.on_click(on_send)
user_input.param.watch(lambda e: on_send() if e.new.endswith("\n") else None, "value")

dashboard = pn.Column(
    pn.pane.Markdown("## 🤖 Conversational Agent", align="center"),
    chat_area,
    pn.layout.Divider(margin=(5, 0)),
    pn.Row(user_input, send_btn, sizing_mode="stretch_width"),
    sizing_mode="stretch_width",
    width=700
)

dashboard.servable()
