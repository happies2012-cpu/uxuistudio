# 🚀 COMPLETE GSWSTUDIO.AI NO-CODE PLATFORM - MASTER PROMPT SYSTEM

## 📋 TABLE OF CONTENTS
1. System Architecture Prompt
2. Frontend Wizard UI Prompt
3. Backend API Server Prompt
4. Database Schema Prompt
5. WordPress Integration Prompt
6. AI Agent System Prompt
7. Deployment Pipeline Prompt
8. Testing & QA Prompt
9. Documentation Generator Prompt
10. One-Command Build Prompt

---

## 🎯 HOW TO USE THIS SYSTEM

### Step 1: Copy each prompt to AI (Claude/ChatGPT)
### Step 2: AI generates complete, production-ready code
### Step 3: Save generated code to files
### Step 4: Run one-command deployment
### Total Time: 30 minutes to full platform

---

# PROMPT 1: SYSTEM ARCHITECTURE PROMPT

```
I need you to design a complete system architecture for a no-code WordPress site builder like gsWstudio.ai. Generate:

1. High-level architecture diagram (as ASCII art or mermaid)
2. Technology stack with justifications
3. Component breakdown with responsibilities
4. Data flow diagrams
5. API endpoint specifications
6. Database schema overview
7. Deployment architecture
8. Scalability considerations
9. Security architecture
10. Cost optimization strategies

Requirements:
- Handle 1000+ concurrent site generations
- 60-second deployment time from input to live site
- Support multiple hosting providers (DigitalOcean, AWS, existing WordPress)
- AI-powered content generation (Claude/GPT-4)
- Real-time progress updates via WebSocket
- Multi-tenant architecture with user accounts
- Payment integration (Stripe) for premium features
- Site management dashboard
- Plugin marketplace integration
- Theme customization
- SEO optimization built-in
- Mobile-first responsive design

Output Format:
- Complete architecture document in Markdown
- Technology decisions with pros/cons
- Scalability roadmap
- Security checklist
- Cost breakdown (infrastructure + API costs)

Generate the complete system architecture now.
```

---

# PROMPT 2: FRONTEND WIZARD UI PROMPT

```
Generate a complete React + TypeScript frontend for a gsWstudio.ai-like no-code WordPress builder.

REQUIREMENTS:

Tech Stack:
- React 18 + TypeScript
- TailwindCSS for styling
- Zustand for state management
- React Query for API calls
- React Router for navigation
- Framer Motion for animations
- Socket.io-client for real-time updates
- Radix UI for components
- Recharts for analytics

Pages to Generate:
1. Landing page with hero, features, pricing, testimonials
2. Sign up / Login page with OAuth (Google, GitHub)
3. Dashboard - list all user's sites with status
4. Wizard - 6-step site creation flow:
   - Step 1: Business Info (name, type, description)
   - Step 2: Design & Theme (visual theme selector)
   - Step 3: Content (AI-generated or import)
   - Step 4: Features & Plugins (checkboxes with descriptions)
   - Step 5: Hosting Setup (existing or new)
   - Step 6: Review & Deploy (summary with one-click deploy)
5. Site Editor - visual page editor with drag-drop
6. Site Settings - domain, SSL, backups, analytics
7. Analytics Dashboard - traffic, pages, performance
8. Billing page - subscription management
9. Support/Help Center
10. Account settings

Key Features:
- Real-time progress bar during site generation
- Live preview of selected theme/colors
- AI-powered content suggestions
- Undo/redo functionality
- Dark mode support
- Mobile responsive (mobile-first)
- Keyboard shortcuts
- Error boundary components
- Loading states and skeletons
- Toast notifications
- Confirmation modals for destructive actions

UI Components Needed:
- Navigation bar with user menu
- Sidebar navigation
- Multi-step wizard with progress indicator
- Theme selector with live preview
- Plugin cards with toggle switches
- Hosting credential form with validation
- Deployment progress modal with steps
- Site card with status badge and actions
- Data table for site list
- Form inputs with validation
- Button variants (primary, secondary, danger)
- Modal/Dialog components
- Dropdown menus
- Tabs component
- Accordion component
- Badge/Chip components
- Tooltip component
- Loading spinners
- Progress bars
- Alert/Banner components

State Management:
- User authentication state
- Current wizard step and data
- Site list with filters/sorting
- Theme customization state
- Real-time deployment progress
- Form validation state

API Integration:
- POST /api/auth/signup
- POST /api/auth/login
- GET /api/sites
- POST /api/sites/create
- GET /api/sites/:id
- PUT /api/sites/:id
- DELETE /api/sites/:id
- GET /api/themes
- GET /api/plugins
- WS /ws/deployment/:id (real-time updates)

Output Requirements:
1. Complete file structure with all components
2. All TypeScript interfaces and types
3. API service layer with error handling
4. Zustand store configurations
5. TailwindCSS configuration
6. React Router setup
7. Environment variables template (.env.example)
8. Package.json with all dependencies
9. README with setup instructions
10. Deployment scripts

Generate the complete frontend code now. Create a comprehensive file structure and provide code for at least 20 key files including:
- App.tsx (main entry)
- All wizard step components
- Dashboard components
- Layout components
- Shared UI components
- API service layer
- State management stores
- Type definitions
- Utility functions
- Configuration files

Make it production-ready with proper error handling, TypeScript types, responsive design, and beautiful UI.
```

