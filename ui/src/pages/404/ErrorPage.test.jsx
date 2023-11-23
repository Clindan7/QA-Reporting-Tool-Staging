import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorPage from './ErrorPage';

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockedUsedNavigate,
}));

describe('ErrorPage component', () => {
    it('Test 1: renders the 404 page correctly', () => {
        render(<ErrorPage />);
        expect(screen.getByText('404')).toBeInTheDocument();
        expect(screen.getByText("Look like you're lost")).toBeInTheDocument();
        expect(screen.getByText("the page you are looking for not avaible!")).toBeInTheDocument();
        expect(screen.getByText('Go to Home')).toBeInTheDocument();
    });

    it('Test 2: navigates to "dashboard" when the "Go to Home" link is clicked', () => {
        render(<ErrorPage />);

        const goToHomeLink = screen.getByText('Go to Home');
        fireEvent.click(goToHomeLink);

        // Check that the navigate function has been called with "dashboard"
        expect(mockedUsedNavigate).toHaveBeenCalledWith('dashboard');
    });
});
