import abc
import datetime
from typing import ClassVar

from langchain.chains.openai_functions import create_openai_fn_runnable
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


class BaseEvent(BaseModel, abc.ABC):
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )

    @property
    @abc.abstractmethod
    def event_type(self) -> str:
        pass


class RecordCoffeeEvent(BaseEvent):
    """Record an event of having coffee along with context of how many cups were had"""

    event_type: ClassVar[str] = "COFFEE"
    cups: int = Field(..., description="number of cups", ge=1)


class RecordSocializingEvent(BaseEvent):
    """record an event meeting up & socializing with friends"""

    event_type: ClassVar[str] = "SOCIALIZE"
    names: list[str] = Field(
        ..., description="list of people socialized with", min_items=1
    )


class _RecordBicepCurlSetEvent(BaseModel):

    rep_count: int = Field(..., description="number of reps", ge=1)
    weight: float = Field(..., description="weight", ge=0.1)


class RecordBicepCurlExerciseEvent(BaseEvent):
    """Record an event of a bicep curl exercise with rep count and weight"""

    event_type: ClassVar[str] = "BICEP_CURL"
    sets: list[_RecordBicepCurlSetEvent] = Field(
        ..., description="list of set data with context of rep count & weight"
    )


class ThoughtEvent(BaseEvent):
    """Record a thought as normal text"""

    event_type: ClassVar[str] = "THOUGHT"
    thought: str = Field(..., description="raw text of the thought")


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


def source_event_from_prompt(prompt: str) -> dict:
    cleaned_prompt = grammar_expert_chain.invoke({"input": prompt}).content
    event_data = entity_transformer_chain.invoke({"input": cleaned_prompt})
    return dict(**event_data.__dict__, raw_prompt=prompt)


if __name__ == "__main__":
    prompts = []
    print([source_event_from_prompt(p) for p in prompts])
