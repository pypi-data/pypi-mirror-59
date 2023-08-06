============================
BTC Simple Wizard
============================

A simple application with some classes and scripts for wizard implementation.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add wizard app to project app list in project settings::

    INSTALLED_APPS = [
        ...
        'simple_wizard'
    ]

2. Add wizard modal to base template::

    {% include 'simple_wizard/wizard_modal.html' %}

3. Construct management view with steps like this::

    class WizardManagementView(WizardBaseView):
        """
        View for creating wizard with 3 steps
        """

        management_url_pattern = 'test_app:wizard_management'
        common_title = 'Common Title'  # for steps without own title

        class FirstStep(WizardModalStepMixin, TemplateView):
            """
            First step - simple modal with text message and continue button.
            """

            unique_name = 'message_step'
            template_name = 'simple_wizard/wizard_modal_message.html'
            message = 'Simple message step'
            cache_step = False  # step doesn't ask server on repeat show (if it already fetched)
            buttons = [
                LoadWizardStepButton(
                    load_step='form_step',  # next step (get request)
                    title='Continue',
                    css_classes=['btn btn-primary']
                )
            ]

        class SecondStep(WizardModalStepWithFormMixin, FormView):
            """
            Second step - modal with form (can be form or model form), validation supported.
            """

            unique_name = 'form_step'
            template_name = 'simple_wizard/wizard_modal_form.html'
            form_class = SecondStepForm
            redirect_to_step_if_valid = 'third_step'
            buttons = [
                LoadWizardStepPostButton(
                    load_step='form_step',
                    title='Continue',
                    css_classes=['btn btn-primary']
                )
            ]

            def form_valid(self, form):
                test_model = TestModel.objects.filter(pk=self.kwargs.ger('pk')).first()
                test_model.field_1 = form.cleaned_data.get('field_1')
                test_model.save()

            return super().form_valid(self, form):

        class ThirdStep(WizardModalStepWithFormMixin, TemplateView):
            """
            Third step - just a template modal
            """

            unique_name = 'third_step'
            template_name = 'third_step.html'
            buttons = [
                CloseWizardModalButton(
                    title='Finish',
                    css_classes=['btn btn-primary']
                )
            ]

4. Setups ``urls``::

    app_name = 'test_app'

    ...

    urlpatterns = [
        ...
        path('wizard-management/<step_to_load>/<int:pk>/', WizardManagementView.as_view(), name='wizard_management')
    ]

5. Add static files for wizard work::

    <script src="{% static 'simple_wizard/wizard.js' %}"></script>

6. Initialize wizard handler::

        $(document).ready(function () {
            const django_modal_wizard = new DjangoModalWizard(
                '#wizard-modal',
                '.js-wizard_modal_content',
                '.js-load_wizard',
                '.js-close_wizard'
            );
            django_modal_wizard.initSignals();
        });

