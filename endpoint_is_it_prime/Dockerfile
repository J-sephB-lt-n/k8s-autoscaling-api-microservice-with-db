FROM python:3.12-slim

# Copy local code to the container image #
WORKDIR /endpoint_is_it_prime
COPY . ./

# Install python dependencies #
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4",  "app:app"] 
