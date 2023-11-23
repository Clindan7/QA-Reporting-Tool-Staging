import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import { act } from 'react-dom/test-utils';
import Severity from './Severity';
import { Chart } from 'chart.js/auto';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';

// Mock the Chart.js library to prevent actual rendering of charts
jest.mock('chart.js/auto', () => ({
  Chart: class Chart {
    constructor(ctx, config) {
      this.ctx = ctx;
      this.config = config;
    }
    destroy() {
      // Mock the destroy method
    }
  },
}));

jest.mock('../../../redux/actions/chartActions', () => ({
  SeverityChartAsync: jest.fn(() => Promise.resolve()),
}));

const mockStore = configureStore([]);
const initialState = {
  SeverityReducer:{
    isLoading: false,
    SeverityData: {
      0:{"table_data": [
        {
            "priority": "high",
            "count": 4,
            "percentage": 12.5
        },
        {
            "priority": "normal",
            "count": 24,
            "percentage": 75.0
        },
        {
            "priority": "low",
            "count": 4,
            "percentage": 12.5
        }
    ]}
          ,
     
          "labels": [
              "2023-10-06","2023-10-13","2023-10-20","2023-10-27","2023-11-03","2023-11-07"
          ],
     
          "datasets": [
              {
                  "priority": "high",
                  "count": [0,1,0,1,2,0]
              },
              {
                  "priority": "normal",
                  "count": [8,5,2,4,5,0]
              },
              {
                  "priority": "low",
                  "count": [0,0,0,2,2,0]
              }
          ]
      
  },
    errors: {},
  }
};
const store = mockStore(initialState);

describe('Severity Component', () => {
  let container = null;

  beforeEach(() => {
    // Set up a DOM element as a render target
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    // Clean up on exiting
    unmountComponentAtNode(container);
    container.remove();
  });

  it('renders without crashing', () => {
    act(() => {
      render(
        <Provider store={store}>
          <Severity id="1" /> 
        </Provider>,
        container
      );
    });
  });
  
  it('updates chart on radio button change', () => {
    act(() => {
      render(
        <Provider store={store}>
          <Severity id="1" /> 
        </Provider>,
        container
      );
    });
  
    act(() => {
      const radio2 = container.querySelector('#docTypeRadio2');
      if (radio2) {
        radio2.click();
      }
    });
  });
});
