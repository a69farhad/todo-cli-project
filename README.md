
# To-Do CLI App

A tiny command-line To-Do app in Python that can run **both** on your machine and inside Docker. Tasks are saved to `data/tasks.json` so they can persist using a Docker volume.

## Features
- `add "task description"` — add a task
- `list` — show all tasks with IDs
- `remove ID` — remove a task by its ID

## Run locally (no Docker)
```bash
python3 todo.py add "Read a book"
python3 todo.py list
python3 todo.py remove 1
```
Tasks are stored at `data/tasks.json` (auto-created on first run).

## Build the Docker image
```bash
docker build -t todo-cli .
```

## Run *interactively* inside Docker 
Start a shell inside the container and run Python commands there:
- **macOS/Linux (bash/zsh):**
```bash
docker run -it --rm -v "$(pwd)/data:/app/data" --entrypoint /bin/bash todo-cli
```
- **Windows PowerShell:**
```powershell
docker run -it --rm -v "${PWD}/data:/app/data" --entrypoint /bin/bash todo-cli
```
Then inside the container:
```bash
python3 todo.py add "Read a book"
python3 todo.py list
python3 todo.py remove 1
```

> Why `--entrypoint /bin/bash`?  
> The image has an entrypoint that directly runs the CLI (so we can pass args from outside when we want). For the interactive exercise, we **override** it to get a shell and run the Python commands *inside* the running container.

## Alternative: pass commands from outside (non-interactive)
```bash
docker run --rm -v "$(pwd)/data:/app/data" todo-cli add "Read a book"
docker run --rm -v "$(pwd)/data:/app/data" todo-cli list
docker run --rm -v "$(pwd)/data:/app/data" todo-cli remove 1
```

## Persisting data
Bind mount the host `./data` directory to `/app/data` in the container:
```bash
docker run -it --rm -v "$(pwd)/data:/app/data" --entrypoint /bin/bash todo-cli
```
All tasks will live in `./data/tasks.json` on your host, so they persist between runs.

## Git & GitHub
Initialize a repo and push:
```bash
git init
git add .
git commit -m "Initial commit: To-Do CLI App"
git branch -M main
git remote add origin https://github.com/<your-username>/todo-cli-app.git
git push -u origin main
```

## Notes
- The same `todo.py` works both inside and outside Docker.
- No external Python packages used.
- Data saved in `data/tasks.json` and persists via a volume mount.
