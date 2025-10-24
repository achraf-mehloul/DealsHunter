FROM python:3.11-slim

WORKDIR /app

# تثبيت النظام
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات التبعيات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY . .

# إنشاء مجلد السجلات
RUN mkdir -p logs

# تشغيل البوت
CMD ["python", "bot.py"]