from django import forms
PRODUCT_QUANTITY_CHOICE = [ (i, str(i)) for i in range(1, 11)]

class AddQuantityForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICE, coerce=int)