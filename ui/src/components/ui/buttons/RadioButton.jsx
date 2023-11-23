import React from 'react';
import PropTypes from 'prop-types';
import './RadioButton.css'

const RadioButton = ({ docType, setDocType }) => {
    const handleRadioChange = (value) => {
        setDocType(value);
    };

    return (
        <>
            <div className="radio-btns">
                <div className="form-check form-check-inline">
                    <input className="form-check-input"
                        type="radio" name="docTypeRadioOptions" id="docTypeRadio1"
                        value="1" checked={docType === "1"}
                        onChange={() => handleRadioChange("1")} />
                    <label className="form-check-label" htmlFor="docTypeRadio1">UI</label>
                </div>
                <div className="form-check form-check-inline">
                    <input className="form-check-input"
                        type="radio" name="docTypeRadioOptions"
                        id="docTypeRadio2" value="2"
                        checked={docType === "2"}
                        onChange={() => handleRadioChange("2")} />
                    <label className="form-check-label" htmlFor="docTypeRadio2">API</label>
                </div>
            </div>
        </>
    );
}

RadioButton.propTypes = {
    docType: PropTypes.any.isRequired,
    setDocType: PropTypes.func.isRequired
}

export default RadioButton
