import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom'; // For rendering Navigate
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import { createMemoryHistory } from 'history';
import AppLayout from './AppLayout';

// Mock localStorage for testing purposes
const mockLocalStorage = {
    getItem: jest.fn(),
};

Object.defineProperty(window, 'localStorage', {
    value: mockLocalStorage,
});
jest.mock('../assets/Logo.png', () => 'LogoMock');


const history = createMemoryHistory({ initialEntries: ['/login'] });
const initialState = {}; // Provide an initial state here
const middlewares = [thunk]; // Add your middlewares here
const mockStore = configureStore(middlewares);
const store = mockStore({
    // Your initial state should match your rootReducer structure
    rootReducer: initialState, 
});

beforeEach(() => {
    mockLocalStorage.getItem.mockClear();
});

describe('AppLayout component', () => {
    it('Test 1: renders the layout when accessToken is present', () => {
        const accessToken = 'thisIsaT0ken';
        mockLocalStorage.getItem.mockReturnValue(accessToken);
        const username = 'testUser';
        mockLocalStorage.getItem.mockReturnValue(username);
      
        render(
            <Provider store={store}>
                <Router>
                    <AppLayout />
                </Router>
            </Provider>
        );
        
        // Check if the Header component is rendered
        const usernameElement = screen.getByText(username);
        expect(usernameElement).toBeInTheDocument();
        expect(screen.getByAltText('Logo')).toBeInTheDocument();

        // Check if the Sidebar component is rendered
        expect(screen.getByText('Dashboard')).toBeInTheDocument();

        // Check if the Outlet component is rendered
        expect(screen.getByTestId('main')).toBeInTheDocument();
    });

      it('Test 2: navigates to Login when accessToken is not present', () => {
        const accessToken = '';
        mockLocalStorage.getItem.mockReturnValue(accessToken);
        render(
            <Provider store={store}>
                <Router>
                    <AppLayout />
                </Router>
            </Provider>
        );

        // Check if it navigates to Login
        expect(history.location.pathname).toBe('/login');
      });
});
