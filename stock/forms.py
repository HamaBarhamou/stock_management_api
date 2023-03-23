from django import forms
from .models import Company, CompanyWarehouse, Product


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'address')
        labels = {
            'name': 'Nom',
            'address': 'Adresse',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CompanyWarehouseForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        label='Company',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = CompanyWarehouse
        fields = ('name', 'address', 'company')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = user.created_companies.all()
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Company.objects.filter(user=user)