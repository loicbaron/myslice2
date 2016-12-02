'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _DashboardStore = require('../stores/DashboardStore');

var _DashboardStore2 = _interopRequireDefault(_DashboardStore);

var _DashboardActions = require('../actions/DashboardActions');

var _DashboardActions2 = _interopRequireDefault(_DashboardActions);

var _View = require('./base/View');

var _View2 = _interopRequireDefault(_View);

var _Dialog = require('./base/Dialog');

var _Dialog2 = _interopRequireDefault(_Dialog);

var _DialogHeader = require('./base/DialogHeader');

var _DialogHeader2 = _interopRequireDefault(_DialogHeader);

var _DialogBody = require('./base/DialogBody');

var _DialogBody2 = _interopRequireDefault(_DialogBody);

var _DialogPanel = require('./base/DialogPanel');

var _DialogPanel2 = _interopRequireDefault(_DialogPanel);

var _Panel = require('./base/Panel');

var _Panel2 = _interopRequireDefault(_Panel);

var _PanelHeader = require('./base/PanelHeader');

var _PanelHeader2 = _interopRequireDefault(_PanelHeader);

var _PanelBody = require('./base/PanelBody');

var _PanelBody2 = _interopRequireDefault(_PanelBody);

var _Title = require('./base/Title');

var _Title2 = _interopRequireDefault(_Title);

var _Button = require('./base/Button');

var _Button2 = _interopRequireDefault(_Button);

var _ProjectsInfo = require('./ProjectsInfo');

var _ProjectsInfo2 = _interopRequireDefault(_ProjectsInfo);

var _ProjectsForm = require('./ProjectsForm');

var _ProjectsForm2 = _interopRequireDefault(_ProjectsForm);

var _ProjectsList = require('./ProjectsList');

var _ProjectsList2 = _interopRequireDefault(_ProjectsList);

var _SlicesForm = require('./SlicesForm');

var _SlicesForm2 = _interopRequireDefault(_SlicesForm);

var _UsersDialog = require('./UsersDialog');

var _UsersDialog2 = _interopRequireDefault(_UsersDialog);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } /**
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                * Created by amirabradai on 14/10/2016.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                */


var DashboardView = function (_React$Component) {
    _inherits(DashboardView, _React$Component);

    function DashboardView(props) {
        _classCallCheck(this, DashboardView);

        return _possibleConstructorReturn(this, (DashboardView.__proto__ || Object.getPrototypeOf(DashboardView)).call(this, props));
    }

    _createClass(DashboardView, [{
        key: 'render',
        value: function render() {}
    }]);

    return DashboardView;
}(_react2.default.Component);

exports.default = DashboardView;

//# sourceMappingURL=DashboardView-compiled.js.map