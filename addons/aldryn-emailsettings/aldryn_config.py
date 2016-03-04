# -*- coding: utf-8 -*-
from aldryn_client.forms import BaseForm, CharField, NumberField, CheckboxField


class Form(BaseForm):

    email_host = CharField('SMTP Host', initial='localhost')
    email_port = NumberField('SMTP Port', initial=25)
    email_host_user = CharField('SMTP User', initial='')
    email_host_password = CharField('SMTP Password', initial='')
    email_use_tls = CheckboxField('Use TLS', required=False, initial=False)

    default_from_email = CharField('Default from email', initial='', required=False)

    email_host_stage = CharField('SMTP Host used on stage', initial='localhost', required=False)
    email_port_stage = NumberField('SMTP Port used on stage', initial=25, required=False)
    email_host_user_stage = CharField('SMTP User used on stage', initial='', required=False)
    email_host_password_stage = CharField('SMTP Password used on stage', initial='', required=False)
    email_use_tls_stage = CheckboxField('Use TLS used on stage', required=False, initial=False)

    mandrill_api_key = CharField('Mandrill API key', initial='', required=False)
    mandrill_api_key_stage = CharField('Mandrill API key for stage', initial='', required=False)

    def to_settings(self, data, settings):
        is_stage = settings.get('DEBUG')
        if is_stage:
            password = data.get('email_host_password_stage') or data.get('email_host_password')
            email_settings = {
                'EMAIL_HOST': data.get('email_host_stage') or data.get('email_host'),
                'EMAIL_HOST_PASSWORD': password.encode('ascii') if password else None,
                'EMAIL_HOST_USER': data.get('email_host_user_stage') or data.get('email_host_user'),
                'EMAIL_PORT': data.get('email_port_stage') or data.get('email_port'),
                'EMAIL_USE_TLS': data.get('email_use_tls_stage') or data.get('email_use_tls'),
            }
            stage_mandrill_api_key = data.get('mandrill_api_key_stage')
            if stage_mandrill_api_key:
                email_settings.update({
                    'EMAIL_BACKEND': 'django_mandrill.mail.backends.mandrillbackend.EmailBackend',
                    'MANDRILL_API_KEY': stage_mandrill_api_key
                })
        else:
            password = data.get('email_host_password')
            email_settings = {
                'EMAIL_HOST': data.get('email_host'),
                'EMAIL_HOST_PASSWORD': password.encode('ascii') if password else None,
                'EMAIL_HOST_USER': data.get('email_host_user'),
                'EMAIL_PORT': data.get('email_port'),
                'EMAIL_USE_TLS': data.get('email_use_tls'),
            }
            mandrill_api_key = data.get('mandrill_api_key')
            if mandrill_api_key:
                email_settings.update({
                    'EMAIL_BACKEND': 'django_mandrill.mail.backends.mandrillbackend.EmailBackend',
                    'MANDRILL_API_KEY': mandrill_api_key
                })

        if data.get('default_from_email', False):
            email_settings['DEFAULT_FROM_EMAIL'] = data.get('default_from_email')
            email_settings['SERVER_EMAIL'] = data.get('default_from_email')
        settings.update(email_settings)
        return settings
