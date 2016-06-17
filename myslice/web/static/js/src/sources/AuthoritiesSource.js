import axios from 'axios';
import actions from '../actions/AuthoritiesActions';

const AuthoritiesSource = () => {
    return {
        fetch: {
            // remotely fetch something (required)
            remote(state) {
                return axios.get('/api/v1/authorities');
            },


            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateAuthorities, // (required)
            error: actions.errorAuthorities, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            /*shouldFetch(state) {
                return true
            }*/
        }
    }
};

export default AuthoritiesSource;