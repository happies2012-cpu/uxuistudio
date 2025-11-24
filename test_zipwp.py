"""
Test script for ZipWP Python Framework
Runs a simple site generation example
"""

import asyncio
import json
import sys
import os
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import framework
from zipwp_python_framework import GSWStudioPlatform, BusinessInput, AIClient, MockWordPressAPI, MockSSHClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ZipWPTest")


async def test_restaurant_site():
    """Test basic site generation without deployment"""
    
    print("=" * 60)
    print("ZipWP Platform - Test Run")
    print("=" * 60)
    print()
    
    # Initialize platform (using mock AI for now)
    platform = GSWStudioPlatform(ai_api_key="test-key-mock")
    
    print("✓ Platform initialized")
    print()
    
    # Test Case 1: Restaurant Website (No Deployment)
    print("Test Case: Restaurant Website")
    print("-" * 60)
    
    result = await platform.create_site(
        business_name="Joe's Pizza",
        business_type="restaurant",
        description="Family-owned pizza restaurant in Brooklyn serving authentic Italian pizza since 1985",
        hosting_info=None  # No deployment, just planning
    )
    
    print()
    print("RESULTS:")
    print("=" * 60)
    print(f"Status: {result['workflow_status']}")
    print(f"Completed Steps: {', '.join(result['completed_steps'])}")
    print()
    
    if 'site_summary' in result:
        summary = result['site_summary']
        print("Site Summary:")
        print(f"  • Business: {summary.get('business_name')}")
        print(f"  • Pages Created: {summary.get('pages_created')}")
        print(f"  • Posts Created: {summary.get('posts_created')}")
        print(f"  • Theme: {summary.get('theme')}")
        print(f"  • Plugins: {summary.get('plugins_count')}")
        print(f"  • Setup Time: {summary.get('estimated_setup_time')}")
        print()
    
    if 'quality_metrics' in result:
        metrics = result['quality_metrics']
        print("Quality Metrics:")
        print(f"  • Overall Confidence: {metrics.get('overall_confidence')}")
        print(f"  • Completeness: {metrics.get('completeness')}")
        print(f"  • Performance: {metrics.get('estimated_performance')}")
        print(f"  • SEO Readiness: {metrics.get('seo_readiness')}")
        print()
    
    # Save detailed results to file
    output_file = "zipwp_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✓ Detailed results saved to: {output_file}")
    print()
    
    # Display architecture details
    if 'results' in result and 'architecture' in result['results']:
        arch = result['results']['architecture']
        if 'site_structure' in arch:
            pages = arch['site_structure'].get('pages', [])
            print(f"Generated Pages ({len(pages)}):")
            for page in pages:
                print(f"  • {page.get('title')} - {page.get('purpose')}")
            print()
        
        if 'plugins' in arch:
            plugins = arch.get('plugins', [])
            print(f"Recommended Plugins ({len(plugins)}):")
            for plugin in plugins[:5]:  # Show first 5
                print(f"  • {plugin.get('name')} - {plugin.get('purpose')}")
            print()
    
    print("=" * 60)
    print("Test completed successfully! ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(test_site_generation())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
