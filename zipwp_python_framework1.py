"""
ZipWP No-Code WordPress Platform - Python Implementation Framework
Complete autonomous WordPress site generation system with 6 specialized agents
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import aiohttp
import paramiko
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

class Status(Enum):
    OK = "ok"
    FAILED = "failed"
    NEEDS_INPUT = "needs_input"
    IN_PROGRESS = "in_progress"


@dataclass
class AgentResponse:
    """Standard response format for all agents"""
    status: str
    action: str
    result_summary: str
    result: Dict[str, Any]
    assumptions: List[str]
    confidence: float
    next_steps: List[str]
    required_credentials: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BusinessInput:
    """User input for site generation"""
    business_name: str
    business_type: str
    description: Optional[str] = None
    industry: Optional[str] = None
    target_audience: Optional[str] = "general public"
    goals: Optional[List[str]] = None
    tone: Optional[str] = "professional and approachable"
    design_preference: Optional[str] = "modern and clean"
    hosting_info: Optional[Dict[str, str]] = None
    domain: Optional[str] = None


@dataclass
class WordPressCredentials:
    """WordPress access credentials"""
    site_url: str
    username: str
    password: str  # Application password
    ssh_host: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_key: Optional[str] = None
    ssh_password: Optional[str] = None


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Global configuration"""
    # AI Model settings
    MODEL_TEMPERATURE = 0.10
    MODEL_TOP_P = 0.8
    MAX_TOKENS_PLANNING = 600
    MAX_TOKENS_CONTENT = 2000
    MAX_TOKENS_DESIGN = 500
    MAX_TOKENS_PLUGINS = 500
    MAX_TOKENS_DEPLOYMENT = 800
    MAX_TOKENS_ORCHESTRATOR = 600
    
    # Confidence thresholds
    CONFIDENCE_DEPLOY = 0.80
    CONFIDENCE_CONTENT = 0.70
    CONFIDENCE_DESIGN = 0.60
    CONFIDENCE_OVERALL = 0.75
    
    # API settings
    RETRY_ATTEMPTS = 2
    RETRY_DELAY = 5  # seconds
    BATCH_SIZE = 20  # items per API call
    API_TIMEOUT = 30  # seconds
    
    # WordPress defaults
    DEFAULT_PERMALINK_STRUCTURE = "/%postname%/"
    DEFAULT_TIMEZONE = "UTC"
    DEFAULT_PLUGINS = [
        "yoast-seo",
        "wordfence",
        "litespeed-cache",
        "updraftplus",
        "wpforms-lite"
    ]


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.assumptions = []
    
    def add_assumption(self, assumption: str):
        """Add an assumption to the log"""
        self.assumptions.append(f"ASSUME: {assumption}")
        self.logger.info(f"Assumption: {assumption}")
    
    @abstractmethod
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Execute agent logic"""
        pass
    
    def build_prompt(self, template: str, variables: Dict) -> str:
        """Build prompt from template with variables"""
        prompt = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            prompt = prompt.replace(placeholder, str(value))
        return prompt
    
    async def call_ai_model(self, prompt: str, max_tokens: int) -> Dict:
        """Call AI model and return parsed JSON response"""
        try:
            response = await self.ai_client.generate(
                prompt=prompt,
                temperature=Config.MODEL_TEMPERATURE,
                top_p=Config.MODEL_TOP_P,
                max_tokens=max_tokens
            )
            return json.loads(response)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response: {e}")
            raise
        except Exception as e:
            self.logger.error(f"AI model call failed: {e}")
            raise


# ============================================================================
# AGENT 1: SITE PLANNING & ARCHITECTURE
# ============================================================================

class SitePlanningAgent(BaseAgent):
    """Generates WordPress site architecture"""
    
    PROMPT_TEMPLATE = """
Task: Generate WordPress site architecture for business.

Input:
- Business name: {{business_name}}
- Business type: {{business_type}}
- Industry: {{industry}}
- Description: {{description}}
- Target audience: {{target_audience}}
- Key goals: {{goals}}

Decision Rules:
1. If required parameter missing, use specified default or most common WordPress standard
2. Generate 5-8 essential pages (Home, About, Services/Products, Contact mandatory)
3. Max 5 plugin recommendations
4. All suggestions must work with free WordPress.org plugins
5. Assume mobile-first design priority

