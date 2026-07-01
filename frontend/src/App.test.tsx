/* @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest'

import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

const originalFetch = globalThis.fetch
const originalMatchMedia = window.matchMedia

afterEach(() => {
  Object.defineProperty(globalThis, 'fetch', {
    configurable: true,
    value: originalFetch,
    writable: true,
  })
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

  it('describes the connected recommendation and assistant workflow', () => {
    render(<App />)

    expect(screen.getByText('Backend recommender')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Find recipes to rank pantry matches with the local backend.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Ask a pantry question to retrieve grounded recipe context.'),
    ).toBeInTheDocument()
    expect(screen.queryByText(/next slice/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/once wired to the backend/i)).not.toBeInTheDocument()
  })

  it('labels starter recommendations as examples before a backend search', () => {
    render(<App />)

    expect(
      screen.getByText('Starter examples shown until you run a backend search.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Egg Fried Rice' })).toBeInTheDocument()
  })

  it('shows recommendation loading context while backend search is running', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(
      () =>
        new Promise<Response>(() => {
          // Keep the request pending so the loading state stays visible.
        }),
    )

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))

    expect(screen.getByText('Searching with 3 pantry items.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Finding recipes' })).toBeDisabled()
  })

  it('describes the assistant context before asking', () => {
    render(<App />)

    expect(
      screen.getByText(
        'Assistant will use your pantry ingredients unless you select a recipe.',
      ),
    ).toBeInTheDocument()
  })

  it('shows assistant loading context while a question is running', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(
      () =>
        new Promise<Response>(() => {
          // Keep the request pending so the loading state stays visible.
        }),
    )

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))

    expect(
      screen.getByText('Retrieving recipe context for 3 pantry items.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Asking assistant' })).toBeDisabled()
  })

  it('adds a pantry ingredient locally', async () => {
    const user = userEvent.setup()

    render(<App />)

    await user.type(screen.getByLabelText('Add ingredient'), 'spinach')
    await user.click(screen.getByRole('button', { name: 'Add' }))

    expect(screen.getByText('spinach')).toBeInTheDocument()
  })

  it('prevents backend actions when the pantry is empty', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async () => Response.json({ results: [] }))

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Remove eggs' }))
    await user.click(screen.getByRole('button', { name: 'Remove rice' }))
    await user.click(screen.getByRole('button', { name: 'Remove tomato' }))

    expect(
      screen.getByText('Add at least one ingredient to use backend matching.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Find recipes' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Ask assistant' })).toBeDisabled()

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))
    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))

    expect(fetch).not.toHaveBeenCalled()
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

  it('loads recipe recommendations from the API', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async () =>
      Response.json({
        results: [
          {
            id: 'starter-spinach-rice-bowl',
            name: 'Spinach Rice Bowl',
            imageUrl: null,
            category: 'Vegetarian',
            area: 'Australian',
            matchedIngredients: ['eggs', 'rice'],
            missingIngredients: ['spinach'],
            score: 0.75,
            instructionsUrl: null,
          },
        ],
      }),
    )

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))

    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/recommend',
      expect.objectContaining({
        body: JSON.stringify({ ingredients: ['eggs', 'rice', 'tomato'] }),
        method: 'POST',
      }),
    )
    expect(
      await screen.findByRole('heading', { name: 'Spinach Rice Bowl' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Matched: eggs, rice')).toBeInTheDocument()
    expect(screen.getByText('Missing: spinach')).toBeInTheDocument()
    expect(screen.getByText('75%')).toBeInTheDocument()
  })

  it('shows an error when recipe recommendations fail', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async () => new Response('Server error', { status: 500 }))

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Could not load recipes. Check the backend and try again.',
    )
  })

  it('asks the cooking assistant with the current pantry ingredients', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async () =>
      Response.json({
        answer: 'Use the rice with eggs and skip the soy sauce.',
        citations: [{ recipeId: 'starter-egg-fried-rice', name: 'Egg Fried Rice' }],
        retrievedContext: [
          {
            recipeId: 'starter-egg-fried-rice',
            name: 'Egg Fried Rice',
            text: 'Egg Fried Rice uses eggs and rice from your pantry.',
            score: 0.29,
          },
        ],
        providerConfigured: false,
      }),
    )

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.clear(screen.getByLabelText('Question'))
    await user.type(screen.getByLabelText('Question'), 'What can I cook with rice?')
    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))

    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/ask',
      expect.objectContaining({
        body: JSON.stringify({
          question: 'What can I cook with rice?',
          ingredients: ['eggs', 'rice', 'tomato'],
        }),
        method: 'POST',
      }),
    )
    expect(
      await screen.findByText('Use the rice with eggs and skip the soy sauce.'),
    ).toBeInTheDocument()
    expect(screen.getAllByText('Egg Fried Rice')).toHaveLength(2)
    expect(
      screen.getByText('Egg Fried Rice uses eggs and rice from your pantry.'),
    ).toBeInTheDocument()
  })

  it('sends the selected recipe id to the cooking assistant', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async (input: string) => {
      if (input.endsWith('/recommend')) {
        return Response.json({
          results: [
            {
              id: 'starter-spinach-rice-bowl',
              name: 'Spinach Rice Bowl',
              imageUrl: null,
              category: 'Vegetarian',
              area: 'Australian',
              matchedIngredients: ['rice'],
              missingIngredients: ['spinach'],
              score: 0.75,
              instructionsUrl: null,
            },
          ],
        })
      }

      return Response.json({
        answer: 'Use the selected rice bowl context.',
        citations: [
          { recipeId: 'starter-spinach-rice-bowl', name: 'Spinach Rice Bowl' },
        ],
        retrievedContext: [
          {
            recipeId: 'starter-spinach-rice-bowl',
            name: 'Spinach Rice Bowl',
            text: 'Name: Spinach Rice Bowl',
            score: 1,
          },
        ],
        providerConfigured: false,
      })
    })

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))
    await screen.findByRole('heading', { name: 'Spinach Rice Bowl' })
    await user.click(
      screen.getByRole('button', { name: 'Use Spinach Rice Bowl in assistant' }),
    )
    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))

    expect(fetch).toHaveBeenLastCalledWith(
      'http://127.0.0.1:8000/ask',
      expect.objectContaining({
        body: JSON.stringify({
          question: 'Can I make the fried rice without soy sauce?',
          ingredients: ['eggs', 'rice', 'tomato'],
          selectedRecipeId: 'starter-spinach-rice-bowl',
        }),
        method: 'POST',
      }),
    )
    expect(await screen.findByText('Use the selected rice bowl context.')).toBeInTheDocument()
    expect(screen.getByText('Selected recipe: Spinach Rice Bowl')).toBeInTheDocument()
  })

  it('clears stale recommendations and assistant context when pantry changes', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async (input: string) => {
      if (input.endsWith('/recommend')) {
        return Response.json({
          results: [
            {
              id: 'starter-spinach-rice-bowl',
              name: 'Spinach Rice Bowl',
              imageUrl: null,
              category: 'Vegetarian',
              area: 'Australian',
              matchedIngredients: ['rice'],
              missingIngredients: ['spinach'],
              score: 0.75,
              instructionsUrl: null,
            },
          ],
        })
      }

      return Response.json({
        answer: 'Use the selected rice bowl context.',
        citations: [
          { recipeId: 'starter-spinach-rice-bowl', name: 'Spinach Rice Bowl' },
        ],
        retrievedContext: [
          {
            recipeId: 'starter-spinach-rice-bowl',
            name: 'Spinach Rice Bowl',
            text: 'Name: Spinach Rice Bowl',
            score: 1,
          },
        ],
        providerConfigured: false,
      })
    })

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Find recipes' }))
    await screen.findByRole('heading', { name: 'Spinach Rice Bowl' })
    await user.click(
      screen.getByRole('button', { name: 'Use Spinach Rice Bowl in assistant' }),
    )
    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))
    await screen.findByText('Use the selected rice bowl context.')

    await user.type(screen.getByLabelText('Add ingredient'), 'spinach')
    await user.click(screen.getByRole('button', { name: 'Add' }))

    expect(screen.queryByRole('heading', { name: 'Spinach Rice Bowl' })).not.toBeInTheDocument()
    expect(screen.queryByText('Selected recipe: Spinach Rice Bowl')).not.toBeInTheDocument()
    expect(screen.queryByText('Use the selected rice bowl context.')).not.toBeInTheDocument()
    expect(
      screen.getByText('Ask a pantry question to retrieve grounded recipe context.'),
    ).toBeInTheDocument()
  })

  it('shows an error when the cooking assistant fails', async () => {
    const user = userEvent.setup()
    const fetch = vi.fn(async () => new Response('Server error', { status: 500 }))

    Object.defineProperty(globalThis, 'fetch', {
      configurable: true,
      value: fetch,
      writable: true,
    })

    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Ask assistant' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Could not ask the assistant. Check the backend and try again.',
    )
  })
})
