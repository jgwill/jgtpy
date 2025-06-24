"""CLI to display small documentation snippets for LLM agents.

The ``guidecli_jgtpy`` entry point prints pieces of guidance embedded in
the package. Use ``guidecli_jgtpy --help`` for options.
"""

import argparse
import importlib.resources as pkg_resources
import os
import sys
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

PACKAGE = 'jgtpy'
DOC_PATH = 'guide_for_llm_agents'

def _doc_dir():
    return pkg_resources.files(PACKAGE) / DOC_PATH

def _ensure_scripts_available():
    """Ensure scripts are available in the package directory"""
    package_dir = pkg_resources.files(PACKAGE)
    scripts_dir = package_dir / "scripts"
    
    # Create scripts directory if it doesn't exist
    if not scripts_dir.exists():
        scripts_dir.mkdir(exist_ok=True)
    
    # Copy scripts from root directory if they don't exist in package
    root_dir = package_dir.parent
    scripts_copied = []
    
    for script_file in root_dir.glob("*.sh"):
        target_file = scripts_dir / script_file.name
        if not target_file.exists():
            try:
                import shutil
                shutil.copy2(script_file, target_file)
                scripts_copied.append(script_file.name)
            except Exception as e:
                print(f"Warning: Could not copy {script_file.name}: {e}")
    
    return scripts_dir

def _scripts_dir():
    """Get the directory containing bash scripts"""
    # Try to ensure scripts are available in package directory
    try:
        return _ensure_scripts_available()
    except Exception:
        pass
    
    # Fallback: Try multiple locations where scripts might be found
    
    # 1. Try package data files (when installed)
    try:
        import pkg_resources
        scripts_dir = pkg_resources.resource_filename(PACKAGE, '')
        if Path(scripts_dir).exists():
            return scripts_dir
    except Exception:
        pass
    
    # 2. Try package root directory (development)
    try:
        package_root = pkg_resources.files(PACKAGE).parent
        if Path(package_root).exists():
            return package_root
    except Exception:
        pass
    
    # 3. Try current working directory
    cwd = Path.cwd()
    if cwd.exists():
        return cwd
    
    # 4. Fallback to package directory
    return pkg_resources.files(PACKAGE)

def list_sections():
    return [p.stem for p in _doc_dir().iterdir() if p.suffix == '.md']

def read_section(name: str) -> str:
    path = _doc_dir() / f"{name}.md"
    if path.is_file():
        return path.read_text()
    raise FileNotFoundError(f"Section {name} not found")

def list_scripts():
    """List available bash scripts in the package"""
    scripts = []
    scripts_dir = _scripts_dir()
    
    try:
        for file in scripts_dir.iterdir():
            if file.suffix == '.sh' and file.is_file():
                scripts.append(file.name)
    except Exception as e:
        print(f"Warning: Could not access scripts directory: {e}")
    
    if not scripts:
        print("No scripts found. This might be because:")
        print("1. The package was installed without scripts")
        print("2. You're not in the development directory")
        print("3. Scripts are not properly included in the package")
        print("\nTry running from the package root directory or reinstall the package.")
    
    return sorted(scripts)

def read_script(name: str) -> str:
    """Read a bash script from the package"""
    scripts_dir = _scripts_dir()
    path = scripts_dir / name
    
    try:
        if path.is_file():
            return path.read_text()
        else:
            raise FileNotFoundError(f"Script {name} not found in {scripts_dir}")
    except Exception as e:
        raise FileNotFoundError(f"Could not read script {name}: {e}")

def show_script_examples():
    """Show examples of how to use the bash scripts"""
    examples = """
# JGT Service Script Examples

## Quick Setup
```bash
# First time setup with full dependencies
./setup-service.sh --full

# Quick setup with defaults
./setup-service.sh --quick
```

## Data Refresh
```bash
# Refresh all data (excludes m1 by default)
./refresh-all.sh

# Refresh specific timeframes and instruments
./refresh-all.sh "H1,H4,D1" "EUR/USD,XAU/USD"

# Refresh with verbose output
./refresh-all.sh "H1" "EUR/USD" --verbose
```

## Service Management
```bash
# Start API server
./start-api-server.sh

# Start continuous daemon
./start-daemon.sh

# Check system status
./check-status.sh --verbose

# Check API endpoints
./check-status.sh --web
```

## Complete Workflow
```bash
# 1. Setup environment
./setup-service.sh --full

# 2. Check everything is working
./check-status.sh --verbose

# 3. Refresh data
./refresh-all.sh "H1,H4" "EUR/USD,XAU/USD"

# 4. Start API server
./start-api-server.sh

# 5. Access data via API
curl http://localhost:8080/api/v1/data/EUR/USD/H1
```
"""
    return examples

