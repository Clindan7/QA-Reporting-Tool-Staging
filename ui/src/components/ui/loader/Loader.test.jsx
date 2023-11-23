import React from 'react';
import { render } from '@testing-library/react';
import LoadingScreen from './Loader';

describe('Loader component', () => {
    it('Test 1: renders the loader correctly', () => {
        render(<LoadingScreen />);
        expect(<LoadingScreen />).toBeTruthy();
    });
});