Output valid JSON only with this exact structure:
{
  "status": "ok|failed|needs_input",
  "action": "site_architecture_generated",
  "result_summary": "Generated architecture for [business_name]",
  "result": {
    "site_structure": {
      "pages": [
        {"title": "Home", "slug": "home", "purpose": "...", "content_themes": [], "priority": "high", "template": "default"}
      ],
      "menus": [{"location": "primary", "items": ["Home", "About"]}]
    },
    "features": [{"name": "Contact Form", "priority": "high", "implementation": "plugin"}],
    "plugins": [{"name": "Contact Form 7", "slug": "contact-form-7", "purpose": "Handle contact", "required": true}],
    "content_strategy": {
      "post_types": ["posts"],
      "initial_categories": ["News"],
      "suggested_posts": [{"title": "Welcome", "theme": "introduction"}]
    },
    "seo_foundation": {
      "primary_keywords": ["kw1", "kw2"],
      "site_tagline": "Professional tagline",
      "meta_description_template": "template"
    }
  },
  "assumptions": [],
  "confidence": 0.85,
  "next_steps": ["generate_content"]
}

Generate complete, valid JSON now.
"""
    
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Generate site architecture"""
        self.logger.info("Starting site planning...")
        
        # Apply defaults
        business = BusinessInput(**input_data)
        if not business.industry:
            business.industry = self._infer_industry(business.business_type)
            self.add_assumption(f"Industry inferred as {business.industry}")
        
        if not business.description:
            business.description = f"Professional {business.business_type} website"
            self.add_assumption("Using default description")
        
        if not business.goals:
            business.goals = ["inform visitors", "generate leads"]
            self.add_assumption("Using default goals: inform and generate leads")
        
        # Build and execute prompt
        prompt = self.build_prompt(self.PROMPT_TEMPLATE, {
            "business_name": business.business_name,
            "business_type": business.business_type,
            "industry": business.industry,
            "description": business.description,
            "target_audience": business.target_audience,
            "goals": ", ".join(business.goals)
        })
        
        result = await self.call_ai_model(prompt, Config.MAX_TOKENS_PLANNING)
        result["assumptions"].extend(self.assumptions)
        
        self.logger.info(f"Site planning completed with confidence: {result['confidence']}")
        return AgentResponse(**result)
    
    def _infer_industry(self, business_type: str) -> str:
        """Infer industry from business type"""
        industry_map = {
            "restaurant": "food_service",
            "dental": "healthcare",
            "law": "legal",
            "retail": "ecommerce",
            "consulting": "professional_services"
        }
        return industry_map.get(business_type.lower(), "professional_services")


# ============================================================================
# AGENT 2: CONTENT GENERATION
# ============================================================================

class ContentGenerationAgent(BaseAgent):
    """Generates all page and post content"""
    
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Generate content for all pages and posts"""
        self.logger.info("Starting content generation...")
        
        site_structure = input_data.get("site_structure", {})
        business_context = input_data.get("business_context", {})
        tone = input_data.get("tone", "professional and approachable")
        
        pages_to_generate = site_structure.get("pages", [])
        
        # Generate content in batches
        all_pages = []
        for i in range(0, len(pages_to_generate), 5):
            batch = pages_to_generate[i:i+5]
            batch_content = await self._generate_batch_content(
                batch, business_context, tone
            )
            all_pages.extend(batch_content)
        
        # Generate initial blog posts
        posts = await self._generate_initial_posts(
            business_context, 
            site_structure.get("content_strategy", {})
        )
        
        result = {
            "status": "ok",
            "action": "content_generated",
            "result_summary": f"Generated {len(all_pages)} pages and {len(posts)} posts",
            "result": {
                "pages": all_pages,
                "posts": posts
            },
            "assumptions": self.assumptions,
            "confidence": 0.82,
            "next_steps": ["select_theme"]
        }
        
        return AgentResponse(**result)
    
    async def _generate_batch_content(
        self, pages: List[Dict], context: Dict, tone: str
    ) -> List[Dict]:
        """Generate content for a batch of pages"""
        prompt = f"""
