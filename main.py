import datetime
from typing import Sequence, TypeVar

from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


class BaseEvent(BaseModel):
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )


class RecordCoffeeEvent(BaseEvent):
    """Record an event of having coffee along with context of how many cups were had"""

    cups: int = Field(..., description="number of cups")
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )


class RecordSocializingEvent(BaseEvent):
    """record an event meeting up & socializing with friends"""

    names: list[str] = Field(..., description="list of people socialized with")
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )


class _RecordBicepCurlSetEvent(BaseModel):
    """Record an event of a bicep curl with context of rep count and weight"""

    rep_count: int = Field(..., description="number of reps")
    weight: float = Field(..., description="weight")


class RecordBicepCurlExerciseEvent(BaseEvent):
    sets: list[_RecordBicepCurlSetEvent] = Field(
        ..., description="list of set data with context of rep count & weight"
    )
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )


event_classes = BaseEvent.__subclasses__()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a world class algorithm for recording entities."),
        (
            "human",
            "Make calls to the relevant function to record the entities in the following input: {input}",
        ),
        ("human", "Tip: Make sure to answer in the correct format"),
    ]
)
chain = create_openai_fn_runnable(
    event_classes,
    llm,
    prompt,
)
chain_invoke_resp = chain.invoke({"input": "bicep curl 5 10 15 kgs and 3 5 15 reps"})
print(chain_invoke_resp)
