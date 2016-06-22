import React from 'react';

import Element from './base/Element';
import ElementTitle from './base/ElementTitle';
import ElementId from './base/ElementId';
import ElementStatus from './base/ElementStatus';
import ElementIcon from './base/ElementIcon';
import DateTime from './base/DateTime';

class SlicesRow extends React.Component {

    render() {
        var label = this.props.slice.name || this.props.slice.shortname;
        var project = this.props.slice.project.name || this.props.slice.project.shortname;
        var authority = this.props.slice.authority.name || this.props.slice.authority.shortname;

        return (
             <Element element={this.props.slice} type="project" select={this.props.select}>
                 <ElementStatus status={this.props.slice.status} />
                 <ElementIcon icon="slice" />
                 <ElementTitle label={label} detail={this.props.slice.shortname} />
                 <ElementId id={this.props.slice.id} />
                 <div className="elementDetail">
                     <span className="elementLabel">Part of project</span> {project}
                     <br />
                     <span className="elementLabel">Managed by</span> {authority}
                 </div>
                 <div className="row elementDate">
                     <div className="col-sm-3">
                         <span className="elementLabel">Created</span>
                         <br />
                         <DateTime timestamp={this.props.slice.created} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Enabled</span>
                         <br />
                         <DateTime timestamp={this.props.slice.enabled} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Updated</span>
                         <br />
                         <DateTime timestamp={this.props.slice.updated} />
                     </div>
                 </div>
             </Element>
         );
    }
}

SlicesRow.propTypes = {
    slice: React.PropTypes.object.isRequired,
    select: React.PropTypes.bool
};

SlicesRow.defaultProps = {
    select: false
};

export default SlicesRow;