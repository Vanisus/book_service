from fastapi import FastAPI, APIRouter, Request, HTTPException, Response
from fastapi.openapi.utils import get_openapi
from starlette.routing import Match
import httpx
import logging

from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Library Gateway",
    description="This is a combined API documentation for all microservices.",
    version="1.0.0",
)

service_routes = {
    "books": settings.book_service_url,
    "rental": settings.rental_service_url,
    "user": settings.user_service_url,
    "files": settings.file_service_url
}


async def proxy_request(request: Request, service_url: str):
    async with httpx.AsyncClient() as client:
        url = service_url
        headers = dict(request.headers)
        method = request.method
        body = await request.body()

        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, headers=headers, content=body)
        elif method == "PUT":
            response = await client.put(url, headers=headers, content=body)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )


def create_proxy_route(service_url_template: str):
    async def proxy_route(request: Request):
        path_params = request.path_params
        service_url = service_url_template.format(**path_params)
        return await proxy_request(request, service_url)
    return proxy_route


@app.on_event("startup")
async def startup_event():
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

    # Обновление схемы OpenAPI с путями из всех микросервисов
    openapi_schema["paths"].update(book_openapi["paths"])
    openapi_schema["paths"].update(rental_openapi["paths"])
    openapi_schema["paths"].update(user_openapi["paths"])
    openapi_schema["paths"].update(file_openapi["paths"])

    # Включение компонентов схемы из каждого микросервиса
    openapi_schema["components"] = {
        "schemas": {
            **book_openapi.get("components", {}).get("schemas", {}),
            **user_openapi.get("components", {}).get("schemas", {}),
            **rental_openapi.get("components", {}).get("schemas", {}),
            **file_openapi.get("components", {}).get("schemas", {})
        }
    }

    # Создание маршрутов на основе путей из схемы OpenAPI
    for path, path_item in openapi_schema["paths"].items():
        for method in path_item:
            service = None
            if path.startswith("/books"):
                service = settings.book_service_url
            elif path.startswith("/rental"):
                service = settings.rental_service_url
            elif path.startswith("/user"):
                service = settings.user_service_url
            elif path.startswith("/files"):
                service = settings.file_service_url

            if service:
                app.add_api_route(
                    path,
                    create_proxy_route(f"{service}{path}"),
                    methods=[method.upper()]
                )

    app.openapi_schema = openapi_schema


@app.get("/openapi.json")
async def get_openapi_json():
    return app.openapi_schema


@app.get("/")
async def get_documentation():
    return app.openapi()
