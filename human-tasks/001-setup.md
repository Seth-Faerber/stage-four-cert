# Setup Checklist

## Environment Setup
- [x] Clone the repository
- [x] Install Node.js 20+
- [x] Run `npm install`
- [ ] Copy `.env.example` to `.env` and fill in values
- [ ] Provision a PostgreSQL database and set `DATABASE_URL`
- [ ] Obtain API key and set `API_KEY`

## Application Verification
- [x] Confirm `npm start` launches without errors
- [x] Verify JWT authentication works (test with a valid token against GET /api/users)
- [ ] Confirm database connection is live (check logs for connection errors)

## API Routes
- [ ] Create `src/app/api/health/route.ts` file
- [ ] Implement `GET /api/health` endpoint
- [x] Create `src/app/api/users/route.ts` file
- [ ] Implement `POST /api/users` endpoint

## Ongoing
- [ ] Set up log aggregation for production
