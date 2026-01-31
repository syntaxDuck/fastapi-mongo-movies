# 🎯 Dynamic Test Runners

This project now includes **3 dynamic test runners** that automatically adapt to any user's directory structure!

## 🚀 Available Scripts

### 1. `run_universal_tests.py` ⭐ **RECOMMENDED**
- **Works from ANY directory** - automatically finds project root
- **Auto-discovers** all test suites  
- **Universal compatibility** - no hardcoded paths
- **Smart filtering** - run specific test categories

```bash
# Run from anywhere in the system!
python /path/to/project/run_universal_tests.py

# Run only specific tests
python /path/to/project/run_universal_tests.py api,backend

# Quick test without coverage
python /path/to/project/run_universal_tests.py --quick
```

### 2. `run_dynamic_tests.py` 
- **Auto-discovers** test directories
- **Individual coverage** per module
- **Pattern matching** for test discovery

```bash
# From within project
python run_dynamic_tests.py

# From anywhere (needs to be in project dir)
cd /path/to/project && python run_dynamic_tests.py
```

### 3. `run_comprehensive_tests.py` ⚠️ **LEGACY**
- **Fixed hardcoded paths** 
- **Static coverage targets**
- **Still functional** but less flexible

## 🔧 Features Comparison

| Feature | Universal | Dynamic | Comprehensive |
|---------|-----------|----------|----------------|
| **Auto-discovery** | ✅ | ✅ | ❌ |
| **Universal paths** | ✅ | ✅ | ❌ |
| **Pattern filtering** | ✅ | ✅ | ❌ |
| **Works from anywhere** | ✅ | ❌ | ❌ |
| **Coverage reports** | ✅ | ✅ | ✅ |

## 🎯 Best Practices

### ✅ **Universal Script** (Recommended)
```bash
# From ANY directory - auto-finds project root
python /path/to/fastapi-mongo-movies/run_universal_tests.py

# Only API tests
python /path/to/fastapi-mongo-movies/run_universal_tests.py api

# Quick test mode  
python /path/to/fastapi-mongo-movies/run_universal_tests.py --quick
```

### ✅ **Dynamic Script** (In-project)
```bash
# Must be run from project directory
cd /path/to/fastapi-mongo-movies
python run_dynamic_tests.py
```

## 🌟 Key Benefits

✅ **Universal Script** makes your test suite:
- **Directory-independent** - works from anywhere
- **Auto-project-root discovery** via pyproject.toml
- **Smart test filtering** by pattern
- **Zero configuration needed**
- **Team-friendly** - works for every developer

## 📊 Coverage Reports

All scripts generate:
- **HTML reports**: `htmlcov/index.html`
- **XML reports**: `coverage.xml`  
- **Terminal summaries**
- **Module-specific coverage**

---

**💡 Pro Tip**: Use `run_universal_tests.py` for the most flexible, universal testing experience!