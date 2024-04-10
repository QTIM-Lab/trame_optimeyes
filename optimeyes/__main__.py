from .app.core import OptimEyes


def main(server=None, **kwargs):
    app = OptimEyes(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