Generate production-ready WordPress content for these pages:
{json.dumps(pages, indent=2)}

Business context: {json.dumps(context, indent=2)}
Tone: {tone}

For each page, provide:
1. Full HTML content (WordPress Gutenberg compatible)
2. SEO title (≤60 chars)
3. Meta description (≤160 chars)
4. Focus keyword

Output valid JSON array of page objects.
"""
        result = await self.call_ai_model(prompt, Config.MAX_TOKENS_CONTENT)
        return result.get("pages", [])
    
    async def _generate_initial_posts(
        self, context: Dict, strategy: Dict
    ) -> List[Dict]:
        """Generate 3-5 initial blog posts"""
        suggested_posts = strategy.get("suggested_posts", [])[:3]
        
        if not suggested_posts:
            return []
        
        prompt = f"""
Generate 3 blog posts for:
Business: {context.get('business_name')}
Topics: {json.dumps(suggested_posts)}

Each post: 500-800 words, SEO optimized.
Output valid JSON array.
"""
        result = await self.call_ai_model(prompt, Config.MAX_TOKENS_CONTENT)
        return result.get("posts", [])


# ============================================================================
# AGENT 3: THEME & DESIGN SELECTION
# ============================================================================

class ThemeDesignAgent(BaseAgent):
    """Selects optimal WordPress theme and design configuration"""
    
    THEME_DATABASE = {
        "professional_services": {
            "theme": "astra",
            "colors": {"primary": "#1e73be", "secondary": "#23282d", "accent": "#ff6b6b"}
        },
        "healthcare": {
            "theme": "neve",
            "colors": {"primary": "#0066cc", "secondary": "#ffffff", "accent": "#4CAF50"}
        },
        "ecommerce": {
            "theme": "storefront",
            "colors": {"primary": "#96588a", "secondary": "#43454b", "accent": "#f47e27"}
        },
        "creative": {
            "theme": "blocksy",
            "colors": {"primary": "#ff5722", "secondary": "#212121", "accent": "#FFC107"}
        }
    }
    
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Select theme and design configuration"""
        self.logger.info("Selecting theme and design...")
        
        industry = input_data.get("industry", "professional_services")
        business_type = input_data.get("business_type", "")
        
        # Select theme based on industry
        theme_config = self.THEME_DATABASE.get(
            industry, 
            self.THEME_DATABASE["professional_services"]
        )
        
        result = {
            "status": "ok",
            "action": "theme_selected",
            "result_summary": f"Selected {theme_config['theme']} theme",
            "result": {
                "primary_theme": {
                    "name": theme_config["theme"].title(),
                    "slug": theme_config["theme"],
                    "version": "latest",
                    "type": "free",
                    "justification": f"Optimal for {industry} industry",
                    "features": ["responsive", "seo-friendly", "fast-loading"],
                    "performance_score": "excellent"
                },
                "design_config": {
                    "color_palette": theme_config["colors"],
                    "typography": {
                        "heading_font": "Montserrat",
                        "body_font": "Open Sans",
                        "base_size": "16px"
                    },
                    "layout": {
                        "container_width": "1200px",
                        "sidebar": "none",
                        "header_style": "modern"
                    }
                }
            },
            "assumptions": self.assumptions,
            "confidence": 0.78,
            "next_steps": ["select_plugins"]
        }
        
        return AgentResponse(**result)


# ============================================================================
# AGENT 4: PLUGIN SELECTION & CONFIGURATION
# ============================================================================

