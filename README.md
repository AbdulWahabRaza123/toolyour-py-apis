# FastAPI Backend - Document Converter

A professional FastAPI backend for document conversion with modular architecture.

## Project Structure

```
fastApiBe/
├── app/
│   ├── main.py                       # FastAPI entry point
│   ├── api/                          # API routes
│   │   └── api.py                    # Main router
│   ├── core/                         # Core configuration
│   │   ├── config.py                 # Settings
│   │   └── logging.py                # Logging setup
│   ├── modules/                      # Feature modules
│   │   └── document_converter/      # Document conversion module
│   │       ├── types.py              # Type definitions
│   │       ├── service.py            # Business logic
│   │       ├── controller.py         # HTTP handlers
│   │       └── routes.py             # API routes
│   └── utils/                        # Utilities
│       └── file_utils.py             # File helpers
├── venv/                             # Virtual environment
├── logs/                             # Application logs
├── uploads/                          # File uploads
├── static/                           # Static files
├── requirements.txt                  # Dependencies
├── start_server.sh                   # Start server script
├── stop_server.sh                    # Stop server script
├── server_status.sh                  # Check server status
└── check_env.sh                      # Verify environment
```

## Quick Start

### 1. Start Server
```bash
./start_server.sh
```

### 2. Access API
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 3. Test DOCX to PDF
```bash
curl -X POST http://localhost:8000/api/v1/documents/docx-to-pdf \
  -F "file=@document.docx" \
  --output result.pdf
```

## API Endpoints

### Document Conversion
- `POST /api/v1/documents/docx-to-pdf` - Convert DOCX to PDF
- `POST /api/v1/documents/docx-to-txt` - Convert DOCX to TXT
- `POST /api/v1/documents/txt-to-pdf` - Convert TXT to PDF
- `GET /api/v1/documents/supported-conversions` - List supported formats

### System
- `GET /` - Welcome message
- `GET /health` - Health check

## Management Scripts

| Script | Purpose |
|--------|---------|
| `./start_server.sh` | Start server (auto-activates venv) |
| `./stop_server.sh` | Stop server |
| `./server_status.sh` | Check status |
| `./check_env.sh` | Verify setup |

## Virtual Environment

The server scripts automatically handle virtual environment activation.

**Manual activation:**
```bash
source venv/bin/activate
```

**Verify venv is active:**
```bash
which python  # Should show: /path/to/venv/bin/python
```

## Dependencies

See `requirements.txt` for full list. Main packages:
- FastAPI - Web framework
- Uvicorn - ASGI server
- python-docx - DOCX handling
- reportlab - PDF generation
- structlog - Logging

## Adding New Modules

Create a new module in `app/modules/`:
```
app/modules/your_module/
├── types.py        # Type definitions
├── service.py      # Business logic
├── controller.py   # HTTP handlers
└── routes.py       # API routes
```

Register in `app/api/api.py`:
```python
from app.modules.your_module import router as your_router
api_router.include_router(your_router, prefix="/your-path")
```

## 🚂 Deploy to Railway

This project is ready for Railway deployment with zero configuration:

1. Push code to GitHub
2. Connect repository to Railway
3. Railway auto-detects Dockerfile and deploys
4. Your API is live! 🎉

See `DEPLOY.md` for detailed instructions.

### Railway Files Included
- ✅ `Dockerfile` - Production-ready container
- ✅ `railway.json` - Railway configuration
- ✅ `.dockerignore` - Optimized build
- ✅ `.gitignore` - venv excluded automatically

## License

MIT
# toolyour-py-apis
