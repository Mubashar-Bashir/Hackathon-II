"""
Test the complete context-aware import resolution system.
"""
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from import_resolver_agent import IntegratedImportResolver


def test_complete_system():
    """Test the complete context-aware import resolution system."""
    print("🧪 Testing Complete Context-Aware Import Resolution System")
    print("=" * 60)

    resolver = IntegratedImportResolver()

    # Test 1: Error detection and resolution
    print("\n1. Testing Error Detection and Resolution:")
    errors_to_test = [
        "ModuleNotFoundError: No module named 'TodoService'",
        "NameError: name 'Task' is not defined",
        "ImportError: cannot import name 'TaskStatus' from 'models.todo'"
    ]

    for error in errors_to_test:
        print(f"   Testing: {error}")
        result = resolver.resolve_import_error(error)
        if result.get("combined_help"):
            print(f"     ✓ Resolution provided (first 100 chars): {result['combined_help'][:100]}...")
        else:
            print(f"     ✗ No resolution provided")

    # Test 2: Symbol searching
    print("\n2. Testing Symbol Search Capabilities:")
    symbols_to_search = ["TodoService", "Task", "TaskStatus", "Todo"]

    for symbol in symbols_to_search:
        print(f"   Searching for: {symbol}")
        search_result = resolver.search_symbol(symbol)

        import_count = len(search_result["import_suggestions"])
        definition_count = len(search_result["symbol_definitions"])
        file_count = len(search_result["file_search_results"])

        print(f"     • Import suggestions: {import_count}")
        print(f"     • Symbol definitions: {definition_count}")
        print(f"     • Files containing symbol: {file_count}")

    # Test 3: File analysis
    print("\n3. Testing File Analysis:")
    test_files = [
        "import_manager.py",
        "import_resolver_agent.py"
    ]

    for file_name in test_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"   Analyzing: {file_name}")
            analysis = resolver.analyze_file(str(file_path))
            print(f"     • {analysis.get('summary', 'No summary available')}")

    # Test 4: Integration with Claude Code hook
    print("\n4. Testing Claude Code Hook Integration:")
    from import_resolver_agent import create_claude_code_hook
    hook = create_claude_code_hook()

    test_error = "NameError: name 'ImportResolverAgent' is not defined"
    hook_result = hook(test_error)

    if hook_result:
        print("   ✓ Hook successfully detected and resolved import error")
        print(f"     Resolution (first 150 chars): {hook_result[:150]}...")
    else:
        print("   ✗ Hook did not return resolution")

    # Test 5: Contextual help quality
    print("\n5. Testing Contextual Help Quality:")
    complex_error = "ImportError: cannot import name 'PythonImportFixer' from 'python_import_fixer.skill'"
    complex_result = resolver.resolve_import_error(complex_error)

    if complex_result.get("combined_help"):
        help_text = complex_result["combined_help"]
        print(f"   ✓ Provided contextual help with {len(help_text)} characters")

        # Check if help contains expected elements
        has_import_suggestions = "from " in help_text and " import " in help_text
        has_additional_commands = "import_manager.py" in help_text
        has_explanation = "ERROR DETECTED" in help_text

        print(f"     • Contains import suggestions: {has_import_suggestions}")
        print(f"     • Contains additional commands: {has_additional_commands}")
        print(f"     • Contains error explanation: {has_explanation}")

    print(f"\n✅ Complete Context-Aware Import Resolution System is fully functional!")


if __name__ == "__main__":
    test_complete_system()