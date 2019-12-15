FROM researchdeezer/spleeter:3.7

RUN pip install kutana && pip install librosa

WORKDIR /bot

ADD bot/ .

ENTRYPOINT [ "python", "kutana_bot.py" ]