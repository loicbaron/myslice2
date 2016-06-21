import axios from 'axios';
import actions from '../actions/SlicesActions';

const SlicesSource = () => {
    return {
        fetch: {
            remote(state) {
                let type = state.options.belongTo.type || null;
                switch (type) {
                    case 'project':
                        return axios.get('/api/v1/projects/' + state.options.belongTo.id + '/slices');
                        break;
                    case 'users':
                        return axios.get('/api/v1/users/' + state.options.belongTo.id + '/slices');
                        break;
                    default:
                        return axios.get('/api/v1/slices');
                }


            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateSlices, // (required)
            error: actions.errorSlices, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        }
    }
};

export default SlicesSource;

