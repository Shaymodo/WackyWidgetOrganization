import pytest
from organization_manager import OrganizationManager

@pytest.fixture
def org():
    return OrganizationManager()

@pytest.fixture
def with_president(org):
    """ Creates a Organization with exactly one president already in place. """
    org.initialize_president("Nelson")
    return org
