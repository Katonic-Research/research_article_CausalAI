FROM python:3.8.2-slim

COPY app.py .
COPY image image
COPY pages pages
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD streamlit run app.py --server.port=8050 --server.address=0.0.0.0 --logger.level error