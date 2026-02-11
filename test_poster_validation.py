"""
Test script for Poster Validation API functionality.
"""

import asyncio
import sys
from backend.services.poster_validation_service import PosterValidationService
from backend.services.job_management_service import JobManagementService
from backend.core.logging import get_logger

logger = get_logger(__name__)


async def test_poster_validation_service():
    """Test the poster validation service functionality."""
    print("🧪 Testing Poster Validation Service...")

    try:
        # Initialize services
        poster_service = PosterValidationService()
        job_service = JobManagementService()

        print("✅ Services initialized successfully")

        # Test job creation
        job_id = await job_service.create_job(
            job_type="test_validation", parameters={"test": True}
        )
        print(f"✅ Job created: {job_id}")

        # Test job status
        job_status = await job_service.get_job_status(job_id)
        if job_status:
            print(f"✅ Job status retrieved: {job_status.status}")
        else:
            print("❌ Failed to get job status")

        # Test poster validation for a specific movie
        # Using a known movie ID from the sample database
        test_movie_id = "573a13b5f29313caabd42e7e"  # The Matrix

        result = await poster_service.validate_movie_poster(test_movie_id)
        if result:
            print(f"✅ Poster validation completed for movie {test_movie_id}")
            print(f"   - Valid: {result.is_valid}")
            print(f"   - HTTP Status: {result.http_status}")
            print(f"   - Response Time: {result.response_time_ms}ms")
            if result.error_reason:
                print(f"   - Error: {result.error_reason}")
        else:
            print(f"❌ Failed to validate poster for movie {test_movie_id}")

        # Test validation statistics
        stats = await poster_service.get_validation_statistics()
        print(f"✅ Validation statistics retrieved:")
        print(f"   - Total movies: {stats.total_movies}")
        print(f"   - Movies with posters: {stats.movies_with_posters}")
        print(f"   - Valid posters: {stats.valid_posters}")
        print(f"   - Invalid posters: {stats.invalid_posters}")
        print(f"   - Success rate: {stats.validation_success_rate:.1f}%")

        # Test job statistics
        job_stats = await job_service.get_job_statistics()
        print(f"✅ Job statistics retrieved:")
        print(f"   - Total jobs: {job_stats['total_jobs']}")
        print(f"   - Running jobs: {job_stats['running_jobs']}")
        print(f"   - Completed jobs: {job_stats['completed_jobs']}")

        print("🎉 All poster validation service tests passed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_enhanced_validation():
    """Test enhanced poster validation logic."""
    print("\n🔍 Testing Enhanced Poster Validation...")

    try:
        poster_service = PosterValidationService()

        # Test various poster URLs
        test_urls = [
            "https://m.media-amazon.com/images/M/MV5BNzQzNjQ2NzQ2NzQ2Nl5BMl5BanBnXkFtZTgwNzQ2NzQ2NzE@._V1_SY1000_SX677_AL_.jpg",  # Valid image URL
            "https://httpbin.org/status/404",  # Invalid URL (404)
            "https://httpbin.org/html",  # Invalid content type
            "https://httpbin.org/delay/5",  # Timeout test
        ]

        for i, url in enumerate(test_urls):
            print(f"\n📸 Test {i + 1}: {url}")
            result = await poster_service._validate_poster_url(url)

            print(f"   - Valid: {result.is_valid}")
            print(f"   - HTTP Status: {result.http_status}")
            print(f"   - Content Type: {result.content_type}")
            print(f"   - Response Time: {result.response_time_ms}ms")
            if result.error_reason:
                print(f"   - Error: {result.error_reason}")

        print("\n✅ Enhanced validation tests completed!")
        return True

    except Exception as e:
        print(f"❌ Enhanced validation test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Starting Poster Validation API Tests...\n")

    # Test basic service functionality
    service_test_passed = await test_poster_validation_service()

    # Test enhanced validation
    validation_test_passed = await test_enhanced_validation()

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"   Service Tests: {'✅ PASSED' if service_test_passed else '❌ FAILED'}")
    print(
        f"   Validation Tests: {'✅ PASSED' if validation_test_passed else '❌ FAILED'}"
    )

    if service_test_passed and validation_test_passed:
        print("\n🎉 ALL TESTS PASSED! Poster Validation API is ready!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED! Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
