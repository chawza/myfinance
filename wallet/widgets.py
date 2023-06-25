from django import forms

class ColorPickerWidget(forms.TextInput):

    def __init__(self, *args, **kwargs) -> None:
        attrs = {
            'type': 'color' 
        }

        if hasattr(kwargs, 'attrs'):
            kwargs.update(attrs)
        else:
            kwargs['attrs'] = attrs

        super().__init__(*args, **kwargs)
