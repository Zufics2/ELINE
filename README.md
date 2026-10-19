# ELINE

ELINE is a web service that solves linear algebra problems and explains every step. You enter a system of linear equations as an augmented matrix, pick a method, and get the result together with each row operation and the matrix after it.

The first method is **Gaussian elimination** (with back substitution) and its **Gauss–Jordan** variant. The architecture is built so new methods can be added without touching the rest of the app.

## Features

- Exact arithmetic with fractions: you see `1/3`, not `0.3333`.
- Step-by-step solutions: row swaps, scaling, elimination and back substitution, each explained and rendered with KaTeX.
- All three outcomes handled: unique solution, infinitely many solutions (free variables shown as `t₁`, `t₂`, …) and no solution.
- Input accepts integers, decimals and fractions such as `1/3`.
- History of solved problems, stored in PostgreSQL (JSONB), with open and delete.
- Large matrices run in a Celery worker, and the client polls until they finish.
- Plugin-style solver registry: the frontend learns about methods from the API.

## Tech stack

| Layer | Tools |
|---|---|
| Frontend | React, Vite, Ant Design, react-router-dom, zustand, axios, katex + react-katex |
| Backend | Python, Django, Django REST Framework, django-cors-headers, Celery + Redis |
| Math | sympy for symbolic results; numpy, scipy and pandas are installed for future numeric methods |
| Database | PostgreSQL via psycopg 3, JSONB through Django `JSONField` |
| DevOps | Docker, Docker Compose, python-dotenv |

## Architecture

```
┌─────────────┐   REST/JSON   ┌──────────────────────────────┐
│  React SPA  │ ────────────► │ Django + DRF                 │
│ AntD, KaTeX │ ◄──────────── │  api → services → solvers    │
│ zustand     │               └───────┬───────────┬──────────┘
└─────────────┘                       │           │
                               PostgreSQL        Redis ◄── Celery worker
                               (JSONB)        (broker)   (large solves)
```

The backend has four layers:

1. **API** (`apps/*/views.py`, `serializers.py`): HTTP and validation only, no math.
2. **Services** (`apps/solutions/services.py`): chooses sync or Celery, runs the solver, saves history.
3. **Solvers** (`solvers/`): plain Python with no Django imports, easy to unit test.
4. **Persistence**: the `Solution` model, with `input`, `steps` and `result` stored as JSONB.

Two contracts keep the system extensible:

- **Solver interface** (`solvers/base.py`): every method subclasses `BaseSolver` and registers itself with `@register`.
- **Step format**: every solver returns the same JSON structure (below), so the frontend renders any method without method-specific code.

### Step format

```json
{
  "steps": [
    {
      "index": 2,
      "title": "Eliminate x_1 from row 2",
      "description": "Use the pivot in row 1 to zero out column 1 in row 2.",
      "operation": "R_{2} \\leftarrow R_{2} + \\frac{3}{2}R_{1}",
      "matrix": "\\left[\\begin{array}{cc|c} ... \\end{array}\\right]",
      "meta": { "pivot": [0, 0], "row": 1 }
    }
  ],
  "result": {
    "type": "unique",
    "rank": 3,
    "variables": 3,
    "free_variables": [],
    "solution": { "x_1": "2", "x_2": "3", "x_3": "-1" }
  },
  "result_latex": "\\begin{aligned} x_{1} &= 2 \\\\ ... \\end{aligned}"
}
```

`result.type` is `unique`, `infinite` or `none`. `operation` and `matrix` are LaTeX strings and can be empty.

## Project structure

```
eline/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/                  # settings, urls, celery, wsgi/asgi
│   ├── apps/
│   │   ├── solutions/           # model, serializers, views, services, Celery task
│   │   └── methods/             # GET /api/methods/
│   ├── solvers/                 # pure math, framework-free
│   │   ├── base.py              # BaseSolver, Step
│   │   ├── registry.py          # @register, get_solver, list_solvers
│   │   ├── latex.py             # LaTeX helpers
│   │   └── gauss.py             # Gaussian / Gauss–Jordan
│   └── tests/
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── api/                 # axios client
        ├── store/               # zustand stores (solver, history)
        ├── routes/
        ├── pages/               # Home, Solver, Solution, History, NotFound
        ├── components/          # MatrixInput, StepsViewer, StepCard, ResultCard, ...
        └── methods/             # input forms, chosen by input_schema.type
```

## Quick start (Docker)

Requirements: Docker with Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

On Windows PowerShell use `Copy-Item .env.example .env`.

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000/api/ |

Compose starts PostgreSQL 17, Redis, the Django backend (migrations run automatically), a Celery worker and the Vite dev server.

To stop everything, run `docker compose down`. Add `-v` only if you also want to delete the database.

## Running without Docker

Requirements: Python 3.12+ (3.14 is the target), Node.js 20.19+ or 22+, PostgreSQL, and Redis if you want the Celery path.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set `POSTGRES_HOST=localhost` in `.env` (the example file uses `db`, the Docker service name), then:

```bash
python manage.py migrate
python manage.py runserver
celery -A config worker --loglevel=info    # optional, for large matrices
```

