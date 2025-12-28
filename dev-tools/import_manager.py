"""
Import Management CLI
A unified tool that combines import fixing and registry functionality
for better Python import resolution in development workflows.
"""

import sys
import os
from pathlib import Path
import json
from typing import List, Dict, Optional

# Add the skills directory to the path to import the skills
sys.path.insert(0, str(Path(__file__).parent / ".claude" / "skills"))

from import_registry.skill import ImportRegistrySkill
from python_import_fixer.skill import PythonImportFixer


class ImportManagementCLI:
    """
    A unified CLI for import management that combines both skills.
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.registry = ImportRegistrySkill(self.project_root)
        self.import_fixer = PythonImportFixer(self.project_root)

    def full_analysis(self) -> Dict:
        """
        Perform a full analysis using both tools.
        """
        print("🔍 Running comprehensive import analysis...")

        result = {
            "registry_analysis": {},
            "import_fixer_analysis": {},
            "recommendations": []
        }

        # Run import fixer analysis
        print("  - Scanning for import issues...")
        issues = self.import_fixer.scan_for_import_issues()
        result["import_fixer_analysis"]["issues"] = issues

        # Run registry analysis
        print("  - Building import registry...")
        symbols = self.registry.build_registry()
        result["registry_analysis"]["symbols_count"] = len(symbols)

        # Provide recommendations
        if issues:
            result["recommendations"].append("Run import_fixer to resolve detected issues")

        if len(symbols) > 50:  # Large project
            result["recommendations"].append("Use import registry for quick symbol lookups")

        print(f"  - Found {len(issues)} import issues")
        print(f"  - Registry contains {len(symbols)} symbols")

        return result

    def find_symbol(self, symbol_name: str) -> str:
        """
        Find import paths for a symbol using the registry.
        """
        imports = self.registry.find_import_path(symbol_name)
        if imports:
            return f"✅ Found import paths for '{symbol_name}':\n" + "\n".join(f"  {imp}" for imp in imports)
        else:
            return f"❌ No import paths found for '{symbol_name}'"

    def fix_imports(self) -> str:
        """
        Fix import issues using the import fixer.
        """
        print("🔧 Running import fixer...")

        # Create package structure
        pkg_result = self.import_fixer.create_package_structure()

        # Fix relative imports
        import_changes = self.import_fixer.fix_relative_imports()

        # Check environment variables
        env_issues = self.import_fixer.check_environment_variables()
        if env_issues:
            env_changes = self.import_fixer.fix_environment_variables()
        else:
            env_changes = {"fixed_vars": []}

        # Integrate with registry
        registry_integration = self.import_fixer.integrate_with_registry()

        summary = f"""✅ Import fixing completed!
  - Created {len(pkg_result['created_files'])} package files
  - Converted {len(import_changes['converted_imports'])} imports
  - Fixed {len(env_changes['fixed_vars'])} environment variables"""

        return summary

    def suggest_imports(self, partial_name: str) -> str:
        """
        Suggest imports based on partial name matching.
        """
        suggestions = self.registry.suggest_import(partial_name)
        if suggestions:
            suggestions = suggestions[:10]  # Limit to 10
            return f"💡 Suggested imports for '{partial_name}' (showing first 10):\n" + "\n".join(f"  {sug}" for sug in suggestions)
        else:
            return f"❌ No suggestions found for '{partial_name}'"


def main():
    """
    Main function to run the Import Management CLI.
    """
    if len(sys.argv) < 2:
        print("""📖 Import Management CLI Usage:
  import_manager analyze          - Full import analysis
  import_manager find <symbol>    - Find import paths for a symbol
  import_manager fix             - Fix import issues
  import_manager suggest <text>   - Suggest imports matching text
  import_manager help            - Show this help

Examples:
  import_manager find TodoService
  import_manager analyze
  import_manager fix
""")
        return

    command = sys.argv[1]
    cli = ImportManagementCLI(".")

    if command == "analyze":
        result = cli.full_analysis()
        print(f"\n📋 Analysis complete!")
        print(f"   Registry contains {result['registry_analysis']['symbols_count']} symbols")
        print(f"   Found {len(result['import_fixer_analysis']['issues'])} import issues")
        if result['recommendations']:
            print("   Recommendations:")
            for rec in result['recommendations']:
                print(f"     • {rec}")

    elif command == "find" and len(sys.argv) > 2:
        symbol = sys.argv[2]
        result = cli.find_symbol(symbol)
        print(result)

    elif command == "fix":
        result = cli.fix_imports()
        print(result)

    elif command == "suggest" and len(sys.argv) > 2:
        partial = sys.argv[2]
        result = cli.suggest_imports(partial)
        print(result)

    elif command == "help":
        print("""📖 Import Management CLI Usage:
  import_manager analyze          - Full import analysis
  import_manager find <symbol>    - Find import paths for a symbol
  import_manager fix             - Fix import issues
  import_manager suggest <text>   - Suggest imports matching text
  import_manager help            - Show this help

Examples:
  import_manager find TodoService
  import_manager analyze
  import_manager fix
""")

    else:
        print("❌ Invalid command. Use 'import_manager help' for usage information.")


if __name__ == "__main__":
    main()