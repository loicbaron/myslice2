import React from 'react';
import Select from 'react-select';

class NodeFilter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': []
        };
        this.setValue = this.setValue.bind(this);
        this.renderOption = this.renderOption.bind(this);
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    setValue(value) {
		this.setState({ 'selected': value });
        this.props.handleChange(value);
	}

    getOptions() {
        return [
            { label: 'For more information on IoT nodes ', disabled: true,
                link: 'https://www.iot-lab.info/hardware'  },
            { value: 'a8', label: 'A8',
                description: 'Powerful open node that can run generic high level OSs like Linux',
                type: 'hardware' },
            { value: 'm3', label: 'M3',
                description: 'Open node based on the STM32 (ARM Cortex M3) micro-controller',
                type: 'hardware' },
            { value: 'wsn430', label: 'WSN430',
                description: 'Open node based on a low power MSP430-based platform with ISM radio and standard sensors',
                type: 'hardware' },
            { value: 'des', label: 'DES', type: 'hardware' },
            { value: 'custom', label: 'Custom', type: 'hardware' },

            { value: 'grenoble', label: 'Grenoble', type: 'city' },
            { value: 'lille', label: 'Lille', type: 'city' },
            { value: 'saclay', label: 'Saclay', type: 'city' },
            { value: 'strasbourg', label: 'Strasbourg', type: 'city' },
            { value: 'rennes', label: 'Rennes', type: 'city' },
            { value: 'paris', label: 'Paris', type: 'city' },
            { value: 'lyon', label: 'Lyon', type: 'city' },
            { value: 'berlin', label: 'Berlin', type: 'city' },

            { value: 'france', label: 'France', type: 'country' },
            { value: 'germany', label: 'Germany', type: 'country' },
        ];
    }

    renderLink(link) {
        if (link) {
            return <a href={link} target="_blank">click here</a>;
        }
	}

	renderDescription(description) {
        if (description) {
            return <div className="selectDescription">{description}</div>;
        }
    }

	renderOption(option) {
		return (
            <div>
                <div className="selectLabel">{option.label}{this.renderLink(option.link)}</div>
                {this.renderDescription(option.description)}
            </div>
        );
	}


	renderValue(option) {
		return (
            <span>
                <span>{option.label}</span>
            </span>
        );

	}

    render() {
        let placeholder = this.props.placeholder || "Filter by site or node type";
        let options = this.getOptions();

        return <Select
                    name="iot-node-type"
                    multi={true}
                    placeholder={placeholder}
                    value={this.state.selected}
                    valueRenderer={this.renderValue}
                    options={options}
                    optionRenderer={this.renderOption}
                    onChange={this.setValue}
                />
    }
}


NodeFilter.propTypes = {
    handleChange: React.PropTypes.func.isRequired
};

NodeFilter.defaultProps = {
};


const IotFilter = ({handleChange}) =>
    <div className="row">
        <div className="col-sm-12">
            <NodeFilter handleChange={handleChange} />
        </div>
    </div>;

IotFilter.propTypes = {
    handleChange: React.PropTypes.func.isRequired
};

IotFilter.defaultProps = {
};

export default IotFilter;