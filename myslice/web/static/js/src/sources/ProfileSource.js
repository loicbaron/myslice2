import axios from 'axios';
import actions from '../actions/UserProfileActions'

const UserProfileSource = () => {
    return { 
            initUser: {
                // remotely fetch something (required)
                remote(state) {
                    return axios.get('/api/v1/profile');
                },

                // this function checks in our local cache first
                // if the value is present it'll use that instead (optional).
                // local(state) {
                //     return state. ? state.: null;
                // },

                // here we setup some actions to handle our response
                //loading: actions.loading, // (optional)
                success: actions.updateUser, // (required)
                error: actions.errorupdateUser, // (required)

                // should fetch has precedence over the value returned by local in determining whether remote should be called
                // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
                shouldFetch(state) {
                    return true
                }
            }, 

            onSubmit: {
                remote(state) {
                    return axios.put('/api/v1/profile',
                        {
                            data: {
                                "first_name": state.first_name,
                                "last_name": state.last_name,
                                "bio": state.bio,
                                "url": state.url
                            }
                        });
                },

                // this function checks in our local cache first
                // if the value is present it'll use that instead (optional).
                // local(state) {
                //     return state. ? state.: null;
                // },

                // here we setup some actions to handle our response
                //loading: actions.loading, // (optional)
                success: actions.updateUser, // (required)
                error: actions.errorupdateUser, // (required)

                // should fetch has precedence over the value returned by local in determining whether remote should be called
                // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
                shouldFetch(state) {
                    return true
                }

            }
    }
};

export default UserProfileSource;