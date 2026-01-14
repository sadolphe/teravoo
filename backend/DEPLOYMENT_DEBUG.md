# Remote Seeding & Frontend Fixes

## 1. Remote Database Seeding
I created a script to easily seed your online database from your local machine.

### How to use
```bash
cd backend
./seed_remote.sh
```
This script automatically detects your remote `DATABASE_URL` from the `.env` file (stored safely as `REMOTE_DATABASE_URL`).

### Data Enriched
The seeding script now includes:
- **5 Producers** (including "Organic Spices Mananara", "Sofia Region", etc.)
- **7 Products** (including Wild Pepper, Pink Peppercorns, Industrial Vanilla)

## 2. Frontend Connection Fixes
### Issues Identified
1.  **CORS**: The backend on Render blocked requests from Vercel.
2.  **Environment Variable**: The frontend on Vercel didn't know the backend URL (`NEXT_PUBLIC_API_URL`).
3.  **Mock Data**: The Traceability page was using hardcoded fake data.

### Fixes Applied
- **Code**: Updated `web/lib/api.ts` and `web/app/orders/[id]/traceability/page.tsx` to use the real API.
- **Boot Script**: Fixed `backend/app/initial_data.py` to stop crashing when the database is already seeded.
- **Config Required**: You need to update `BACKEND_CORS_ORIGINS` on Render (add your shiny new domain) and `NEXT_PUBLIC_API_URL` on Vercel.

## 3. Verification
- Validated that the remote database contains the new products using `check_data.py`.
- Validated backend accessibility via `curl`.

## Next Steps for You
1.  **Redeploy Frontend**: Go to Vercel and redeploy to apply the code changes.

## 4. Troubleshooting & Lessons Learned (Critical)
We encountered significant deployment issues that are now resolved. Here is the summary for future reference:

### Repository Mismatch (The "Hidden" Ancestor)
- **Problem**: Render was stuck on an old commit (`7e2fbf8`) and ignored new pushes to `origin`.
- **Cause**: Render was connected to the legacy repository `sadolphe/teravoo` (remote: `production-legacy`), while we were pushing to `sadolphe/teravoo-core` (remote: `origin`).
- **Fix**: We pushed our changes to the legacy remote:
  ```bash
  git push production-legacy main
  ```
  *Recommendation*: Update the Render service settings to point to the correct `teravoo-core` repository to avoid this confusion in the future.

### Boot Script Crash (`initial_data.py`)
- **Problem**: Deployment failed because `app.initial_data.py` (run by Render on startup) tried to re-insert producers that already existed (duplicate ID error).
- **Fix**: We modified `backend/app/initial_data.py` to check if `ProducerProfile` count > 0 before inserting. If the DB is seeded, it now skips the default data gracefully.

### Deployment "Stuck"
- **Symptom**: "Manual Deploy > Latest Commit" kept claiming "No commits found".
- **Fix**: This was a direct consequence of the repository mismatch. Once we pushed to the correct remote (`production-legacy`), Render immediately picked up the new commit.
