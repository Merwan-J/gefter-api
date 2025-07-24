from injector import Module, provider, singleton, Injector
from config import Config, get_config


class AppModule(Module):
    @provider
    @singleton
    def provide_config(self) -> Config:
        return get_config()


def create_injector():
    return Injector(modules=create_modules())


def create_modules():
    modules = [
        AppModule(),
    ]
    return modules
