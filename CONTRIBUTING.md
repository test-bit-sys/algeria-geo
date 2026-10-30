# Contributing to algeria-geo

Contributions are welcome! Whether you are reporting an erratum in administrative names, adding verified postal codes, or improving language bindings, here is how you can help.

## Development Workflow

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Local Setup & Building
1. Clone the repository:
   ```bash
   git clone https://github.com/djazairdev/algeria-geo.git
   cd algeria-geo
   ```
2. Validate the canonical dataset:
   ```bash
   python scripts/build.py --check
   ```
3. Build all distributions (JSON, CSV, SQL, package sources):
   ```bash
   python scripts/build.py
   ```
4. Run tests:
   - **Python**:
     ```bash
     cd packages/python
     pip install -e ".[test]"
     pytest
     ```
   - **Node / TypeScript**:
     ```bash
     cd packages/node
     npm install
     npm run build
     npm test
     ```

## Administrative Data Guidelines

- Any correction to wilaya, daira, or commune boundaries **must** cite the corresponding decree in the *Journal officiel de la République algérienne démocratique et populaire*.
- The canonical data lives in `data/wilayas.json`, `data/dairas.json`, and `data/communes.json`.
- Do not edit generated distributions (`dist/`, `packages/node/src/data.ts`, or `packages/python/src/algeria_geo/data/`) manually. Always run `python scripts/build.py` after editing source JSON.

## Code Standards
- **Zero Runtime Dependencies**: Both the Python and Node packages must keep 0 runtime dependencies.
- **Dual API Parity**: Every query method added to Python must have an equivalent counterpart in TypeScript, and vice-versa.
- **Strict Typing**: TypeScript code uses strict mode (`noImplicitAny`, etc.); Python code uses full type annotations and `py.typed`.
