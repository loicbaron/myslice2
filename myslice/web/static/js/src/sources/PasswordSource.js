import axios from 'axios';
import actions from '../actions/PasswordActions'

const PasswordSource = () => {
    return {
            onSubmit: {
                remote(state) {
                    return axios.put('/api/v1/profile',
                        {
                            data: {
                                "password": childstate.first_name,
                                "last_name": childstate.last_name,
                                "bio": childstate.bio,
                                "url": childstate.url
                            }
                        });
                },

                success: actions.updatePassword, // (required)
                error: actions.errorupdatePassword, // (required)

                shouldFetch(state) {
                    return true
                }
            },

    }
};

export default PasswordSource;
