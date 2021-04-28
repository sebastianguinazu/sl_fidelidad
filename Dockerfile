FROM python:3.8-slim-buster
COPY . /sl_fidelidad
WORKDIR /sl_fidelidad
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["app_sl.py"]
