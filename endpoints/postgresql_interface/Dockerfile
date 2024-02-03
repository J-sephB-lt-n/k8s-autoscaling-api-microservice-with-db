FROM python:3.12-slim

# Copy local code to the container image #
WORKDIR /postgresql_interface
COPY . ./

# Install python dependencies #
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80 

CMD ["gunicorn", "--bind", ":80", "--workers", "1", "--threads", "4",  "app:app"] 
