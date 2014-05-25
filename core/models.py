from base.model import Model
from utils import db


class Patron(Model):
    @classmethod
    def filter(cls, sort=None, **kwargs):
        """Retrieves entries from the database that match the specified
        filter parameters. Only allows for basic strict matching.
        """
        pass

    def __init__(self, patron_id=None, name=None, phone=None, email=None, *args,
                 **kwargs):
        """Should accept parameters representing fields of the entity and
        populate the Model attributes as appropriate.

        Args:
            patron_id: Should not be set manually.
        """
        self.patron_id = patron_id
        self.name = name
        self.phone = phone
        self.email = email

    def validate(self):
        """
        Perform checks to ensure that the Model's data follows any validation
        rules.

        Returns: bool indicating data validity.
        """
        return self.name is not None and len(self.name) > 0

    def save(self):
        """Update the database with the data from the Model. If the entity is
        new, INSERT. If the entity is already stored, UPDATE.
        """
        if not self.validate():
            raise Exception("The name field is required.")

        connection = db.get_db()
        cursor = connection.cursor()
        if self.identity():
            # the record exists -> UPDATE
            sql = 'update `Patron` set `name` = ?, `phone` = ?, `email` = ? ' \
                  'where `patron_id` = ?'
            data = self.name, self.phone, self.email, self.patron_id
            cursor.execute(sql, data)
        else:
            # the record does not exist -> INSERT
            sql = 'insert into `Patron` set `name` = ?, `phone` = ?, ' \
                  '`email` = ?'
            data = self.name, self.phone, self.email
            cursor.execute(sql, data)

    def delete(self):
        """If the entity has been saved, DELETE it from the database. If not, do
        nothing.

        If the object existed, its patron_id is set to None to signify that it
        has not been saved.
        """
        if self.identity():
            connection = db.get_db()
            cursor = connection.cursor()
            sql = 'delete from `Patron` where `patron_id` = ?'
            data = self.patron_id,
            cursor.execute(sql, data)
            self.patron_id = None

    def identity(self):
        """

        Returns: a string uniquely identifying the record, if it exists in the
            database. If the record has not been saved, None.
        """
        return self.patron_id if hasattr(self, "patron_id") else None

    def get(self, identity):
        """
        Args:
            identity: Should be a value obtained by running the identity method
                on a Model.
        """
        sql = 'select * from `Patron` where `patron_id` = ?'
        pass
