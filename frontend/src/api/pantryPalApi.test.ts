import { describe, expect, it, vi } from 'vitest'

import {
  PantryPalApiError,
  createPantryPalApi,
} from './pantryPalApi'

describe('createPantryPalApi', () => {
  it('posts ingredients to the recommendation endpoint', async () => {
    const fetcher = vi.fn(async () =>
      Response.json({
        results: [
          {
            id: 'starter-egg-fried-rice',
            name: 'Egg Fried Rice',
            imageUrl: null,
            category: null,
            area: null,
            matchedIngredients: ['eggs', 'rice'],
            missingIngredients: ['soy sauce'],
            score: 0.67,
            instructionsUrl: null,
          },
        ],
      }),
    )
    const api = createPantryPalApi({
      baseUrl: 'http://api.test',
      fetcher,
    })

    const response = await api.recommendRecipes(['eggs', 'rice'])

    expect(fetcher).toHaveBeenCalledWith(
      'http://api.test/recommend',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ ingredients: ['eggs', 'rice'] }),
      }),
    )
    expect(response.results[0].name).toBe('Egg Fried Rice')
  })

  it('posts assistant questions to the ask endpoint', async () => {
    const fetcher = vi.fn(async () =>
      Response.json({
        answer: 'Use the rice with eggs.',
        citations: [{ recipeId: 'starter-egg-fried-rice', name: 'Egg Fried Rice' }],
        retrievedContext: [
          {
            recipeId: 'starter-egg-fried-rice',
            name: 'Egg Fried Rice',
            text: 'Name: Egg Fried Rice',
            score: 0.29,
          },
        ],
        providerConfigured: false,
      }),
    )
    const api = createPantryPalApi({
      baseUrl: 'http://api.test',
      fetcher,
    })

    const response = await api.askCookingQuestion({
      question: 'What can I cook?',
      ingredients: ['eggs'],
      selectedRecipeId: 'starter-egg-fried-rice',
    })

    expect(fetcher).toHaveBeenCalledWith(
      'http://api.test/ask',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          question: 'What can I cook?',
          ingredients: ['eggs'],
          selectedRecipeId: 'starter-egg-fried-rice',
        }),
      }),
    )
    expect(response.answer).toBe('Use the rice with eggs.')
    expect(response.providerConfigured).toBe(false)
  })

  it('throws an API error when the backend returns a failure', async () => {
    const fetcher = vi.fn(async () =>
      new Response('Server error', { status: 500 }),
    )
    const api = createPantryPalApi({
      baseUrl: 'http://api.test',
      fetcher,
    })

    await expect(api.recommendRecipes(['eggs'])).rejects.toMatchObject({
      name: 'PantryPalApiError',
      status: 500,
      message: 'PantryPal API request failed with status 500',
    } satisfies Partial<PantryPalApiError>)
  })
})
