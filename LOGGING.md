# Logging Configuration Examples

## Environment Variables

### Basic Logging
```bash
# Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export LOG_LEVEL=INFO

# Enable/disable console logging
export LOG_TO_CONSOLE=true

# Enable/disable file logging
export LOG_TO_FILE=true

# Log format (simple, detailed)
export LOG_FORMAT=detailed
```

### Development Configuration
```bash
export LOG_LEVEL=DEBUG
export LOG_TO_CONSOLE=true
export LOG_TO_FILE=true
export LOG_FORMAT=detailed
```

### Production Configuration
```bash
export LOG_LEVEL=INFO
export LOG_TO_CONSOLE=false
export LOG_TO_FILE=true
export LOG_FORMAT=simple
```

## Log Files

Logs are written to the `logs/` directory:
- `app.log` - All application logs
- `errors.log` - Error and critical logs only

## Log Formats

### Simple Format
```
2024-01-31 12:00:00 - app.api.routes.movies - INFO - Retrieved 10 movies
```

### Detailed Format
```
2024-01-31 12:00:00 - app.api.routes.movies - INFO - 📽 Movie request received with query: {'title': 'Action'}
2024-01-31 12:00:01 - app.core.database - DEBUG - Fetching documents from sample_mflix.movies with filter: {'title': 'Action'}, limit: 10, skip: 0
2024-01-31 12:00:01 - app.core.database - INFO - 📊 Retrieved 5 documents from sample_mflix.movies
2024-01-31 12:00:01 - app.api.routes.movies - INFO - ✅ Successfully retrieved 5 movies
```

## Log Levels by Component

- **app.core.database**: DEBUG (for query details)
- **app.repositories**: INFO
- **app.services**: INFO
- **app.api**: INFO
- **uvicorn.access**: WARNING (reduces noise)
- **motor**: WARNING
- **pymongo**: WARNING

## Integration with Monitoring

### Structured Logging (JSON)
For production monitoring, you can modify the logging configuration to output JSON:

```python
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        })
```

### External Services
The logs can be integrated with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Datadog**
- **Grafana + Loki**
- **CloudWatch** (AWS)

Example with filebeat for ELK:
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /path/to/app/logs/app.log
  fields:
    service: fastapi-mongo-movies
    environment: production
```