---

# PROMPT 3: BACKEND API SERVER PROMPT

```
Generate a complete Node.js + TypeScript backend API server for the gsWstudio.ai platform.

TECH STACK:
- Node.js 20 + TypeScript
- Express.js framework
- PostgreSQL database (with Prisma ORM)
- Redis for caching and queues
- Bull for job queues
- Socket.io for WebSockets
- JWT for authentication
- Stripe for payments
- Winston for logging
- Jest for testing
- Docker for containerization

API ENDPOINTS TO IMPLEMENT:

Authentication:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- POST /api/v1/auth/refresh-token
- POST /api/v1/auth/forgot-password
- POST /api/v1/auth/reset-password
- GET /api/v1/auth/me

Sites:
- GET /api/v1/sites (list user's sites with pagination)
- POST /api/v1/sites (create new site - triggers async job)
- GET /api/v1/sites/:id (get site details)
- PUT /api/v1/sites/:id (update site configuration)
- DELETE /api/v1/sites/:id (delete site)
- POST /api/v1/sites/:id/deploy (redeploy site)
- POST /api/v1/sites/:id/backup (create backup)
- GET /api/v1/sites/:id/status (get deployment status)

Content:
- POST /api/v1/content/generate (AI content generation)
- GET /api/v1/themes (list available themes)
- GET /api/v1/plugins (list available plugins)

WordPress:
- POST /api/v1/wordpress/validate (validate WP credentials)
- POST /api/v1/wordpress/install (install WordPress)
- POST /api/v1/wordpress/configure (configure settings)

Hosting:
- POST /api/v1/hosting/provision (provision new server)
- GET /api/v1/hosting/providers (list hosting providers)

Billing:
- POST /api/v1/billing/create-subscription
- POST /api/v1/billing/cancel-subscription
- GET /api/v1/billing/invoices
- POST /api/v1/billing/webhook (Stripe webhooks)

Analytics:
- GET /api/v1/analytics/sites/:id (site analytics)

BACKGROUND JOBS:
1. SiteGenerationJob - orchestrates entire site creation
2. ContentGenerationJob - generates AI content
3. WordPressInstallJob - installs WordPress
4. ThemeInstallJob - installs theme
5. PluginInstallJob - installs plugins
6. BackupJob - creates site backup
7. EmailJob - sends notifications

KEY FEATURES:
- JWT-based authentication with refresh tokens
- Role-based access control (admin, user)
- Request validation using Joi/Zod
- Rate limiting (express-rate-limit)
- CORS configuration
- Request logging
- Error handling middleware
- API versioning
- Pagination helper
- File upload handling
- WebSocket events for real-time updates
- Job queue with retries and dead-letter queue
- Caching strategy (Redis)
- Database transactions
- Soft deletes
- Audit logging
- Health check endpoint
- Metrics endpoint (Prometheus format)

SERVICES TO IMPLEMENT:
1. AuthService - user authentication
2. UserService - user management
3. SiteService - site CRUD operations
4. AIService - AI content generation (Anthropic/OpenAI)
5. WordPressService - WP API interactions
6. HostingService - provision servers (DO/AWS)
7. DNSService - domain management (Cloudflare)
8. EmailService - send notifications (SendGrid)
9. PaymentService - Stripe integration
10. BackupService - site backups
11. AnalyticsService - usage analytics
12. CacheService - Redis operations

MIDDLEWARE:
- authenticate (JWT verification)
- authorize (role check)
- validate (request validation)
- errorHandler (global error handling)
- notFound (404 handler)
- rateLimiter (rate limiting)
- requestLogger (log requests)
- corsHandler (CORS configuration)

ERROR HANDLING:
- Custom error classes (BadRequestError, UnauthorizedError, etc.)
- Centralized error handling
- Proper HTTP status codes
- Error logging
- Error responses in consistent format

SECURITY:
- Helmet for security headers
- Input sanitization
- SQL injection prevention (Prisma)
- XSS protection
- CSRF protection
- Password hashing (bcrypt)
- Secrets management (environment variables)
- API key rotation

OUTPUT REQUIREMENTS:
1. Complete project structure
2. All API routes with controllers
3. All services with business logic
4. Database models (Prisma schema)
5. Middleware implementations
6. Job queue definitions
7. WebSocket event handlers
8. Configuration files
9. Environment variables template
10. Docker Compose configuration
11. Package.json with dependencies
12. tsconfig.json
13. .eslintrc and .prettierrc
14. README with API documentation
15. Postman collection for API testing

Generate the complete backend code now. Provide at least 30 key files including:
- src/server.ts (main entry point)
- src/app.ts (Express app setup)
- All route handlers
- All service classes
- All middleware
- Prisma schema
- Job definitions
- WebSocket handlers
- Config files
- Docker setup
- Testing examples

Make it production-ready with proper error handling, logging, validation, and security.
```

