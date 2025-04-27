from django import forms
from django.core.files.storage import default_storage # For saving files
from django.conf import settings # To access MEDIA_URL
import os # For path joining
from .models import ApplicationFormField, ApplicationSubmission, ApplicationSubmissionData

class DynamicApplicationForm(forms.Form):
    """Dynamically generates form fields based on ApplicationFormField model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ApplicationFormField.objects.filter(is_active=True).order_by('order')

        for field_model in fields:
            field_key = field_model.field_name
            field_label = field_model.label
            # File/Image fields cannot be required if they might be empty in POST data
            # Let the view handle validation if truly required
            field_required = field_model.is_required and field_model.field_type not in ['file', 'image', 'checkbox']
            field_help_text = field_model.help_text
            field_choices = field_model.get_choices_list()

            common_attrs = {
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'aria-label': field_label,
            }
            file_attrs = {
                 'class': 'mt-1 block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }

            # --- Field Type Logic ---
            if field_model.field_type == 'text':
                self.fields[field_key] = forms.CharField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.TextInput(attrs=common_attrs)
                )
            elif field_model.field_type == 'textarea':
                self.fields[field_key] = forms.CharField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.Textarea(attrs={**common_attrs, 'rows': 4})
                )
            elif field_model.field_type == 'email':
                self.fields[field_key] = forms.EmailField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.EmailInput(attrs=common_attrs)
                )
            elif field_model.field_type == 'number':
                 self.fields[field_key] = forms.IntegerField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.NumberInput(attrs=common_attrs)
                )
            elif field_model.field_type == 'select':
                 self.fields[field_key] = forms.ChoiceField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    choices=[('', '---------')] + field_choices,
                    widget=forms.Select(attrs=common_attrs)
                )
            elif field_model.field_type == 'checkbox':
                 self.fields[field_key] = forms.BooleanField(
                    label=field_label, required=False, # Checkboxes usually aren't required
                    help_text=field_help_text,
                    widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'})
                 )
            elif field_model.field_type == 'radio':
                 self.fields[field_key] = forms.ChoiceField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    choices=field_choices,
                    # Render radios manually in template for better styling if needed
                    widget=forms.RadioSelect(attrs={'class': 'mr-2'})
                 )
            elif field_model.field_type == 'date':
                 self.fields[field_key] = forms.DateField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.DateInput(attrs={**common_attrs, 'type': 'date'})
                 )
            # --- ADDED File/Image Fields ---
            elif field_model.field_type == 'file':
                self.fields[field_key] = forms.FileField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.ClearableFileInput(attrs=file_attrs) # Allows clearing
                )
            elif field_model.field_type == 'image':
                self.fields[field_key] = forms.ImageField(
                    label=field_label, required=field_required, help_text=field_help_text,
                    widget=forms.ClearableFileInput(attrs=file_attrs) # Allows clearing
                )

    def save(self, files_data=None): # Accept files data
        """Saves the form data into ApplicationSubmission and ApplicationSubmissionData."""
        if not self.is_valid():
            raise ValueError("Form is not valid, cannot save.")

        cleaned_data = self.cleaned_data

        # Create the main submission record
        applicant_name = cleaned_data.get('full_name', '')
        applicant_email = cleaned_data.get('email_address', '')
        submission = ApplicationSubmission.objects.create(
            applicant_name=applicant_name,
            applicant_email=applicant_email
        )

        # Get field definitions again to link data correctly
        fields_map = {f.field_name: f for f in ApplicationFormField.objects.filter(is_active=True)}

        data_to_create = []
        for field_name, value in cleaned_data.items():
            if field_name in fields_map:
                field_model = fields_map[field_name]
                value_to_save = ""

                # --- Handle File/Image Uploads ---
                if field_model.field_type in ['file', 'image'] and files_data and field_name in files_data:
                    uploaded_file = files_data[field_name]
                    # Define a path within MEDIA_ROOT
                    # Example: media/application_files/submission_<id>/<filename>
                    file_dir = os.path.join('application_files', f'submission_{submission.id}')
                    file_path = os.path.join(file_dir, uploaded_file.name)
                    # Save the file using default storage
                    saved_path = default_storage.save(file_path, uploaded_file)
                    # Store the relative path (URL) in the value field
                    value_to_save = default_storage.url(saved_path) # Get URL path
                    # Or store relative path from MEDIA_ROOT: value_to_save = saved_path
                elif value is not None: # Handle non-file fields
                    # Convert value to string for TextField storage
                    value_to_save = ', '.join(value) if isinstance(value, list) else str(value)

                if value_to_save: # Only save if there's a value or a file was uploaded
                    data_to_create.append(
                        ApplicationSubmissionData(
                            submission=submission,
                            field=field_model,
                            value=value_to_save
                        )
                    )

        if data_to_create:
            ApplicationSubmissionData.objects.bulk_create(data_to_create)
        return submission
