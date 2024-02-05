from django import forms


class CellUpdateForm(forms.Form):
    """Form for updating the state of a cell."""

    row = forms.IntegerField()
    col = forms.IntegerField()
    is_alive = forms.BooleanField(required=False)
