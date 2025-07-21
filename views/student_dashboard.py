# views/student_dashboard.py

from views.base_dashboard import BaseDashboard
from views.pages.profile import ProfilePage
from views.pages.library import LibraryPage
from views.pages.history import HistoryPage

class StudentDashboard(BaseDashboard):
    def __init__(self, user):
        menu = ["Profile", "Library", "History"]
        # Pages currently expect no args
        pages = [
            ProfilePage(),
            LibraryPage(),
            HistoryPage()
        ]
        super().__init__(user, menu, pages)
