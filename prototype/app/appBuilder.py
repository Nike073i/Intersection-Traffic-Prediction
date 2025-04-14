from fastapi import FastAPI, APIRouter

class AppBuilder:
    def __init__(self):
        self._app = FastAPI()
        self._rootRouter = APIRouter(prefix='/api')

    def add_module(self, module_router):
        self._rootRouter.include_router(module_router)
        return self

    def build(self):
        self._app.include_router(self._rootRouter)
        return self._app