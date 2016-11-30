/**
 * Created by amirabradai on 29/11/2016.
 */
import InputText from './InputText';
import actions from '../actions/AddOrganizationActions';
import store from '../stores/AddOrganizationStore';
class AddOrganisazation extends React.Component {




     submitForm(event) {
        event.preventDefault();
        //actions.submitForm();
    }
    render() {
        return (
                    <form onSubmit={this.submitForm}>
                        <div className="row">
                            <div className="col-sm-7 col-sm-offset-3">
                                <p className="inputDescription">
                                   Please provide information about your organization and designate a manager (you or another person) from your organization.
                                   OneLab is open to enterprise, to scientific researchers, and to educators.
                                <br />
                                   We grant manager access to people in positions of responsibility (e.g., executives, professors, senior researchers), and delegate
                                   to these managers the right to grant standard user access to other people in their organizations.
                                </p>
                            </div>
                        </div>

                        <div className="row">
                            <InputText name="organization" placeholder="Name" />
                        </div>
                        <div className="row">
                            <InputText name="web" placeholder="http://" />
                        </div>

                        <div className="row">
                        <div className="col-sm-4 col-sm-offset-4 inputForm">
                            <input type="checkbox" name="terms" onChange={this.updateTerms} />&nbsp;&nbsp; I agree to the&nbsp;
                            <a href="#" data-toggle="modal" data-target="#myModal">terms and conditions.</a>
                        </div>
                    </div>
                    </form>

        );
    }
}
