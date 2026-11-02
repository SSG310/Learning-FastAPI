# FastAPI Photo and Video Sharing API

A learning project for building a photo and video sharing backend with FastAPI. It provides user registration and JWT authentication, authenticated media uploads, a post feed, and owner-only post deletion.

## Features

- User registration, login, password reset, and email verification routes provided by FastAPI Users.
- JWT bearer-token authentication.
- Authenticated image and video uploads to ImageKit.
- SQLite persistence with SQLAlchemy's async API.
- An authenticated feed containing post details and ownership information.
- Post deletion restricted to the post's owner.
- Interactive API documentation at `/docs`.

## Requirements

- Python 3.12 or later.
- [uv](https://docs.astral.sh/uv/) for installing and running the project.
- An ImageKit account and private API key to use the upload endpoint.

## Setup

1. Install the project dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root. Generate a strong secret locally with:

   ```bash
   uv run python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

   Add the generated value and your ImageKit private key to `.env`:

   ```dotenv
   SECRET_KEY=paste_the_generated_secret_here
   IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
   ```

   Keep these values private and do not commit `.env`. `SECRET_KEY` is used for JWTs and password-reset and verification tokens. Keep it stable between runs; changing it invalidates existing tokens.

3. Start the development server:

   ```bash
   uv run uvicorn app.app:app --reload
   ```

   The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` to explore and call the endpoints.

## API overview

| Method | Path | Purpose | Authentication |
|---|---|---|---|
| `POST` | `/auth/register` | Register a user | No |
| `POST` | `/auth/jwt/login` | Log in and receive a JWT | No |
| `POST` | `/auth/forgot-password` | Request a password reset | No |
| `POST` | `/auth/reset-password` | Reset a password using a token | No |
| `POST` | `/auth/request-verify-token` | Request an email verification token | No |
| `POST` | `/auth/verify` | Verify an email using a token | No |
| `GET` | `/users/me` | Get the current user's profile | Yes |
| `PATCH` | `/users/me` | Update the current user's profile | Yes |
| `POST` | `/upload` | Upload an image or video with an optional caption | Yes |
| `GET` | `/feed` | List posts, newest first | Yes |
| `DELETE` | `/posts/{post_id}` | Delete a post owned by the current user | Yes |

FastAPI Users provides additional user-management routes. See `/docs` for the complete route list and request schemas.

### Authentication

Log in at `POST /auth/jwt/login` using form-encoded credentials. Copy the returned access token, then select **Authorize** in `/docs` and enter the token. For other clients, send the token as a bearer token in the `Authorization` request header.

### Uploading media

Send a `multipart/form-data` request to `POST /upload` with:

- `file`: the image or video file.
- `caption`: optional text.

The endpoint stores media in ImageKit and records the post and its owner in SQLite.

## Database

The app uses `sqlite+aiosqlite:///./test.db`, which creates or opens `test.db` in the working directory. Tables are created at startup. `create_all()` does not migrate existing tables when the models change; use a migration or carefully update/backup an existing database if the schema has changed.

## Project layout

```text
app/
  app.py      FastAPI application and API endpoints
  db.py       SQLAlchemy models, database engine, and dependencies
  images.py   ImageKit client configuration
  schemas.py  API and user schemas
  users.py    FastAPI Users manager and JWT configuration
main.py       Uvicorn entry point
```
