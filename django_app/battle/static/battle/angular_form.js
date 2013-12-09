// Generated by CoffeeScript 1.6.3
(function() {
  var AngularForm;

  AngularForm = (function() {
    AngularForm.prototype._id = 1;

    AngularForm.prototype.fields = null;

    AngularForm.prototype.enabled = false;

    AngularForm.prototype.selector = null;

    AngularForm.prototype.submitting = false;

    AngularForm.prototype.valid = false;

    function AngularForm(selector) {
      this.selector = selector;
      this.fields = {};
    }

    AngularForm.prototype.closeDom = function() {
      this.reset();
      return this.toggleDom();
    };

    AngularForm.prototype.addField = function(field_key, label, placeholder, defaultValue) {
      if (placeholder == null) {
        placeholder = null;
      }
      if (defaultValue == null) {
        defaultValue = null;
      }
      return this.fields[field_key] = {
        defaultValue: defaultValue,
        errors: [],
        id: this._id++,
        label: label,
        placeholder: placeholder,
        valid: true,
        value: defaultValue
      };
    };

    AngularForm.prototype.payload = function() {
      var field, field_key, payload, _ref;
      payload = {};
      _ref = this.fields;
      for (field_key in _ref) {
        field = _ref[field_key];
        payload[field_key] = field.value;
      }
      return payload;
    };

    AngularForm.prototype.reset = function() {
      var field, field_key, _ref, _results;
      this.submitting = false;
      this.valid = true;
      _ref = this.fields;
      _results = [];
      for (field_key in _ref) {
        field = _ref[field_key];
        field.errors = [];
        field.valid = true;
        _results.push(field.value = field.defaultValue || '');
      }
      return _results;
    };

    AngularForm.prototype.setErrors = function(errors) {
      var field, field_name, _ref;
      this.valid = false;
      this.submitting = false;
      console.info('setErrors @fields', this.fields);
      _ref = this.fields;
      for (field_name in _ref) {
        field = _ref[field_name];
        if (errors[field_name]) {
          field.valid = false;
          field.errors = errors[field_name];
        } else {
          field.valid = true;
          field.errors = [];
        }
      }
    };

    AngularForm.prototype.submit = function(apiEndpoint, scopeObject) {
      var self;
      if (scopeObject == null) {
        scopeObject = null;
      }
      self = this;
      this.submitting = true;
      apiEndpoint.post(this.payload()).then(function(response) {
        if (scopeObject) {
          scopeObject.push(response);
        }
        return self.closeDom();
      }, function(response) {
        return self.setErrors(response.data);
      });
      return false;
    };

    AngularForm.prototype.toggleDom = function() {
      var $el;
      $el = $(this.selector);
      if ($el.length === 0) {
        return false;
      }
      this.enabled = !this.enabled;
      return $el.modal('setting', {
        transition: 'horizontal flip',
        onApprove: function() {
          return false;
        }
      }).modal('toggle');
    };

    return AngularForm;

  })();

  window.AngularForm = AngularForm;

}).call(this);