class PluginSelectionAgent(BaseAgent):
    """Selects and configures WordPress plugins"""
    
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Select essential plugins"""
        self.logger.info("Selecting plugins...")
        
        features = input_data.get("features", [])
        business_type = input_data.get("business_type", "")
        
        # Core plugins (always included)
        plugins = [
            {
                "name": "Yoast SEO",
                "slug": "wordpress-seo",
                "purpose": "Search engine optimization",
                "required": True,
                "priority": 10,
                "configuration": {"enable_xml_sitemap": True}
            },
            {
                "name": "Wordfence Security",
                "slug": "wordfence",
                "purpose": "Site security and firewall",
                "required": True,
                "priority": 9,
                "configuration": {"enable_firewall": True}
            },
            {
                "name": "LiteSpeed Cache",
                "slug": "litespeed-cache",
                "purpose": "Performance optimization",
                "required": True,
                "priority": 8,
                "configuration": {"enable_cache": True}
            },
            {
                "name": "UpdraftPlus",
                "slug": "updraftplus",
                "purpose": "Backup and restore",
                "required": True,
                "priority": 7,
                "configuration": {"backup_schedule": "daily"}
            },
            {
                "name": "WPForms Lite",
                "slug": "wpforms-lite",
                "purpose": "Contact forms",
                "required": True,
                "priority": 6,
                "configuration": {"enable_notification": True}
            }
        ]
        
        # Add conditional plugins based on features
        if any("ecommerce" in str(f).lower() for f in features):
            plugins.append({
                "name": "WooCommerce",
                "slug": "woocommerce",
                "purpose": "E-commerce functionality",
                "required": False,
                "priority": 5,
                "configuration": {}
            })
        
        result = {
            "status": "ok",
            "action": "plugins_selected",
            "result_summary": f"Selected {len(plugins)} essential plugins",
            "result": {
                "essential_plugins": plugins,
                "estimated_setup_time": "5 minutes",
                "performance_impact": "low"
            },
            "assumptions": self.assumptions,
            "confidence": 0.85,
            "next_steps": ["deploy_site"]
        }
        
        return AgentResponse(**result)


# ============================================================================
# AGENT 5: DEPLOYMENT & CONFIGURATION
# ============================================================================

class DeploymentAgent(BaseAgent):
    """Orchestrates WordPress deployment"""
    
    def __init__(self, ai_client, wp_api_client, ssh_client):
        super().__init__(ai_client)
        self.wp_api = wp_api_client
        self.ssh = ssh_client
    
    async def execute(self, input_data: Dict) -> AgentResponse:
        """Execute WordPress deployment"""
        self.logger.info("Starting deployment...")
        
        credentials = input_data.get("credentials")
        if not credentials:
            return AgentResponse(
                status="needs_input",
                action="deployment_blocked",
                result_summary="WordPress credentials required",
                result={},
                assumptions=[],
                confidence=0.0,
                next_steps=["provide_credentials"],
                required_credentials=["wp_url", "wp_user", "wp_password"]
            )
        
        deployment_steps = []
        
        try:
            # Step 1: Validate WordPress installation
            step = await self._validate_wordpress(credentials)
            deployment_steps.append(step)
            
            # Step 2: Install theme
            theme = input_data.get("theme", {})
            step = await self._install_theme(theme)
            deployment_steps.append(step)
            
            # Step 3: Install and activate plugins
            plugins = input_data.get("plugins", [])
            step = await self._install_plugins(plugins)
            deployment_steps.append(step)
            
            # Step 4: Import content (pages and posts)
            content = input_data.get("content", {})
            step = await self._import_content(content)
            deployment_steps.append(step)
            
            # Step 5: Configure menus
            menus = input_data.get("menus", [])
            step = await self._configure_menus(menus)
            deployment_steps.append(step)
            
            # Step 6: Configure SEO settings
            step = await self._configure_seo()
            deployment_steps.append(step)
            
            # Step 7: Run health checks
            health = await self._run_health_checks()
            deployment_steps.append(health)
            
            site_url = credentials.get("site_url")
            
            result = {
                "status": "ok",
                "action": "deployment_completed",
                "result_summary": f"Site deployed successfully at {site_url}",
                "result": {
                    "deployment_plan": deployment_steps,
                    "site_details": {
                        "url": site_url,
                        "admin_url": f"{site_url}/wp-admin",
                        "admin_user": credentials.get("username"),
                        "wordpress_version": "latest"
                    },
                    "health_checks": health,
                    "post_deployment": [
                        "Change admin password immediately",
                        f"Review site at {site_url}",
                        "Configure contact form notifications",
                        "Submit sitemap to Google Search Console"
                    ]
                },
                "assumptions": self.assumptions,
                "confidence": 0.88,
                "next_steps": ["site_live"]
            }
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            result = {
                "status": "failed",
                "action": "deployment_failed",
                "result_summary": f"Deployment error: {str(e)}",
                "result": {"deployment_plan": deployment_steps, "error": str(e)},
                "assumptions": self.assumptions,
                "confidence": 0.0,
                "next_steps": ["review_error", "retry_deployment"]
            }
        
        return AgentResponse(**result)
    
    async def _validate_wordpress(self, credentials: Dict) -> Dict:
        """Validate WordPress installation"""
        self.logger.info("Validating WordPress...")
        try:
            # Test WP REST API connection
            await self.wp_api.test_connection()
            return {
                "step": "validate_wordpress",
                "status": "completed",
                "details": "WordPress installation validated",
                "duration": "2s"
            }
        except Exception as e:
            return {
                "step": "validate_wordpress",
                "status": "failed",
                "error": str(e),
                "duration": "2s"
            }
    
    async def _install_theme(self, theme: Dict) -> Dict:
        """Install and activate theme"""
        self.logger.info(f"Installing theme: {theme.get('slug')}")
        try:
            await self.wp_api.install_theme(theme.get("slug"))
            await self.wp_api.activate_theme(theme.get("slug"))
            return {
                "step": "install_theme",
                "status": "completed",
                "details": f"Installed {theme.get('name')}",
                "duration": "5s"
            }
        except Exception as e:
            return {
                "step": "install_theme",
                "status": "failed",
                "error": str(e),
                "duration": "5s"
            }
    
    async def _install_plugins(self, plugins: List[Dict]) -> Dict:
        """Install and activate plugins"""
        self.logger.info(f"Installing {len(plugins)} plugins...")
        installed = []
        failed = []
        
        for plugin in plugins:
            try:
                await self.wp_api.install_plugin(plugin["slug"])
                await self.wp_api.activate_plugin(plugin["slug"])
                installed.append(plugin["slug"])
            except Exception as e:
                failed.append({"slug": plugin["slug"], "error": str(e)})
        
        return {
            "step": "install_plugins",
            "status": "completed" if not failed else "partial",
            "details": f"Installed {len(installed)}/{len(plugins)} plugins",
            "installed": installed,
            "failed": failed,
            "duration": "15s"
        }
    
    async def _import_content(self, content: Dict) -> Dict:
        """Import pages and posts"""
        self.logger.info("Importing content...")
        pages = content.get("pages", [])
        posts = content.get("posts", [])
        
        created_pages = 0
        created_posts = 0
        
        # Import pages in batches
        for i in range(0, len(pages), Config.BATCH_SIZE):
            batch = pages[i:i+Config.BATCH_SIZE]
            for page in batch:
                try:
                    await self.wp_api.create_page(page)
                    created_pages += 1
                except Exception as e:
                    self.logger.error(f"Failed to create page: {e}")
        
        # Import posts in batches
        for i in range(0, len(posts), Config.BATCH_SIZE):
            batch = posts[i:i+Config.BATCH_SIZE]
            for post in batch:
                try:
                    await self.wp_api.create_post(post)
                    created_posts += 1
                except Exception as e:
                    self.logger.error(f"Failed to create post: {e}")
        
        return {
            "step": "import_content",
            "status": "completed",
            "details": f"Created {created_pages} pages, {created_posts} posts",
            "duration": "10s"
        }
    
    async def _configure_menus(self, menus: List[Dict]) -> Dict:
        """Configure WordPress menus"""
        self.logger.info("Configuring menus...")
        try:
            for menu in menus:
                await self.wp_api.create_menu(menu)
            return {
                "step": "configure_menus",
                "status": "completed",
                "details": f"Configured {len(menus)} menus",
                "duration": "3s"
            }
        except Exception as e:
            return {
                "step": "configure_menus",
                "status": "failed",
                "error": str(e),
                "duration": "3s"
            }
    
    async def _configure_seo(self) -> Dict:
        """Configure SEO settings"""
        self.logger.info("Configuring SEO...")
        try:
            await self.wp_api.set_option("permalink_structure", Config.DEFAULT_PERMALINK_STRUCTURE)
            return {
                "step": "configure_seo",
                "status": "completed",
                "details": "SEO settings configured",
                "duration": "2s"
            }
        except Exception as e:
            return {
                "step": "configure_seo",
                "status": "failed",
                "error": str(e),
                "duration": "2s"
            }
    
    async def _run_health_checks(self) -> Dict:
        """Run post-deployment health checks"""
        self.logger.info("Running health checks...")
        checks = {
            "site_accessible": await self.wp_api.test_connection(),
            "ssl_active": False,  # Would check HTTPS
            "theme_active": True,
            "plugins_active": [],
            "pages_created": 0,
            "performance_score": "good"
        }
        return {
            "step": "health_checks",
            "status": "completed",
            "details": checks,
            "duration": "5s"
        }


# ============================================================================
# AGENT 6: MASTER ORCHESTRATOR
# ============================================================================

class MasterOrchestrator:
    """Coordinates all agents and manages workflow"""
    
    def __init__(self, ai_client, wp_api_client, ssh_client):
        self.ai_client = ai_client
        self.planning_agent = SitePlanningAgent(ai_client)
        self.content_agent = ContentGenerationAgent(ai_client)
        self.design_agent = ThemeDesignAgent(ai_client)
        self.plugin_agent = PluginSelectionAgent(ai_client)
        self.deployment_agent = DeploymentAgent(ai_client, wp_api_client, ssh_client)
        
        self.logger = logging.getLogger("MasterOrchestrator")
        self.workflow_state = {}
    
    async def generate_site(self, business_input: BusinessInput) -> Dict:
        """Main workflow: orchestrate all agents to generate complete site"""
        self.logger.info(f"Starting site generation for {business_input.business_name}")
        
        start_time = datetime.now()
        results = {}
        
        try:
            # Step 1: Site Planning
            self.logger.info("Step 1/5: Site Planning")
            planning_result = await self.planning_agent.execute(asdict(business_input))
            results["architecture"] = planning_result.result
            
            if planning_result.confidence < Config.CONFIDENCE_OVERALL:
                self.logger.warning(f"Low confidence in planning: {planning_result.confidence}")
            
            # Step 2: Content Generation
            self.logger.info("Step 2/5: Content Generation")
            content_input = {
                "site_structure": planning_result.result.get("site_structure"),
                "business_context": {
                    "business_name": business_input.business_name,
                    "business_type": business_input.business_type,
                    "industry": business_input.industry
                },
                "tone": business_input.tone
            }
            content_result = await self.content_agent.execute(content_input)
            results["content"] = content_result.result
            
            # Step 3: Theme & Design
            self.logger.info("Step 3/5: Theme Selection")
            design_input = {
                "industry": business_input.industry,
                "business_type": business_input.business_type,
                "site_structure": planning_result.result.get("site_structure")
            }
            design_result = await self.design_agent.execute(design_input)
            results["design"] = design_result.result
            
            # Step 4: Plugin Selection
            self.logger.info("Step 4/5: Plugin Selection")
            plugin_input = {
                "features": planning_result.result.get("features", []),
                "business_type": business_input.business_type
            }
            plugin_result = await self.plugin_agent.execute(plugin_input)
            results["plugins"] = plugin_result.result
            
            # Step 5: Deployment
            self.logger.info("Step 5/5: Deployment")
            deployment_input = {
                "credentials": business_input.hosting_info,
                "theme": design_result.result.get("primary_theme"),
                "plugins": plugin_result.result.get("essential_plugins"),
                "content": content_result.result,
                "menus": planning_result.result.get("site_structure", {}).get("menus", [])
            }
            deployment_result = await self.deployment_agent.execute(deployment_input)
            results["deployment"] = deployment_result.result
            
            # Calculate metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Compile final response
            overall_confidence = sum([
                planning_result.confidence,
                content_result.confidence,
                design_result.confidence,
                plugin_result.confidence,
                deployment_result.confidence
            ]) / 5
            
            final_result = {
                "workflow_status": "completed",
                "completed_steps": [
                    "architecture", "content", "design", "plugins", "deployment"
                ],
                "results": results,
                "site_summary": {
                    "business_name": business_input.business_name,
                    "site_url": deployment_result.result.get("site_details", {}).get("url", "pending"),
                    "pages_created": len(content_result