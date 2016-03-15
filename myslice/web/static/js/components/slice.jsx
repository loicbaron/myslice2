var SliceRow = React.createClass({

     render: function() {
         return (
             <tr>
                 <td>
                     {this.props.slice.name}
                     <div className="">{this.props.slice.id}</div>
                 </td>
                 <td>{this.props.slice.created}</td>
                 <td>{this.props.slice.updated}</td>
             </tr>
         );
     }
 });

var SliceList = React.createClass({
    load: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data.slices});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: function() {
        this.load();
        // open websocket to get updates
        //setInterval(this.loadResources, this.props.pollInterval);
    },
    render: function() {
        return (
            <table className="table"><tbody>
            {this.state.data.map(function(slice) { return <SliceRow key={slice.id} slice={slice}></SliceRow>; }) }
            </tbody></table>
        );
    }
});

ReactDOM.render(
        <SliceList url="http://localhost:8111/api/v1/slice" />,
        document.getElementById('slice-list')
);

var SliceAdd = React.createClass({

    render: function() {
        var imgsrc = "/static/icons/plus.png";
        return (
            <h4><img className="icon" src="/static/icons/plus.png" alt="+" /> <a href="#" className="link-action">New Experiment</a></h4>
        );
    }
});

        ReactDOM.render(
        <SliceAdd />,
        document.getElementById('slice-add')
);

