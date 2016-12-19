/**
 * Created by amirabradai on 09/12/2016.
 */
import axios from 'axios';
import actions from '../actions/AddOrganizationActions';

const AddOrganizationSource = () => {
    return {

        submitAuthority: {
            // remotely fetch something (required)
            remote(state) {
                return axios.post('/api/v1/authorities', {

                    'name': state.name,
                    'domains': state.domains,
                    'shortname' : state.shortname,
                    'authority': "urn:publicid:IDN+onelab+authority+sa",

                    'users': [{ 'first_name': state.first_name,
                               'last_name': state.last_name,
                               'shortname':state.short_name,
                               'password': state.password,
                               'email': state.email,
                               'terms': state.terms,
                    }
                    ],
                    'pi_users': [ {'email': state.email}
                    ]
                });




            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loading, // (optional)
            success: actions.submitAuthoritySuccess, // (required)
            error: actions.submitAuthorityError, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        }
    }
};

export default AddOrganizationSource;
