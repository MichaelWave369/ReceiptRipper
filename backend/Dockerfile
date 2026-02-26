FROM node:20-alpine AS webbuild
WORKDIR /web
COPY web/package*.json ./
RUN npm install
COPY web ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr libgl1 && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY backend /app/backend
COPY --from=webbuild /web/dist /app/web/dist
ENV PYTHONPATH=/app/backend
EXPOSE 8000
CMD ["uvicorn", "receiptrip.main:app", "--host", "0.0.0.0", "--port", "8000"]
