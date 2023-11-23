import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from 'react-router-dom';
import App from "./App";

jest.mock('../src/assets/Logo.png', () => 'LogoMock');

describe("App Component", () => {
    it("renders the App component with Login page", () => {
        const { getByAltText} = render(<Router>
            <App />
        </Router>);
        const loginIcon = getByAltText('Login');
        expect(loginIcon).toBeInTheDocument();
        const loginButton = screen.getByRole('button');
        expect(loginButton).toBeInTheDocument();
    });

});
