import React from 'react';
import { render, screen } from '@testing-library/react';
import BugDetail from '../../BugDetail';


        describe('BugDetail Component', () => {
        test('BugDetail component renders correctly', () => {
        const projectDetail = {
            openBugs: 10,
            totalTcExecuted: 100,
            totalBugsReported: 30,
            bugsReportsByClient: 12,
        };

        render(<BugDetail projectDetail={projectDetail} />);
        expect(screen.getByText('Bug Statistics')).toBeInTheDocument();
        expect(screen.getByText('Open Bugs')).toBeInTheDocument();
        expect(screen.getByText('Closed Bugs')).toBeInTheDocument();
        expect(screen.getByText('Bugs InProgress')).toBeInTheDocument();
        expect(screen.getByText('Resolved Bugs')).toBeInTheDocument();
        expect(screen.getByText('Total Bugs reported')).toBeInTheDocument();
        expect(screen.getByText('Bugs Reports by Client')).toBeInTheDocument();
        });

})