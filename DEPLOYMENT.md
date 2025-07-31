# Truify Deployment Guide

## Overview

Truify is a data engineering application with AI-powered analysis capabilities. This guide covers deployment for both local development and production environments.

## Platform Compatibility

### GPT4All Support
- **✅ macOS (native)**: Full GPT4All support
- **✅ x86_64 Linux (production)**: Full GPT4All support  
- **❌ ARM64 Linux (Apple Silicon Docker)**: Limited GPT4All support

## Local Development

### Option 1: Native macOS (Recommended for Apple Silicon)
```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the application
streamlit run code/main.py
```

**Benefits:**
- ✅ Full GPT4All support
- ✅ Fastest performance
- ✅ No Docker overhead

### Option 2: Docker (Limited GPT4All on Apple Silicon)
```bash
# Build and run
./build.sh
docker-compose up -d

# Access at http://localhost:8501
```

**Note:** On Apple Silicon, GPT4All features will show fallback messages instead of AI analysis.

## Production Deployment

### Option 1: Docker (Recommended for x86_64 servers)
```bash
# Build for production
./deploy.sh

# Run with environment variables
docker run -d -p 8501:8501 \
  -e GMAIL_USER=your-email@domain.com \
  -e GMAIL_APP_PASSWORD=your-app-password \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/email.csv:/app/email.csv \
  -v $(pwd)/users.csv:/app/users.csv \
  --name truify-production \
  truify
```

### Option 2: Docker Compose
```bash
# Create production environment file
cp .env.example .env.production
# Edit .env.production with your credentials

# Deploy
docker-compose --env-file .env.production up -d
```

### Option 3: Native Python (Any platform)
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GMAIL_USER=your-email@domain.com
export GMAIL_APP_PASSWORD=your-app-password

# Run
streamlit run code/main.py --server.port=8501 --server.address=0.0.0.0
```

## Environment Variables

Create a `.env` file or set these environment variables:

```bash
GMAIL_USER=your-email@domain.com
GMAIL_APP_PASSWORD=your-app-password
```

## File Structure

```
truify/
├── code/                 # Application code
├── data/                 # Data files
├── users.csv            # User credentials
├── email.csv            # Email notification recipients
├── Dockerfile           # Container definition
├── docker-compose.yml   # Local development
├── build.sh             # Platform-aware build script
├── deploy.sh            # Production deployment script
└── requirements.txt     # Python dependencies
```

## Platform-Specific Notes

### Apple Silicon (M1/M2)
- **Local Development**: Use native Python for full GPT4All support
- **Docker**: GPT4All features will show fallback messages
- **Production**: Deploy to x86_64 servers for full functionality

### x86_64 (Intel/AMD)
- **All Environments**: Full GPT4All support
- **Docker**: Works perfectly with native x86_64 containers

### ARM64 Linux (Raspberry Pi, etc.)
- **Limited Support**: GPT4All may not work due to missing ARM64 wheels
- **Fallback**: Application will work with statistical analysis only

## Troubleshooting

### GPT4All Not Working
**Symptoms:** "Could not generate dataset description" errors

**Solutions:**
1. **Local Development**: Use native Python instead of Docker
2. **Production**: Deploy to x86_64 servers
3. **Fallback**: The application provides detailed statistical analysis when AI is unavailable

### Docker Build Issues
**Symptoms:** Build failures or platform compatibility errors

**Solutions:**
1. Use `./build.sh` for platform-aware builds
2. Use `./deploy.sh` for production deployments
3. Check Docker Desktop settings for platform emulation

### Email Notifications Not Working
**Symptoms:** Login notifications not being sent

**Solutions:**
1. Verify Gmail credentials in environment variables
2. Check Gmail App Password setup
3. Ensure `email.csv` file exists with recipient addresses

## Performance Considerations

### Local Development
- **Native Python**: Fastest performance, full AI support
- **Docker on Apple Silicon**: Slower due to emulation, limited AI support

### Production
- **x86_64 Docker**: Optimal performance, full AI support
- **ARM64**: Limited AI support, but application remains functional

## Security Notes

1. **Credentials**: Never commit `.env` files or credentials to version control
2. **Users**: Store user credentials in `users.csv` (consider hashing passwords)
3. **Data**: Mount data directories as volumes for persistence
4. **Network**: Use reverse proxy (nginx) for production deployments

## Monitoring

### Health Check
```bash
# Check if container is running
docker ps

# View logs
docker logs truify-truify-1

# Test application
curl http://localhost:8501
```

### Logs
```bash
# Stream logs
docker-compose logs -f

# View specific service logs
docker logs truify-truify-1 --tail=100
```

## Scaling

### Horizontal Scaling
```bash
# Run multiple instances
docker run -d -p 8501:8501 truify
docker run -d -p 8502:8501 truify
docker run -d -p 8503:8501 truify
```

### Load Balancing
Use nginx or similar reverse proxy to distribute traffic across multiple instances.

## Backup and Recovery

### Data Backup
```bash
# Backup data directory
tar -czf truify-data-backup-$(date +%Y%m%d).tar.gz data/

# Backup configuration
cp users.csv users-backup.csv
cp email.csv email-backup.csv
```

### Recovery
```bash
# Restore data
tar -xzf truify-data-backup-YYYYMMDD.tar.gz

# Restore configuration
cp users-backup.csv users.csv
cp email-backup.csv email.csv
```

## Support

For issues related to:
- **GPT4All**: Check platform compatibility and use native Python when possible
- **Docker**: Use platform-aware build scripts
- **Email**: Verify Gmail credentials and App Password setup
- **Data**: Check file permissions and volume mounts 