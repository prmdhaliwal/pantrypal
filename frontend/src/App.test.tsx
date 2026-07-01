/* @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest'

import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

const originalMatchMedia = window.matchMedia

afterEach(() => {
  Object.defineProperty(window, 'matchMedia', {
    configurable: true,
    value: originalMatchMedia,
    writable: true,
  })
  cleanup()
})

describe('App', () => {
  it('renders the three panel pantry workspace', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { name: 'Your pantry' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Recipe recommendations' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Cooking assistant' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Find recipes' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Ask assistant' }),
    ).toBeInTheDocument()
  })

  it('adds a pantry ingredient locally', async () => {
    const user = userEvent.setup()

    render(<App />)

    await user.type(screen.getByLabelText('Add ingredient'), 'spinach')
    await user.click(screen.getByRole('button', { name: 'Add' }))

    expect(screen.getByText('spinach')).toBeInTheDocument()
  })

  it('switches between dark, light, and system theme modes', async () => {
    const user = userEvent.setup()
    const matchMedia = vi.fn().mockImplementation((query: string) => ({
      addEventListener: vi.fn(),
      addListener: vi.fn(),
      dispatchEvent: vi.fn(),
      matches: false,
      media: query,
      onchange: null,
      removeEventListener: vi.fn(),
      removeListener: vi.fn(),
    }))

    Object.defineProperty(window, 'matchMedia', {
      configurable: true,
      value: matchMedia,
      writable: true,
    })

    render(<App />)

    expect(screen.getByRole('main')).toHaveAttribute(
      'data-theme',
      'pantrypal-dark',
    )

    await user.click(screen.getByRole('button', { name: 'Use light theme' }))
    expect(screen.getByRole('main')).toHaveAttribute(
      'data-theme',
      'pantrypal-light',
    )

    await user.click(screen.getByRole('button', { name: 'Follow system theme' }))
    expect(screen.getByRole('main')).toHaveAttribute(
      'data-theme',
      'pantrypal-light',
    )
    expect(
      screen.getByRole('button', { name: 'Follow system theme' }),
    ).toHaveClass('btn-active')
  })
})
