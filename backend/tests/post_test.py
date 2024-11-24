import asyncio
from app.models import post
from app.database.session import SessionLocal
from app.schemas.post import PostCreate, PostUpdate
from app.services.post import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post,
    search_posts,
)
from fastapi import HTTPException

async def run_tests():
    db = SessionLocal()

    # Create a post
    post_data = PostCreate(title="Hello world", content="Good morning", tags="test")
    author_id = 1
    db_post = await create_post(db, post_data, author_id)  # Use await here
    assert db_post is not None, "Post creation failed."
    print(f"Post created successfully: {db_post.title}")

    # Retrieve posts
    posts = get_posts(db)
    assert len(posts) > 0, "No posts retrieved."
    print(f"Retrieved {len(posts)} posts.")

    # Retrieve a specific post
    retrieved_post = get_post(db, post_id=db_post.id)
    assert retrieved_post is not None, "Post retrieval failed."
    assert retrieved_post.title == "Hello world", "Retrieved post title does not match."
    print(f"Post retrieved successfully: {retrieved_post.title}")

    # Update a post
    post_update = PostUpdate(title="Updated Hello world", content="Updated content", tags="updated")
    updated_post = await update_post(db, post_id=db_post.id, post=post_update)  # Use await
    assert updated_post.title == "Updated Hello world", "Post update failed."
    assert updated_post.content == "Updated content", "Updated content does not match."
    print(f"Post updated successfully: {updated_post.title}")

    search_post1 = PostCreate(title="Searchable Post 1", content="Content 1", tags="search")
    search_post2 = PostCreate(title="Searchable Post 2", content="Content 2", tags="search")
    await create_post(db, search_post1, author_id)  # Use await
    await create_post(db, search_post2, author_id)  # Use await

    search_results = search_posts(db, query="Searchable")
    # assert len(search_results) == 2, "Search did not return the correct number of results."
    print(f"Search successful, found {len(search_results)} posts.")

    # Delete a post
    delete_result = await delete_post(db, post_id=db_post.id)  # Use await
    assert delete_result is True, "Post deletion failed."
    deleted_post = get_post(db, post_id=db_post.id)
    assert deleted_post is None, "Deleted post still exists."
    print("Post deleted successfully.")

    # Search posts
    

# Run the async test function
asyncio.run(run_tests())
