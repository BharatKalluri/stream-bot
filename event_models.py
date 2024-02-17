import abc
import datetime

from langchain.pydantic_v1 import BaseModel, Field


class BaseEvent(BaseModel, abc.ABC):
    event_at: datetime.datetime = Field(
        description="time at which the event occurred",
        default=datetime.datetime.now(),
    )


class RecordCoffeeEvent(BaseEvent):
    """Record an event of having coffee along with context of how many cups were had"""

    event_type: str = "COFFEE"
    cups: int = Field(..., description="number of cups", ge=1)


class RecordSocializingEvent(BaseEvent):
    """record an event meeting up & socializing with friends"""

    event_type: str = "SOCIALIZE"
    names: list[str] = Field(
        ..., description="list of people socialized with", min_items=1
    )


class _RecordBicepCurlSetEvent(BaseModel):

    rep_count: int = Field(..., description="number of reps", ge=1)
    weight: float = Field(..., description="weight", ge=0.1)


class RecordBicepCurlExerciseEvent(BaseEvent):
    """Record an event of a bicep curl exercise with rep count and weight"""

    event_type: str = "BICEP_CURL"
    sets: list[_RecordBicepCurlSetEvent] = Field(
        ..., description="list of set data with context of rep count & weight"
    )


class RecordPushUpsExerciseEvent(BaseEvent):
    """Record event of push-ups with count"""

    event_type: str = "PUSH_UP"
    count: int = Field(..., description="number of push ups", ge=1)


class ThoughtEvent(BaseEvent):
    """Record a thought as normal text"""

    event_type: str = "THOUGHT"
    thought: str = Field(..., description="raw text of the thought")
