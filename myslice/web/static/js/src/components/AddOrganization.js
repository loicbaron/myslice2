/**
 * Created by amirabradai on 29/11/2016.
 */

var React = require('react');
import InputText from './InputText';
import actions from '../actions/AddOrganizationActions';
import store from '../stores/AddOrganizationStore';
import LoadingPanel from './LoadingPanel';
class AddOrganization extends React.Component {

     constructor(props) {
        super(props);
       //  this.state={};
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
         this.submitForm = this.submitForm.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
       // console.log("changed");
        this.setState(state);
    }
    updateEmail(value) {
        actions.updateEmail(value);
    }
    updatePassword(value) {
        actions.updatePassword(value);
    }
    updateAName(value) {
        actions.updateAName(value);
    }
    updateSiteweb(value) {
        actions.updateSiteweb(value);
    }
    updateFirstname(value) {
        actions.updateFirstname(value);
    }
    updateLastname(value) {
        actions.updateLastname(value);
    }

    updateTerms(event) {
        actions.updateTerms(event.target.value);
    }

     submitForm(event) {
        event.preventDefault();
         //extract domains

         var nu=this.state.email.split('@');
         this.state.domains.push(nu[1]);
         console.log(this.state.domains)

         // exract shortname
          var u=this.state.siteweb.split('.');
         this.state.shortname= u[1];
         console.log(this.state.shortname);
        actions.submitForm();
    }
    render() {
        // var emailRegExp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        return (
                    <form onSubmit={this.submitForm}>

                        <div className="row">
                            <div className="col-md-3">
                                <i className="fa fa-university" aria-hidden="true"></i>
                            </div>
                            <div className="col-sm-9">
                                <p className="inputDescription">
                                   Please provide information about your organization and you will be as a manager.
                                   OneLab is open to enterprise, to scientific researchers, and to educators.
                                </p>
                            </div>
                        </div>

                        <div className="row">
                            <InputText name="aname" handleChange={this.updateAName} placeholder="Name" />
                        </div>
                        <div className="row">
                            <InputText name="siteweb" handleChange={this.updateSiteweb} placeholder="http://" />
                        </div>
                    <div className="row">
                        <div className="col-md-3">
                            <i className="fa fa-user" aria-hidden="true"></i>
                        </div>
                        <div className="col-sm-9">
                            <p className="inputDescription">
                                Please provide your First name, your last name and Email address (your identifier for logging in). <br />
                                We will also contact you to verify your account and occasionally for important communications.
                            </p>
                        </div>
                    </div>

                         <div className="row">
                        <InputText name="first_name" handleChange={this.updateFirstname} placeholder="Firstname" required={true} message="is required" />
                    </div>
                    <div className="row">
                        <InputText name="last_name" handleChange={this.updateLastname} placeholder="Lastname" required={true} message="is required" />
                    </div>
                    <div className="row">
                    <p>&nbsp;</p>
                    </div>

                    <div className="row">
                        <InputText name="email" handleChange={this.updateEmail} placeholder="Email address"  message="Invalid email" />
                    </div>
                    <div className="row">
                        <InputText name="password" handleChange={this.updatePassword} placeholder="Password" regex=".{8,}$" message="must be at least 8 characters" type="password" />
                    </div>

                        <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input type="checkbox" name="terms" onChange={this.updateTerms} />&nbsp;&nbsp; I agree to the&nbsp;
                            <a href="#" data-toggle="modal" data-target="#myModal">terms and conditions.</a>
                        </div>
                        </div>
                        <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputSubmit">
                            <input type="submit" className="btn btn-default"/>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-sm-4 col-sm-offset-4">
                            {this.state.message}
                        </div>
                    </div>
                    <LoadingPanel show={this.state.loading}/>

                    </form>

        );
    }
}

AddOrganization.propTypes = {

};

export default AddOrganization;