def install_scripts(target_dir: str = None, overwrite: bool = False):
    """Install bash scripts to target directory"""
    if target_dir is None:
        target_dir = os.getcwd()
    
    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
    
    installed = []
    failed = []
    
    for script_name in list_scripts():
        source_path = _scripts_dir() / script_name
        target_file = target_path / script_name
        
        if target_file.exists() and not overwrite:
            failed.append(f"{script_name} (already exists, use --overwrite)")
            continue
            
        try:
            shutil.copy2(source_path, target_file)
            # Make executable
            target_file.chmod(0o755)
            installed.append(script_name)
        except Exception as e:
            failed.append(f"{script_name} (error: {e})")
    
    return installed, failed

def show_script_content(script_name: str):
    """Show the content of a specific script"""
    try:
        content = read_script(script_name)
        return f"# Content of {script_name}\n\n```bash\n{content}\n```"
    except FileNotFoundError:
        return f"Script {script_name} not found"

def main():
    parser = argparse.ArgumentParser(description="JGTPY documentation for LLM agents")
    parser.add_argument('--list', action='store_true', help='List available sections')
    parser.add_argument('--section', help='Display a specific section')
    parser.add_argument('--all', action='store_true', help='Display all sections')
    
    # Script-related options
    parser.add_argument('--scripts', action='store_true', help='List available bash scripts')
    parser.add_argument('--script', help='Show content of a specific script')
    parser.add_argument('--examples', action='store_true', help='Show script usage examples')
    parser.add_argument('--install-scripts', help='Install scripts to specified directory (or current if not specified)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files when installing scripts')
    
    args = parser.parse_args()

    if args.list:
        print("Available documentation sections:")
        for sec in list_sections():
            print(f"  {sec}")
        return

    if args.scripts:
        print("Available bash scripts:")
        for script in list_scripts():
            print(f"  {script}")
        return

    if args.examples:
        print(show_script_examples())
        return

    if args.script:
        print(show_script_content(args.script))
        return

    if args.install_scripts:
        target_dir = args.install_scripts if args.install_scripts != "current" else None
        installed, failed = install_scripts(target_dir, args.overwrite)
        
        print("Script installation results:")
        if installed:
            print("\n✅ Installed scripts:")
            for script in installed:
                print(f"  {script}")
        
        if failed:
            print("\n❌ Failed to install:")
            for script in failed:
                print(f"  {script}")
        
        if installed:
            print(f"\n📁 Scripts installed to: {target_dir or os.getcwd()}")
            print("🔧 Make sure to configure your environment before using the scripts.")
        return

    if args.all:
        for sec in list_sections():
            print(f"# {sec}\n")
            print(read_section(sec))
            print()
        return

    if args.section:
        print(read_section(args.section))
        return

    # Default help
    print("JGTPY Guide System for LLM Agents")
    print("==================================")
    print()
    print("Documentation Commands:")
    print("  --list                    List available documentation sections")
    print("  --section <name>          Display specific documentation section")
    print("  --all                     Display all documentation sections")
    print()
    print("Script Commands:")
    print("  --scripts                 List available bash scripts")
    print("  --script <name>           Show content of specific script")
    print("  --examples                Show script usage examples")
    print("  --install-scripts [dir]   Install scripts to directory (or current)")
    print("  --overwrite               Overwrite existing files when installing")
    print()
    print("Examples:")
    print("  guidecli_jgtpy --section jgtservice")
    print("  guidecli_jgtpy --scripts")
    print("  guidecli_jgtpy --script refresh-all.sh")
    print("  guidecli_jgtpy --examples")
    print("  guidecli_jgtpy --install-scripts")
    print("  guidecli_jgtpy --install-scripts /path/to/trading/env")

if __name__ == '__main__':
    main()
