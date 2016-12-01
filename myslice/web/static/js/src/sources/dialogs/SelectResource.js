import axios from 'axios';
import actions from '../../actions/dialogs/SelectResource';

const SelectResourceDialog = () => {
    return {
        testbeds: {
            remote(state) {
                return axios.get('/api/v1/testbeds');
            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateTestbeds, // (required)
            error: actions.errorTestbeds, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },


        submitReservation: {
            remote(state) {
                return axios.post('/api/v1/leases/',
                    {
                        "testbed":state.testbed.id,
                        "slice_id": currentSlice.id,
                        "start_time" : state.start_date,
                        " duration" : state.duration,
                        "resources" :state.selectedIdList
                    });
            },

            success: actions.successReservation, // (required)
            error: actions.errorreservation, // (required)

            shouldFetch(state) {
                return true
            }

        },

        resources: {
            remote(state) {
                return axios.get('/api/v1/testbeds/'+state.testbed.id+'/resources');
            },

            success: actions.updateResources,
            error: actions.errorResources,

            shouldFetch(state) {
                return true
            }
        }
    }
};

export default SelectResourceDialog;

