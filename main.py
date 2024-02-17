import os

from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
import logging
from telegram import Update
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
)

from event_models import BaseEvent

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


entity_transformer_chain = create_openai_fn_runnable(
    functions=BaseEvent.__subclasses__(),
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system", "You are a world class algorithm for recording entities."),
            (
                "human",
                "Make calls to the relevant function to record the entities in the following input: {input}",
            ),
            (
                "human",
                "Tip: Make sure to answer in the correct format.",
            ),
        ]
    ),
)

open_ai_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

grammar_expert_chain = (
    ChatPromptTemplate.from_template(
        """
{input}
---
add punctuation & fix grammar in the above input"""
    )
    | open_ai_llm
)


def source_event_from_prompt(prompt: str) -> BaseModel:
    cleaned_prompt = grammar_expert_chain.invoke({"input": prompt}).content
    event_data: BaseModel = entity_transformer_chain.invoke({"input": cleaned_prompt})
    return event_data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")


async def text_message_handler_fn(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await contex.bot.send_message(chat_id=update.effective_chat.id, text="processing..")
    parsed_event = source_event_from_prompt(update.message.text)
    await contex.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
stored event

{parsed_event.json(indent=4)}
""",
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()
    )

    text_message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), text_message_handler_fn
    )
    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)
    application.add_handler(text_message_handler)

    application.run_polling()
