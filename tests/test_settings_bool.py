from backend.core.config import settings
import os

print(f"Default ENABLE_DOCS: {settings.ENABLE_DOCS} ({type(settings.ENABLE_DOCS)})")

# Test with environment variable
os.environ["ENABLE_DOCS"] = "false"
# Note: Pydantic settings are usually instantiated once.
# To test change, we might need to re-instantiate or just trust Pydantic.
from backend.core.config import Settings
new_settings = Settings()
print(f"ENABLE_DOCS with env=false: {new_settings.ENABLE_DOCS} ({type(new_settings.ENABLE_DOCS)})")
