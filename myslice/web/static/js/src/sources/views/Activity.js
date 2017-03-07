import axios from 'axios';
import actions from '../../actions/views/Activity';

const ActivitySource = () => {
    return {
        fetchActivity: {
            // remotely fetch something (required)
            remote(state) {
                return axios.get('/api/v1/activity', {
                    params: {
                        filter: state.filter
                    }
                });
            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loading, // (optional)
            success: actions.updateActivity, // (required)
            error: actions.errorActivity, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        getUserToken: {

            remote(state) {
                return axios.get('/api/v1/usertoken');
            },

            success: actions.setUserToken,
            error: actions.errorUserToken,
        }
    }
};

export default ActivitySource;