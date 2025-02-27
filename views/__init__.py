# Import view functions
from .home import show as show_home
from .assessment import show as show_assessment
from .dashboard import show as show_dashboard
from .documentation import show as show_documentation
from .admin import show as show_admin

# Create view objects with show methods
class View:
    def __init__(self, show_func):
        self.show = show_func

# Initialize view objects
home = View(show_home)
assessment = View(show_assessment)
dashboard = View(show_dashboard)
documentation = View(show_documentation)
admin = View(show_admin)