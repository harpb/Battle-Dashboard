class AngularForm
    fields: {}
    enabled: false
    selector: null
    submitting: false
    valid: false

    constructor: (selector)->
        @selector = selector

    closeDom: ->
        @reset()
        @toggleDom()

    addField: (field_key, label, default_value = null)->
        @fields[field_key] =
            default_value: default_value
            errors: []
            label: label
            placeholder: null
            valid: true
            value: ''

    payload: ->
        payload = {}
        for field_key, field of @fields
            payload[field_key] = field.value
        #            console.info('payload', payload)
        return payload

    reset: ->
        @submitting = false
        @valid = true
        for field_key, field of @fields
            field.errors = []
            field.valid = true
            field.value = field.default_value or ''
    setErrors: (errors)->
        @valid = false
        @submitting = false
        for field_name, errors of errors
            formField = @fields[field_name]
            formField.valid = false
            formField.errors = errors

    submit: (apiEndpoint, scopeObject = null)->
        self = @
        @submitting = true
        apiEndpoint.post(@payload()).then((response)->
            if scopeObject
                scopeObject.push(response)
            self.closeDom()
        ,(response)->
            self.setErrors(response.data)
        )
        return false

    toggleDom: ->
        $el = $(@selector)
        if $el.length is 0
            return false
        @enabled = !@enabled
        $el.modal('setting',
            transition: 'horizontal flip'
            onApprove: ->
                return false
        ).modal('toggle')


window.AngularForm = AngularForm
#window.AngularField = AngularField