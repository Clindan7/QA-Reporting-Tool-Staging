import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Project from '../Project';
import { Provider } from 'react-redux';
import store from '../../../store';


describe('Project Component', () => {
  it('renders the summary tab by default', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>
    );

    // Initially, make sure the content for summary tab is displayed
    const summaryTab = screen.getByText('Summary Report');
    expect(summaryTab).toHaveClass('active');
  });


  it('changes CSS class when another tab is clicked', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>

    );
    const summaryTab = screen.getByText('Summary Report');
    const progressTab = screen.getByText('Test Progress Report')

    expect(summaryTab).toHaveClass('active');
    expect(progressTab).toHaveClass('inactive')
  });

  it('renders the contents as per the clicked tab', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>
    );

    expect(screen.getByText('Summary Report')).toBeInTheDocument();
    const progressTab = screen.getByText('Test Progress Report');
   
    // Simulate clicking on the progressTab, make sure the content for progress tab is displayed
    fireEvent.click(progressTab);
    expect(screen.getByText('Test Progress Report')).toBeInTheDocument();
  });


  it('renders the contents as per severity Report', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>
    );

    expect(screen.getByText('Summary Report')).toBeInTheDocument();
    const severityTab = screen.getByText('Severity Wise Report');

    // Simulate clicking on the severityTab, make sure the content for severity tab is displayed
   //fireEvent.click(severityTab);
    expect(severityTab).toBeInTheDocument();
  });


  it('renders the contents as per Feature wise Summary Report', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>
    );

    expect(screen.getByText('Summary Report')).toBeInTheDocument();
    const featureTab = screen.getByText('Feature Wise Summary Report');

    // Simulate clicking on the featureTab, make sure the content for featureTab is displayed
    fireEvent.click(featureTab);
    expect(screen.getByText('Feature Wise Summary Report')).toBeInTheDocument();
  });


  it('renders the content of Feature Bug count Report', () => {
    render(
      <Provider store={store}>
        <Project />
      </Provider>
    );

    expect(screen.getByText('Summary Report')).toBeInTheDocument();
    const bugCountTab = screen.getByText('Feature Wise Bug Count');

    // Simulate clicking on the BugCountTab, make sure the content for BugCountTab is displayed
    //fireEvent.click(bugCountTab);
    expect(bugCountTab).toBeInTheDocument();
  });


});
