"""
Enhanced Mock AI Client for ZipWP Testing
Returns realistic data structures for all agent types
"""

import json
import re


class EnhancedMockAIClient:
    """Enhanced mock AI client that returns realistic responses based on prompt type"""
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4"):
        self.api_key = api_key
        self.model = model
    
    async def generate(
        self, 
        prompt: str, 
        temperature: float = 0.1, 
        top_p: float = 0.8,
        max_tokens: int = 600
    ) -> str:
        """Generate contextual mock response based on prompt"""
        
        # Detect agent type from prompt
        if "site architecture" in prompt.lower():
            return self._generate_planning_response(prompt)
        elif "generate production-ready wordpress content" in prompt.lower():
            return self._generate_content_response(prompt)
        elif "blog posts" in prompt.lower():
            return self._generate_posts_response(prompt)
        else:
            # Default response
            return json.dumps({
                "status": "ok",
                "action": "generic_action",
                "result_summary": "Generic result",
                "result": {},
                "assumptions": [],
                "confidence": 0.85,
                "next_steps": []
            })
    
    def _extract_business_name(self, prompt: str) -> str:
        """Extract business name from prompt"""
        match = re.search(r"Business name:\s*(.+)", prompt)
        return match.group(1).strip() if match else "Business"
    
    def _generate_planning_response(self, prompt: str) -> str:
        """Generate site planning response"""
        business_name = self._extract_business_name(prompt)
        
        response = {
            "status": "ok",
            "action": "site_architecture_generated",
            "result_summary": f"Generated architecture for {business_name}",
            "result": {
                "site_structure": {
                    "pages": [
                        {
                            "title": "Home",
                            "slug": "home",
                            "purpose": "Welcome visitors and showcase key offerings",
                            "content_themes": ["hero_section", "services_overview", "testimonials", "cta"],
                            "priority": "high",
                            "template": "front-page"
                        },
                        {
                            "title": "About Us",
                            "slug": "about",
                            "purpose": "Tell the business story and build trust",
                            "content_themes": ["company_history", "team", "values", "mission"],
                            "priority": "high",
                            "template": "default"
                        },
                        {
                            "title": "Services",
                            "slug": "services",
                            "purpose": "Detail all services offered",
                            "content_themes": ["service_list", "pricing", "process"],
                            "priority": "high",
                            "template": "default"
                        },
                        {
                            "title": "Menu",
                            "slug": "menu",
                            "purpose": "Display food menu and pricing",
                            "content_themes": ["menu_items", "specials", "pricing"],
                            "priority": "high",
                            "template": "default"
                        },
                        {
                            "title": "Gallery",
                            "slug": "gallery",
                            "purpose": "Showcase photos",
                            "content_themes": ["photo_gallery"],
                            "priority": "medium",
                            "template": "default"
                        },
                        {
                            "title": "Contact",
                            "slug": "contact",
                            "purpose": "Provide contact information and form",
                            "content_themes": ["contact_form", "location_map", "hours"],
                            "priority": "high",
                            "template": "default"
                        },
                        {
                            "title": "Blog",
                            "slug": "blog",
                            "purpose": "Share news and updates",
                            "content_themes": ["blog_posts"],
                            "priority": "medium",
                            "template": "default"
                        }
                    ],
                    "menus": [
                        {
                            "location": "primary",
                            "name": "Main Menu",
                            "items": ["Home", "About Us", "Services", "Menu", "Gallery", "Contact", "Blog"]
                        }
                    ]
                },
                "features": [
                    {
                        "name": "Contact Form",
                        "priority": "high",
                        "implementation": "plugin"
                    },
                    {
                        "name": "Online Ordering",
                        "priority": "medium",
                        "implementation": "plugin"
                    },
                    {
                        "name": "Photo Gallery",
                        "priority": "medium",
                        "implementation": "theme"
                    }
                ],
                "plugins": [
                    {
                        "name": "Contact Form 7",
                        "slug": "contact-form-7",
                        "purpose": "Handle contact inquiries",
                        "required": True
                    },
                    {
                        "name": "Yoast SEO",
                        "slug": "wordpress-seo",
                        "purpose": "Search engine optimization",
                        "required": True
                    },
                    {
                        "name": "WP Super Cache",
                        "slug": "wp-super-cache",
                        "purpose": "Performance optimization",
                        "required": True
                    }
                ],
                "content_strategy": {
                    "post_types": ["posts"],
                    "initial_categories": ["News", "Updates", "Recipes"],
                    "suggested_posts": [
                        {
                            "title": "Welcome to Our Restaurant",
                            "theme": "introduction"
                        },
                        {
                            "title": "Our Story: Family Tradition Since 1985",
                            "theme": "history"
                        },
                        {
                            "title": "Fresh Ingredients, Authentic Taste",
                            "theme": "quality"
                        }
                    ]
                },
                "seo_foundation": {
                    "primary_keywords": ["pizza restaurant", "italian food", "brooklyn pizza"],
                    "site_tagline": "Authentic Italian Pizza Since 1985",
                    "meta_description_template": f"{business_name} - Your trusted local business"
                }
            },
            "assumptions": [],
            "confidence": 0.87,
            "next_steps": ["generate_content"]
        }
        
        return json.dumps(response)
    
    def _generate_content_response(self, prompt: str) -> str:
        """Generate page content response"""
        response = {
            "pages": [
                {
                    "title": "Home",
                    "slug": "home",
                    "content_html": "<h1>Welcome to Our Restaurant</h1><p>Experience authentic Italian cuisine...</p>",
                    "seo": {
                        "title": "Home - Authentic Italian Pizza",
                        "meta_description": "Family-owned pizza restaurant serving authentic Italian pizza since 1985",
                        "slug": "home",
                        "focus_keyword": "italian pizza"
                    }
                },
                {
                    "title": "About Us",
                    "slug": "about",
                    "content_html": "<h1>Our Story</h1><p>Since 1985, we've been serving Brooklyn...</p>",
                    "seo": {
                        "title": "About Us - Our Story",
                        "meta_description": "Learn about our family tradition of authentic Italian cooking",
                        "slug": "about",
                        "focus_keyword": "family restaurant"
                    }
                },
                {
                    "title": "Menu",
                    "slug": "menu",
                    "content_html": "<h1>Our Menu</h1><h2>Pizzas</h2><p>Margherita, Pepperoni, Quattro Formaggi...</p>",
                    "seo": {
                        "title": "Menu - Pizza & Italian Dishes",
                        "meta_description": "View our full menu of authentic Italian pizzas and dishes",
                        "slug": "menu",
                        "focus_keyword": "pizza menu"
                    }
                },
                {
                    "title": "Contact",
                    "slug": "contact",
                    "content_html": "<h1>Contact Us</h1><p>Visit us or get in touch...</p>",
                    "seo": {
                        "title": "Contact Us - Get In Touch",
                        "meta_description": "Contact us for reservations or inquiries",
                        "slug": "contact",
                        "focus_keyword": "contact"
                    }
                }
            ]
        }
        
        return json.dumps(response)
    
    def _generate_posts_response(self, prompt: str) -> str:
        """Generate blog posts response"""
        response = {
            "posts": [
                {
                    "title": "Welcome to Our Restaurant",
                    "slug": "welcome",
                    "content_html": "<p>We're excited to welcome you to our family restaurant...</p>",
                    "excerpt": "Welcome to our authentic Italian restaurant",
                    "categories": ["News"],
                    "tags": ["welcome", "announcement"]
                },
                {
                    "title": "Our Story: Family Tradition Since 1985",
                    "slug": "our-story",
                    "content_html": "<p>Our journey began in 1985 when...</p>",
                    "excerpt": "Learn about our family's journey",
                    "categories": ["News"],
                    "tags": ["history", "family"]
                },
                {
                    "title": "Fresh Ingredients, Authentic Taste",
                    "slug": "fresh-ingredients",
                    "content_html": "<p>We source only the finest ingredients...</p>",
                    "excerpt": "Quality ingredients make the difference",
                    "categories": ["Updates"],
                    "tags": ["quality", "ingredients"]
                }
            ]
        }
        
        return json.dumps(response)
