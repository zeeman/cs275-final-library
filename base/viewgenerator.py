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
from jinja2 import Template


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
        """Function

        Args:
            params:


        Returns: A list of models.
        """
        return cls.model.find(**params)

class ViewFieldWidget(object):
    """Defines a way of representing a field in a form.

    Attributes:
        display_template: Jinja2 Template object.
        edit_template: Template.
    """
    def __init__(self, url_name):
        """
        Args:
            urlname: A unique name to identify the field by.
        """
        self.url_name = url_name

    def render_display(self, value=None):
        """
        Args:
            value: A preset value to put in the field when it's rendered.

        Returns: a string containing the HTML to display for the widget
            when displaying a read only value.
        """
        return self.display_template.render(
            url_name=self.url_name, value=value)

    def render_edit(self, value=None):
        """
        Args:
            value: A preset value to put in the field when it's rendered.

        Returns: a string containing the HTML to display for the widget
            when displaying a widget for editing.
        """
        return self.edit_template.render(
            url_name=self.url_name, value=value)


class TextWidget(ViewFieldWidget):
    """Placeholder stub to be implemented later.
    """
    def __init__(self, display_name, url_name):
        self.display_name = display_name
        self.url_name = url_name
        self.display_template = Template('{{ value }}')
        self.edit_template = Template(
            '<input type="text" class="form-control" id="{{ url_name }}" value='
            '"{{ value }}">')


class ViewField(object):
    """Enables ViewGenerator objects to interact with Model objects in a
    standard way.

    attributes:
        attribute_name: The name of the Model attribute to modify.
        url_name:
        display_name: The name to display when rendering the field. optional.
        widget: The ViewFieldWidget to use when displaying and editing the
            value.
    """
    def __init__(self, attribute_name, url_name=None, display_name=None,
                 widget=None):
        if not display_name:
            display_name = attribute_name
        if not url_name:
            url_name = attribute_name
        self.url_name = url_name
        self.display_name = display_name
        self.attribute_name = attribute_name
        self.widget = widget or TextWidget(display_name, attribute_name)


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
        return self.widget.render_display(value)

    def render_edit(self, obj=None):
        value = None
        if obj:
            value = self.retrieve(obj)
        return self.widget.render_edit(value)

    def update(self, model, value):
        """Take the given value and update the database as needed using the
        Model object.
        """
        if hasattr(self, "attribute_name"):
            setattr(model, self.attribute_name, value)
        else:
            raise NotImplementedError("attribute_name is not specified, so you "
                                      "must implement a custom update() "
                                      "method")



class ViewGenerator(object):
    """Standard interface for generating data-based views.

    Attributes:
        fields: A list of tuples of ViewField objects defining the data elements
            to be displayed, their storage and retrieval from Models and their
            form names.
            [(ViewField, str)]
        data: A list of Models containing the data to display.
        template: A string containing the name of the base template to use
            when displaying the view.
        model: class. The model this view is for.
    """
    def __init__(self, data):
        """Load the data to be displayed into the generator.
        """
        self.data = data

    def render(self):
        """Take the stored data and display it as needed using the template.
        """
        return self.template.render(fields=self.fields, data=self.data)


class TableViewGenerator(ViewGenerator):
    """Generates tabular displays of data using HTML table elements."""
    template = Template(
        """
<table class="table">
    <thead>
    <tr>
{% for f in fields %}
        <th>{{ f.display_name }}</th>
{% endfor %}
    </tr>
    </thead>
    <tbody>
{% for d in data %}
    <tr>
{% for f in fields %}
        <td>{{ f.render_display(d) }}</td>
{% endfor %}
    </tr>
{% endfor %}
    </tbody>
</table>
        """
    )


class EditableDetailViewGenerator(ViewGenerator):
    """Generates record-focused displays of data that can also be edited.
    """
    template = Template(
        """
{% for d in data %}
{% for f in fields %}
<p><b>{{ f.display_name }}</b> {{ f.render_display(d) }}</p>
{% endfor %}
{% endfor %}"""
    )

    form_template = Template(
        """
{% for d in data %}
<form role="form">
{% if d.identity() %}
    <input type="hidden" id="id" value="{{ d.identity() }}">
{% endif %}
{% for f in fields %}
    <div class="form-group">
        <label for="{{ f.url_name }}">{{ f.display_name }}</label>
        {{ f.render_edit(d) }}
    </div>
{% endfor %}
    <button type="submit" class="btn btn-default">Submit</button>
</form>
{% endfor %}
"""
    )
    def __init__(self, data, *args, **kwargs):
        self.field_url_names = {}
        for f in self.fields:
            self.field_url_names.update({f.url_name: f})

        # since this is mainly used for single objects, handle the case where
        # a single object is passed in
        if not isinstance(data, list):
            data = [data]
        super(EditableDetailViewGenerator, self).__init__(data, *args, **kwargs)

    def render_form(self):
        return self.form_template.render(fields=self.fields, data=self.data)

    def process_form(self, data):
        if "id" in data:
            obj = self.model.get(data["id"])

        for field_name in data:
            if field_name in self.field_url_names:
                self.field_url_names[field_name].update(obj, data[field_name])


class GenericView(object):
    pass