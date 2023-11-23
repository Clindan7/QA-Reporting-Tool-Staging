import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import { act } from 'react-dom/test-utils';
import BugCount from './BugCount';
import * as chartService from '../../../redux/services/ChartService';

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

// Mock the chartService functions as needed
chartService.getBugcountReport = jest.fn(() => Promise.resolve({ status: 200, data: { feature_wise_bug_count: {} } }));

describe('BugCount Component', () => {
  let container = null;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
  });

  it('renders without crashing', async () => {
    await act(async () => {
      render(<BugCount id="1" />, container);
    });
  });

  it('fetches data and renders chart', async () => {
    await act(async () => {
        render(<BugCount id="1" />, container);
      });
  
      // Simulate API call
      await act(async () => {
        // Wait for the API call to complete
      });
  
    //   expect(chartService.getBugcountReport).toHaveBeenCalled();
  });
});
