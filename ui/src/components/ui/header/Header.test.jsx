import React from 'react';
import { render, screen } from '@testing-library/react';
import { userEvent } from "@testing-library/user-event";
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from './Header';

// Mock localStorage for testing purposes
const mockLocalStorage = {
  getItem: jest.fn(),
};

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

// Mock useNavigate to check routing 
const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockedUsedNavigate,
}));

describe('Header Component', () => {
  beforeEach(() => {
    // Clear any previous mock calls
    mockLocalStorage.getItem.mockClear();
    mockedUsedNavigate.mockReset();
  });

  it('Test 1: should render component with props', () => {
    render(
        <Router> 
          <Header />
        </Router>
      );
      expect(<Header />).toBeTruthy();
  });
  
  it('Test 2: renders username when present in localStorage', () => {
    const username = 'testUser';
    mockLocalStorage.getItem.mockReturnValue(username);
    render(
        <Router> 
          <Header />
        </Router>
      );

    const usernameElement = screen.getByText(username);
    expect(usernameElement).toBeInTheDocument();
  });

  it('Test 3: renders logo and handles click correctly', async() => {
    mockLocalStorage.getItem.mockReturnValue(null);
    render(
        <Router> 
          <Header />
        </Router>
      );
    const logoElement = screen.getByAltText('Logo');
    expect(logoElement).toBeInTheDocument();
    const userSession = screen.getByTestId("user-session");
    expect(userSession).toBeInTheDocument();
    await userEvent.click(logoElement);
    expect(mockedUsedNavigate).toBeCalledTimes(1);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/dashboard');
  });
});
