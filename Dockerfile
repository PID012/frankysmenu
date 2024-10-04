# Verwenden des offiziellen Python-Images
FROM python:3.9-slim

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Kopieren der Anforderungen in das Containerverzeichnis
COPY requirements.txt .

# Installieren der Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript in das Arbeitsverzeichnis
COPY main.py .

# Starten des Python-Skripts
CMD ["python", "main.py"]
