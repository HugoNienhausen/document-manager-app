# PDF Manager

A web application for managing directories and PDF files with a modern, minimalist interface.

## Features

- **Directory Management**: Create, navigate, and delete directories
- **PDF Upload**: Drag & drop or click to upload PDF files
- **File Operations**: Download and delete PDF files
- **Expandable Directories**: View directory contents without navigation
- **Breadcrumb Navigation**: Clear path indication
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Python 3.8+**: Core programming language
- **Uvicorn**: ASGI server

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox
- **Font Awesome**: Icons

## Project Structure

```
workplace/
├── app/                    # Backend application
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints
│   ├── config.py          # Configuration settings
│   ├── main.py           # FastAPI application
│   ├── models.py         # Data models
│   └── services.py       # Business logic
├── static/                # Frontend files
│   ├── index.html        # Main HTML page
│   ├── styles.css        # CSS styles
│   └── app.js           # JavaScript application
├── uploads/              # PDF file storage
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── requirements.txt      # Python dependencies
├── main.py              # Application entry point
└── README.md            # Project overview
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd workplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - Frontend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

### Directories
- `GET /api/v1/directories` - List all directories
- `POST /api/v1/directories` - Create new directory
- `DELETE /api/v1/directories/{path}` - Delete directory

### Files
- `GET /api/v1/files/{path}` - List files in directory
- `POST /api/v1/files/upload` - Upload PDF file
- `GET /api/v1/files/download/{path}` - Download file
- `DELETE /api/v1/files/{path}` - Delete file

### Health
- `GET /api/v1/health` - Application health check

## Usage

### Creating Directories
1. Click "New Folder" button
2. Enter directory name
3. Click "Create"

### Uploading Files
1. Click "Upload PDF" button
2. Drag & drop PDF file or click to select
3. File will be uploaded to current directory

### Navigation
- Click directory names to navigate
- Use breadcrumb to navigate back
- Click ".." to go to parent directory

### File Operations
- Click download icon to download file
- Click trash icon to delete file/directory

## Configuration

Environment variables (optional):
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: "INFO")

## Development

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Keep functions small and focused
- Add basic comments for complex logic

### Git Workflow
1. Use conventional commit messages
2. Update CHANGELOG.md for significant changes
3. Create tags for releases
4. Use the provided git helper scripts

### Testing
- Test file uploads with different sizes
- Verify directory navigation
- Check responsive design on mobile
- Test error handling

## Deployment

### Production Setup
1. Set `DEBUG=False` in environment
2. Configure proper CORS origins
3. Use production ASGI server (Gunicorn)
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## Troubleshooting

### Common Issues

**Port already in use**
```bash
lsof -ti:8000 | xargs kill -9
```

**Permission errors**
```bash
chmod +x scripts/git-helpers.sh
```

**File upload fails**
- Check file size (max 50MB)
- Verify file is PDF format
- Check uploads directory permissions

### Logs
- Application logs are printed to console
- Check for error messages in browser console
- API errors return detailed messages

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper commits
4. Test thoroughly
5. Submit pull request

## License

This project is open source and available under the MIT License.

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history. 