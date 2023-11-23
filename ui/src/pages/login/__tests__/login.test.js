import React from 'react';
import { render } from '@testing-library/react';
import Login from '../Login';
import { GoogleOAuthProvider } from '@react-oauth/google';

        // Mock the Logo.png import
        jest.mock('../../../assets/Logo.png', () => 'LogoMock');

        //mock the accesstoken for check api calls
        jest.mock("../../../redux/services/LoginService",()=>({
            getAccessToken:jest.fn()
        }))


        const mockedUsedNavigate = jest.fn();
        jest.mock('react-router-dom', () => ({
            ...jest.requireActual('react-router-dom'),
            useNavigate: () => mockedUsedNavigate,
        }));


        const mockSetItem = jest.fn();
        const mockGetItem = jest.fn();

          const mockLocalStorage = {
            getItem: mockGetItem,
            setItem: mockSetItem,
          };


        Object.defineProperty(window,'localStorage',{
          value:mockLocalStorage,
        })



        describe('Login Component', () => {
              it('render component with the correct button text', () => {
                const { getByText } = render(
                  <GoogleOAuthProvider>
                    <Login />
                  </GoogleOAuthProvider>
                );
                expect(getByText('Log in with google')).toBeInTheDocument();
              });
            


 });

  
