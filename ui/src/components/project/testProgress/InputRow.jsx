import React, { useState } from 'react';
import PropTypes from 'prop-types';

const InputRow = ({ data, onDataUpdate, editable }) => {
    const { date_of_execution, executed_test_case_count, passed_test_case_count } = data;
    const [executedValue, setExecutedValue] = useState(executed_test_case_count);
    const [passedValue, setPassedValue] = useState(passed_test_case_count);

    const handleExecutedChange = (e) => {
        const value = e.target.value;
        setExecutedValue(value);
        const executedCount = value === '' ? 0 : parseInt(value, 10);
        onDataUpdate(date_of_execution, executedCount,passedValue); 
      };
      
      const handlePassedChange = (e) => {
        const value = e.target.value;
        setPassedValue(value);
        const passedCount = value === '' ? 0 : parseInt(value, 10);
        onDataUpdate(date_of_execution, executedValue, passedCount); 
      };

    const isNumberKey = (evt) => {
        let charCode = evt.which ? evt.which : evt.keyCode;

        if (
            (charCode > 31 &&
                (charCode < 48 || charCode > 57) &&
                (charCode < 96 || charCode > 105)) ||
            evt.shiftKey
        ) {
            evt.preventDefault();
        }
        return true;
    };

    return (
        <tr>
            <td>{date_of_execution}</td>
            <td>
                {editable ? (
                    <input
                        data-testid="executed"
                        type="text"
                        value={executedValue}
                        onChange={handleExecutedChange}
                        onKeyDown={isNumberKey}
                    />
                ) : (
                    executedValue
                )}
            </td>
            <td>
                {editable ? (
                    <input
                        data-testid="passed"
                        type="text"
                        value={passedValue}
                        onChange={handlePassedChange}
                        onKeyDown={isNumberKey}
                    />
                ) : (
                    passedValue
                )}
            </td>
        </tr>
    );
};

InputRow.propTypes = {
    data: PropTypes.shape({
        date_of_execution: PropTypes.any.isRequired,
        executed_test_case_count: PropTypes.any.isRequired,
        passed_test_case_count: PropTypes.any.isRequired,
    }).isRequired,
    onDataUpdate: PropTypes.func.isRequired,
    editable: PropTypes.bool.isRequired,
};

export default InputRow;
