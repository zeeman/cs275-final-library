"""
Copyright (c) 2014, Zane Salvatore.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


class Model(object):
    """Represents some distinct entity, handles relevant business logic, and
    handles database insertion and deletion.

    Based on the Active Record design pattern.
    """
    @classmethod
    def filter(cls, sort=None, **kwargs):
        """Retrieves entries from the database that match the specified
        filter parameters. Only allows for basic strict matching.
        """
        pass

    def __init__(self, *args, **kwargs):
        """Should accept parameters representing fields of the entity and
        populate the Model attributes as appropriate.
        """
        pass

    def validate(self):
        """
        Perform checks to ensure that the Model's data follows any validation
        rules.

        Returns: bool indicating data validity.
        """
        pass

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