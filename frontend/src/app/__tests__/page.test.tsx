import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders main heading', () => {
    render(<Home />);
    const heading = screen.getByText(/Voice-Driven SaaS MVP/i);
    expect(heading).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<Home />);
    expect(screen.getByText(/Voice Input/i)).toBeInTheDocument();
    expect(screen.getByText(/Documents/i)).toBeInTheDocument();
    expect(screen.getByText(/Entries/i)).toBeInTheDocument();
    expect(screen.getByText(/Transactions/i)).toBeInTheDocument();
  });

  it('has links to all pages', () => {
    render(<Home />);
    expect(screen.getByRole('link', { name: /Voice Input/i })).toHaveAttribute('href', '/voice');
    expect(screen.getByRole('link', { name: /Documents/i })).toHaveAttribute('href', '/documents');
    expect(screen.getByRole('link', { name: /Entries/i })).toHaveAttribute('href', '/entries');
    expect(screen.getByRole('link', { name: /Transactions/i })).toHaveAttribute('href', '/transactions');
  });
});