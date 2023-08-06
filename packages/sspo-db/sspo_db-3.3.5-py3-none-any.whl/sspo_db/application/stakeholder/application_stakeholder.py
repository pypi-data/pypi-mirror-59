from sspo_db.model.organization.models import Person
from sspo_db.service.organization.service import PersonService

class ApplicationStakeholder():

    def __init__(self):
        self.person_service = PersonService()

    def create_person(self, name, email, organization):
        person = Person()
        person.name = name
        person.description = ""
        person.organization = organization
        person.email = email 

        self.person_service.create (person)

        return person