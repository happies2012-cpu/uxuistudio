#!/bin/bash
# SSL Certificate Generation Script for gsWstudio.ai
# Generates self-signed SSL certificates for local development

echo "🔐 Generating SSL Certificates for gsWstudio.ai"
echo "================================================"

# Create ssl directory
mkdir -p ssl
cd ssl

# Generate private key
echo "📝 Generating private key..."
openssl genrsa -out key.pem 2048

# Generate certificate signing request
echo "📝 Generating certificate signing request..."
openssl req -new -key key.pem -out csr.pem -subj "/C=US/ST=State/L=City/O=gsWstudio.ai/CN=localhost"

# Generate self-signed certificate (valid for 365 days)
echo "📝 Generating self-signed certificate..."
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem

# Create certificate with SAN (Subject Alternative Names)
echo "📝 Creating certificate with SAN..."
cat > openssl.cnf << EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=US
ST=State
L=City
O=gsWstudio.ai
CN=localhost

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
DNS.3 = 127.0.0.1
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

# Regenerate with SAN
openssl req -new -key key.pem -out csr.pem -config openssl.cnf
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem -extensions v3_req -extfile openssl.cnf

# Clean up
rm csr.pem openssl.cnf

echo ""
echo "✅ SSL Certificates generated successfully!"
echo ""
echo "📁 Files created:"
echo "   - ssl/key.pem  (Private key)"
echo "   - ssl/cert.pem (Certificate)"
echo ""
echo "⚠️  Note: These are self-signed certificates for development only."
echo "   Browsers will show a security warning. Click 'Advanced' → 'Proceed to localhost'"
echo ""
echo "🔧 To use with FastAPI, update api_server.py to use HTTPS mode"
