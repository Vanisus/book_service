from fastapi import FastAPI, APIRouter, Request
from fastapi.openapi.utils import get_openapi
import httpx

from settings import settings

app = FastAPI(
    title="Library Gateway",
    description="This is a combined API documentation for all microservices.",
    version="1.0.0",
)

book_service = APIRouter()
rental_service = APIRouter()
user_service = APIRouter()
file_service = APIRouter()


@book_service.api_route("/{path:path}", methods=["GET"], name="book_proxy_get")
async def proxy_books_get(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.book_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.get(url, headers=headers)
        return response.json()


@book_service.api_route("/{path:path}", methods=["POST"], name="book_proxy_post")
async def proxy_books_post(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.book_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.post(url, headers=headers, content=await request.body())
        return response.json()


@book_service.api_route("/{path:path}", methods=["PUT"], name="book_proxy_put")
async def proxy_books_put(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.book_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.put(url, headers=headers, content=await request.body())
        return response.json()


@book_service.api_route("/{path:path}", methods=["DELETE"], name="book_proxy_delete")
async def proxy_books_delete(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.book_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.delete(url, headers=headers)
        return response.json()


@rental_service.api_route("/{path:path}", methods=["GET"], name="rental_proxy_get")
async def proxy_rental_get(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.rental_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.get(url, headers=headers)
        return response.json()


@rental_service.api_route("/{path:path}", methods=["POST"], name="rental_proxy_post")
async def proxy_rental_post(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.rental_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.post(url, headers=headers, content=await request.body())
        return response.json()


@rental_service.api_route("/{path:path}", methods=["PUT"], name="rental_proxy_put")
async def proxy_rental_put(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.rental_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.put(url, headers=headers, content=await request.body())
        return response.json()


@rental_service.api_route("/{path:path}", methods=["DELETE"], name="rental_proxy_delete")
async def proxy_rental_delete(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.rental_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.delete(url, headers=headers)
        return response.json()


@user_service.api_route("/{path:path}", methods=["GET"], name="user_proxy_get")
async def proxy_user_get(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.user_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.get(url, headers=headers)
        return response.json()


@user_service.api_route("/{path:path}", methods=["POST"], name="user_proxy_post")
async def proxy_user_post(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.user_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.post(url, headers=headers, content=await request.body())
        return response.json()


@user_service.api_route("/{path:path}", methods=["PUT"], name="user_proxy_put")
async def proxy_user_put(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.user_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.put(url, headers=headers, content=await request.body())
        return response.json()


@user_service.api_route("/{path:path}", methods=["DELETE"], name="user_proxy_delete")
async def proxy_user_delete(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.user_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.delete(url, headers=headers)
        return response.json()


@file_service.api_route("/{path:path}", methods=["GET"], name="file_proxy_get")
async def proxy_file_get(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.file_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.get(url, headers=headers)
        return response.json()


@file_service.api_route("/{path:path}", methods=["POST"], name="file_proxy_post")
async def proxy_file_post(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.file_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.post(url, headers=headers, content=await request.body())
        return response.json()


@file_service.api_route("/{path:path}", methods=["PUT"], name="file_proxy_put")
async def proxy_file_put(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.file_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.put(url, headers=headers, content=await request.body())
        return response.json()


@file_service.api_route("/{path:path}", methods=["DELETE"], name="file_proxy_delete")
async def proxy_file_delete(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.file_service_url}/{path}"
        headers = dict(request.headers)
        response = await client.delete(url, headers=headers)
        return response.json()


app.include_router(book_service, prefix='/books')
app.include_router(rental_service, prefix='/rental')
app.include_router(user_service, prefix='/user')
app.include_router(file_service, prefix='/files')


@app.get("/openapi.json")
async def custom_openapi():
    async with httpx.AsyncClient() as client:
        book_openapi = (await client.get(f"{settings.book_service_url}/openapi.json")).json()
        user_openapi = (await client.get(f"{settings.user_service_url}/openapi.json")).json()
        rental_openapi = (await client.get(f"{settings.rental_service_url}/openapi.json")).json()
        file_openapi = (await client.get(f"{settings.file_service_url}/openapi.json")).json()

    openapi_schema = get_openapi(
        title="Library Management API Gateway",
        version="1.0.0",
        description="This is a combined API documentation for all microservices.",
        routes=app.routes,
    )
    openapi_schema["paths"].update(book_openapi["paths"])
    openapi_schema["paths"].update(rental_openapi["paths"])
    openapi_schema["paths"].update(user_openapi["paths"])
    openapi_schema["paths"].update(file_openapi["paths"])

    return openapi_schema


@app.get("/")
async def get_documentation():
    return app.openapi()
