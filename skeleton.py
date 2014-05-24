"""
cs275_final_library internal API skeleton.
Copyright (c) 2014 Zane Salvatore. All Rights Reserved.
"""
##############################################################################
# Models
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

##############################################################################
# Metaview
class Filter(object):
    """Stupid interface for objects that take a Model and carry out some
    action on it to get desired values. It also can optionally show a form to
    allow more complex filtering.

    Stupid because you can only pick one filter at a time...

    Class Attributes:
        form_template: str or Jinja2 Template. str should be the name of a
            template in the templates dir. Defines a form to be displayed
            when using the filter, so params can be altered. If None, no
            form is displayed.
        model: The model that should be filtered.
    """
    @classmethod
    def filter(cls, params):
        """Function that

        Args:
            obj: The Model we're working on.


        Returns: A list of models.
        """
        pass

class ViewFieldWidget(object):
    """Defines a way of representing a field in a form.

    Attributes:
        template: Jinja2 Template object
    """
    def render_display(self, value=None):
        """
        Args:
            value: A preset value to put in the field when it's rendered.

        Returns: a string containing the HTML to display for the widget
            when displaying a read only value.
        """
        pass

    def render_edit(self, value=None):
        """
        Args:
            value: A preset value to put in the field when it's rendered.

        Returns: a string containing the HTML to display for the widget
            when displaying a widget for editing.
        """
        pass


class TextWidget(ViewFieldWidget):
    """Placeholder stub to be implemented later.
    """
    pass


class ViewField(object):
    """Enables ViewGenerator objects to interact with Model objects in a
    standard way.

    attributes:
        attribute_name: The name of the Model attribute to modify.
        display_name: The name to display when rendering the field. optional.
        widget: The ViewFieldWidget to use when displaying and editing the
            value.
    """
    def __init__(self, attribute_name, display_name=None, widget=TextWidget):
        if not display_name:
            display_name = attribute_name

        self.display_name = display_name
        self.attribute_name = attribute_name
        self.widget = widget

    def retrieve(self, model):
        """Handles retireval of the field's corresponding attribute from the
        Model. If the field represents a value which is not directly on the
        Model, then it will be necessary to subclass this class and implement
        a custom retrieve() method.
        """
        if hasattr(self, "attribute_name"):
            return getattr(model, self.attribute_name)
        else:
            raise NotImplementedError("attribute_name is not specified, so you "
                                      "must implement a custom retrieve() "
                                      "method")

    def render_display(self, obj):
        value = None
        if obj:
            value = self.retrieve(obj)
        return self.display_widget.render(value)

    def render_edit(self, obj=None):
        value = None
        if obj:
            value = self.retrieve(obj)
        return self.edit_widget.render(value)

    def update(self, model, value):
        """Take the given value and update the database as needed using the
        Model object.
        """
        pass



class ViewGenerator(object):
    """Standard interface for generating data-based views.

    Attributes:
        fields: A list of ViewField objects defining the data elements to be
            displayed, their storage and retrieval from Models.
        data: A list of Models containing the data to display.
        template: A string containing the name of the base template to use
            when displaying the view.
    """
    def __init__(self, data):
        """Load the data to be displayed into the generator.
        """
        self.data = data

    def render(self):
        """Take the stored data and display it as needed using the template.
        """
        pass


class TableViewGenerator(ViewGenerator):
    """Generates tabular displays of data using HTML table elements."""
    def render(self):
        rendered = ""
        for obj in self.data:
            for col in self.fields:
                rendered += col.render_display(obj)
        return rendered


class EditableDetailViewGenerator(object):
    """Generates record-focused displays of data that can also be edited.
    """
    def render(self):
        pass

    def render_form(self):
        pass

    def process_form(self, data):
        pass
##############################################################################