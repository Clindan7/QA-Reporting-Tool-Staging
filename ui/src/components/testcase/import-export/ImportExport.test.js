import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ImportExport from './ImportExport';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';

jest.mock('../../../redux/actions/fileActions', () => ({
  ImportExportAsync: jest.fn(() => Promise.resolve()),
}));

const mockStore = configureStore([]);
const initialState = {
  fileReducer: {
    isLoading: false,
  },
};
const store = mockStore(initialState);
const mockDocTypeChange = jest.fn();

describe('ImportExport', () => {
  it('should render the component correctly', () => {
    render(<Provider store={store}>
      <ImportExport id="123" docType="1" onDocTypeChange={mockDocTypeChange}/>
    </Provider>);

    expect(screen.getByText('Import')).toBeInTheDocument();
    expect(screen.getByText('UI')).toBeInTheDocument();
    expect(screen.getByText('API')).toBeInTheDocument();
    const sweepCountInput = screen.getByLabelText('Sweep Count *');
    expect(sweepCountInput).toBeInTheDocument();
  });

  it('should open file input when the Import button is clicked', () => {
    render(<Provider store={store}>
      <ImportExport id="123" docType="1" onDocTypeChange={mockDocTypeChange}/>
    </Provider>);

    const importButton = screen.getByText('Import');
    const fileInput = screen.getByRole('button', { name: 'Import' });

    fireEvent.click(importButton);

    expect(fileInput).toHaveAttribute('type', 'button');
  });


  it('handles file change correctly', () => {
    render(
      <Provider store={store}>
        <ImportExport id="123" docType="1" onDocTypeChange={mockDocTypeChange}/>
      </Provider>
    );

    const inputRef = screen.getByTestId('file-input');
    const validFile = new File(['valid content'], 'valid.xlsx', { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    fireEvent.change(inputRef, { target: { files: [validFile] } });

    const errorModal = screen.queryByTestId('error-modal');
    expect(errorModal).toBeNull();
  });

  it('displays error message when clicking "Import" without entering counts and "UI" selected', () => {
    render(
      <Provider store={store}>
        <ImportExport id="123" docType="1" onDocTypeChange={mockDocTypeChange}/>
      </Provider>
    );

    // Find the "Import" button and click it
    const uiRadioButton = screen.getByLabelText('UI');
    fireEvent.click(uiRadioButton);
    const importButton = screen.getByTestId('import-btn');
    fireEvent.click(importButton);

    // Check if the validation message is displayed
    const errorModal = screen.getByRole('presentation');
    expect(errorModal).not.toBeNull();
    const validationMessage = screen.getByText("Sweep Count is required");
    expect(validationMessage).toBeInTheDocument();
  });

  it('opens the file upload dialog when clicking "Import" with counts entered and "UI" selected', () => {
    render(
      <Provider store={store}>
        <ImportExport id="123" docType="1" onDocTypeChange={mockDocTypeChange}/>
      </Provider>
    );

    // Enter values in the input fields
    const sweepCountInput = screen.getByLabelText('Sweep Count *');
    fireEvent.change(sweepCountInput, { target: { value: '10' } });

    // Find the "Import" button and click it with UI select
    const uiRadioButton = screen.getByLabelText('UI');
    fireEvent.click(uiRadioButton);
    const importButton = screen.getByTestId('import-btn');
    fireEvent.click(importButton);

    // Check that the file input element is visible
    const fileInput = screen.getByTestId('file-input');
    expect(fileInput).not.toBeNull();
  });

  it('opens the file upload dialog when clicking "Import" with count entered and "API" selected', () => {
    render(
      <Provider store={store}>
        <ImportExport id="123" docType="2" onDocTypeChange={mockDocTypeChange}/>
      </Provider>
    );

    // Enter values in the input fields
    const sweepCountInput = screen.getByLabelText('Sweep Count *');
    fireEvent.change(sweepCountInput, { target: { value: '2' } });
    // Find the "Import" button and click it with API select
    const apiRadioButton = screen.getByLabelText('API');
    fireEvent.click(apiRadioButton);
    const importButton = screen.getByTestId('import-btn');
    fireEvent.click(importButton);

    // Assure that the validation message is not displayed
    const errorModal = screen.queryAllByRole('presentation');
    expect(errorModal.length).toBe(0);
    // Check that the file input element is visible
    const fileInput = screen.getByTestId('file-input');
    expect(fileInput).not.toBeNull();
  });

});
