import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ProjectList from './ProjectList';
import { Provider } from "react-redux";
import thunk from "redux-thunk";
import configureMockStore from "redux-mock-store";
import { BrowserRouter } from 'react-router-dom';

const middlewares = [thunk];
const initialState = {
  isLoading: false,
  DashboardReducer: {
    DashboardData: [],
  },
  ProjectReducer: {
    ProjectData: [],
  },
  errors: {},
};
let mockStore = configureMockStore(middlewares);

describe('ProjectList component', () => {
  it('Test 1: should render component', () => {
    const handleLinkClickMock = jest.fn();
    render(
      <Provider store={mockStore(initialState)}>
        <ProjectList
          currentPath="/project/1"
          handleLinkClick={handleLinkClickMock}
        /></Provider>
    );
    expect(<ProjectList />).toBeTruthy();
  });

  it('Test 2: should render the search box and handles search', () => {
    const handleLinkClickMock = jest.fn();
    render(
      <Provider store={mockStore(initialState)}>
        <ProjectList
          currentPath="/project/1"
          handleLinkClick={handleLinkClickMock}
        /></Provider>
    );
    // Assert that the search input is rendered
    const searchInput = screen.getByPlaceholderText('Search project');
    expect(searchInput).toBeInTheDocument();

    //     Mock a change event for the search input
    fireEvent.change(searchInput, { target: { value: 'Project 1' } });
    expect(searchInput.value).toBe('Project 1');
  });

  it('Test 3: should render component with project list', () => {
    const handleLinkClickMock = jest.fn();
    const newState = {
      isLoading: false,
      DashboardReducer: {
        DashboardData: [{
          "id": 1,
          "name": "Project 1"
        },
        {
          "id": 2,
          "name": "Project 2"
        }],
      },
      ProjectReducer: {
        ProjectData: [],
      },
      errors: {},
    };
    render(
      <Provider store={mockStore(newState)}>
        <BrowserRouter><ProjectList
          currentPath="/project/1"
          handleLinkClick={handleLinkClickMock}
        /></BrowserRouter>
      </Provider>
    );
    expect(screen.getByText("Project 1")).toBeInTheDocument();
    expect(screen.getByText("Project 2")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Project 1"));
    expect(handleLinkClickMock).toBeCalledWith("/project/1")
  });

  it('Test 4: should render the loader if delay in API call', async() => {
    const handleLinkClickMock = jest.fn();
    const newState = {
      DashboardReducer: {
        isLoading: true,
        DashboardData: [],
        errors: {},
      },
      ProjectReducer: {
        ProjectData: [],
      },
    };
    const { getByTestId } = render(
      <Provider store={mockStore(newState)}>
        <ProjectList
          currentPath="/project/1"
          handleLinkClick={handleLinkClickMock}
        /></Provider>
    );
    expect(getByTestId('loading-screen')).toBeInTheDocument();
  });
});