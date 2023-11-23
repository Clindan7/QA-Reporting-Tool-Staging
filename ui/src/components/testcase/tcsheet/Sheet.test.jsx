import { render, screen} from '@testing-library/react';
import { Provider } from 'react-redux';
import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk'; 

import Sheet from "./Sheet";

const initialState = {
  TCSheetDetailReducer: {
    isLoading: false,
    SheetData: {
      columns: [
        { field: "", checkboxSelection: true, headerCheckboxSelection: true, width: 50 },
        { field: "module", headerName: "Module" },
        { field: "No_of_Test_Cases", headerName: "No.of Test Cases", cellDataType: 'number' },
        { field: "No_of_TestCases_Executed", headerName: "No.of TestCases Executed", cellDataType: 'number' },
        { field: "No_of_TestCases_Passed", headerName: "No of TestCases Passed", cellDataType: 'number' },
        { field: "No_of_TestCases_Failed", headerName: "No of TestCases Failed", cellDataType: 'number' },
        { field: "No_of_TestCases_Not_tested", headerName: "No of TestCases Not Executed", cellDataType: 'number' },
    ],
    rows: [
        { id: 1, module: "Login", No_of_Test_Cases: 12, No_of_TestCases_Executed: 0, No_of_TestCases_Passed: 12, No_of_TestCases_Failed: 47, No_of_TestCases_Not_tested: 0 },
        { id: 2, module: "Project_Management", No_of_Test_Cases: 41, No_of_TestCases_Executed: 0, No_of_TestCases_Passed: 12, No_of_TestCases_Failed: "32", No_of_TestCases_Not_tested: 0 },
        { id: 3, module: "Dashboard", No_of_Test_Cases: 89, No_of_TestCases_Executed: 0, No_of_TestCases_Passed: 1, No_of_TestCases_Failed: "3", No_of_TestCases_Not_tested: 3 },
        { id: 4, module: "Testcase_Management", No_of_Test_Cases: 12, No_of_TestCases_Executed: 0, No_of_TestCases_Passed: 7, No_of_TestCases_Failed: "9", No_of_TestCases_Not_tested: "1" },
    ]
    },
    errors: {},
  }
};

const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

jest.mock('ag-grid-react', () => {
  return {
    AgGridReact: (props) => {
      return <div data-testid="ag-grid-mock" />;
    },
  };
});


describe('Testcase component', () => {
  it('Test 1: should render component', () => {

    render(
      <Provider store={mockStore(initialState)}>
        <Sheet sheetName="Summary" projectId ="1" docType="1"/>
      </Provider>
    );
    expect(<Sheet />).toBeTruthy();
    expect(screen.getByTestId('ag-grid-mock')).toBeInTheDocument();
  });
  
});