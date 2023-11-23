import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from './Dashboard';
import { Provider } from "react-redux";
import thunk from "redux-thunk";
import configureMockStore from "redux-mock-store";
import { BrowserRouter } from 'react-router-dom';

const middlewares = [thunk];
const initialState = {
  DashboardReducer: {
    isLoading: false,
    DashboardData: [],
    errors: {},
  }
};
let mockStore = configureMockStore(middlewares);

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

describe('Dashboard component', () => {
  beforeEach(() => {
    mockedUsedNavigate.mockReset()
  });
  afterEach(() => {
    mockedUsedNavigate.mockClear()
  });

  it('Test 1: should render component', () => {
    render(
      <Provider store={mockStore(initialState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );
    expect(<Dashboard />).toBeTruthy();
  });

  it('Test 2: renders loading screen when API is delayed and isLoading is true', () => {
    const newState = {
      DashboardReducer: {
        isLoading: true,
        DashboardData: [],
        errors: {},
      }
    };
    const { getByTestId } = render(
      <Provider store={mockStore(newState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );

    expect(getByTestId('loading-screen')).toBeInTheDocument();
  });

  it('Test 3: renders No data message when the dashboard is empty', () => {
    const { queryByTestId } = render(
      <Provider store={mockStore(initialState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );

    expect(queryByTestId('loading-screen')).not.toBeInTheDocument();
    expect(screen.getByText('No Data Found !!')).toBeInTheDocument();
  });

  it('Test 4: handles search input in the Dashboard screen', () => {
    const { getByPlaceholderText, getByDisplayValue } = render(
      <Provider store={mockStore(initialState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );
    const searchInput = getByPlaceholderText('Search Project');

    fireEvent.change(searchInput, { target: { value: 'Search Text' } });
    expect(getByDisplayValue('Search Text')).toBeInTheDocument();
  });

  it('Test 5: handles status change in the Dashboard screen', () => {
    const { getByPlaceholderText } = render(
      <Provider store={mockStore(initialState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );
    const selectInput = getByPlaceholderText('Filter by status');

    fireEvent.change(selectInput, { target: { value: '0' } });
    expect(selectInput.value).toBe('0');
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('Test 6: renders the Project list in the Dashboard screen', () => {
    const newState = {
      DashboardReducer: {
        isLoading: false,
        DashboardData: [
          {
            "id": 10,
            "name": "Project_One",
            "notes": "None",
            "release_date": "2023-09-29",
            "risk": "As per schedule",
            "issue_count": 4
          },
          {
            "id": 9,
            "name": "Project_Two",
            "notes": "None",
            "release_date": "2023-09-28",
            "risk": 1,
            "issue_count": 5
          }
        ],
        errors: {},
      }
    };

    render(
      <Provider store={mockStore(newState)}>
        <BrowserRouter><Dashboard /></BrowserRouter>
      </Provider>
    );

    expect(screen.getByText('Project_One')).toBeInTheDocument();
    expect(screen.getByText('Project_Two')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Project_One'))
    expect(mockedUsedNavigate).toBeCalledTimes(1);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/project/10');
  });
});