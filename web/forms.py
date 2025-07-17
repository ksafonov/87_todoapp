from django import forms
from .models import TodoItem


class TodoItemForm(forms.ModelForm):
    """
    Form for creating new todo items.
    """
    
    class Meta:
        model = TodoItem
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 resize-none',
                'rows': 3,
                'placeholder': 'Enter your todo item...',
                'required': True,
            }),
        }
        labels = {
            'content': 'Todo Item',
        }
    
    def clean_content(self):
        """
        Validate that content is not empty or just whitespace.
        """
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if not content:
                raise forms.ValidationError("Todo content cannot be empty.")
        return content