To try the app without PostgreSQL, set `USE_SQLITE=1` before each command. This is meant for local runs and tests only.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8000`. Change the target with `VITE_PROXY_TARGET`.

## Configuration

All settings come from `.env` (loaded with python-dotenv).

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | `dev-insecure-key` | Django secret key. Change it outside development. |
| `DJANGO_DEBUG` | `0` | Set `1` for debug mode. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names. |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | Origins allowed to call the API directly. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | `eline` | Database credentials. |
| `POSTGRES_HOST`, `POSTGRES_PORT` | `localhost`, `5432` | Use `db` inside Docker. |
| `REDIS_URL` | `redis://localhost:6379/0` | Celery broker. |
| `SOLVE_ASYNC_THRESHOLD` | `30` | Systems with more equations or variables than this run in Celery. |
| `CELERY_TASK_ALWAYS_EAGER` | `0` | Set `1` to run tasks inline without a worker. |
| `USE_SQLITE` | unset | Set `1` to use SQLite instead of PostgreSQL. |
| `VITE_API_URL` | `/api` | API base URL for the frontend. |
| `VITE_PROXY_TARGET` | `http://localhost:8000` | Dev-server proxy target. |

## API

| Method | URL | Description |
|---|---|---|
| GET | `/api/methods/` | Available solvers and their input schemas. |
| POST | `/api/solutions/` | Solve. Returns `200` with the solution, or `202` with a `task_id` when queued. |
| GET | `/api/solutions/` | History, latest 50. |
| GET | `/api/solutions/<id>/` | One saved solution with all steps. |
| DELETE | `/api/solutions/<id>/` | Remove from history. |
| GET | `/api/tasks/<task_id>/` | Status of a queued solve: `pending`, `done` or `failed`. |

Example request:

```bash
curl -X POST http://localhost:8000/api/solutions/ \
  -H "Content-Type: application/json" \
  -d '{
    "method": "gauss",
    "input": {
      "matrix": [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]],
      "mode": "gauss"
    }
  }'
```

`input.matrix` is the augmented matrix: the last column holds the constants. Entries can be numbers or strings such as `"1/3"`. `mode` is `gauss` or `gauss_jordan`. Add `"run_async": true` to force the Celery path.

Invalid input returns `400` with a readable message, for example `{"input": "Cannot read “x” as a number. ..."}`.

## Adding a new method

1. Create `backend/solvers/inverse.py`:

   ```python
   from .base import BaseSolver, SolverInputError, Step
   from .registry import register

   @register
   class InverseSolver(BaseSolver):
       key = "inverse"
       name = "Matrix inverse"
       description = "Find the inverse of a square matrix."
       input_schema = {"type": "square_matrix", "min": 1, "max": 10}

       def validate(self, payload):
           ...  # raise SolverInputError on bad input

       def solve(self, payload):
           steps = [Step(1, "Title", "Explanation", "LaTeX operation", "LaTeX matrix")]
           return {
               "steps": [s.to_dict() for s in steps],
               "result": {"type": "..."},
               "result_latex": "...",
           }
   ```

2. Import it in `backend/solvers/__init__.py`:

   ```python
   from . import inverse  # noqa: F401
   ```

3. If it uses a new input type, add a form component in `frontend/src/methods/` and map it in `frontend/src/methods/index.js`:

   ```js
   export const inputForms = {
     augmented_matrix: AugmentedMatrixForm,
     square_matrix: SquareMatrixForm,
   };
   ```

Methods that reuse `augmented_matrix` need no frontend work. The method list, routes and the step and result views update automatically.

## Tests

```bash
cd backend
USE_SQLITE=1 python manage.py test tests
```

Windows PowerShell: `$env:USE_SQLITE=1; python manage.py test tests`

The tests cover:

- Unique, infinite and inconsistent systems.
- Row swaps, fractions and invalid input.
- The step contract.
- The API: methods, solve, history, validation errors, and the queued 202 and polling flow.

Tests run on SQLite, so run `docker compose up` once to confirm the PostgreSQL setup.

## Troubleshooting

**`Could not resolve "prop-types"` in the frontend container.**
`react-katex` needs `prop-types`, which is listed in `package.json`. Docker keeps an old `node_modules` in an anonymous volume, so rebuild and renew it:

```bash
docker compose down
docker compose build --no-cache frontend
docker compose up --renew-anon-volumes
```

**npm complains about React peer dependencies.**
`frontend/.npmrc` sets `legacy-peer-deps=true` because `react-katex` declares an older React range. That setting also stops npm from installing peer dependencies automatically, so any such package must be listed in `package.json` directly.

**Backend cannot connect to the database.**
Inside Docker, `POSTGRES_HOST` must be `db`. Outside Docker, set it to `localhost`.

**Large matrices stay on "still being computed".**
The Celery worker is not running. Start it with `celery -A config worker`, or set `CELERY_TASK_ALWAYS_EAGER=1`.

**`pip install` fails on Python 3.14.**
Some packages may not have wheels for the newest Python yet. Loosen the version pins in `requirements.txt`, or use Python 3.12 or 3.13.

## Limitations

- History is shared by everyone who uses the instance. There are no user accounts yet.
- The frontend input grid is limited to 10 × 10. The API accepts up to 50 × 50.
- Docker runs the Vite dev server and `gunicorn` without a reverse proxy. For production, build the frontend (`npm run build`), serve it with nginx, set `DJANGO_DEBUG=0`, and use a real `DJANGO_SECRET_KEY`.

## Ideas for next methods

Determinant, matrix inverse, LU decomposition, rank and null space, eigenvalues and eigenvectors, least squares.