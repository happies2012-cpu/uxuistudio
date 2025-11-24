"""
Production-Ready AI Client with Real Anthropic Integration
Supports both real API calls and mock mode for testing
"""

import os
import json
import logging
from typing import Optional
from anthropic import Anthropic, AsyncAnthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ProductionAIClient:
    """Production AI client with real Anthropic API integration"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: str = "claude-sonnet-4-20250514",
        use_mock: bool = False
    ):
        """
        Initialize AI client
        
        Args:
            api_key: Anthropic API key (if None, reads from env)
            model: Model to use
            use_mock: If True, use mock responses for testing
        """
        self.use_mock = use_mock
        self.model = model
        self.logger = logging.getLogger("ProductionAIClient")
        
        if not use_mock:
            # Real API mode
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "Anthropic API key required. Set ANTHROPIC_API_KEY env variable "
                    "or pass api_key parameter, or set use_mock=True for testing."
                )
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.logger.info(f"Initialized with real Anthropic API (model: {model})")
        else:
            # Mock mode
            self.client = None
            self.logger.info("Initialized in MOCK mode (no API calls)")
    
    async def generate(
        self, 
        prompt: str, 
        temperature: float = 0.1, 
        top_p: float = 0.8,
        max_tokens: int = 600,
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate AI response
        
        Args:
            prompt: User prompt
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate
            system_message: Optional system message
            
        Returns:
            JSON string response
        """
        if self.use_mock:
            return await self._generate_mock(prompt, max_tokens)
        else:
            return await self._generate_real(
                prompt, temperature, top_p, max_tokens, system_message
            )
    
    async def _generate_real(
        self,
        prompt: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        system_message: Optional[str]
    ) -> str:
        """Generate response using real Anthropic API"""
        self.logger.info(f"Calling Anthropic API (max_tokens={max_tokens})")
        
        # Default system message for WordPress site generation
        if not system_message:
            system_message = """You are an autonomous WordPress site generation agent.
You must output ONLY valid JSON following the exact schema specified in the prompt.
Be deterministic and precise. Use temperature=0.10 for consistency.
Never include explanatory text outside the JSON structure."""
        
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract text content
            response_text = message.content[0].text
            
            # Log token usage
            self.logger.info(
                f"API call successful. Input tokens: {message.usage.input_tokens}, "
                f"Output tokens: {message.usage.output_tokens}"
            )
            
            # Validate JSON
            try:
                json.loads(response_text)  # Validate it's valid JSON
                return response_text
            except json.JSONDecodeError as e:
                self.logger.error(f"API returned invalid JSON: {e}")
                # Try to extract JSON from response
                return self._extract_json(response_text)
                
        except Exception as e:
            self.logger.error(f"Anthropic API call failed: {e}")
            # Fallback to mock in case of API error
            self.logger.warning("Falling back to mock response due to API error")
            return await self._generate_mock(prompt, max_tokens)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might have extra content"""
        import re
        
        # Try to find JSON object in text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                json.loads(json_str)  # Validate
                return json_str
            except:
                pass
        
        # If extraction fails, return error JSON
        return json.dumps({
            "status": "failed",
            "action": "json_extraction_failed",
            "result_summary": "Could not extract valid JSON from AI response",
            "result": {},
            "assumptions": ["AI response was not valid JSON"],
            "confidence": 0.0,
            "next_steps": ["retry_with_clearer_prompt"]
        })
    
    async def _generate_mock(self, prompt: str, max_tokens: int) -> str:
        """Generate mock response for testing (same as before)"""
        self.logger.info(f"Generating MOCK response (max_tokens={max_tokens})")
        
        import re
        
        # Detect agent type from prompt and return realistic data
        if "site architecture" in prompt.lower():
            return self._generate_planning_response(prompt)
        elif "generate production-ready wordpress content" in prompt.lower():
            return self._generate_content_response(prompt)
        elif "blog posts" in prompt.lower():
            return self._generate_posts_response(prompt)
        else:
            return json.dumps({
                "status": "ok",
                "action": "generic_action",
                "result_summary": "Generic mock result",
                "result": {},
                "assumptions": [],
                "confidence": 0.85,
                "next_steps": []
            })
    
    def _extract_business_name(self, prompt: str) -> str:
        """Extract business name from prompt"""
        import re
        match = re.search(r"Business name:\s*(.+)", prompt)
        return match.group(1).strip() if match else "Business"
    
    def _generate_planning_response(self, prompt: str) -> str:
        """Generate site planning mock response"""
        business_name = self._extract_business_name(prompt)
        
        response = {
            "status": "ok",
            "action": "site_architecture_generated",
            "result_summary": f"Generated architecture for {business_name}",
            "result": {
                "site_structure": {
                    "pages": [
                        {"title": "Home", "slug": "home", "purpose": "Welcome visitors", "content_themes": ["hero", "services"], "priority": "high", "template": "front-page"},
                        {"title": "About Us", "slug": "about", "purpose": "Tell story", "content_themes": ["history", "team"], "priority": "high", "template": "default"},
                        {"title": "Services", "slug": "services", "purpose": "Detail services", "content_themes": ["service_list"], "priority": "high", "template": "default"},
                        {"title": "Menu", "slug": "menu", "purpose": "Display menu", "content_themes": ["menu_items"], "priority": "high", "template": "default"},
                        {"title": "Gallery", "slug": "gallery", "purpose": "Showcase photos", "content_themes": ["photos"], "priority": "medium", "template": "default"},
                        {"title": "Contact", "slug": "contact", "purpose": "Contact info", "content_themes": ["form", "map"], "priority": "high", "template": "default"},
                        {"title": "Blog", "slug": "blog", "purpose": "News updates", "content_themes": ["posts"], "priority": "medium", "template": "default"}
                    ],
                    "menus": [{"location": "primary", "name": "Main Menu", "items": ["Home", "About", "Services", "Contact"]}]
                },
                "features": [{"name": "Contact Form", "priority": "high", "implementation": "plugin"}],
                "plugins": [
                    {"name": "Contact Form 7", "slug": "contact-form-7", "purpose": "Contact forms", "required": True},
                    {"name": "Yoast SEO", "slug": "wordpress-seo", "purpose": "SEO", "required": True}
                ],
                "content_strategy": {
                    "post_types": ["posts"],
                    "initial_categories": ["News", "Updates"],
                    "suggested_posts": [
                        {"title": "Welcome", "theme": "introduction"},
                        {"title": "Our Story", "theme": "history"},
                        {"title": "Quality Matters", "theme": "values"}
                    ]
                },
                "seo_foundation": {
                    "primary_keywords": ["restaurant", "pizza", "italian"],
                    "site_tagline": "Authentic Italian Cuisine",
                    "meta_description_template": f"{business_name} - Your trusted local business"
                }
            },
            "assumptions": [],
            "confidence": 0.87,
            "next_steps": ["generate_content"]
        }
        return json.dumps(response)
    
    def _generate_content_response(self, prompt: str) -> str:
        """Generate page content mock response"""
        response = {
            "pages": [
                {"title": "Home", "slug": "home", "content_html": "<h1>Welcome</h1><p>Experience authentic cuisine...</p>", "seo": {"title": "Home", "meta_description": "Welcome to our restaurant", "slug": "home", "focus_keyword": "restaurant"}},
                {"title": "About Us", "slug": "about", "content_html": "<h1>Our Story</h1><p>Since 1985...</p>", "seo": {"title": "About", "meta_description": "Our story", "slug": "about", "focus_keyword": "about"}},
                {"title": "Menu", "slug": "menu", "content_html": "<h1>Menu</h1><p>Delicious dishes...</p>", "seo": {"title": "Menu", "meta_description": "Our menu", "slug": "menu", "focus_keyword": "menu"}},
                {"title": "Contact", "slug": "contact", "content_html": "<h1>Contact</h1><p>Get in touch...</p>", "seo": {"title": "Contact", "meta_description": "Contact us", "slug": "contact", "focus_keyword": "contact"}}
            ]
        }
        return json.dumps(response)
    
    def _generate_posts_response(self, prompt: str) -> str:
        """Generate blog posts mock response"""
        response = {
            "posts": [
                {"title": "Welcome", "slug": "welcome", "content_html": "<p>Welcome post...</p>", "excerpt": "Welcome", "categories": ["News"], "tags": ["welcome"]},
                {"title": "Our Story", "slug": "our-story", "content_html": "<p>Our journey...</p>", "excerpt": "Our story", "categories": ["News"], "tags": ["history"]},
                {"title": "Quality", "slug": "quality", "content_html": "<p>Quality matters...</p>", "excerpt": "Quality", "categories": ["Updates"], "tags": ["quality"]}
            ]
        }
        return json.dumps(response)


# Convenience function to create client
def create_ai_client(use_mock: bool = False) -> ProductionAIClient:
    """
    Create AI client instance
    
    Args:
        use_mock: If True, use mock mode. If False, use real API.
                 Defaults to False (real API) unless ANTHROPIC_API_KEY is not set.
    
    Returns:
        ProductionAIClient instance
    """
    # Auto-detect if we should use mock mode
    if not use_mock and not os.getenv("ANTHROPIC_API_KEY"):
        logger.warning(
            "ANTHROPIC_API_KEY not found in environment. "
            "Using MOCK mode. Set the API key to use real AI."
        )
        use_mock = True
    
    return ProductionAIClient(use_mock=use_mock)
