"""
Test script to verify API fixes are working correctly
Run this from the backend directory: python test_api_fixes.py
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all modified API modules can be imported"""
    print("Testing API module imports...")
    
    try:
        from app.api import recommendations
        print("✅ recommendations.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import recommendations.py: {e}")
        return False
    
    try:
        from app.api import prediction
        print("✅ prediction.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import prediction.py: {e}")
        return False
    
    try:
        from app.api import chat
        print("✅ chat.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import chat.py: {e}")
        return False
    
    try:
        from app.api import medical
        print("✅ medical.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import medical.py: {e}")
        return False
    
    return True

def test_syntax():
    """Test Python syntax of all modified files"""
    print("\nTesting Python syntax...")
    
    files_to_test = [
        'backend/app/api/recommendations.py',
        'backend/app/api/prediction.py',
        'backend/app/api/chat.py',
        'backend/app/api/medical.py'
    ]
    
    all_valid = True
    for file_path in files_to_test:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                compile(f.read(), full_path, 'exec')
            print(f"✅ {file_path} - syntax valid")
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {file_path} - error: {e}")
            all_valid = False
    
    return all_valid

def main():
    print("=" * 60)
    print("API FIXES VERIFICATION TEST")
    print("=" * 60)
    
    syntax_ok = test_syntax()
    imports_ok = test_imports()
    
    print("\n" + "=" * 60)
    if syntax_ok and imports_ok:
        print("✅ ALL TESTS PASSED - API fixes are ready!")
        print("\nNext steps:")
        print("1. Start MongoDB: mongod")
        print("2. Start backend: cd backend && uvicorn app.main:app --reload")
        print("3. Start frontend: cd frontend && npm run dev")
        print("4. Test the fixed endpoints in your browser")
    else:
        print("❌ SOME TESTS FAILED - Please review the errors above")
    print("=" * 60)

if __name__ == "__main__":
    main()
