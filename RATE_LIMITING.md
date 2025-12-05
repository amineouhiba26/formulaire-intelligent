# Rate Limiting Configuration

This application now includes rate limiting on all endpoints to prevent abuse and ensure fair usage.

## Rate Limits by Endpoint

### AI Endpoints (Most Resource-Intensive)
- **POST /api/classify** - 30 requests/minute per IP
  - Mission classification from user prompts
  
- **POST /api/generate-fields** - 20 requests/minute per IP
  - Dynamic field generation (most expensive operation)
  
- **POST /api/submit** - 10 requests/minute per IP
  - Form submission with AI-generated confirmation

### Database Query Endpoints
- **GET /api/submissions** - 60 requests/minute per IP
  - Retrieve form submissions
  
- **GET /api/submissions/stats** - 30 requests/minute per IP
  - Get submission statistics
  
- **DELETE /api/submissions/{id}** - 20 requests/minute per IP
  - Delete a submission

### System Endpoints
- **GET /health** - 100 requests/minute per IP
  - Health check endpoint

## How It Works

Rate limiting is implemented using [SlowAPI](https://github.com/laurentS/slowapi), which:
- Tracks requests by IP address
- Returns HTTP 429 (Too Many Requests) when limits are exceeded
- Includes `X-RateLimit-*` headers in responses showing limit status

## Rate Limit Headers

Each response includes:
- `X-RateLimit-Limit` - The rate limit ceiling for the endpoint
- `X-RateLimit-Remaining` - Number of requests remaining in current window
- `X-RateLimit-Reset` - Time when the rate limit window resets

## Customization

To modify rate limits, edit the `@limiter.limit()` decorator on each endpoint in:
- `app/routers/classify.py`
- `app/routers/generate.py`
- `app/routers/submit.py`
- `app/routers/submissions.py`
- `app/main.py`

Example:
```python
@router.post("/endpoint")
@limiter.limit("50/minute")  # Change this value
async def my_endpoint(request: Request):
    # ...
```

## Supported Rate Limit Formats

- `X/second` - X requests per second
- `X/minute` - X requests per minute
- `X/hour` - X requests per hour
- `X/day` - X requests per day

You can also use multiple limits:
```python
@limiter.limit("100/hour;10/minute")
```

## Error Response

When rate limit is exceeded, the API returns:
```json
{
  "error": "Rate limit exceeded: X per Y minute"
}
```

## Production Considerations

For production deployments:
1. Consider using Redis as a backend for distributed rate limiting
2. Adjust limits based on your infrastructure capacity
3. Monitor rate limit violations to detect potential abuse
4. Consider implementing user-based rate limiting (requires authentication)
