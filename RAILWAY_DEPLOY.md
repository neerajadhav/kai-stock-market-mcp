# Railway Deployment Guide

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub
3. **Environment Variables**: Prepare your AUTH_TOKEN and MY_NUMBER

## Deployment Steps

### 1. Connect Repository to Railway

1. Go to [railway.app](https://railway.app) and log in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `kai-stock-market-mcp` repository
5. Railway will automatically detect the Dockerfile and start building

### 2. Set Environment Variables

In your Railway project dashboard:

1. Go to the **Variables** tab
2. Add the following environment variables:
   ```
   AUTH_TOKEN=your-auth-token-here
   MY_NUMBER=91your-phone-number-here
   ```

### 3. Configure Domain (Optional)

1. Go to the **Settings** tab
2. Under **Domains**, click "Generate Domain" for a free railway.app subdomain
3. Or add your custom domain

### 4. Monitor Deployment

1. Check the **Deployments** tab for build logs
2. Once deployed, your service will be available at the generated URL
3. Test the health endpoint: `https://your-app.railway.app/health`

## Key Features for Railway

- ✅ **Dockerfile-based deployment** for consistent builds
- ✅ **Dynamic port binding** via `PORT` environment variable
- ✅ **Health check endpoints** at `/` and `/health`
- ✅ **Minimal Docker image** with only necessary dependencies
- ✅ **Security**: Non-root user in container
- ✅ **Resource optimized**: Slim Python base image

## Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `AUTH_TOKEN` | Authentication token for the MCP server | `your-secret-token` |
| `MY_NUMBER` | Phone number for validation | `91xxxxxxxxxx` |
| `PORT` | Server port (auto-set by Railway) | `8087` |

## Local Testing

Test the Docker container locally before deployment:

```bash
# Build the Docker image
docker build -t stock-market-mcp .

# Run with environment variables
docker run -p 8087:8087 \
  -e AUTH_TOKEN=your-token \
  -e MY_NUMBER=91xxxxxxxxxx \
  stock-market-mcp
```

## Troubleshooting

### Build Issues
- Ensure all dependencies are in `pyproject.toml`
- Check Railway build logs in the Deployments tab

### Runtime Issues
- Verify environment variables are set correctly
- Check application logs in Railway dashboard
- Test health endpoints: `/` and `/health`

### Memory Issues
- Railway's free tier has memory limits
- Consider upgrading to paid tier for production use

## API Endpoints

After deployment, your MCP server will be available at:

- **Health Check**: `GET /health`
- **Root**: `GET /`
- **MCP Tools**: Available via the MCP protocol

## Cost Optimization

- Uses Python 3.11-slim base image (smaller size)
- Multi-stage builds not needed for this simple service
- Efficient dependency management with `uv`
- Non-root user for security without extra overhead
