import React from 'react';

const Message = (props) => {
    if(props.message && Object.keys(props.message).length>0){
        if(props.message.type=='success'){
            var classMessage = "alert alert-success";
        }else if(props.message.type=='error'){
            var classMessage = "alert alert-danger";
        }else{
            var classMessage = "alert alert-info";
        }
        return (
        <div className="p-view-body">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-12">
                        <div id="project-form">
                            <div className={classMessage}>
                            {props.message.msg}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        );
    }else{
        return(
            <div></div>
        );
    }

};

Message.propTypes = {
    message: React.PropTypes.object
};

Message.defaultProps = {
    message: null,
};

export default Message;
