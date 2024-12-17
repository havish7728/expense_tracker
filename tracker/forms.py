from django import forms
from .models import Category,Expense

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date']

    # Filter categories for the logged-in user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance').user if kwargs.get('instance') else None
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
