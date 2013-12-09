class AngularForm
    _id: 1
    fields: null
    enabled: false
    errors: null
    selector: null
    submitting: false
    valid: false

    constructor: (selector)->
        @selector = selector
        @errors = {}
        @fields = {}

    closeDom: ->
        @reset()
        @toggleDom()

    addField: (field_key, label, placeholder = null, defaultValue = null)->
        @fields[field_key] =
            defaultValue: defaultValue
            errors: []
            id: @_id++
            label: label
            placeholder: placeholder
            valid: true
            value: defaultValue

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
            field.value = field.defaultValue or ''

    setErrors: (errors)->
        @valid = false
        @submitting = false
        console.info('setErrors @fields', @fields)
        for field_name, field of @fields
            if errors[field_name]
                field.valid = false
                field.errors = errors[field_name]
            else
                field.valid = true
                field.errors = []
        return

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