'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }(); /**
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Created by amirabradai on 14/10/2016.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      */


var _alt = require('../alt');

var _alt2 = _interopRequireDefault(_alt);

var _DashboardActions = require('../actions/DashboardActions');

var _DashboardActions2 = _interopRequireDefault(_DashboardActions);

var _DashboardSource = require('../sources/DashboardSource');

var _DashboardSource2 = _interopRequireDefault(_DashboardSource);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var removeFromArray = function removeFromArray(myArray, searchTerm) {
    var property = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;

    for (var i = 0, len = myArray.length; i < len; i++) {
        if (property == null) {
            var a = myArray[i];
        } else {
            var a = myArray[i][property];
        }
        if (a === searchTerm) {
            myArray.splice(i, 1);
            return myArray;
        }
    }
    return myArray;
};

var DashboardStore = function () {
    function DashboardStore() {
        _classCallCheck(this, DashboardStore);

        this.filter = [];

        this.dialog = null;

        this.bindListeners({

            updateSlices: _DashboardActions2.default.UPDATE_SLICES,
            fetchProjects: _DashboardActions2.default.FETCH_PROJECTS,
            errorProjects: _DashboardActions2.default.ERROR_PROJECTS,
            showDialog: _DashboardActions2.default.SHOW_DIALOG,
            updateProjects: _DashboardActions2.default.UPDATE_PROJECTS
        });

        this.registerAsync(_DashboardSource2.default);
    }

    _createClass(DashboardStore, [{
        key: 'fetchProjects',
        value: function fetchProjects(filter) {

            this.filter = filter;

            if (!this.getInstance().isLoading()) {
                this.getInstance().fetch();
            }
        }
    }, {
        key: 'updateProjects',
        value: function updateProjects(projects) {
            if (projects.hasOwnProperty('data')) {
                this.projects = projects.data.result;
            } else {
                this.projects = projects;
            }
        }
    }, {
        key: 'showDialog',
        value: function showDialog(dialog) {
            this.dialog = dialog;
        }
    }, {
        key: 'updateSlices',
        value: function updateSlices(slices) {
            if (slices.hasOwnProperty('data')) {
                this.current.slices = slices.data.result;
            } else {
                this.current.slices = slices;
            }
        }
    }, {
        key: 'errorProjects',
        value: function errorProjects(errorMessage) {
            console.log(errorMessage);
        }
    }]);

    return DashboardStore;
}();

exports.default = _alt2.default.createStore(DashboardStore, 'DashboardStore');

//# sourceMappingURL=DashboardStore-compiled.js.map