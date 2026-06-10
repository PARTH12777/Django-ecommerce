from django import forms


class CheckoutForm(forms.Form):
    shipping_first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    shipping_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    same_as_shipping = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    billing_first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control billing-field'}))
    billing_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_postal_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))
    billing_country = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control billing-field'}))

    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('same_as_shipping'):
            billing_fields = [
                'billing_first_name', 'billing_last_name', 'billing_email',
                'billing_phone', 'billing_address', 'billing_city',
                'billing_state', 'billing_postal_code', 'billing_country',
            ]
            for field in billing_fields:
                if not cleaned.get(field):
                    self.add_error(field, 'This field is required when billing differs from shipping.')
        return cleaned
