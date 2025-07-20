import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Example component for demonstration
function ExampleButton({ onClick }) {
  return <button onClick={onClick}>Click Me</button>;
}

describe('ExampleButton', () => {
  it('renders the button with correct text', () => {
    render(<ExampleButton onClick={() => {}} />);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<ExampleButton onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
}); 