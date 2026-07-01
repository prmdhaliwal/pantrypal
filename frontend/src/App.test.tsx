/* @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest'

import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it } from 'vitest'

import App from './App'

afterEach(() => {
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
})