---

# PROMPT 4: DATABASE SCHEMA PROMPT

```
Generate a complete PostgreSQL database schema using Prisma ORM for the gsWstudio.ai platform.

REQUIREMENTS:

Tables/Models Needed:
1. User - user accounts with authentication
2. Site - WordPress sites created by users
3. SiteDeployment - deployment history and status
4. Theme - available WordPress themes
5. Plugin - available WordPress plugins
6. SitePlugin - many-to-many relationship for site plugins
7. Page - pages in a site
8. Post - blog posts in a site
9. Media - uploaded media files
10. Subscription - user subscription plans
11. Payment - payment transactions
12. ApiKey - API keys for programmatic access
13. Backup - site backup records
14. Domain - custom domains
15. Analytics - site analytics data
16. ActivityLog - audit log for user actions
17. Notification - user notifications
18. Template - site templates
19. Webhook - webhook configurations
20. EmailLog - email sending history

Fields for User Model:
- id (UUID, primary key)
- email (unique, indexed)
- password (hashed)
- firstName
- lastName
- avatar (URL)
- role (enum: USER, ADMIN)
- emailVerified (boolean)
- emailVerificationToken
- passwordResetToken
- passwordResetExpiry
- lastLoginAt
- createdAt
- updatedAt
- deletedAt (soft delete)

Fields for Site Model:
- id (UUID, primary key)
- userId (foreign key to User)
- name
- businessType
- industry
- description
- url (unique)
- wpUsername
- wpPassword (encrypted)
- wpVersion
- themeId (foreign key to Theme)
- status (enum: DRAFT, GENERATING, DEPLOYED, FAILED, ARCHIVED)
- deploymentProgress (JSON)
- siteMetadata (JSON) - colors, fonts, etc.
- hosting (JSON) - provider, credentials
- ssl (boolean)
- createdAt
- updatedAt
- deletedAt

Fields for SiteDeployment Model:
- id (UUID, primary key)
- siteId (foreign key to Site)
- status (enum: PENDING, IN_PROGRESS, COMPLETED, FAILED)
- steps (JSON array) - deployment steps with status
- logs (text)
- startedAt
- completedAt
- errorMessage
- createdAt

Fields for Theme Model:
- id (UUID, primary key)
- name
- slug (unique)
- description
- thumbnail (URL)
- demoUrl
- category
- tags (array)
- isPremium (boolean)
- price
- rating
- downloads
- version
- createdAt
- updatedAt

Fields for Plugin Model:
- id (UUID, primary key)
- name
- slug (unique)
- description
- category
- isPremium (boolean)
- price
- required (boolean)
- configuration (JSON)
- createdAt
- updatedAt

Fields for Page Model:
- id (UUID, primary key)
- siteId (foreign key to Site)
- title
- slug
- content (text)
- template
- seoTitle
- seoDescription
- focusKeyword
- status (enum: DRAFT, PUBLISHED)
- order
- parentId (self-referential for hierarchy)
- createdAt
- updatedAt

Fields for Post Model:
- id (UUID, primary key)
- siteId (foreign key to Site)
- title
- slug
- content (text)
- excerpt
- featuredImage
- categories (array)
- tags (array)
- seoTitle
- seoDescription
- status (enum: DRAFT, PUBLISHED)
- publishedAt
- createdAt
- updatedAt

Fields for Subscription Model:
- id (UUID, primary key)
- userId (foreign key to User)
- plan (enum: FREE, STARTER, PROFESSIONAL, ENTERPRISE)
- status (enum: ACTIVE, CANCELED, EXPIRED)
- stripeSubscriptionId
- stripeCustomerId
- currentPeriodStart
- currentPeriodEnd
- cancelAt
- createdAt
- updatedAt

Fields for Payment Model:
- id (UUID, primary key)
- userId (foreign key to User)
- subscriptionId (foreign key to Subscription)
- amount
- currency
- status (enum: PENDING, COMPLETED, FAILED, REFUNDED)
- stripePaymentIntentId
- paymentMethod
- createdAt

Fields for Backup Model:
- id (UUID, primary key)
- siteId (foreign key to Site)
- size (bytes)
- storageUrl
- status (enum: IN_PROGRESS, COMPLETED, FAILED)
- type (enum: MANUAL, SCHEDULED)
- createdAt

Fields for ActivityLog Model:
- id (UUID, primary key)
- userId (foreign key to User)
- action
- resourceType
- resourceId
- metadata (JSON)
- ipAddress
- userAgent
- createdAt

RELATIONSHIPS:
- User has many Sites (one-to-many)
- User has one Subscription (one-to-one)
- User has many Payments (one-to-many)
- Site has many Pages (one-to-many)
- Site has many Posts (one-to-many)
- Site has many Deployments (one-to-many)
- Site has many Backups (one-to-many)
- Site has many Plugins (many-to-many through SitePlugin)
- Site has one Theme (many-to-one)

INDEXES:
- User: email, createdAt
- Site: userId, status, url, createdAt
- Page: siteId, slug, status
- Post: siteId, slug, status, publishedAt
- Payment: userId, createdAt
- ActivityLog: userId, createdAt

CONSTRAINTS:
- Unique constraints on emails, URLs, slugs
- Foreign key constraints with CASCADE/SET NULL
- Check constraints on enums
- NOT NULL constraints on required fields

OUTPUT REQUIRED:
1. Complete Prisma schema file (schema.prisma)
2. Migration files for initial setup
3. Seed data script (seed.ts)
4. Database configuration
5. Connection pooling setup
6. Backup and restore scripts
7. Database indexes optimization
8. Query performance guidelines
9. Data retention policy
10. GDPR compliance notes

Generate the complete Prisma schema now with:
- All models with proper fields and types
- All relationships properly defined
- All indexes and constraints
- Seed data for themes and plugins
- Migration commands
- Environment variable configuration

Make it production-ready and scalable.
```

