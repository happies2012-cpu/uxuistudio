# ZipWP Platform - Complete Setup & Integration Guide

## 📦 Installation

### Requirements
```bash
# Python 3.8+
python --version

# Install dependencies
pip install aiohttp paramiko python-dotenv anthropic
```

### Project Structure
```
zipwp-platform/
├── main.py                 # Main framework code
├── config.py               # Configuration settings
├── agents/                 # Agent modules
│   ├── __init__.py
│   ├── planning.py
│   ├── content.py
│   ├── design.py
│   ├── plugins.py
│   └── deployment.py
├── clients/                # API clients
│   ├── __init__.py
│   ├── wordpress.py
│   ├── ssh.py
│   └── ai_client.py
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── validators.py
│   └── helpers.py
├── tests/                  # Test suite
│   ├── test_agents.py
│   └── test_integration.py
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
└── README.md
```

### requirements.txt
```txt
aiohttp==3.9.1
paramiko==3.4.0
python-dotenv==1.0.0
anthropic==0.18.1
pydantic==2.5.3
pytest==7.4.3
pytest-asyncio==0.21.1
```

### .env Configuration
```bash
# AI Model API
ANTHROPIC_API_KEY=your_anthropic_key_here
AI_MODEL=claude-sonnet-4-20250514

# WordPress Default Credentials (optional)
DEFAULT_WP_ADMIN_USER=admin
DEFAULT_WP_ADMIN_EMAIL=admin@example.com

# Hosting Provider APIs (optional)
DIGITALOCEAN_TOKEN=your_do_token
AWS_ACCESS_KEY=your_aws_key
AWS_SECRET_KEY=your_aws_secret

# DNS Provider APIs (optional)
CLOUDFLARE_API_TOKEN=your_cf_token
CLOUDFLARE_ZONE_ID=your_zone_id

# Application Settings
LOG_LEVEL=INFO
MAX_CONCURRENT_SITES=5
ENABLE_CACHING=true
CACHE_TTL_HOURS=24
```

---

## 🚀 Quick Start (5 minutes)

### 1. Basic Usage - No Hosting (Planning Only)

```python
import asyncio
from main import ZipWPPlatform

async def quick_start():
    # Initialize platform
    platform = ZipWPPlatform(ai_api_key="your-key")
    
    # Generate site architecture and content (no deployment)
    result = await platform.create_site(
        business_name="Joe's Pizza",
        business_type="restaurant",
        description="Family pizza restaurant in Brooklyn"
    )
    
    print(f"Site architecture created!")
    print(f"Pages: {result['site_summary']['pages_created']}")
    print(f"Confidence: {result['quality_metrics']['overall_confidence']}")

asyncio.run(quick_start())
```

### 2. Full Deployment - Existing WordPress

```python
import asyncio
from main import ZipWPPlatform

async def deploy_to_existing():
    platform = ZipWPPlatform(ai_api_key="your-key")
    
    result = await platform.create_site(
        business_name="Summit Law Group",
        business_type="law",
        description="Corporate law firm specializing in startups",
        hosting_info={
            "wp_credentials": {
                "site_url": "https://summitlaw.com",
                "username": "admin",
                "password": "your-app-password",  # WP Application Password
                "ssh_host": "summitlaw.com",
                "ssh_user": "root",
                "ssh_key": "/path/to/private_key"  # or ssh_password
            }
        }
    )
    
    if result["workflow_status"] == "completed":
        print(f"✅ Site live at: {result['site_summary']['site_url']}")
    else:
        print(f"❌ Deployment failed: {result.get('error')}")

asyncio.run(deploy_to_existing())
```

### 3. CLI Interface

