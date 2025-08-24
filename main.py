from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/posts')
def get_posts():
    return {"data": "This is your posts data"}


@app.post('/create-post')
def create_post(payload: dict = Body(...)):
    print(payload)
    # return {"message": "Post created successfully", "data": payload}
    return {'new post': f'title: {payload["title"]} content: {payload["content"]}'}


@app.post('/create-new-post')
def new_post(new_post: Post):
    print(new_post.rating)
    print(new_post.dict())
    # return {'new post': f'title: {new_post.title} content: {new_post.content} published: {new_post.published} rating: {new_post.rating}'}
    return {'new post': new_post}


my_post = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
           {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

@app.get('/my-post')
def get_my_post():
    return {'data': my_post}


@app.post('/again-post')
def again_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_post.append(post_dict)
    return {'data': post_dict}


@app.get('/find-post/{id}')
def find_post(id: int, response: Response):
    for p in my_post:
        if p['id'] == id:
            return {'post detail': p}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'message': 'post not found'}


@app.get('/my-post/{id}')
def get_post(id: int):
    for p in my_post:
        if p['id'] == id:
            return {'post detail': p}
    return {'message': 'post not found'}


@app.get('posts/{id}')
def get_post(id: int, response):
    post = find_post(id)
    if not post:
        response.status_code = 404
        return {'message': 'post not found'}
    return {'post detail': post}