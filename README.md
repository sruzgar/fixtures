# Scotland National Team Fixtures & Results

[![Last
updated](https://img.shields.io/github/last-commit/sruzgar/fixtures.svg)](https://github.com/sruzgar/fixtures/commits/main)

A lightweight, mobile-first web application for subscribing to Scotland National Football Team fixtures with automatic calendar synchronization.

🔗 **Live Site**: https://fixtures.eh30.net/

## Technical Overview

This is a static single-page application that provides calendar subscription links and displays upcoming match information by parsing ICS (iCalendar) files directly in the browser.

### Key Features

- **Zero backend required** - Pure client-side JavaScript
- **Real-time ICS parsing** - Fetches and parses `.ics` files on page load
- **Timezone conversion** - Handles Europe/London (GMT/BST) to user's local timezone
- **Mobile-optimized** - Responsive design with touch-friendly interactions
- **Multi-platform calendar support** - Apple Calendar, Google Calendar, Outlook.com

## How It Works

### 1. Calendar Subscription

The site provides `webcal://` links that allow users to subscribe to the ICS feed:

```
webcal://fixtures.eh30.net/calendars/scotland.ics
```

Once subscribed, calendar apps automatically poll the ICS file for updates (typically every 5-10 mins).

### 2. Next Match Display

On page load, the site:

1. **Fetches** the ICS file via `fetch('https://fixtures.eh30.net/calendars/scotland.ics')`
2. **Parses** the ICS format using a custom parser (`parseICS()`)
3. **Filters** events to find future matches (`event.start > now`)
4. **Sorts** by date to get the earliest upcoming match
5. **Displays** the match with proper timezone conversion

### 3. ICS Parsing

The `parseICS()` function manually parses the ICS text format:

```
BEGIN:VEVENT
DTSTART;TZID=Europe/London:20260331T193000
SUMMARY:🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland v 🇨🇮 Côte D'Ivoire
LOCATION:Hill Dickinson Stadium...
DESCRIPTION:Friendly Match
END:VEVENT
```

Extracts:
- `DTSTART` → Match date/time
- `SUMMARY` → Opponent (with emoji flags)
- `LOCATION` → Stadium/venue
- `DESCRIPTION` → Competition details

### 4. Timezone Conversion

All matches in the ICS file use `TZID=Europe/London`, which means:
- **GMT** (UTC+0) in winter
- **BST** (UTC+1) in summer

The `parseICSDate()` function:

1. Detects if the date falls during British Summer Time
2. Converts from Europe/London to UTC
3. Creates a JavaScript `Date` object in UTC
4. Browser automatically converts to user's local timezone for display

**BST Rules:**
- Starts: Last Sunday in March at 01:00
- Ends: Last Sunday in October at 02:00

Example conversion:
```
19:30 BST (UTC+1) → 18:30 UTC → 14:30 EDT (UTC-4)
```

### 5. Error Handling

Three states are handled:

1. **Match found** → Display match details
2. **No upcoming matches** → Show "No upcoming matches scheduled"
3. **Fetch/parse error** → Show "Unable to load fixture information"

### 6. Performance Optimizations

- `<link rel="preconnect">` to establish early connection to domain (~100-300ms faster)
- Preload grass background image
- Minimal JavaScript (no frameworks, ~3KB)
- CSS animations for smooth interactions

## Architecture

```
Single HTML file (index4.html)
├── HTML structure
├── Embedded CSS (<style> tag)
└── Embedded JavaScript (<script> tag)
    ├── loadUpcomingMatch() - Main entry point
    ├── parseICS() - ICS file parser
    ├── parseICSDate() - Date/timezone converter
    ├── isBritishSummerTime() - BST detection
    ├── updateMatchDisplay() - Display match info
    ├── showNoMatchesMessage() - Empty state
    └── showErrorMessage() - Error state
```

## ICS File Format

The ICS feed includes:

- **Event UID** - Unique identifier for each match
- **Timezone definition** - `VTIMEZONE` block for Europe/London
- **Emoji flags** - Country flags in summaries (e.g., 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🇯🇵)
- **Structured locations** - Apple Maps integration via `X-APPLE-STRUCTURED-LOCATION`
- **Match results** - Scores appended to summaries for completed matches (e.g., "(0-1)")
- **Competition links** - URLs to FIFA/UEFA match centres in descriptions

Example event:
```ics
BEGIN:VEVENT
UID:scotland-japan-20260328@scotlandfixtures
DTSTAMP:20260217T120000Z
DTSTART;TZID=Europe/London:20260328T170000
DTEND;TZID=Europe/London:20260328T184500
SUMMARY:🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland v 🇯🇵 Japan (0-1)
DESCRIPTION:Friendly Match
LOCATION:Barclays Hampden\nLetherby Drive\, Glasgow\, G42 9BA\, Scotland
END:VEVENT
```

## Browser Compatibility

- **Modern browsers**: Full support (Chrome, Safari, Firefox, Edge)
- **JavaScript required**: Yes (for Next Match feature)
- **Progressive enhancement**: Calendar subscription works without JS

## Development

No build process required - just edit the HTML file and deploy.

### Local Testing

```bash
# Serve locally (any static server works)
python3 -m http.server 8000

# Visit http://localhost:8000/index4.html
```

### Testing Timezone Conversion

To test timezone handling, add console logging:

```javascript
console.log(parseICSDate('20260331T193000')); // Should show correct local time
```

## Deployment

Static hosting options:
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages
- Any CDN/static host

Just serve the HTML file and ICS calendar feed - no server-side processing needed.

## User Guide

### Subscribing to the Calendar

**Apple Calendar (iPhone/Mac):**
1. Tap/click the "Apple Calendar" button
2. Confirm subscription when prompted

**Google Calendar:**
1. Click "Google Calendar" button
2. Sign in to Google if needed
3. Confirm calendar addition

**Outlook:**
1. Click "Outlook Calendar" button
2. Sign in to Microsoft account
3. Confirm calendar subscription

**Manual Download:**
1. Expand "Having trouble subscribing?" accordion
2. Click download link
3. Import `.ics` file into your calendar app

## Technical Decisions

### Why No Framework?

- **Simplicity**: Single file, no build step, no dependencies
- **Performance**: Minimal JS payload (~3KB gzipped)
- **Maintenance**: No framework updates or security patches
- **Learning**: Easy to understand and modify

### Why Client-Side Parsing?

- **Zero infrastructure**: No backend server or API required
- **Cache-friendly**: Browser caches ICS file, reduces bandwidth
- **Real-time**: Always shows latest data from ICS feed
- **Privacy**: No data collection, tracking, or analytics

### Why Not Use a Calendar API?

- **Standard compliance**: ICS is an open standard (RFC 5545)
- **Universal support**: Works with all calendar apps
- **No vendor lock-in**: Not tied to Google/Apple/Microsoft APIs
- **Simplicity**: Direct subscription, no authentication needed
- **Reliability**: No API rate limits or service dependencies

## Project Structure

```
/
├── index.html          # Main application
├── calendars/
│   └── scotland.ics     # ICS calendar feed
└── media/
    ├── grass.png        # Background image
    ├── apple.png        # Apple Calendar icon
    ├── google.png       # Google Calendar icon
    └── outlook.png      # Outlook Calendar icon
```

## Future Enhancements

Potential improvements being considered:

- [ ] PWA manifest for "Add to Home Screen"
- [ ] Web Share API for sharing the calendar
- [ ] `prefers-color-scheme` dark mode support
- [ ] Countdown timer to next match
- [ ] Display last match result

## Contributing

This is a personal project, but suggestions and improvements are welcome via GitHub issues.

## License

MIT License - Feel free to fork and adapt for other teams or sports.

## Credits

- Fixtures data sourced from official Scotland FA, FIFA, and UEFA websites
- Built with vanilla HTML, CSS, and JavaScript
- Inspired by the Tartan Army's passion for Scotland football

---

**Alba gu bràth!** 🏴󠁧󠁢󠁳󠁣󠁴󠁿
