# Stream bot

## The "why"

It's 2024, why is it still hard to answer questions like

- did I exercise at least three times a week as as I planned?
- when did I last meet X?
- when did I last run?
- how much did I spend this month on cabs?

## The "how"

Here's the solution I'm proposing. Talk into the bot & send it a message. It'll figure out the type of the event & metadata and store it in a database as an event. There will be other importers which will import data to the same event database.

Later on, natural language queries will be turned to structured queries & run on the database. The LLM will answer the questions in natural language.

## Setup

- setup a virtual env
- setup your openai API key with a env var named `OPENAI_API_KEY`
- setup your own stream bot on telegram & setup the bot token with a env var named `TELEGRAM_BOT_TOKEN`
- install requirements from `requirements.txt`
- run `python main.py`

### Context

I've been thinking of [self quantification](https://notes.bharatkalluri.com/Self-quantification) since a while.

Before this project, there was one more project I created in 2022 called [stream](https://github.com/BharatKalluri/stream) which was solving the same problem asking questions. The idea was that you'll explicitly put events into the database.

This was way too much effort and irritating. Say for example you did bicep curls of 3 sets. 16, 14, 12 reps of weights 5, 7.5 & 10. The idea was to type this out in a particular format so that it can be parsed, converted & stored to the database. Maybe in this example, it would be `/event bicep_curls 16,14,12 5,7.5,10`. This does not scale neatly when you want to collect a lot of data.

With this version, you can say into the mic using your keyboard TTS & send this message `did bicep curls of 3 sets. 16, 14, 12 reps of weights 5, 7.5 & 10` & an event with the corresponding metadata will be created and stored. Much more natural and simple.

Ideally you don't talk to the system at all, data flows from hardware & the database builds up by itself using importers. But unfortunately we are not there yet.

### TODO

This is still in very early stages

- [ ] add events into a database
- [ ] add more event models
- [ ] add a natural language query parser which feeds off the database & reports back with answers
