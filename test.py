from base import viewgenerator
from core.models import Patron


class PatronTableViewGenerator(viewgenerator.TableViewGenerator):
    model = Patron
    fields = [
        viewgenerator.ViewField("name"),
        viewgenerator.ViewField("phone"),
        viewgenerator.ViewField("email"),
    ]


class PatronDetailViewGenerator(viewgenerator.EditableDetailViewGenerator):
    model = Patron
    fields = [
        viewgenerator.ViewField("name"),
        viewgenerator.ViewField("phone"),
        viewgenerator.ViewField("email"),
    ]


patrons = [
    Patron("Jane Doe", "555 555 0155", "jane.doe@example.com"),
    Patron("John Doe", "555 555 0156", "john.doe@example.net")
]

pvg = PatronTableViewGenerator(patrons)
# print pvg.render()

dvg = PatronDetailViewGenerator(patrons[0])
print dvg.render()
print dvg.render_form()
