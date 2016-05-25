var ProjectForm = React.createClass({
    getInitialState () {
        return projectstore.getState();
    },
    componentDidMount: function() {
        // store
        projectstore.listen(this.onChange);
    },
    componentWillUnmount() {
        projectstore.unlisten(this.onChange);
    },
    onChange(state) {
        this.setState(state);
    },

    handleLabelChange(e) {
        projectactions.updateLabel(e.target.value);
        projectactions.updateName(this.normaliseLabel(e.target.value));
    },
    normaliseLabel(text) {
        return text.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    },
    handleUrlChange: function(e) {
       projectactions.updateUrl(e.target.value);
    },
    handleDescriptionChange: function(e) {
       projectactions.updateDescription(e.target.value);
    },
    handleStartDateChange: function(e) {
       projectactions.updateStartDate(e.target.value);
    },
    handleEndDateChange: function(e) {
       projectactions.updateEndDate(e.target.value);
    },
    onPublicChanged: function (e) {
        projectactions.updatePublic(e.currentTarget.checked);
        projectactions.updateProtected(!e.currentTarget.checked);
        projectactions.updatePrivate(!e.currentTarget.checked);
    },
    onProtectedChanged: function (e) {
        projectactions.updatePublic(!e.currentTarget.checked);
        projectactions.updateProtected(e.currentTarget.checked);
        projectactions.updatePrivate(!e.currentTarget.checked);
    },
    onPrivateChanged: function (e) {
        projectactions.updatePublic(!e.currentTarget.checked);
        projectactions.updateProtected(!e.currentTarget.checked);
        projectactions.updatePrivate(e.currentTarget.checked);
    },
    handleSubmit: function(e) {
        // prevent the browser's default action of submitting the form
        e.preventDefault();
        var label = this.state.label;
        var description = this.state.description;

        var flag = false;
        var msg = '';
        if(!label){
            msg += 'Name is required \n';
            flag = true;
        }
        if(!description){
            msg += 'Description is required \n';
            flag = true;
        }
        if(flag){ 
            alert(msg); 
            return;
        }

        projectactions.postForm();

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
            <input type="text" placeholder="Name" value={this.state.label} onChange={this.handleLabelChange} />
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
        <ProjectForm />,
        document.getElementById('project-form')
);