```python
# cli.py
import click
import asyncio
from main import ZipWPPlatform

@click.command()
@click.option('--business-name', required=True, help='Business name')
@click.option('--business-type', required=True, help='Business type')
@click.option('--description', help='Business description')
@click.option('--deploy/--no-deploy', default=False, help='Deploy to WordPress')
@click.option('--wp-url', help='WordPress site URL')
@click.option('--wp-user', help='WordPress admin username')
@click.option('--wp-pass', help='WordPress application password')
def create_site(business_name, business_type, description, deploy, wp_url, wp_user, wp_pass):
    """Create a WordPress site via CLI"""
    
    hosting_info = None
    if deploy and wp_url:
        hosting_info = {
            "wp_credentials": {
                "site_url": wp_url,
                "username": wp_user,
                "password": wp_pass
            }
        }
    
    async def run():
        platform = ZipWPPlatform(ai_api_key="your-key")
        result = await platform.create_site(
            business_name=business_name,
            business_type=business_type,
            description=description,
            hosting_info=hosting_info
        )
        
        click.echo(f"\n✅ Site generation completed!")
        click.echo(f"Pages created: {result['site_summary']['pages_created']}")
        click.echo(f"Confidence: {result['quality_metrics']['overall_confidence']}")
        
        if deploy:
            click.echo(f"🌐 Live at: {result['site_summary']['site_url']}")
    
    asyncio.run(run())

if __name__ == '__main__':
    create_site()
```

Usage:
```bash
# Plan only (no deployment)
python cli.py --business-name "Joe's Pizza" --business-type restaurant

# Full deployment
python cli.py \
  --business-name "Summit Law" \
  --business-type law \
  --deploy \
  --wp-url https://summitlaw.com \
  --wp-user admin \
  --wp-pass "xxxx xxxx xxxx xxxx"
```

---

## 🔌 API Integration Examples

### WordPress REST API Setup

#### Generate Application Password in WordPress
```bash
# 1. Log into WordPress admin
# 2. Go to Users > Profile
# 3. Scroll to "Application Passwords"
# 4. Enter app name: "ZipWP Platform"
# 5. Click "Add New Application Password"
# 6. Copy the generated password (format: xxxx xxxx xxxx xxxx)
```

#### Test WordPress Connection
```python
import aiohttp
import asyncio

async def test_wp_connection():
    site_url = "https://yoursite.com"
    username = "admin"
    app_password = "xxxx xxxx xxxx xxxx"
    
    auth = aiohttp.BasicAuth(username, app_password)
    
    async with aiohttp.ClientSession(auth=auth) as session:
        # Test connection
        async with session.get(f"{site_url}/wp-json/wp/v2/posts") as resp:
            if resp.status == 200:
                print("✅ WordPress API connection successful!")
                data = await resp.json()
                print(f"Found {len(data)} posts")
            else:
                print(f"❌ Connection failed: {resp.status}")

asyncio.run(test_wp_connection())
```

### WP-CLI via SSH Setup

#### Install WP-CLI on Host
```bash
# SSH into your server
ssh user@yoursite.com

# Download WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar

# Make executable
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Test
wp --info
```

#### Python SSH Operations
```python
import paramiko

def test_ssh_wp_cli():
    # Connect via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    client.connect(
        hostname="yoursite.com",
        username="root",
        key_filename="/path/to/private_key"
    )
    
    # Test WP-CLI
    stdin, stdout, stderr = client.exec_command("wp --info")
    print(stdout.read().decode())
    
    # Install plugin example
    stdin, stdout, stderr = client.exec_command(
        "cd /var/www/html && wp plugin install contact-form-7 --activate"
    )
    print(stdout.read().decode())
    
    client.close()

test_ssh_wp_cli()
```

### AI Model Integration (Anthropic Claude)

```python
import anthropic
import json

def call_claude_with_prompt(prompt: str, max_tokens: int = 1000):
    """Call Claude API with system prompt"""
    
    client = anthropic.Anthropic(api_key="your-api-key")
    
    # System message for all agents
    system_message = """You are an autonomous WordPress site generation agent.
Output must be valid JSON following the specified schema.
Operate deterministically with temperature=0.10."""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        temperature=0.10,
        system=system_message,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse JSON response
    response_text = message.content[0].text
    return json.loads(response_text)

# Example: Site Planning Agent
planning_prompt = """
Task: Generate WordPress site architecture for business.

Input:
- Business name: Joe's Pizza
- Business type: restaurant
- Industry: food_service
- Description: Family pizza restaurant in Brooklyn

Generate complete JSON architecture with pages, features, plugins, and SEO foundation.
"""

result = call_claude_with_prompt(planning_prompt, max_tokens=600)
print(json.dumps(result, indent=2))
```

