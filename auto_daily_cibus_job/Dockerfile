FROM python:3.12-bookworm

RUN pip install playwright==1.42.0 && \
    playwright install --with-deps chromium

COPY ./main.py .
CMD ["python", "./main.py"]