FROM node:20-alpine AS builder

WORKDIR /app

# Copy semua file
COPY package*.json ./
RUN npm install

COPY . .

# CREATE .env.local FILE DURING BUILD
RUN echo "NEXT_PUBLIC_SUPABASE_URL=https://owmrezsemtzosfuzhwfz.supabase.co" > .env.local
RUN echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MioiJzdXBhYmFzZSIsInJ1ZiI6Im93bXJlenNlbXR6b3NmdXpod2Z6Iiwiicm9sZSI6ImFub24iLCJpYXQiojE3Nzk3MTcwNTMsImV4cCI6MjA5NTI5MzA1M30.mdonuHSeYP" >> .env.local

# Build
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.env.local ./.env.local

EXPOSE 3000

# Gunakan $PORT seperti yang diwarisi daripada Railway
CMD ["sh", "-c", "npm start -- --port ${PORT:-3000}"]