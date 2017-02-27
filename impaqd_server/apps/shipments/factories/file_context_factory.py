import factory
import factory.django
from faker import Faker
from django.db.models.signals import pre_save, post_save
from ..models import FileContext

fake = Faker()


@factory.django.mute_signals(pre_save, post_save)
class FileContextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FileContext

    # created_at
    # updated_at
    # uuid = factory.LazyAttribute(lambda f: uuid.uuid4())
    path = factory.LazyAttribute(lambda f: fake.uri_path())
    # url_ttl
    
