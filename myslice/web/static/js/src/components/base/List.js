import React from 'react';

class List extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <ul className="elementList">
                {this.props.children}
            </ul>
        );
        
    }
}

export default List;