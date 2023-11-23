import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import Feature from './Feature';

const mockStore = configureStore([]);

describe('Feature Component', () => {
  let store;

  beforeEach(() => {
    store = mockStore({
      FeatureTblReducer: {
        tableData: [
          {
            feature: 'Google sign in',
            total_tc: 7,
            passed_tc: 2,
            progress: '28.57%',
            no_of_bugs: 3,
            detection_rate: '42.86%',
          },
          {
            feature: 'Access Token Generation From Refresh Token',
            total_tc: 5,
            passed_tc: 2,
            progress: '40.00%',
            no_of_bugs: 2,
            detection_rate: '40.00%',
          },
        ],
        isLoading: false,
      },
    });
  });

  it('renders component with loading screen', () => {
    store = mockStore({
      FeatureTblReducer: {
        tableData: [],
        isLoading: true,
      },
    });

    render(
      <Provider store={store}>
        <Feature id={1} />
      </Provider>
    );

    expect(screen.getByTestId('loading-screen')).toBeInTheDocument();
  });

  it('renders component with table data', async () => {
    render(
      <Provider store={store}>
        <Feature id={1} />
      </Provider>
    );

    // Wait for table to be rendered
    await waitFor(() => {
      expect(screen.getByText('Feature')).toBeInTheDocument();
      expect(screen.getByText('Number of functional testcases')).toBeInTheDocument();
      expect(screen.getByText('Bugs')).toBeInTheDocument();
    });

    expect(screen.getByText('Google sign in')).toBeInTheDocument();
    expect(screen.getByText('7')).toBeInTheDocument();
    expect(screen.getByText('28.57%')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
    expect(screen.getByText('42.86%')).toBeInTheDocument();
  });

  it('handles radio button change', async () => {
    render(
      <Provider store={store}>
        <Feature id={1} />
      </Provider>
    );

    const radioBtn = screen.getByLabelText('API');
    userEvent.click(radioBtn);

  });
});
