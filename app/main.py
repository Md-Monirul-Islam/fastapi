from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.extras
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123456Pl@',
                            cursor_factory=psycopg2.extras.DictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Database connection failed")
    print("Error:", error)


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


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
    return None


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



# @app.delete('/delete-posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     my_post.pop(index)
#     return {'message': 'post deleted successfully'}



@app.delete('/delete-posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)