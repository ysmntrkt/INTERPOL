# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 5000
RUN pip install --upgrade pip
# Install pip requirements
COPY ./requirements.txt .
RUN  python3 -m pip install -r requirements.txt --no-cache-dir 

WORKDIR /app
COPY . .
CMD ["python",  "./app.py"]
