import React from 'react';

const Section = ({children}) =>
    <div className="section">
        {children}
    </div>;

const SectionBody = ({children}) =>
    <div className="s-body">
        <div className="row">
            <div className="col-md-12">
                {children}
            </div>
        </div>
    </div>;

const SectionHeader = ({children}) => {
    var num = React.Children.count(children);
    if (num >= 2) {
        return (
            <div className="s-header">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 s-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="s-header">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }
};

class SectionTitle extends React.Component {
  render() {

      return <h3>{this.props.title} <span>{this.props.subtitle}</span></h3>;
  }
}

SectionTitle.propTypes = {
    title: React.PropTypes.string.isRequired,
    subtitle: React.PropTypes.string
};

SectionTitle.defaultProps = {
    subtitle: ''
};

export { Section, SectionBody, SectionHeader, SectionTitle };