import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import InputRow from './InputRow';

// Mock the onDataUpdate function
const mockOnDataUpdate = jest.fn();

const sampleData = {
    date_of_execution: '2023-11-09',
    executed_test_case_count: 5,
    passed_test_case_count: 3
};

describe('InputRow component', () => {
    it('renders the component with editable fields', () => {
        const { getByText, getByRole, queryAllByRole } = render(
            <InputRow data={sampleData} onDataUpdate={mockOnDataUpdate} editable={true} />
        );

        // Check if the component renders the date, executed, and passed values
        expect(getByText('2023-11-09')).toBeInTheDocument();
        expect(getByRole('row', { name: "2023-11-09 5 3" })).toBeInTheDocument();
        expect(screen.getByTestId('executed')).toBeInTheDocument();
        expect(screen.getByTestId('passed')).toBeInTheDocument();
        const textboxes = queryAllByRole('textbox', { name: "" });
        expect(textboxes.length).toBe(2);
    });

    it('calls onDataUpdate when changing executed value', () => {
        render(
            <InputRow data={sampleData} onDataUpdate={mockOnDataUpdate} editable={true} />
        );

        const executedInput = screen.getByTestId('executed');
        fireEvent.change(executedInput, { target: { value: '6' } });
        expect(mockOnDataUpdate).toHaveBeenCalledWith('2023-11-09', parseInt('6'), 3);
    });

    it('calls onDataUpdate when changing passed value', () => {
        render(
            <InputRow data={sampleData} onDataUpdate={mockOnDataUpdate} editable={true} />
        );

        const passedInput = screen.getByTestId('passed');
        fireEvent.change(passedInput, { target: { value: '4' } });
        expect(mockOnDataUpdate).toHaveBeenCalledWith('2023-11-09', 5, parseInt('4'));
    });

    it('renders non-editable fields when editable is false', () => {
        const { queryByRole, getByRole } = render(
            <InputRow data={sampleData} onDataUpdate={mockOnDataUpdate} editable={false} />
        );

        expect(queryByRole('textbox')).toBeNull();
        expect(getByRole('row', { name: "2023-11-09 5 3" })).toBeInTheDocument();
        expect(getByRole('cell', { name: "5" })).toBeInTheDocument();
        expect(getByRole('cell', { name: "3" })).toBeInTheDocument();
    });

    it('should prevent non-numeric input for executed field', () => {
        const { getByTestId } = render(
            <InputRow data={sampleData} onDataUpdate={mockOnDataUpdate} editable={true} />
        );

        const executedInput = getByTestId('executed');
        fireEvent.keyDown(executedInput, {
            key: "A",
            code: "A",
            keyCode: 65,
            charCode: 65
        });

        expect(executedInput.value).toBe('5'); // Input should be the same due to preventDefault
    });

});