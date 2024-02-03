# Use the official lightweight Python image #
# https://hub.docker.com/_/python #
FROM python:3.12-slim

# Copy local code to the container image #
WORKDIR /api_gateway
COPY . ./

# Install python dependencies #
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Use CMD to run something every time the the container starts up #
# See also "ENTRYPOINT" command # 
CMD ["gunicorn", "--bind", ":5000", "--workers", "1", "--threads", "8", "main:app"]
