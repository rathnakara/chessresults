# UI Updates - 4 Session Limit

## Overview
Updated the Chess Tournament Monitor UI to enforce a maximum of 4 concurrent monitoring sessions with an improved user experience.

## Changes Made

### 1. Backend (app.py)
- **Added MAX_SESSIONS constant**: Set to 4
- **Session limit enforcement**: `/api/monitor` endpoint now returns 429 error when limit reached
- **Updated startup message**: Shows max concurrent sessions in feature list

### 2. Home Page (simple_index.html)
**New Features:**
- Session counter badge showing "X / 4 sessions active"
- Real-time session count updates
- Automatic form disabling when limit reached
- Warning banner when maximum sessions reached
- Auto-refresh session count after adding new session

**Visual Updates:**
- Session counter with gradient background (blue/purple when available, red when full)
- Yellow warning banner when limit is reached
- Better user feedback

### 3. All Sessions View (simple_view.html)
**Layout Changes:**
- 2x2 grid layout optimized for 4 sessions
- Responsive design (single column on mobile)
- Session counter in header

**Functionality:**
- Auto-update session count when session is removed
- Better empty state messaging

### 4. Single Session View (single_view.html)
- No changes needed (already works well)

## Features

### Session Management
- ✅ Maximum 4 concurrent sessions
- ✅ Real-time session counting
- ✅ Automatic UI updates
- ✅ Clear visual feedback when limit reached
- ✅ Server-side enforcement

### Visual Design
- ✅ 2x2 grid layout for 4 sessions
- ✅ Responsive design
- ✅ Color-coded session counter
- ✅ Warning messages
- ✅ Smooth animations

### User Experience
- ✅ Cannot add more than 4 sessions
- ✅ Must remove a session before adding new one
- ✅ Clear visual indicators
- ✅ Form automatically disables at limit
- ✅ Helpful warning messages

## How to Use

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Access the UI:**
   - Home: http://localhost:8080/
   - All Sessions: http://localhost:8080/view

3. **Add sessions:**
   - Enter tournament URL
   - Click "Start Monitoring"
   - Session counter updates automatically
   - Form disables at 4 sessions

4. **Remove sessions:**
   - Go to "View All Sessions"
   - Click the × button on any session card
   - Session count updates automatically
   - Can now add new sessions

## Technical Details

### Session Limit Enforcement
- **Frontend**: JavaScript checks session count and disables form
- **Backend**: Returns 429 status code when limit exceeded
- **Real-time**: SSE updates keep all pages synchronized

### Grid Layout
- Desktop: 2 columns (2x2 grid for 4 sessions)
- Mobile: 1 column (responsive breakpoint at 1200px)

### Session Counter
- Updates on page load
- Updates after adding session
- Updates after removing session
- Color changes: Blue (available) → Red (full)

## Testing Checklist

- [x] Python syntax validation
- [ ] Start application
- [ ] Add 1st session - counter shows 1/4
- [ ] Add 2nd session - counter shows 2/4
- [ ] Add 3rd session - counter shows 3/4
- [ ] Add 4th session - counter shows 4/4, form disables, warning appears
- [ ] Try to add 5th session - should show error
- [ ] Remove one session - counter updates, form enables
- [ ] Verify 2x2 grid layout
- [ ] Test responsive design on mobile

## Files Modified

1. `app.py` - Backend session limit enforcement
2. `templates/simple_index.html` - Home page with session counter
3. `templates/simple_view.html` - Grid view with 2x2 layout
4. `UI_UPDATES.md` - This documentation file

## Next Steps

To run and test:
```bash
python app.py
# Open http://localhost:8080 in browser
# Test adding 4 sessions and attempting a 5th
```
