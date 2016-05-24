var ExperimentForm = React.createClass({
    getInitialState () {
    var d = new Date();
    var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+ d.getMinutes()+":"+d.getSeconds()
        return {
            label: '',
            name: '',
            v_public: true,
            v_protected: false,
            v_private: false,
            url: '',
            description: '',
            start_date: df,
            end_date: '',
        };
    },
    handleKeyPress(event) {
        this.setState(
            {
                label: event.target.value,
                name: this.normaliseLabel(event.target.value)
            }
        );
    },
    normaliseLabel(text) {
        return text.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    },
    handleVisibilityChange: function(e) {
       this.setState({visibility: e.target.value});
    },
    handleUrlChange: function(e) {
       this.setState({url: e.target.value});
    },
    handleDescriptionChange: function(e) {
       this.setState({description: e.target.value});
    },
    handleStartDateChange: function(e) {
       this.setState({start_date: e.target.value});
    },
    handleEndDateChange: function(e) {
       this.setState({end_date: e.target.value});
    },
    onPublicChanged: function (e) {
        this.setState({
        v_public: e.currentTarget.checked,
        v_protected: !e.currentTarget.checked,
        v_private: !e.currentTarget.checked,
        });
    },
    onProtectedChanged: function (e) {
        this.setState({
        v_public: !e.currentTarget.checked,
        v_protected: e.currentTarget.checked,
        v_private: !e.currentTarget.checked,
        });
    },
    onPrivateChanged: function (e) {
        this.setState({
        v_public: !e.currentTarget.checked,
        v_protected: !e.currentTarget.checked,
        v_private: e.currentTarget.checked,
        });
    },
    handleSubmit: function(e) {
        // prevent the browser's default action of submitting the form
        e.preventDefault();
        var label = this.state.label;
        var description = this.state.description;
        var flag = false;
        if(!label){
            alert('Name is required');
            flag = true;
        }
        if(!description){
            alert('Description is required');
            flag = true;
        }
        if(flag) return;

        var d = new Date();
        var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+ d.getMinutes()+":"+d.getSeconds()
        this.setState({
            label: '',
            name: '',
            v_public: true,
            v_protected: false,
            v_private: false,
            url: '',
            description: '',
            start_date: df,
            end_date: '',
        });
        /*
        $.ajax({
          url: this.props.url,
          dataType: 'json',
          type: 'POST',
          data: comment,
          success: function(data) {
            this.setState({data: data});
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
        */
    },
    render: function () {
        return ( 
            <div>
            <form className="experimentForm" onSubmit={this.handleSubmit}>
            <input type="text" placeholder="Name" value={this.state.label} onChange={this.handleKeyPress} />
            <div>{this.state.name}</div>
            <input type="radio" value={this.state.v_public} checked={this.state.v_public === true } onChange={this.onPublicChanged} /> Public
            <input type="radio" value={this.state.v_protected} checked={this.state.v_protected === true } onChange={this.onProtectedChanged} /> Protected
            <input type="radio" value={this.state.v_private} checked={this.state.v_private === true } onChange={this.onPrivateChanged} /> Private <br/>

            <input type="text" placeholder="URL" value={this.state.url} onChange={this.handleUrlChange} /><br/>
            <textarea name="description" placeholder="Describe your project in a few words..." value={this.state.description} onChange={this.handleDescriptionChange} /><br/>
            Start: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.start_date} onChange={this.handleStartDateChange} />
            End: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.end_date} onChange={this.handleEndDateChange} /><br/>
            <br/>
            <div><i><b>Important: </b>quote in your papers</i></div>
            <div>Experiments leading to the publication of this paper have been performed using the OneLab Federation of testbeds.</div>
            <input type="submit" value="Save"/>
            </form>
            </div>
        );
    }
});

ReactDOM.render(
        <ExperimentForm />,
        document.getElementById('project-form')
);
