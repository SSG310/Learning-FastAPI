from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app=FastAPI(lifespan=lifespan)

text_posts={
    1: {"title":"New Post","content":"cool test post"},
    2: {"title": "Hello World", "content": "Just another day in the database."},
    3: {"title": "Lorem Ipsum", "content": "Dolor sit amet, consectetur adipiscing elit."},
    4: {"title": "Debugging 101", "content": "Why does this error only happen on Tuesdays?"},
    5: {"title": "Coffee Break", "content": "BRB, getting my fourth cup of coffee."},
    6: {"title": "Random Thought", "content": "If a tree falls in a forest, does the log get printed?"},
    }

@app.get("/posts")
def get_all_posts(limit: int):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys())+1] = new_post
    return new_post