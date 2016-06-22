import axios from 'axios';
import actions from '../actions/SettingsActions'

const SettingsSource = () => {
    return {
            fetchSettings: {
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
                success: actions.updateSettings, // (required)
                error: actions.errorupdateSettings, // (required)

                shouldFetch(state) {
                    return true
                }
            }, 

            onSubmit: {
                remote(state, childstate) {
                    return axios.put('/api/v1/profile',
                        {
                            data: {
                                "first_name": childstate.first_name,
                                "last_name": childstate.last_name,
                                "bio": childstate.bio,
                                "url": childstate.url
                            }
                        });
                },

                success: actions.updateSettings, // (required)
                error: actions.errorupdateSettings, // (required)

                shouldFetch(state) {
                    return true
                }

            },

            generateKeys: {

                remote(state) {
                    return axios.put('/api/v1/profile',
                        {
                            data: {
                                "generate_keys": "True"
                            }
                        });
                },
                
                success: actions.updateSettings,  // (required)
                error: actions.errorupdateSettings, // (required)

                shouldFetch(state) {
                    return true
                }
            }
    }
};

export default SettingsSource;