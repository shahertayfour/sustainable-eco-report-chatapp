# Changelog

## [Unreleased] - 2025-10-16

### Added
- ✨ **Professional Arabic Reports**: Beautiful HTML reports with Shaheen branding (green & gold gradients)
- 🚀 **Two Frontend Modes**:
  - `flask_app_simple.py` - Fast direct MCP access (recommended)
  - `flask_app.py` - AI-powered with Ollama integration
- 📊 **Professional Report Components**:
  - Document metadata with report numbers
  - Executive summary with key metrics cards
  - Intelligent key findings with data-driven insights
  - Detailed statistics tables
  - Methodology section with industry standards (ASHRAE, WHO)
  - Multi-phase action plans (immediate, short-term, long-term)
  - Professional footer with compliance info
- 🎯 **START_APP.bat**: One-click Windows startup script
- 🔧 **run_server.py**: HTTP server wrapper for MCP tools using uvicorn
- 📁 **create_dataset.py**: Synthetic data generation script
- 🌐 **Bilingual Support**: Full Arabic & English language support with RTL
- 📝 **.env.example**: Environment configuration template

### Changed
- 📦 **Streamlined Dependencies**:
  - Backend: Reduced from 12 to 3 packages (fastmcp, pandas, uvicorn)
  - Frontend: Minimal dependencies (Flask, mcp-use, langchain-ollama, python-dotenv)
- 📚 **Enhanced README**:
  - Added frontend comparison table
  - Added Arabic query examples
  - Added quick start instructions
  - Added data generation documentation
  - Updated architecture diagram
- 🎨 **Enhanced UI**:
  - Professional report formatting in chat.html
  - Shaheen color scheme integration
  - Responsive grid layouts
  - Gradient backgrounds
- 🔒 **Updated .gitignore**:
  - Added .claude/ directory
  - Added .env file
  - Added temporary files (nul, *.json)
  - Added test files

### Fixed
- ✅ **JavaScript Template Literals**: Fixed all missing backticks in chat.html
- 🐛 **HTML Errors**: Removed stray text and instruction comments
- 🔧 **Dependency Issues**: Cleaned up redundant backend requirements
- 📊 **Data Processing**: Improved Arabic JSON handling in reports
- 🎨 **Report Display**: Enhanced JSON parsing and formatting

### Technical Details
- **MCP Tools**: 3 async tools with Arabic output
  - `get_building_energy_stats()`: Energy statistics with mean/max/min
  - `get_sustainability_metrics()`: Environmental metrics with recommendations
  - `analyze_eco_impact()`: Carbon footprint and water usage analysis
- **Dataset**: 8,640 sensor readings (30 days × 288 readings/day)
- **Response Format**: Professional HTML with inline CSS
- **Server Architecture**:
  - Backend: FastMCP + Uvicorn (port 4141)
  - Frontend: Flask (port 5000)

### Performance
- ⚡ **flask_app_simple.py**: 3-5x faster than mcp-use version
- 🚀 **Direct Imports**: No HTTP overhead for MCP tools
- 📊 **7,400+ character reports**: Generated in <1 second

### Documentation
- 📖 Updated README with comprehensive setup instructions
- 📝 Added .env.example with all configuration options
- 🗒️ Created CHANGELOG.md for version tracking
- ✅ Created WORKING_STATUS.md for application verification

---

## Previous Releases

See git commit history for earlier changes.
