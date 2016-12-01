'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }(); /**
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Created by amirabradai on 14/10/2016.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      */


var _alt = require('../alt');

var _alt2 = _interopRequireDefault(_alt);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var DashboardActions = function () {
    function DashboardActions() {
        _classCallCheck(this, DashboardActions);
    }

    _createClass(DashboardActions, [{
        key: 'fetchProjects',
        value: function fetchProjects() {
            var filter = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

            return filter;
        }
    }, {
        key: 'updateProject',
        value: function updateProject(project) {
            return project;
        }
    }, {
        key: 'setCurrentProject',
        value: function setCurrentProject(project) {
            return project;
        }
    }, {
        key: 'showDialog',
        value: function showDialog(dialog) {
            return dialog;
        }
    }, {
        key: 'errorProjects',
        value: function errorProjects(errorMessage) {
            return errorMessage;
        }
    }, {
        key: 'updateSlices',
        value: function updateSlices(slices) {
            return slices;
        }
    }, {
        key: 'updateProjects',
        value: function updateProjects(project) {
            return project;
        }
    }]);

    return DashboardActions;
}();

exports.default = _alt2.default.createActions(DashboardActions);

//# sourceMappingURL=DashboardActions-compiled.js.map