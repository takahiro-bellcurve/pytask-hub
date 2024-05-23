FROM prefecthq/prefect:2-latest

WORKDIR /app
ENV PREFECT_HOME "/prefect"

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN useradd -r prefect
