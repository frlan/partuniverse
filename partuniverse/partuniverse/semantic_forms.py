from django.utils.encoding import smart_text, force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils import six
from django.forms.widgets import CheckboxInput

def as_semantic(self):
    """Helper function for to generate a form with semantic ui styling."""
    normal_row='<div%(html_class_attr)s><label>%(label)s</label> %(field)s%(help_text)s</div>'
    checkbox_row='<div class="field"><div class="ui checkbox">%(field)s%(label)s</div></div>'
    error_row='<li>%s</li>'
    row_ender=''
    help_text_html=' <span class="helptext">%s</span>'
    errors_on_separate_row = False
    top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
    output, hidden_fields,error_box = [], [], []
    for name, field in self.fields.items():
        html_class_attr = ''
        bf = self[name]
        # bf.field.default_error_messages['required'] = 'The field %(name)s is required.' % ({ 'name': name })
        # Escape and cache in local variable.
        bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
        if bf.is_hidden:
            if bf_errors:
                top_errors.extend(
                    [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                     for e in bf_errors])
            hidden_fields.append(six.text_type(bf))
        else:
            # Create a 'class="..."' attribute if the row should have any
            # CSS classes applied.
            css_classes = bf.css_classes()
            if (bf_errors):
                css_classes = css_classes + ' error'
            html_class_attr = ' class="field %s%s"' % ("required " if bf.field.required else "",css_classes)

            if bf_errors:
                for error in bf_errors:
                    error_box.append(error_row % force_text(error))

            if bf.label:
                label = conditional_escape(force_text(bf.label))
                if (isinstance(bf.field.widget,CheckboxInput)):
                    label = bf.label_tag(label,label_suffix='')
                else:
                    label = bf.label_tag(label) or ''
            else:
                label = ''

            if field.help_text:
                help_text = help_text_html % force_text(field.help_text)
            else:
                help_text = ''

            row = checkbox_row if (isinstance(bf.field.widget,CheckboxInput)) else normal_row
            output.append(row % {
                'errors': force_text(bf_errors),
                'has_errors': True if len(force_text(bf_errors)) > 0 else False,
                'label': force_text(label),
                'field': six.text_type(bf),
                'help_text': help_text,
                'html_class_attr': html_class_attr,
                'field_name': bf.html_name,
            })

    if top_errors:
        output.insert(0, '<div class="ui error message segment" style="display: block;><ul class="list">%s</ul></div>' % force_text(top_errors))

    if len(error_box) > 0:
        output.insert(0, '<div class="ui error message segment" style="display: block;"><ul class="list">%s</ul></div>' % force_text("\n".join(error_box)))
    

    if hidden_fields:  # Insert any hidden fields in the last row.
        str_hidden = ''.join(hidden_fields)
        if output:
            last_row = output[-1]
            # Chop off the trailing row_ender (e.g. '</td></tr>') and
            # insert the hidden fields.
            if not last_row.endswith(row_ender):
                # This can happen in the as_p() case (and possibly others
                # that users write): if there are only top errors, we may
                # not be able to conscript the last row for our purposes,
                # so insert a new, empty row.
                last_row = (normal_row % {'errors': '', 'label': '',
                                          'field': '', 'help_text': '',
                                          'html_class_attr': html_class_attr})
                output.append(last_row)
            output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
        else:
            # If there aren't any rows in the output, just append the
            # hidden fields.
            output.append(str_hidden)
    return mark_safe('\n'.join(output))
