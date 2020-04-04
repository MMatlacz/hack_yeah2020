import factory

from apps.common.factories import SQLAlchemyModelFactory


class HelpRequestFactory(SQLAlchemyModelFactory):
    full_name = factory.Faker('name')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    products = factory.Faker('text')
    pickup_time = factory.Faker('future_datetime')
    call_time = factory.Faker('time')
    finished_at = None
    accepted_at = None

    accepted_by = factory.SubFactory('apps.users.factories.UserFactory')

    class Meta:
        model = 'apps.help_requests.models.HelpRequest'