### Hosting Provider Integration

#### DigitalOcean Droplet Provisioning
```python
import aiohttp
import asyncio

async def create_wordpress_droplet():
    """Create a DigitalOcean droplet with WordPress"""
    
    api_token = "your-do-token"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Create droplet
    droplet_config = {
        "name": "wordpress-site-001",
        "region": "nyc3",
        "size": "s-1vcpu-1gb",
        "image": "wordpress-20-04",  # WordPress one-click image
        "ssh_keys": ["your-ssh-key-id"],
        "backups": True,
        "ipv6": True,
        "monitoring": True
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "https://api.digitalocean.com/v2/droplets",
            json=droplet_config
        ) as resp:
            if resp.status == 201:
                data = await resp.json()
                droplet_id = data["droplet"]["id"]
                print(f"✅ Droplet created: {droplet_id}")
                
                # Wait for IP assignment
                await asyncio.sleep(30)
                
                # Get droplet details
                async with session.get(
                    f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
                ) as resp2:
                    droplet = await resp2.json()
                    ip_address = droplet["droplet"]["networks"]["v4"][0]["ip_address"]
                    print(f"🌐 IP Address: {ip_address}")
                    return ip_address
            else:
                print(f"❌ Failed to create droplet: {resp.status}")

asyncio.run(create_wordpress_droplet())
```

#### AWS Lightsail WordPress Instance
```python
import boto3

def create_lightsail_wordpress():
    """Create AWS Lightsail WordPress instance"""
    
    client = boto3.client(
        'lightsail',
        aws_access_key_id='your-key',
        aws_secret_access_key='your-secret',
        region_name='us-east-1'
    )
    
    response = client.create_instances(
        instanceNames=['wordpress-site-001'],
        availabilityZone='us-east-1a',
        blueprintId='wordpress',  # WordPress blueprint
        bundleId='nano_2_0',      # Instance size
        userData='''#!/bin/bash
            # Custom setup script
            apt-get update
            apt-get install -y wp-cli
        '''
    )
    
    instance_name = response['operations'][0]['resourceName']
    print(f"✅ Lightsail instance created: {instance_name}")
    
    # Wait and get public IP
    import time
    time.sleep(60)
    
    instance = client.get_instance(instanceName=instance_name)
    ip_address = instance['instance']['publicIpAddress']
    print(f"🌐 IP Address: {ip_address}")
    
    return ip_address

create_lightsail_wordpress()
```

### DNS Automation (Cloudflare)

```python
import aiohttp
import asyncio

async def update_cloudflare_dns(domain: str, ip_address: str):
    """Update DNS A record in Cloudflare"""
    
    api_token = "your-cloudflare-token"
    zone_id = "your-zone-id"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Get existing DNS records
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            params={"name": domain, "type": "A"}
        ) as resp:
            data = await resp.json()
            records = data.get("result", [])
            
            if records:
                # Update existing record
                record_id = records[0]["id"]
                update_data = {
                    "type": "A",
                    "name": domain,
                    "content": ip_address,
                    "ttl": 1,  # Automatic
                    "proxied": True  # Enable Cloudflare proxy
                }
                
                async with session.put(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                    json=update_data
                ) as resp2:
                    if resp2.status == 200:
                        print(f"✅ DNS updated: {domain} -> {ip_address}")
                    else:
                        print(f"❌ DNS update failed: {resp2.status}")
            else:
                # Create new record
                create_data = {
                    "type": "A",
                    "name": domain,
                    "content": ip_address,
                    "ttl": 1,
                    "proxied": True
                }
                
                async with session.post(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                    json=create_data
                ) as resp2:
                    if resp2.status == 200:
                        print(f"✅ DNS record created: {domain} -> {ip_address}")

asyncio.run(update_cloudflare_dns("example.com", "192.0.2.1"))
```

---

## 🧪 Testing

