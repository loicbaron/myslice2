var navbar_tabs = [
    {
        "label": "Experiments",
        "name":   "projects",
    },
    {
        "label": "Activity",
        "name":   "activity",
    },
];



var MySliceTabIcon = React.createClass({
    getInitialState: function(){
        return {
            img: '/static/icons/'+this.props.tab.name+'-w-16.png'
        };
    },
    active: function() {
        this.setState({img: '/static/icons/'+this.props.tab.name+'-16.png'});
    },
    inactive: function() {
        this.setState({img: '/static/icons/'+this.props.tab.name+'-w-16.png'});
    },
    render: function() {
        return (
            <img className="icon" src={this.state.img} alt={this.props.tab.label} />
        );
    }
});

var MySliceTab = React.createClass({
    mouseOver: function() {
        this.refs.icon.active();
    },
    mouseOut: function() {
        this.refs.icon.inactive();
    },
    render: function() {
        return (
            <li onMouseOver={this.mouseOver} onMouseOut={this.mouseOut}>
                <a href="#"><MySliceTabIcon ref='icon' tab={this.props.tab} /> {this.props.tab.label}</a>
            </li>
        );
    }
});

var MySliceNav = React.createClass({
    render: function() {
        var tabs = this.props.tabs;

        return (
            <ul className="nav navbar-nav">
            { tabs.map(function(tab) { return <MySliceTab key={tab.name} tab={tab} /> }) }
            </ul>
        );
    }
});

ReactDOM.render(
        <MySliceNav tabs={ navbar_tabs } />,
        document.getElementById('test')
);
