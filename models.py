from base.model import Model


class Patron(Model):
    @classmethod
    def filter(cls, sort=None, **kwargs):
        """Retrieves entries from the database that match the specified
        filter parameters. Only allows for basic strict matching.
        """
        pass

    def __init__(self, name, phone=None, address=None, *args, **kwargs):
        """Should accept parameters representing fields of the entity and
        populate the Model attributes as appropriate.
        """
        self.name = name
        self.phone = phone
        self.address = address

    def validate(self):
        """
        Perform checks to ensure that the Model's data follows any validation
        rules.

        Returns: bool indicating data validity.
        """
        return True

    def save(self):
        """Update the database with the data from the Model. If the entity is
        new, INSERT. If the entity is already stored, UPDATE.
        """
        pass

    def delete(self):
        """If the entity has been saved, DELETE it. If not, ???
        """
        pass

    def identity(self):
        """
        Returns: a string uniquely identifying the record, if it exists in the
            database. If the record has not been saved, None.
        """
        pass

    def get(self, identity):
        """
        Args:
            identity: Should be a value obtained by running the identity method
                on a Model.
        """
        pass