---

# PROMPT 5: WORDPRESS INTEGRATION PROMPT

```
Generate complete WordPress integration code for the gsWstudio.ai platform.

REQUIREMENTS:

Create three integration modules:

1. WORDPRESS REST API CLIENT
- Class-based TypeScript client for WP REST API
- Methods for all CRUD operations
- Authentication (Application Passwords)
- Error handling and retries
- Rate limiting
- Batch operations for performance
- TypeScript interfaces for all WP entities

Operations to Support:
- Test connection
- Create/update/delete pages
- Create/update/delete posts
- Upload media files
- Create/configure menus
- Install/activate themes
- Install/activate plugins
- Update WordPress settings
- Configure permalinks
- Set up SEO (Yoast)
- Configure security plugins
- Set up caching
- Create user accounts
- Manage categories/tags
- Import/export content

2. WP-CLI SSH CLIENT
- SSH connection management
- Execute WP-CLI commands remotely
- WordPress core installation
- Theme/plugin management via CLI
- Database operations
- File system operations
- Backup/restore operations
- Error handling and logging

Commands to Support:
- wp core download
- wp core install
- wp core update
- wp config create
- wp theme install/activate
- wp plugin install/activate
- wp user create
- wp db export/import
- wp rewrite flush
- wp cache flush
- wp search-replace (for domain changes)

3. WORDPRESS AUTOMATION SERVICE
- High-level service that orchestrates site creation
- Step-by-step deployment with progress tracking
- Rollback capability on failure
- Health checks after each step
- Validation and verification
- Comprehensive error handling

Deployment Steps:
1. Validate hosting credentials
2. Install WordPress core
3. Create wp-config.php
4. Set up database
5. Install and activate theme
6. Install and activate plugins
7. Configure plugin settings
8. Create initial pages
9. Create initial posts
10. Upload media files
11. Configure menus
12. Set permalinks
13. Configure SEO settings
14. Set up security
15. Enable caching
16. Create backup
17. Run health checks
18. Send completion notification

KEY FEATURES:
- Concurrent operations where safe (e.g., plugin installs)
- Progress callbacks for real-time updates
- Detailed logging at each step
- Validation before and after operations
- Automatic retry on transient failures
- Graceful degradation (continue even if non-critical steps fail)
- Performance optimization (batch API calls)
- Memory-efficient media uploads
- Connection pooling
- Timeout handling

ERROR HANDLING:
- Network errors with retry
- Authentication failures
- Permission errors
- WordPress errors (plugin conflicts, etc.)
- Resource limitations (memory, storage)
- SSL certificate errors
- DNS propagation delays

SECURITY:
- Secure credential storage (encrypted)
- SSH key-based authentication preferred
- Application Password generation
- Credential validation before use
- Secure file transfers
- No hardcoded credentials

PERFORMANCE:
- Batch API requests (20 items max per call)
- Parallel operations where safe
- Connection reuse
- Caching of WordPress metadata
- Efficient media uploads (chunked)
- Minimal API calls

OUTPUT REQUIRED:
1. WordPressAPIClient class with all methods
2. SSHClient class for WP-CLI operations
3. WordPressService for high-level orchestration
4. TypeScript interfaces for all WP entities
5. Error classes for WP-specific errors
6. Helper utilities (URL validation, slug generation)
7. Configuration management
8. Logging setup
9. Test suite with mocks
10. Integration test examples
11. Documentation with usage examples
12. Performance benchmarks

Generate complete code for:
- src/integrations/wordpress/api-client.ts
- src/integrations/wordpress/ssh-client.ts
- src/integrations/wordpress/wordpress.service.ts
- src/integrations/wordpress/types.ts
- src/integrations/wordpress/errors.ts
- src/integrations/wordpress/utils.ts
- src/integrations/wordpress/config.ts
- tests/wordpress.test.ts

Provide production-ready code with:
- Full TypeScript types
- Comprehensive error handling
- Logging and monitoring
- Performance optimization
- Security best practices
- Test coverage
- Clear documentation

Also include usage examples showing:
- How to create a complete WordPress site
- How to update existing site
- How to backup/restore
- How to handle errors
- How to monitor progress
```

