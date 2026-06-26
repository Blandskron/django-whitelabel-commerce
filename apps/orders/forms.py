from django import forms


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(label="Nombre", max_length=160)
    customer_phone = forms.CharField(label="Telefono", max_length=40)
    customer_email = forms.EmailField(label="Email", required=False)
    shipping_address = forms.CharField(label="Direccion", max_length=255, required=False)
    customer_note = forms.CharField(
        label="Comentario",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
