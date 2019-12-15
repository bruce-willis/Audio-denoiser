FROM researchdeezer/spleeter:conda-gpu

ENV PATH /opt/conda/bin:$PATH

RUN conda install librosa -c conda-forge -y

RUN pip install kutana

WORKDIR /bot

ADD bot/ .

ENTRYPOINT [ "python", "kutana_bot.py" ]