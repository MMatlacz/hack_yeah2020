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
