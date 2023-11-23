import React from 'react';
import { render, screen } from '@testing-library/react';
import { userEvent } from "@testing-library/user-event";
import { BrowserRouter as Router } from 'react-router-dom';
import Sidebar from './Sidebar';

// Mock useNavigate to check routing 
const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

const mockedUseDispatch = jest.fn();
const mockedUseSelector = jest.fn();
jest.mock('react-redux', () => ({
  ...jest.requireActual('react-router-dom'),
  useDispatch: () => mockedUseDispatch,
  useSelector: () => mockedUseSelector
}));

// Mock ProjectList component
jest.mock('./ProjectList', () => {
  return function MockedProjectList() {
    return <div data-testid="project-list">Mocked Project List</div>;
  };
});

describe('Sidebar Component', () => {
  beforeEach(() => {
    // Clear any previous mock calls
    mockedUsedNavigate.mockReset()
    mockedUseDispatch.mockReset()
    mockedUseSelector.mockReset()
  });
  afterEach(() => {
    // Clear any previous mock calls
    mockedUsedNavigate.mockClear()
    mockedUseDispatch.mockClear()
    mockedUseSelector.mockClear()
  });

  it('Test 1: should render component', () => {
    render(
      <Router>
        <Sidebar />
      </Router>
    );
    expect(<Sidebar />).toBeTruthy();
  });

  it('Test 2: renders Sidebar component with Dashboard link initially', () => {
    render(
      <Router>
        <Sidebar />
      </Router>
    );

    // Test whether elements are rendered as expected
    const dashboardLink = screen.getByTestId('dash-link');
    const logoutIcon = screen.getByTestId('logout-icon');
    expect(dashboardLink).toBeInTheDocument();
    expect(logoutIcon).toBeInTheDocument();

    // Check whether the ProjectList component is rendered when isProject is false
    const projectListMock = screen.queryByTestId('project-list');
    expect(projectListMock).not.toBeInTheDocument();
  });

  it('Test 3: checks the Dashboard link is working properly', async () => {

    render(
      <Router>
        <Sidebar/>
      </Router>
    );

    // Test Dashbaord link exists and check if navigate to '/dashboard'
    const dashboardLink = screen.getByTestId('dash-link');
    expect(dashboardLink).toBeInTheDocument();

    await userEvent.click(dashboardLink);
    // Get the component instance
    const sidebarComponent = screen.getByRole('navigation');

    // Check that the handleLinkClick function has updated the currentPath state
    expect(sidebarComponent).toHaveTextContent('Dashboard');
  });

  it('Test 4: checks the Logout button working properly', async () => {
    render(
      <Router>
        <Sidebar />
      </Router>
    );

    // Test Dashbaord link exists and check if navigate to '/dashboard'
    const logoutIcon = screen.getByTestId('logout-icon');
    expect(logoutIcon).toBeInTheDocument();

    await userEvent.click(logoutIcon);
    expect(mockedUsedNavigate).toBeCalledTimes(1);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/login');
  });


});