---

# PROMPT 6: AI AGENT SYSTEM PROMPT

```
Generate a complete AI agent orchestration system for gsWstudio.ai that uses Claude/GPT-4 to generate site content and architecture.

REQUIREMENTS:

Create 6 specialized AI agents:

1. SITE PLANNING AGENT
- Analyzes business description
- Generates site architecture (pages, features)
- Recommends plugins and themes
- Creates content strategy
- Output: JSON with complete site structure

2. CONTENT GENERATION AGENT
- Generates page content (HTML)
- Generates blog posts
- Creates SEO metadata (titles, descriptions)
- Writes compelling copy
- Output: JSON with all content

3. DESIGN AGENT
- Selects optimal theme
- Chooses color palette
- Selects typography
- Creates design system
- Output: JSON with design configuration

4. PLUGIN SELECTION AGENT
- Chooses essential plugins
- Configures plugin settings
- Ensures compatibility
- Minimizes plugin count
- Output: JSON with plugin list and configs

5. DEPLOYMENT AGENT
- Creates deployment plan
- Validates prerequisites
- Generates deployment steps
- Handles errors gracefully
- Output: JSON with deployment instructions

6. MASTER ORCHESTRATOR
- Coordinates all agents
- Manages workflow
- Handles inter-agent dependencies
- Tracks progress
- Output: Complete site generation result

IMPLEMENTATION REQUIREMENTS:

Each Agent Should Have:
- System prompt (role definition)
- User prompt template
- Input schema (TypeScript interface)
- Output schema (TypeScript interface)
- Confidence threshold
- Retry logic
- Error handling
- Assumption logging
- Token budget limits
- Temperature/sampling settings

AI Service Layer:
- Support multiple AI providers (Anthropic, OpenAI)
- Fallback to alternative models
- Rate limiting and quotas
- Cost tracking per generation
- Response caching where appropriate
- Streaming support for real-time updates
- Prompt versioning
- A/B testing of prompts

Orchestration System:
- Sequential agent execution with dependencies
- Parallel execution where possible
- State management across agents
- Rollback on failure
- Resume from checkpoint
- Progress tracking (0-100%)
- Real-time WebSocket updates
- Quality gates between agents

Prompt Engineering:
- System prompts that enforce JSON output
- Few-shot examples in prompts
- Chain-of-thought reasoning
- Output validation instructions
- Confidence scoring requirements
- Assumption documentation
- Edge case handling
- Fallback instructions

Quality Control:
- JSON schema validation on outputs
- Confidence thresholds (0.75 minimum)
- Content quality checks (no placeholders, proper grammar)
- SEO optimization validation
- Accessibility checks
- Performance scoring
- Manual review triggers for low confidence

Cost Optimization:
- Token budgets per agent (600-2000 tokens)
- Smaller models for simple tasks
- Caching of similar requests
- Batch processing where possible
- Prompt compression techniques
- Early termination on errors

OUTPUT REQUIRED:
Generate complete code for:

1. src/ai/agents/PlanningAgent.ts
2. src/ai/agents/ContentAgent.ts
3. src/ai/agents/DesignAgent.ts
4. src/ai/agents/PluginAgent.ts
5. src/ai/agents/DeploymentAgent.ts
6. src/ai/agents/Orchestrator.ts
7. src/ai/AIService.ts (multi-provider support)
8. src/ai/PromptBuilder.ts
9. src/ai/PromptTemplates.ts (all prompt templates)
10. src/ai/types.ts (all interfaces)
11. src/ai/config.ts
12. src/ai/utils.ts (validation, parsing)
13. tests/ai/agents.test.ts

Each agent file should include:
- Class with execute() method
- Private methods for sub-tasks
- Error handling
- Logging
- Telemetry
- Unit tests

PromptTemplates.ts should include:
- All 6 agent prompts as constants
- Variable substitution helpers
- Prompt composition utilities
- Examples and few-shots

AIService.ts should support:
- Anthropic Claude (primary)
- OpenAI GPT-4 (fallback)
- Provider selection logic
- Streaming responses
- Cost tracking
- Rate limiting
- Error handling
- Retries with exponential backoff

Orchestrator.ts should:
- Execute agents in sequence
- Pass outputs between agents
- Track overall progress
- Handle failures gracefully
- Provide rollback capability
- Send real-time updates via WebSocket
- Generate final summary report
- Calculate overall confidence

Also provide:
- Example agent inputs/outputs
- Prompt engineering guidelines
- Cost analysis per site generation
- Performance benchmarks
- Quality metrics
- Testing strategy

Make it production-ready with:
- Full TypeScript types
- Comprehensive error handling
- Detailed logging
- Cost tracking
- Performance monitoring
- High-quality prompts that produce excellent results
```

