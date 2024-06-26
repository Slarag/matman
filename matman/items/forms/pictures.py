from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from .. import models


PictureFormset = forms.inlineformset_factory(models.Item, models.ItemPicture,
                                             fields=['file', 'title', 'description'],
                                             extra=1, can_order=True)
# PictureFormset.ordering_widget = forms.HiddenInput()


class PictureFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'formset-container'
        self.layout = Layout(
            Div(
                Field('title', placeholder='Title'),
                Field('description'),
                Field('ORDER'),
                Field('file'),
                Field('DELETE'),
                # id and item are automatically added when form is initialized with instance keyword
                Field('id'),
                Field('item'),
                css_class='card p-2 m-1 draggable formset-form',
                draggable="true",
            ),
        )
        self.render_required_fields = True
