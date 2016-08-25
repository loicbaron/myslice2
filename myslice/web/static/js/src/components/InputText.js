import React from 'react';

export default class InputText extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            'class' : '',
            'message': ''
        };

        this.updateText = this.updateText.bind(this);
    }

    validateText(txt) {
        if(!this.props.regex && this.props.required){
            return txt.length>0;
        }
        if(typeof(this.props.regex)==='string'){
    	    var re = new RegExp(this.props.regex);
        }else{
            var re = this.props.regex;
        }
    	return re.test(txt);
	}

    updateText(event) {
        var txt = event.target.value;
        if (this.validateText(txt)) {
            this.setState({'class' : ''});
            this.setState({'message': ''})
        } else {
            this.setState({'class' : 'error'});
            this.setState({'message':this.props.message})
        }
        this.props.handleChange(txt);
    }

    render() {
        var messageWarning;
        if(this.state.message.length>0){
            messageWarning = <div className="col-sm-4 alert alert-danger message"><div>{this.state.message}</div></div>
        }else{
            messageWarning = '';
        }
        if(!this.props.type){
            var type = "text"; 
        }else{
            var type = this.props.type;
        }
        return (
            <div>
                <div className="col-sm-4 col-sm-offset-4 inputForm">
                    <input onChange={this.updateText} className={this.state.class} placeholder={this.props.placeholder} type="text" name={this.props.name} type={type} />
                </div>
                {messageWarning}
            </div>
        );
    }
}
