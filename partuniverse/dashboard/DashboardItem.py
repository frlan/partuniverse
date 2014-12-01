class DashboardItem:
    name = ""
    description = ""
    container = None

    def __init__(self,container):
        self.container = container

    def render(self):
        raise NotImplementedError( "Should have implemented this" )
