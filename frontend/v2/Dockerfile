# =========================
# Build stage
# =========================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./ 
COPY bun.lockb ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# =========================
# Production stage
# =========================
FROM node:18-alpine AS production

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expose port
EXPOSE 8080

# Set environment variable for serve
ENV PORT=8080

# Lightweight health check using Node.js
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:8080', res => process.exit(res.statusCode===200?0:1)).on('error',()=>process.exit(1))"

# Serve the built application using local node_modules/serve
CMD ["npx", "serve", "-s", "dist", "-l", "8080"]
