"""
Integration Test - Full Stack Test
Tests the complete flow: Frontend API → FastAPI → Python Backend
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any

# Configuration
# Configuration
FASTAPI_URL = "https://localhost:8000"
NEXTJS_API_URL = "http://localhost:3002/api"


async def test_fastapi_health():
    """Test FastAPI health endpoint"""
    print("=" * 60)
    print("TEST 1: FastAPI Health Check")
    print("=" * 60)
    
    # Use ssl=False for self-signed certificates
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(f"{FASTAPI_URL}/health") as resp:
            if resp.status == 200:
                data = await resp.json()
                print("✅ FastAPI is healthy")
                print(f"   Status: {data['status']}")
                print(f"   AI Mode: {data['ai_mode']}")
                print(f"   Timestamp: {data['timestamp']}")
                print(f"   SSL Enabled: {data.get('ssl_enabled', False)}")
                return True
            else:
                print(f"❌ FastAPI health check failed: {resp.status}")
                return False


async def test_site_generation():
    """Test site generation via FastAPI"""
    print("\n" + "=" * 60)
    print("TEST 2: Site Generation (FastAPI Direct)")
    print("=" * 60)
    
    request_data = {
        "business_name": "Sunset Dental Care",
        "business_type": "dental",
        "description": "Modern dental practice in Los Angeles",
        "deploy": False
    }
    
    print(f"\nRequest: {json.dumps(request_data, indent=2)}")
    
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Start generation
        async with session.post(
            f"{FASTAPI_URL}/api/v1/sites/generate",
            json=request_data
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                job_id = data['job_id']
                print(f"\n✅ Job created: {job_id}")
                print(f"   Status: {data['status']}")
                print(f"   Message: {data['message']}")
                
                # Poll for completion
                print("\n⏳ Polling for completion...")
                return await poll_job_status(session, job_id)
            else:
                error = await resp.text()
                print(f"❌ Failed to create job: {resp.status}")
                print(f"   Error: {error}")
                return False


async def poll_job_status(session: aiohttp.ClientSession, job_id: str, max_attempts: int = 30) -> bool:
    """Poll job status until completion"""
    for attempt in range(max_attempts):
        await asyncio.sleep(1)  # Wait 1 second between polls
        
        async with session.get(f"{FASTAPI_URL}/api/v1/jobs/{job_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                status = data['status']
                progress = data['progress']
                message = data['message']
                
                print(f"   [{attempt + 1}/{max_attempts}] Status: {status} | Progress: {progress}% | {message}")
                
                if status == "completed":
                    print("\n✅ Site generation completed!")
                    result = data.get('result', {})
                    
                    # Display summary
                    if 'site_summary' in result:
                        summary = result['site_summary']
                        print("\n📊 Site Summary:")
                        print(f"   • Business: {summary.get('business_name')}")
                        print(f"   • Pages: {summary.get('pages_created')}")
                        print(f"   • Posts: {summary.get('posts_created')}")
                        print(f"   • Theme: {summary.get('theme')}")
                        print(f"   • Plugins: {summary.get('plugins_count')}")
                    
                    if 'quality_metrics' in result:
                        metrics = result['quality_metrics']
                        print("\n📈 Quality Metrics:")
                        print(f"   • Confidence: {metrics.get('overall_confidence')}")
                        print(f"   • Completeness: {metrics.get('completeness')}")
                        print(f"   • Performance: {metrics.get('estimated_performance')}")
                    
                    return True
                    
                elif status == "failed":
                    print(f"\n❌ Job failed: {message}")
                    return False
            else:
                print(f"   ❌ Failed to get status: {resp.status}")
                return False
    
    print(f"\n⏱️ Timeout: Job did not complete in {max_attempts} seconds")
    return False


async def test_nextjs_api():
    """Test Next.js API route (if available)"""
    print("\n" + "=" * 60)
    print("TEST 3: Next.js API Route")
    print("=" * 60)
    
    try:
        # Next.js is HTTP, so no SSL context needed, but we can reuse the connector or create new session
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NEXTJS_API_URL}/generate-site") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print("✅ Next.js API route is accessible")
                    print(f"   Message: {data.get('message')}")
                    print(f"   Backend: {data.get('pythonBackend')}")
                    return True
                else:
                    print(f"⚠️  Next.js API route returned: {resp.status}")
                    return False
    except Exception as e:
        print(f"⚠️  Next.js API not accessible (may not be running): {e}")
        return False


async def test_list_jobs():
    """Test listing all jobs"""
    print("\n" + "=" * 60)
    print("TEST 4: List All Jobs")
    print("=" * 60)
    
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(f"{FASTAPI_URL}/api/v1/jobs") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Found {data['total']} jobs")
                
                if data['jobs']:
                    print("\n📋 Recent Jobs:")
                    for job in data['jobs'][:5]:  # Show first 5
                        print(f"   • {job['job_id'][:8]}... | {job['status']} | {job['progress']}%")
                
                return True
            else:
                print(f"❌ Failed to list jobs: {resp.status}")
                return False


async def run_all_tests():
    """Run all integration tests"""
    print("\n" + "🚀" * 30)
    print("gsWstudio.ai Platform - Full Integration Test")
    print("🚀" * 30 + "\n")
    
    start_time = time.time()
    
    results = {
        "health_check": await test_fastapi_health(),
        "site_generation": await test_site_generation(),
        "nextjs_api": await test_nextjs_api(),
        "list_jobs": await test_list_jobs()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    print(f"Duration: {time.time() - start_time:.1f} seconds")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
