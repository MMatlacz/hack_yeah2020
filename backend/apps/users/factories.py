import factory

from apps.common.factories import SQLAlchemyModelFactory


class UserFactory(SQLAlchemyModelFactory):
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = 'password123'
    is_active = True

    class Meta:
        model = 'apps.users.models.User'

    @factory.post_generation
    def accepted_help_requests(self, create, extracted, **kwargs):
        if create and extracted:
            for help_request in extracted:
                self.accepted_help_requests.append(help_request)