---

# PROMPT 7: DEPLOYMENT PIPELINE PROMPT

```
Generate a complete CI/CD deployment pipeline for the gsWstudio.ai platform.

REQUIREMENTS:

Create deployment configurations for:

1. DOCKER SETUP
- Multi-stage Dockerfile for frontend
- Multi-stage Dockerfile for backend
- Docker Compose for local development
- Docker Compose for production
- Health checks for all containers
- Volume management
- Network configuration
- Environment variable management

2. KUBERNETES DEPLOYMENT
- Deployment manifests for all services
- Service definitions
- Ingress configuration
- ConfigMaps and Secrets
- HorizontalPodAutoscaler
- PersistentVolumeClaims
- Resource limits and requests
- Liveness and readiness probes
- Rolling update strategy

3. CI/CD PIPELINE (GitHub Actions)
- Automated testing on PR
- Build and push Docker images
- Deploy to staging on merge to main
- Deploy to production on release tag
- Run database migrations
- Run integration tests
- Security scanning
- Performance testing
- Rollback capability

4. INFRASTRUCTURE AS CODE (Terraform)
- AWS/DigitalOcean infrastructure setup
- VPC and networking
- Load balancers
- Database (RDS/managed PostgreSQL)
- Redis cluster
- S3 buckets for media
- CloudFront CDN
- Route53 DNS
- SSL certificates
- Monitoring and alerting

5. MONITORING & OBSERVABILITY
- Prometheus metrics
- Grafana dashboards
- Loki for log aggregation
- Jaeger for tracing
- Alert manager rules
- Uptime monitoring
- Error tracking (Sentry)
- Performance monitoring

COMPONENTS TO DEPLOY:
1. Frontend (React app)
2. Backend API (Node.js)
3. PostgreSQL database
4. Redis cache
5. Job queue workers
6. WebSocket server
7. Nginx reverse proxy

ENVIRONMENTS:
- Development (local with Docker Compose)
- Staging (Kubernetes on cloud)
- Production (Kubernetes with HA)

OUTPUT REQUIRED:

Docker Files:
1. frontend/Dockerfile
2. backend/Dockerfile
3. docker-compose.yml (development)
4. docker-compose.prod.yml (production)
5. .dockerignore files

Kubernetes Files:
1. k8s/frontend-deployment.yaml
2. k8s/backend-deployment.yaml
3. k8s/postgres-statefulset.yaml
4. k8s/redis-deployment.yaml
5. k8s/worker-deployment.yaml
6. k8s/nginx-ingress.yaml
7. k8s/services.yaml
8. k8s/configmaps.yaml
9. k8s/secrets.yaml (template)
10. k8s/hpa.yaml
11. k8s/pvc.yaml

GitHub Actions:
1. .github/workflows/test.yml
2. .github/workflows/build.yml
3. .github/workflows/deploy-staging.yml
4. .github/workflows/deploy-production.yml
5. .github/workflows/security-scan.yml

Terraform:
1. terraform/main.tf
2. terraform/variables.tf
3. terraform/outputs.tf
4. terraform/vpc.tf
5. terraform/database.tf
6. terraform/redis.tf
7. terraform/s3.tf
8. terraform/cloudfront.tf

Monitoring:
1. monitoring/prometheus.yml
2. monitoring/grafana-dashboards.json
3. monitoring/alertmanager.yml
4. monitoring/alerts.rules

Scripts:
1. scripts/deploy.sh
2. scripts/rollback.sh
3. scripts/migrate.sh
4. scripts/backup.sh
5. scripts/restore.sh
6. scripts/health-check.sh

FEATURES:

Docker:
- Multi-stage builds for smaller images
- Layer caching optimization
- Security scanning
- Non-root user
- Health checks
- Graceful shutdown

Kubernetes:
- Zero-downtime deployments
- Auto-scaling (CPU/memory based)
- Self-healing (restart unhealthy pods)
- Rolling updates with max surge/unavailable
- Resource quotas
- Network policies
- Pod disruption budgets

CI/CD:
- Automated testing (unit, integration, e2e)
- Code coverage requirements
- Linting and formatting checks
- Security vulnerability scanning
- Container image scanning
- Database migration automation
- Blue-green deployments
- Canary deployments
- Automatic rollback on failure
- Slack/Discord notifications

Monitoring:
- Application metrics (requests, errors, latency)
- Infrastructure metrics (CPU, memory, disk)
- Business metrics (sites created, user signups)
- Custom dashboards
- Alerts for critical issues
- Log aggregation and search
- Distributed tracing
- Error tracking with stack traces

SECURITY:
- Secrets management (Kubernetes secrets, Vault)
- Network policies (pod-to-pod communication)
- RBAC (role-based access control)
- Image scanning for vulnerabilities
- SSL/TLS everywhere
- Rate limiting
- DDoS protection
- Backup encryption

SCALABILITY:
- Horizontal pod autoscaling
- Database read replicas
- Redis clustering
- CDN for static assets
- Load balancing
- Connection pooling
- Caching strategies

Generate complete, production-ready deployment configurations with:
- All configuration files
- Clear documentation
- Setup instructions
- Troubleshooting guide
- Cost estimates
- Performance benchmarks
- Security checklist
- Disaster recovery plan
```

