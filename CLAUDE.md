# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
cd app
uv sync          # Install dependencies
uv run python main.py   # Run development server on http://localhost:8080
```

## Architecture Overview

### Routing & Layout Pattern

The app uses a **decorator-based layout** with **sub-pages** for client-side navigation:

```python
# main.py
@ui.page('/')
@with_base_layout
def root():
    ui.sub_pages({
        '/': index,
        '/watchlist': watchlist,
        # ...
    })

def index():
    components.dashboard_content.content()
```

- `@with_base_layout` wraps routes with the header/sidebar shell from `header.py`
- `ui.sub_pages()` enables SPA-style navigation without full page reloads
- Each route handler calls a component's `content()` function

### Component Structure

All page components follow this pattern:

```python
# components/xxx_content.py
def content() -> None:
    # Page header
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        # ...

    # KPI cards row
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        # ...

    # Main content
    with ui.element('div').classes('card'):
        # ...
```

The `content()` function is the entry point - never render at module level.

### Data Services Pattern

Mock data lives in `services/dashboard_data.py`. To swap for real data:

```python
# services/dashboard_data.py
def get_kpis() -> dict:
    # Replace mock data with API/DB calls here
    return {...}
```

Components import and call these functions; the UI layer never knows the data source.

### Print System

The print system uses URL tokens to pass print content:

```python
from components.print_component import encode_html, encode_image, encode_page, open_print

# Raw HTML
open_print(encode_html('<h1>Report</h1>'))

# Base64 image (no data-URI prefix)
open_print(encode_image(b64_str, mime='image/png', caption='Chart'))

# Structured document
open_print(encode_page(
    title='Portfolio Report',
    subtitle='March 2026',
    sections=[
        {'type': 'html', 'content': '<p>Summary</p>'},
        {'type': 'image', 'content': b64_str, 'mime': 'image/png', 'caption': 'Chart'},
    ],
))
```

The `/print/{data}` route is standalone (no layout wrapper) and auto-triggers the browser print dialog.

### Notifications

Use the custom notification service:

```python
from services.notifications import notify, notify_ongoing

notify('Saved', type='positive', title='Success')
notify('Error occurred', type='negative', title='Error')
notify('Review needed', type='warning')

# Persistent loading notification
handle = notify_ongoing('Processing...', title='Loading')
# ... async work ...
handle.dismiss()
```

Types: `'positive'`, `'negative'`, `'warning'`, `'info'`, `'default'`

### CSS Classes

The design system provides utility classes defined in `assets/css/global-css.css`:

- Cards: `.card`, `.panel`
- Badges: `.badge`, `.badge-success`, `.badge-warning`, `.badge-danger`, `.badge-info`
- Buttons: `.button`, `.button-primary`, `.button-outline`, `.button-ghost`
- Status dots: `.status-dot`, `.status-dot.success`, `.status-dot.warning`, `.status-dot.danger`
- Tables: `.data-table`

### Sidebar Navigation

Sidebar entries are defined in `header.py` in the `frame()` context manager. Each entry has:
- Link element with route path
- Icon and label
- Nav link tracking for active state highlighting

To add a new page:
1. Create `components/new_page_content.py` with `content()` function
2. Add route in `main.py` under `ui.sub_pages()`
3. Add sidebar entry in `header.py`
4. Add handler function in `main.py`