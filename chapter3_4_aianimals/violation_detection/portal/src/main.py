from container import Application
from dependency_injector.wiring import Provide, inject
from view import AbstractViolationListView


@inject
def main(
    violation_list_view: AbstractViolationListView = Provide[Application.views.violation_list_view],
):
    violation_list_view.build()


if __name__ == "__main__":
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main()
