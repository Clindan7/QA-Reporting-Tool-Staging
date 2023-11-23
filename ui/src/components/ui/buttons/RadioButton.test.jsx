import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import RadioButton from './RadioButton';

// Mock the setDocType function
const setDocTypeMock = jest.fn();

test('RadioButton component renders correctly and handles changes', () => {
  const docType = "1";

  const { getByText, getByLabelText } = render(
    <RadioButton docType={docType} setDocType={setDocTypeMock} />
  );

  const uiRadio = getByLabelText("UI");
  const apiRadio = getByLabelText("API");

  // Check if the UI radio button is checked
  expect(uiRadio).toBeChecked();
  expect(apiRadio).not.toBeChecked();

  // Simulate a change event on the API radio button
  fireEvent.click(apiRadio);
  expect(setDocTypeMock).toHaveBeenCalledWith("2");
});
