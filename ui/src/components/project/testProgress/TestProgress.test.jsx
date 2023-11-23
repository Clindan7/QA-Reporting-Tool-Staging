import React from 'react';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import TestProgress from './TestProgress';

// Mock the Chart.js library
jest.mock('chart.js/auto');

const mockStore = configureStore([]);

describe('TestProgress Component', () => {
  let store;

  beforeEach(() => {
    store = mockStore({
      TestProgressReducer: {
        isLoading: false,
        TestProgressData: {
        },
      },
    });
  });

  it('renders without crashing', async () => {
    await act(async () => {
      render(
        <Provider store={store}>
          <TestProgress id="1" />
        </Provider>
      );
    });

    expect(screen.getByText('Enter Data')).toBeInTheDocument();
  });

  it('updates chart on radio button change', async () => {
    await act(async () => {
      render(
        <Provider store={store}>
          <TestProgress id="1" />
        </Provider>
      );
    });

   expect(screen.getByLabelText('UI')).toBeInTheDocument();
    const radio2 = screen.getByLabelText('API'); 
    await userEvent.click(radio2);
  });

 
});