---

# PROMPT 8: TESTING & QA PROMPT

```
Generate a complete testing suite for the gsWstudio.ai platform covering unit tests, integration tests, E2E tests, and load tests.

REQUIREMENTS:

1. UNIT TESTS (Jest + React Testing Library)
- Test all React components
- Test all API services
- Test all utility functions
- Test all AI agents
- Test all WordPress integrations
- Test all state management (Zustand stores)
- Aim for 80% code coverage
- Mock external APIs (Stripe, OpenAI, WordPress)
- Snapshot testing for UI components

2. INTEGRATION TESTS (Jest + Supertest)
- Test API endpoints with real database
- Test authentication flows
- Test job queue processing
- Test WebSocket events
- Test database transactions
- Test error handling middleware

3. E2E TESTS (Playwright)
- Critical user flows:
  - User signup and login
  - Site creation wizard (all 6 steps)
  - Dashboard navigation
  - Site deployment simulation
  - Subscription upgrade
  - Account settings update
- Cross-browser testing (Chrome, Firefox, Safari)
- Mobile responsiveness testing

4. LOAD TESTS (k6)
- Simulate 100 concurrent users
- Test site generation endpoint under load
- Test WebSocket connection limits
- Measure API latency
- Identify bottlenecks

OUTPUT REQUIRED:

Configuration:
1. jest.config.js (frontend & backend)
2. playwright.config.ts
3. k6-script.js

Test Files:
1. tests/unit/components/Wizard.test.tsx
2. tests/unit/services/AIService.test.ts
3. tests/integration/api/sites.test.ts
4. tests/e2e/site-creation.spec.ts
5. tests/load/generation-load.js

Mocks & Helpers:
1. tests/mocks/openai.ts
2. tests/mocks/stripe.ts
3. tests/factories/user.ts
4. tests/setup.ts

Generate the complete testing suite setup and example tests now.
```

