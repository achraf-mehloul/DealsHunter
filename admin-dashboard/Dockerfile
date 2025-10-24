# Admin Dashboard Dockerfile
FROM node:18-alpine

WORKDIR /app

# نسخ ملفات التبعيات
COPY package*.json ./
RUN npm ci --only=production

# نسخ الكود المصدري
COPY . .

# بناء التطبيق
RUN npm run build

# تعريض المنفذ
EXPOSE 3000

# تشغيل التطبيق
CMD ["npm", "start"]
