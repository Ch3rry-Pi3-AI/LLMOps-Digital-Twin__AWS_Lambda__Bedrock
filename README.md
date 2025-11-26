# 🚀 **Project Setup — Branch Overview**

This branch prepares the core structure for the **LLMOps Digital Twin** project. The focus is on creating the initial directory layout, generating the Next.js frontend without nested Git issues, and installing a modern Python package manager for backend development.

## Part 1: Create the Core Project Structure

### Step 1: Open Your Workspace

1. Open **Cursor** (or your preferred IDE).
2. Select **File → Open Folder**.
3. Create a new folder named `twin`.
4. Open the `twin` folder in Cursor.

### Step 2: Create Required Directories

Inside the `twin` folder:

1. Right-click in the file explorer.
2. Select **New Folder** → name it `backend`.
3. Right-click again → **New Folder** → name it `memory`.

Your structure should now be:

```
llmops-digital-twin/
├── backend/
└── memory/
```

### Step 3: Create the Frontend Application

Open a terminal inside Cursor:

```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --no-git
```

This command creates a Next.js 14+ app using:

* TypeScript
* TailwindCSS
* The App Router
* A clean root folder (no `src/`)
* **No Git initialisation**, preventing accidental nested repos

Accept all defaults when prompted.

Once completed, you will see output indicating that dependencies and route types were installed successfully.

### Step 4: Add the Components Directory

Inside Cursor:

1. Expand the `frontend` directory.
2. Right-click on it.
3. Select **New Folder** → name it `components`.

Your project structure now becomes:

```
llmops-digital-twin/
├── backend/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   └── (config files: package.json, next.config.js, tsconfig.json, etc.)
└── memory/
```

## Part 2: Install the Python Package Manager (uv)

The Digital Twin backend uses **uv**, a modern and extremely fast Python toolchain. It replaces pip and venv with a unified, efficient workflow.

### Step 1: Install uv

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart the terminal and confirm uv is available:

```bash
uv --version
```

You should see output similar to:

```
uv 0.x.x
```

### Step 2: Confirm Installation Is Working

If `uv --version` returns a valid version number, the setup is complete and you can proceed to backend environment configuration in the next branch.
