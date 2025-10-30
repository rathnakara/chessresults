# Database Setup for Render

This app now uses **PostgreSQL** to persist tournament monitoring sessions across app restarts.

## Why Database?

- **Sessions survive restarts**: Even when Render's free tier sleeps or restarts, your monitoring sessions are preserved
- **Automatic recovery**: Monitoring threads automatically restart when the app wakes up
- **No data loss**: Tournament data persists between deployments

## Setup on Render (Free Tier)

### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → Select **"PostgreSQL"**
3. Configure:
   - **Name**: `chess-monitor-db` (or your preferred name)
   - **Database**: `chessmonitor`
   - **User**: (auto-generated)
   - **Region**: Same as your web service
   - **Plan**: **Free** (500 MB storage, expires after 90 days)
4. Click **"Create Database"**
5. Wait 2-3 minutes for database to be ready

### Step 2: Get Database URL

1. Once database is created, go to database dashboard
2. Copy the **"External Database URL"** (starts with `postgres://`)
3. Example format:
   ```
   postgres://username:password@dpg-xxxxx.region.render.com/dbname
   ```

### Step 3: Connect Database to Web Service

1. Go to your web service dashboard (chess-pr4v)
2. Click **"Environment"** tab
3. Add new environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the database URL you copied
4. Click **"Save Changes"**
5. Your app will automatically redeploy with database support

## How It Works

### Automatic Behavior:

1. **First Deploy**: Creates database tables automatically
2. **Add Session**: Saves session info to PostgreSQL
3. **App Restarts**: Loads all active sessions from database
4. **Monitoring Resumes**: Automatically restarts monitoring threads

### Database Structure:

```sql
CREATE TABLE sessions (
    id VARCHAR PRIMARY KEY,
    url VARCHAR NOT NULL,
    config TEXT NOT NULL,  -- JSON
    status VARCHAR DEFAULT 'starting',
    created_at TIMESTAMP DEFAULT NOW(),
    last_update TIMESTAMP,
    data TEXT,  -- JSON
    error VARCHAR
);
```

## Local Development

For local testing without PostgreSQL:

```bash
# App automatically uses SQLite locally
# No configuration needed!
python app.py
```

The app creates `sessions.db` file in your project directory.

## Verify Database Connection

After deployment, check logs in Render dashboard:

```
✅ Good signs:
🔄 Checking for existing sessions to restart...
✅ Restarted X monitoring sessions
♟️  Chess Tournament Monitor - Multi-Session

❌ Problems:
- Connection errors
- Database not found
- Authentication failed
```

## Important Notes

### Render Free Tier Limitations:

1. **Database expires after 90 days**
   - You'll need to create a new database
   - Export important data before expiry

2. **500 MB storage limit**
   - Perfect for this use case
   - Each session is ~1-5 KB
   - Can store thousands of sessions

3. **Shared resources**
   - Performance may vary
   - Suitable for small-medium use

### Best Practices:

1. **Clean up old sessions**
   - Remove finished tournament sessions
   - Prevents database clutter

2. **Monitor storage**
   - Check database size in Render dashboard
   - Delete old sessions if needed

3. **Backup important data**
   - Export session data if needed
   - Before database expiry (90 days)

## Upgrade Options

If you need more:

### Render Paid Plans:
- **Starter ($7/month)**: 1 GB storage, no expiry
- **Standard ($20/month)**: 10 GB storage, daily backups

### Alternative Free Databases:
- **Supabase**: 500 MB PostgreSQL (permanent)
- **Railway**: 1 GB PostgreSQL + 500 hours/month
- **Neon**: 3 GB PostgreSQL (free tier)

To use alternative database:
1. Create database on your chosen platform
2. Copy connection URL
3. Add to Render environment as `DATABASE_URL`

## Troubleshooting

### Sessions not restarting after deployment?

Check logs for errors:
```bash
# In Render dashboard → Logs tab
# Look for: "🔄 Checking for existing sessions"
```

### Database connection errors?

1. Verify `DATABASE_URL` is set correctly
2. Check database is running (not expired)
3. Ensure URL format is correct (`postgresql://` not `postgres://`)

### Local SQLite not working?

```bash
# Delete old database and restart
rm sessions.db
python app.py
```

### Want to reset all sessions?

```bash
# In Render Shell or locally:
python -c "from src.database import Database; db = Database(); db.create_tables()"
```

## Migration from In-Memory

If you're upgrading from the old in-memory version:

1. All previous sessions will be lost (they were in memory)
2. Deploy with database setup
3. Start fresh - add tournaments again
4. From now on, sessions persist!

## Summary

✅ **Free PostgreSQL** on Render
✅ **Automatic setup** - just add DATABASE_URL
✅ **Sessions persist** across restarts
✅ **Auto-restart** monitoring threads
✅ **Local development** uses SQLite

Your chess tournament monitor is now production-ready! 🎉
