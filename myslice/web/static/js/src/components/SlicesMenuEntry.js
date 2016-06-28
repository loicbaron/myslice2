import React from 'react';

class SlicesMenuEntry extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        this.props.setCurrentSlice(this.props.slice);
    }

    sliceLabel() {
        return (this.props.slice.name || this.props.slice.shortname);
    }

    projectLabel() {
        return this.props.slice.project.name || this.props.slice.project.shortname;
    }

    render() {

        return <li className="slice-menu-entry" onClick={this.handleClick}>
            <h5><i className="fa fa-flask"></i> {this.projectLabel()}</h5>
            <h4>{this.sliceLabel()}</h4>
            <span>{this.props.slice.shortname}</span>
        </li>;

    }
}

SlicesMenuEntry.propTypes = {
    slice: React.PropTypes.object.isRequired
};

SlicesMenuEntry.defaultProps = {
};

export default SlicesMenuEntry;