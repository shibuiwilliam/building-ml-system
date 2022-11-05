from container import Application
from dependency_injector.wiring import Provide, inject
from view import AbstractSidePane


@inject
def main(
    side_pane: AbstractSidePane = Provide[Application.views.side_pane],
):
    side_pane.build()


if __name__ == "__main__":
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main()
