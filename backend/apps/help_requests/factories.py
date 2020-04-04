import factory

from apps.common.factories import SQLAlchemyModelFactory


class HelpRequestFactory(SQLAlchemyModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    things = factory.Faker('text')
    finished_at = None
    accepted_at = None

    accepted_by = factory.SubFactory('apps.users.factories.UserFactory')

    class Meta:
        model = 'apps.help_requests.models.HelpRequest'