### Unit Tests
```python
# tests/test_agents.py
import pytest
from main import SitePlanningAgent, AIClient

@pytest.mark.asyncio
async def test_planning_agent():
    """Test site planning agent"""
    ai_client = AIClient(api_key="test-key")
    agent = SitePlanningAgent(ai_client)
    
    input_data = {
        "business_name": "Test Business",
        "business_type": "restaurant",
        "industry": "food_service"
    }
    
    result = await agent.execute(input_data)
    
    assert result.status == "ok"
    assert result.confidence >= 0.60
    assert "site_structure" in result.result
    assert len(result.result["site_structure"]["pages"]) >= 5

@pytest.mark.asyncio
async def test_content_generation():
    """Test content generation agent"""
    # Similar structure
    pass
```

### Integration Tests
```python
# tests/test_integration.py
import pytest
from main import ZipWPPlatform

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete site generation workflow"""
    platform = ZipWPPlatform(ai_api_key="test-key")
    
    result = await platform.create_site(
        business_name="Test Site",
        business_type="professional_services"
    )
    
    assert result["workflow_status"] == "completed"
    assert result["site_summary"]["pages_created"] > 0
    assert result["quality_metrics"]["overall_confidence"] >= 0.75
```

Run tests:
```bash
pytest tests/ -v
pytest tests/test_agents.py::test_planning_agent -v
```

---

## 📊 Production Deployment

### Docker Setup
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  zipwp-platform:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ~/.ssh:/root/.ssh:ro
    restart: unless-stopped
```

### Kubernetes Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zipwp-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: zipwp
  template:
    metadata:
      labels:
        app: zipwp
    spec:
      containers:
      - name: zipwp
        image: zipwp-platform:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: zipwp-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### API Endpoint (FastAPI)
```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import ZipWPPlatform
import asyncio

app = FastAPI(title="ZipWP Platform API")

class SiteCreationRequest(BaseModel):
    business_name: str
    business_type: str
    description: str = None
    hosting_info: dict = None

@app.post("/api/v1/sites/create")
async def create_site(request: SiteCreationRequest):
    """Create a new WordPress site"""
    try:
        platform = ZipWPPlatform(ai_api_key="your-key")
        
        result = await platform.create_site(
            business_name=request.business_name,
            business_type=request.business_type,
            description=request.description,
            hosting_info=request.hosting_info
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run: uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 🔒 Security Best Practices

### 1. Credential Management
```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
WP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Never log credentials
logger.info(f"Connecting to {site_url}")  # ✅ Good
logger.info(f"Using password {password}")  # ❌ Never do this
```

### 2. SSH Key Management
```python
# Use SSH keys instead of passwords
credentials = WordPressCredentials(
    site_url="https://example.com",
    username="admin",
    password="app-password",
    ssh_host="example.com",
    ssh_user="deploy",
    ssh_key="/path/to/private_key",  # ✅ Preferred
    # ssh_password="password"  # ❌ Avoid
)
```

### 3. Input Validation
```python
from pydantic import BaseModel, validator, HttpUrl

class SiteInput(BaseModel):
    business_name: str
    site_url: HttpUrl
    
    @validator('business_name')
    def validate_business_name(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Business name must be 2-100 characters')
        return v
```

---

## 📈 Monitoring & Logging

### Structured Logging
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName
        }
        return json.dumps(log_data)

# Configure
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Metrics Collection
```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
sites_created = Counter('sites_created_total', 'Total sites created')
deployment_duration = Histogram('deployment_duration_seconds', 'Deployment time')

# In code
sites_created.inc()
with deployment_duration.time():
    await orchestrator.generate_site(business_input)

# Start metrics server
start_http_server(9090)
```

---

## 🎯 Next Steps

1. **Implement AI Integration**: Replace mock AI client with actual Anthropic API
2. **Add Web Interface**: Build React/Vue frontend for visual wizard
3. **Database Layer**: Add PostgreSQL for storing site configs and history
4. **Queue System**: Use Celery/Redis for async site generation
5. **Multi-tenancy**: Add user accounts and site management
6. **Monitoring**: Integrate with Datadog/New Relic
7. **CI/CD**: Set up GitHub Actions for automated testing and deployment

Ready to build the next ZipWP! 🚀