---

# PROMPT 9: DOCUMENTATION GENERATOR PROMPT

```
Generate comprehensive documentation for the gsWstudio.ai platform using Docusaurus or similar.

REQUIREMENTS:

1. ARCHITECTURE DOCUMENTATION
- System overview diagram
- Component interaction flow
- Data models and relationships
- Security architecture
- Scalability design

2. API DOCUMENTATION (OpenAPI/Swagger)
- Authentication methods
- Request/Response schemas
- Error codes
- Rate limits
- Example requests (curl, js, python)

3. DEVELOPER GUIDE
- Local setup instructions
- Environment variables
- Database migration guide
- Testing guide
- Contribution guidelines
- Coding standards

4. USER GUIDE
- Getting started tutorial
- Creating your first site
- Managing domains
- Troubleshooting common issues
- Billing and subscriptions

5. OPERATIONAL RUNBOOKS
- Deployment guide
- Backup and restore procedures
- Incident response plan
- Monitoring and alerting
- Secret rotation

OUTPUT REQUIRED:

1. Docusaurus project structure
2. docusaurus.config.js
3. docs/intro.md
4. docs/architecture/overview.md
5. docs/api/spec.json (OpenAPI)
6. docs/guides/setup.md
7. docs/runbooks/deployment.md

Generate the documentation structure and key content files now.
```

---

# PROMPT 10: ONE-COMMAND BUILD PROMPT

```
Create a "Magic Build Script" that sets up the entire gsWstudio.ai platform with a single command.

REQUIREMENTS:

The script should:
1. Check for prerequisites (Node, Docker, Git)
2. Clone the repository (if not already)
3. Generate SSL certificates for local dev
4. Create .env files from examples
5. Start Docker containers (Postgres, Redis)
6. Run database migrations
7. Seed the database with initial data
8. Build frontend and backend
9. Start all services
10. Open the app in the browser

FEATURES:
- Cross-platform support (Mac, Linux, Windows WSL)
- Interactive CLI with progress bars
- Error handling and rollback
- Idempotency (can be run multiple times safely)
- Colorful output (using chalk/ora)
- Health checks before opening browser

OUTPUT REQUIRED:

1. scripts/setup.sh (Bash)
2. scripts/setup.js (Node.js version for cross-platform)
3. package.json scripts entry

Generate the complete one-command setup script now.
```

---

# 🚀 CONGRATULATIONS!

If you have executed all 10 prompts, you now have a complete, production-ready No-Code WordPress Platform called **gsWstudio.ai**.

## NEXT STEPS:

1. Run the **One-Command Build** script
2. Navigate to `http://localhost:3000`
3. Create your admin account
4. Generate your first AI-powered WordPress site!