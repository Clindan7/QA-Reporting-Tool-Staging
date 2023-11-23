
import { render } from "@testing-library/react";
import CardContent from './CardContent';

jest.mock('./DashboardCard.css');

describe('<CardContent>', () => {
  it('Test 1: should render component with props', () => {
    render(
      <CardContent title="Test Title" content="Test Content" />
      );
      expect( <CardContent />).toBeTruthy();
  });

  it('Test 2: renders the title correctly', () => {
    const { getByText } = render(
      <CardContent title="Test Title" content="Test Content" />
    );
    const titleElement = getByText('Test Title');
    expect(titleElement).toBeInTheDocument();
    expect(titleElement).toHaveClass('card_content_style'); 
  });

  it('Test 3: renders full content when not truncated', () => {
    const content = 'ShortContent';
    const { getByText } = render(
      <CardContent title="Test Title" content={content} />
    );
    expect(getByText(content)).toBeInTheDocument();
  });
});