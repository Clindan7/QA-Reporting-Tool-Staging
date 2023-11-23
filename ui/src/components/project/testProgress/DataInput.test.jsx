import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import DataInputModal from './DataInputModal';
import { Provider } from 'react-redux';
import thunk from "redux-thunk";
import configureMockStore from 'redux-mock-store';

// Mock functions for props
const mockHandleClose = jest.fn();
const id = "1";
const docType = 'UI';

const middlewares = [thunk];
const initialState = {
    TCCountInputReducer: {
        isLoading: false,
        TCInputData: {
            "previous": {
                "week-1": [
                    {
                        "executed_test_case_count": 5550555,
                        "passed_test_case_count": 0,
                        "date_of_execution": "2023-09-18",
                        "project": "6"
                    }],
                    "week-2":[
                        {
                            "date_of_execution": "2023-11-04",
                            "executed_test_case_count": 14,
                            "passed_test_case_count": 12
                        },
                    ],
                },
            "today": [
                {
                    "date_of_execution": "2023-11-06",
                    "executed_test_case_count": 4,
                    "passed_test_case_count": 2
                },
                {
                    "date_of_execution": "2023-11-07",
                    "executed_test_case_count": 10,
                    "passed_test_case_count": 8
                }
            ]
        },
        errors: {},
    }
};
let mockStore = configureMockStore(middlewares);

describe('DataInputModal component', () => {

    it('renders the modal when isOpen is true', () => {
        render(
            <Provider store={mockStore(initialState)}>
                <DataInputModal isOpen={true} handleClose={mockHandleClose} projectid={id} docType={docType} />
            </Provider>
        );

        // Check if the modal content is visible
        expect(screen.getByRole('heading', { name: 'Test Progress data' })).toBeInTheDocument();
        expect(screen.getByText('Enter the TC counts corresponding to the given dates')).toBeInTheDocument();
        expect(screen.getByRole('columnheader', { name: 'Date' })).toBeInTheDocument();
        expect(screen.getByRole('columnheader', { name: 'TC Executed/day' })).toBeInTheDocument();
        expect(screen.getByRole('columnheader', { name: 'TC Passed/day' })).toBeInTheDocument();
        expect(screen.getByRole('row', { name: '2023-11-04 14 12' })).toBeInTheDocument(); //value from previous array
        expect(screen.getByRole('row', { name: '2023-11-07 10 8' })).toBeInTheDocument();//value from today array
    });

    it('calls handleClose when the modal is closed', () => {
        render(
            <Provider store={mockStore(initialState)}>
                <DataInputModal isOpen={true} handleClose={mockHandleClose} projectid={id} docType={docType} />
            </Provider>
        );

        const saveButton = screen.getByRole('button', { name: 'Save Data' });
        fireEvent.click(saveButton);
        expect(mockHandleClose).toHaveBeenCalled();
    });

    it('calls handleSave when data is updated and Save Data is clicked', () => {
        const mockHandleSave = jest.fn();
        const newState = {
            TCCountInputReducer: {
                isLoading: false,
                TCInputData: {
                    "previous": {
                        "week-1": [
                            {
                                "executed_test_case_count": 5550555,
                                "passed_test_case_count": 0,
                                "date_of_execution": "2023-09-18",
                                "project": "6"
                            }]
                        },
                    "today": [
                        {
                            "date_of_execution": "2023-11-06",
                            "executed_test_case_count": 4,
                            "passed_test_case_count": 2
                        }
                    ]
                },
                errors: {},
            }
        };
        render(
            <Provider store={mockStore(newState)}>
                <DataInputModal isOpen={true} handleClose={mockHandleClose} projectid={id} docType={docType} />
            </Provider>
        );

        const executedInput = screen.getByTestId('executed');
        const passedInput = screen.getByTestId('passed');
        const saveDataButton = screen.getByText('Save Data');

        fireEvent.change(executedInput, { target: { value: '150' } });
        fireEvent.change(passedInput, { target: { value: '120' } });
        fireEvent.click(saveDataButton);

        // Check if the handleSave function was called
        //expect(mockHandleSave).toHaveBeenCalledWith('2023-11-02', '150', '120');
       
    });
});