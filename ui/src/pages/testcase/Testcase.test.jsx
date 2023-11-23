import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureMockStore from 'redux-mock-store';
import Testcase from './Testcase';
import thunk from 'redux-thunk';

const initialState = {
  TCSheetListReducer: {
    isLoading: false,
    TCSheetList: [],
    errors: {},
  }
};

const middlewares = [thunk]; 
const mockStore = configureMockStore(middlewares);

const mockAgGrid = jest.mock();
jest.mock('ag-grid-react', () => ({
  AgGridReact: mockAgGrid
}));

jest.mock('../../components/testcase/tcsheet/Sheet'); // Mock the Sheet component
jest.mock('../../components/testcase/import-export/ImportExport'); //Mock the Import-Export buttons

describe('Testcase component', () => {
  it('Test 1: should render component', () => {
    render(
      <Provider store={mockStore(initialState)}>
        <Testcase />
      </Provider>
    );
    expect(<Testcase />).toBeTruthy();
  });

  it('Test 2: should not render the buttons with empty data in the component', () => {
    render(
      <Provider store={mockStore(initialState)}>
        <Testcase />
      </Provider>
    );
    expect(screen.getByTestId('import-export')).toBeInTheDocument();
    const message = screen.queryAllByText("Testcase Document Not Found");
    expect(message.length).toBe(1);
  });

  it('Test 3: should render component with tablist', () => {
    const newState = {
      TCSheetListReducer: {
        isLoading: false,
        TCSheetList:
          ['Amendment of TC', 'Summary', 'Login' ],
        errors: {},
      }
    };
    render(
      <Provider store={mockStore(newState)}>
        <Testcase />
      </Provider>
    );
    const tabs = screen.queryAllByRole("tab");
    expect(tabs.length).toBe(3);
    expect(screen.getByText("Amendment of TC")).toBeInTheDocument();
    expect(screen.getByText("Summary")).toBeInTheDocument();
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

});