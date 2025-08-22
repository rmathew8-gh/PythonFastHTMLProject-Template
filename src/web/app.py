from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fasthtml.common import H1, Body, Div, Head, Html, Link, P, Style, Title
from fasthtml.core import to_xml

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def hello():
    return to_xml(Html(
        Head(
            Title("Agno-2.Trials - Hello World"),
            Link(rel="icon", type="image/svg+xml", href="/static/favicon.svg", sizes="any"),
            Style("""
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    line-height: 1.6;
                }
                h1 {
                    color: #2563eb;
                    border-bottom: 2px solid #e5e7eb;
                    padding-bottom: 0.5rem;
                }
                .container {
                    background: #f9fafb;
                    padding: 2rem;
                    border-radius: 8px;
                    border: 1px solid #e5e7eb;
                }
            """)
        ),
        Body(
            H1("Hello from Agno-2.Trials!"),
            Div(
                P("Welcome to your basic FastHTML application."),
                P("This is a minimal starting point for your project."),
                cls="container"
            )
        )
    ))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
