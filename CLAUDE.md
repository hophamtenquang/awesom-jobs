# CLAUDE.md - Awesom Jobs

## Project Overview

Awesom Jobs is a Python Flask web application that scrapes and displays job listings from the [awesome-jobs/vietnam](https://github.com/awesome-jobs/vietnam) GitHub repository. It crawls GitHub issue pages, stores job data in SQLite, and serves it through a simple web UI.

**Author:** hophamtenquang

## Tech Stack

- **Language:** Python 3
- **Web Framework:** Flask 0.12.2
- **Database:** SQLite 3
- **Scraping:** BeautifulSoup 4.6.0, Requests 2.18.1, html5lib
- **Frontend:** Jinja2 templates, Bootstrap 3.3.7, jQuery 3.2.1
- **Additional:** Scrapy 1.4.0 (listed in deps but not used directly in scripts)

## Repository Structure

```
awesom-jobs/
├── crawljobs.py       # Scraper - fetches jobs from GitHub issues -> jobs.json
├── sqlhelper.py        # ETL script - loads jobs.json into SQLite -> jobs.db
├── jobs.py             # Flask web app - serves job listings from jobs.db
├── jobs.json           # Scraped job data (intermediate JSON file)
├── jobs.db             # SQLite database (production data store)
├── requirements.txt    # Python dependencies (pinned versions)
└── templates/
    ├── index.html      # Job listing page
    └── detail.html     # Single job detail page
```

## Data Pipeline

The application has a three-stage data pipeline:

1. **Crawl:** `crawljobs.py` scrapes GitHub issue pages using BeautifulSoup/Requests and writes `jobs.json`
2. **Load:** `sqlhelper.py` reads `jobs.json`, parses dates, and inserts records into `jobs.db` (SQLite)
3. **Serve:** `jobs.py` runs a Flask server that queries `jobs.db` and renders HTML templates

## Database Schema

```sql
CREATE TABLE jobs (
    id integer PRIMARY KEY,       -- GitHub issue number
    date_create datetime,         -- Job posting date
    title varchar(500),           -- Job title
    detail varchar(500),          -- Raw HTML content from the issue
    path varchar(200)             -- URL to original GitHub issue
);
```

## Flask Routes

| Route | Function | Description |
|---|---|---|
| `/` | `hello()` | Returns plain text "Hello" (stub/health check) |
| `/jobs` | `index()` | Lists all jobs ordered by date descending |
| `/jobs/detail/<id>` | `detail(id)` | Shows detail for a single job by ID |

## Development Workflow

### Setup

```bash
pip install -r requirements.txt
```

### Running the Data Pipeline

```bash
# Step 1: Scrape job listings from GitHub
python crawljobs.py

# Step 2: Load scraped data into SQLite
python sqlhelper.py
```

### Running the Web Server

```bash
python jobs.py
# Starts Flask dev server on http://127.0.0.1:5000 with debug=True
```

### No Build Step Required

This is a pure Python project with no compilation or build process.

## Testing

There is no test suite. No test framework is configured.

## Linting / Formatting

No linting or formatting tools are configured (no flake8, pylint, black, etc.).

## CI/CD

No CI/CD pipeline is configured.

## Key Conventions and Notes

- **Indentation:** Mixed — `jobs.py` uses tabs in route functions; other files use spaces. Be consistent with the surrounding code when editing a file.
- **SQL queries:** Use parameterized queries (e.g., `WHERE id = ?`) to prevent SQL injection. The detail route already does this correctly.
- **Template rendering:** `detail.html` renders `job[4]` with `|safe` filter (raw HTML from GitHub). Be cautious — this is a known XSS surface.
- **Database connections:** Opened per-request inline (no connection pooling or Flask-SQLAlchemy). Each route creates its own `sqlite3.connect('jobs.db')` call.
- **Date parsing format:** `'%b %d, %Y'` (e.g., "Jun 1, 2017") — parsed from GitHub's `<relative-time>` element text.
- **Job IDs:** Correspond to GitHub issue numbers (integers).
- **No environment variables or config files** — all configuration (DB path, debug mode, URLs) is hardcoded.
- **Scrapy** is listed in `requirements.txt` but the actual scraping uses BeautifulSoup + Requests directly.

## Common Pitfalls

- The `crawljobs.py` scraper depends on GitHub's HTML structure (CSS selectors like `ul.js-navigation-container`, `a.link-gray-dark`, etc.). If GitHub changes its markup, the scraper will break.
- `sqlhelper.py` silently catches `IntegrityError` on duplicate inserts — re-running it with existing data won't update records.
- The `jobs.db` table creation SQL is commented out in `sqlhelper.py`. To recreate the database from scratch, uncomment the `CREATE TABLE` and `DELETE` statements.
- Flask runs with `debug=True` — not suitable for production deployment.
